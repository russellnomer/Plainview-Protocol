"""
Forensic Logger for The Plainview Protocol V8.1+

Database-backed error and traffic logging with rate limiting
and nefarious activity detection.

Features:
- Error logging with stack traces
- Traffic logging with session tracking
- Rate limiting for FOIA requests
- Nefarious activity flagging (>10 requests/60s)
"""

import os
import json
import logging
import traceback
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get("DATABASE_URL")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SovereignLedger")


def get_db_connection():
    """Get database connection."""
    if not DATABASE_URL:
        return None
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None


def init_database():
    """Initialize database tables for logging."""
    conn = get_db_connection()
    if not conn:
        logger.warning("No database connection - using fallback logging")
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sentinel_logs (
                    id SERIAL PRIMARY KEY,
                    incident_id VARCHAR(64) UNIQUE NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    error_type VARCHAR(50),
                    page_url TEXT,
                    stack_trace TEXT,
                    user_session_id VARCHAR(64),
                    resolved BOOLEAN DEFAULT FALSE,
                    resolution_notes TEXT
                )
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS traffic_ledger (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_id VARCHAR(64),
                    page_url TEXT,
                    referrer TEXT,
                    action_type VARCHAR(50),
                    ip_hash VARCHAR(64)
                )
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS nefarious_activity (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_hash VARCHAR(64),
                    request_count INTEGER,
                    time_window_seconds INTEGER,
                    action_taken VARCHAR(50),
                    reviewed BOOLEAN DEFAULT FALSE
                )
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sentinel_signups (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_id VARCHAR(64),
                    affidavit_hash VARCHAR(64),
                    signer_name_hash VARCHAR(64),
                    referrer TEXT
                )
            """)
            
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_traffic_timestamp 
                ON traffic_ledger(timestamp)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_traffic_session 
                ON traffic_ledger(session_id)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_traffic_ip 
                ON traffic_ledger(ip_hash)
            """)
            
            conn.commit()
            logger.info("Database tables initialized successfully")
            return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def generate_incident_id() -> str:
    """Generate unique incident ID for error tracking."""
    timestamp = datetime.now().isoformat()
    return hashlib.sha256(f"INCIDENT|{timestamp}".encode()).hexdigest()[:16].upper()


