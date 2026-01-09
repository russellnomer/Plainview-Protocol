"""
Asynchronous Traffic Ledger for The Plainview Protocol V8.3

Non-blocking database writes using Queue and Thread for high-performance
traffic logging that won't slow down the main application.

Features:
- Background worker thread for database writes
- Queue-based buffering to prevent blocking
- Graceful shutdown handling
- Queue depth monitoring for dashboards
"""

import os
import logging
import threading
import queue
import atexit
from datetime import datetime
from typing import Optional, Dict, Any
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AsyncTrafficLedger")

_traffic_queue: queue.Queue = queue.Queue(maxsize=10000)
_worker_thread: Optional[threading.Thread] = None
_shutdown_event = threading.Event()
_is_initialized = False


def get_db_connection():
    """Get database connection."""
    if not DATABASE_URL:
        return None
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None


def _worker_loop():
    """Background worker that processes the traffic queue."""
    logger.info("Traffic Ledger worker thread started")
    
    batch_size = 50
    batch = []
    
    while not _shutdown_event.is_set():
        try:
            try:
                item = _traffic_queue.get(timeout=1.0)
                batch.append(item)
                _traffic_queue.task_done()
            except queue.Empty:
                pass
            
            if len(batch) >= batch_size or (_shutdown_event.is_set() and batch):
                _flush_batch(batch)
                batch = []
                
        except Exception as e:
            logger.error(f"Worker loop error: {e}")
    
    if batch:
        _flush_batch(batch)
    
    logger.info("Traffic Ledger worker thread stopped")


def _flush_batch(batch):
    """Flush a batch of traffic entries to the database."""
    if not batch:
        return
    
    conn = get_db_connection()
    if not conn:
        logger.warning(f"No DB connection - dropping {len(batch)} traffic entries")
        return
    
    try:
        with conn.cursor() as cur:
            args_list = [(
                entry['session_id'],
                entry['page_url'],
                entry['referrer'],
                entry['action_type'],
                entry['ip_hash'],
                entry['timestamp']
            ) for entry in batch]
            
            cur.executemany("""
                INSERT INTO traffic_ledger 
                (session_id, page_url, referrer, action_type, ip_hash, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, args_list)
            
            conn.commit()
            logger.debug(f"Flushed {len(batch)} traffic entries to database")
            
    except Exception as e:
        logger.error(f"Failed to flush batch: {e}")
        conn.rollback()
    finally:
        conn.close()


def init_async_ledger():
    """Initialize and start the background worker thread."""
    global _worker_thread, _is_initialized
    
    if _is_initialized:
        return
    
    _shutdown_event.clear()
    _worker_thread = threading.Thread(target=_worker_loop, daemon=True, name="TrafficLedgerWorker")
    _worker_thread.start()
    _is_initialized = True
    
    atexit.register(shutdown_ledger)
    
    logger.info("Async Traffic Ledger initialized")


def async_log_traffic(session_id: str, page_url: str, action_type: str,
                      referrer: Optional[str] = None, ip_hash: Optional[str] = None):
    """
    Non-blocking traffic logging. Adds entry to queue for background processing.
    
    This function returns immediately and never blocks the main thread.
    """
    if not _is_initialized:
        init_async_ledger()
    
    entry = {
        'session_id': session_id,
        'page_url': page_url,
        'action_type': action_type,
        'referrer': referrer,
        'ip_hash': ip_hash,
        'timestamp': datetime.now()
    }
    
    try:
        _traffic_queue.put_nowait(entry)
    except queue.Full:
        logger.warning("Traffic queue full - dropping entry")


def shutdown_ledger():
    """Gracefully shutdown the worker thread."""
    global _is_initialized
    
    if not _is_initialized:
        return
    
    logger.info("Shutting down Traffic Ledger...")
    _shutdown_event.set()
    
    if _worker_thread and _worker_thread.is_alive():
        _worker_thread.join(timeout=5.0)
        if _worker_thread.is_alive():
            logger.warning("Worker thread did not stop gracefully")
    
    _is_initialized = False
    logger.info("Traffic Ledger shutdown complete")


def get_queue_depth() -> int:
    """Get current queue depth for monitoring."""
    return _traffic_queue.qsize()


def get_queue_stats() -> Dict[str, Any]:
    """Get queue statistics for the Protocol Pulse dashboard."""
    return {
        'queue_depth': _traffic_queue.qsize(),
        'max_size': _traffic_queue.maxsize,
        'worker_alive': _worker_thread.is_alive() if _worker_thread else False,
        'is_initialized': _is_initialized
    }


def force_flush():
    """Force flush the queue (for debugging/shutdown)."""
    remaining = []
    while not _traffic_queue.empty():
        try:
            remaining.append(_traffic_queue.get_nowait())
            _traffic_queue.task_done()
        except queue.Empty:
            break
    
    if remaining:
        _flush_batch(remaining)
        logger.info(f"Force flushed {len(remaining)} entries")


if __name__ == "__main__":
    init_async_ledger()
    
    for i in range(100):
        async_log_traffic(
            session_id=f"test-session-{i}",
            page_url="/test",
            action_type="TEST",
            referrer="localhost",
            ip_hash=f"hash-{i}"
        )
    
    print(f"Queue depth after adding 100 items: {get_queue_depth()}")
    
    import time
    time.sleep(2)
    
    print(f"Queue depth after 2 seconds: {get_queue_depth()}")
    
    shutdown_ledger()
    print("Shutdown complete")