def log_error(error_type: str, page_url: str, exception: Exception, 
              session_id: Optional[str] = None) -> str:
    """Log an error to the database with full stack trace."""
    incident_id = generate_incident_id()
    stack_trace = traceback.format_exc()
    
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO sentinel_logs 
                    (incident_id, error_type, page_url, stack_trace, user_session_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (incident_id, error_type, page_url, stack_trace, session_id))
                conn.commit()
                logger.info(f"Error logged: {incident_id} - {error_type}")
        except Exception as e:
            logger.error(f"Failed to log error to database: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    _fallback_log_error(incident_id, error_type, page_url, stack_trace, session_id)
    
    return incident_id


def _fallback_log_error(incident_id: str, error_type: str, page_url: str, 
                        stack_trace: str, session_id: Optional[str]):
    """Fallback to JSON file if database is unavailable."""
    log_entry = {
        "incident_id": incident_id,
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        "page_url": page_url,
        "stack_trace": stack_trace,
        "session_id": session_id
    }
    
    try:
        logs = []
        if os.path.exists("sentinel_logs.json"):
            with open("sentinel_logs.json", "r") as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        logs = logs[-100:]
        
        with open("sentinel_logs.json", "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        logger.error(f"Fallback logging failed: {e}")


def log_traffic(session_id: str, page_url: str, action_type: str,
                referrer: Optional[str] = None, ip_hash: Optional[str] = None):
    """Log traffic event to the database."""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO traffic_ledger 
                    (session_id, page_url, referrer, action_type, ip_hash)
                    VALUES (%s, %s, %s, %s, %s)
                """, (session_id, page_url, referrer, action_type, ip_hash))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log traffic: {e}")
            conn.rollback()
        finally:
            conn.close()


def check_rate_limit(ip_hash: str, action_type: str = "FOIA_FIRE",
                     max_requests: int = 10, window_seconds: int = 60) -> bool:
    """
    Check if IP exceeds rate limit. Returns True if blocked.
    Flags nefarious activity if limit exceeded.
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            window_start = datetime.now() - timedelta(seconds=window_seconds)
            
            cur.execute("""
                SELECT COUNT(*) FROM traffic_ledger
                WHERE ip_hash = %s 
                AND action_type = %s
                AND timestamp > %s
            """, (ip_hash, action_type, window_start))
            
            count = cur.fetchone()[0]
            
            if count >= max_requests:
                cur.execute("""
                    INSERT INTO nefarious_activity 
                    (ip_hash, request_count, time_window_seconds, action_taken)
                    VALUES (%s, %s, %s, %s)
                """, (ip_hash, count, window_seconds, "RATE_LIMITED"))
                conn.commit()
                
                logger.warning(f"Rate limit exceeded for {ip_hash[:8]}... - {count} requests in {window_seconds}s")
                return True
            
            return False
    except Exception as e:
        logger.error(f"Rate limit check failed: {e}")
        return False
    finally:
        conn.close()


def log_sentinel_signup(session_id: str, affidavit_hash: str, 
                        signer_name: str, referrer: Optional[str] = None):
    """Log new Sentinel signup for adoption tracking."""
    signer_hash = hashlib.sha256(signer_name.encode()).hexdigest()
    
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO sentinel_signups 
                    (session_id, affidavit_hash, signer_name_hash, referrer)
                    VALUES (%s, %s, %s, %s)
                """, (session_id, affidavit_hash, signer_hash, referrer))
                conn.commit()
                logger.info(f"Sentinel signup logged: {signer_hash[:8]}...")
        except Exception as e:
            logger.error(f"Failed to log signup: {e}")
            conn.rollback()
        finally:
            conn.close()


def get_recent_errors(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent errors for admin dashboard."""
    conn = get_db_connection()
    if not conn:
        if os.path.exists("sentinel_logs.json"):
            with open("sentinel_logs.json", "r") as f:
                logs = json.load(f)
            return logs[-limit:]
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM sentinel_logs
                ORDER BY timestamp DESC
                LIMIT %s
            """, (limit,))
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch errors: {e}")
        return []
    finally:
        conn.close()


def get_traffic_stats() -> Dict[str, Any]:
    """Get traffic statistics for Protocol Pulse dashboard."""
    conn = get_db_connection()
    if not conn:
        return {"total_visits": 0, "unique_sessions": 0, "foia_fires": 0}
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM traffic_ledger")
            total_visits = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(DISTINCT session_id) FROM traffic_ledger")
            unique_sessions = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM traffic_ledger WHERE action_type = 'FOIA_FIRE'")
            foia_fires = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM sentinel_signups")
            total_sentinels = cur.fetchone()[0]
            
            return {
                "total_visits": total_visits,
                "unique_sessions": unique_sessions,
                "foia_fires": foia_fires,
                "total_sentinels": total_sentinels
            }
    except Exception as e:
        logger.error(f"Failed to fetch traffic stats: {e}")
        return {"total_visits": 0, "unique_sessions": 0, "foia_fires": 0, "total_sentinels": 0}
    finally:
        conn.close()


def get_sentinel_growth() -> List[Dict[str, Any]]:
    """Get cumulative Sentinel signups over time."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT DATE(timestamp) as signup_date, 
                       COUNT(*) as daily_signups,
                       SUM(COUNT(*)) OVER (ORDER BY DATE(timestamp)) as cumulative
                FROM sentinel_signups
                GROUP BY DATE(timestamp)
                ORDER BY DATE(timestamp)
            """)
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch sentinel growth: {e}")
        return []
    finally:
        conn.close()


def get_top_referrers(limit: int = 10) -> List[Dict[str, Any]]:
    """Get top referrer domains for adoption tracking."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT referrer, COUNT(*) as visit_count
                FROM traffic_ledger
                WHERE referrer IS NOT NULL AND referrer != ''
                GROUP BY referrer
                ORDER BY visit_count DESC
                LIMIT %s
            """, (limit,))
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch referrers: {e}")
        return []
    finally:
        conn.close()


def get_nefarious_activity(limit: int = 20) -> List[Dict[str, Any]]:
    """Get flagged nefarious activity for human review."""
    conn = get_db_connection()
    if not conn:
        if os.path.exists("nefarious_activity.json"):
            with open("nefarious_activity.json", "r") as f:
                return json.load(f)[-limit:]
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM nefarious_activity
                WHERE reviewed = FALSE
                ORDER BY timestamp DESC
                LIMIT %s
            """, (limit,))
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch nefarious activity: {e}")
        return []
    finally:
        conn.close()


def mark_error_resolved(incident_id: str, resolution_notes: str):
    """Mark an error as resolved with notes."""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE sentinel_logs
                    SET resolved = TRUE, resolution_notes = %s
                    WHERE incident_id = %s
                """, (resolution_notes, incident_id))
                conn.commit()
                logger.info(f"Error {incident_id} marked as resolved")
        except Exception as e:
            logger.error(f"Failed to mark error resolved: {e}")
            conn.rollback()
        finally:
            conn.close()


if __name__ == "__main__":
    print("Initializing Forensic Logger database...")
    init_database()
    print("Database initialization complete.")
