"""
Sovereign Affidavit Portal for The Plainview Protocol V8.3

This module provides the access control gate for sensitive pages
(Foreign Influence Tracker, FARA Reporter) requiring users to
digitally sign an Affidavit of Integrity before accessing data.

Features:
- SHA-256 signature binding to CODE_OF_CONDUCT.md version
- Session-based oath storage with localStorage persistence
- Reusable guard for protected pages
"""

import hashlib
import json
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from streamlit_local_storage import LocalStorage
    localS = LocalStorage()
    LOCAL_STORAGE_AVAILABLE = True
except ImportError:
    localS = None
    LOCAL_STORAGE_AVAILABLE = False

LOCAL_STORAGE_KEY = "plainview_affidavit_v1"


AFFIDAVIT_CLAUSES = [
    {
        "number": 1,
        "text": "I am a U.S. Person as defined by 52 U.S.C. § 30121 and am not acting under the direction of a foreign principal.",
        "legal_basis": "52 U.S.C. § 30121 - Contributions and donations by foreign nationals"
    },
    {
        "number": 2,
        "text": "I attest that all evidence submitted to the Protocol is authentic, unaltered, and gathered through lawful public records requests.",
        "legal_basis": "State FOIA laws, 5 U.S.C. § 552"
    },
    {
        "number": 3,
        "text": "I understand that providing false information in this affidavit may result in removal from the Protocol and referral to the Office of Congressional Conduct (OCC).",
        "legal_basis": "18 U.S.C. § 1001 - False Statements Act"
    }
]


def get_code_of_conduct_hash() -> str:
    """Get SHA-256 hash of the current CODE_OF_CONDUCT.md file."""
    try:
        with open("CODE_OF_CONDUCT.md", "r") as f:
            content = f.read()
        return hashlib.sha256(content.encode()).hexdigest()
    except FileNotFoundError:
        return hashlib.sha256(b"CODE_OF_CONDUCT_V6.18").hexdigest()


def generate_signature_hash(signer_name: str, timestamp: str, coc_hash: str) -> str:
    """
    Generate SHA-256 hash binding the signature to the Code of Conduct version.
    
    Components:
    - Signer's typed name
    - Timestamp of signature
    - CODE_OF_CONDUCT.md hash (version binding)
    """
    signature_string = f"{signer_name}|{timestamp}|{coc_hash}"
    return hashlib.sha256(signature_string.encode()).hexdigest()


def is_affidavit_signed() -> bool:
    """Check if the user has signed the affidavit in the current session."""
    return st.session_state.get('affidavit_signed', False)


def get_signature_details() -> Optional[Dict[str, Any]]:
    """Get the details of the signed affidavit if available."""
    if is_affidavit_signed():
        return {
            "signer_name": st.session_state.get('affidavit_signer_name'),
            "timestamp": st.session_state.get('affidavit_timestamp'),
            "signature_hash": st.session_state.get('affidavit_signature_hash'),
            "coc_version_hash": st.session_state.get('affidavit_coc_hash')
        }
    return None


def load_persisted_affidavit():
    """Check localStorage for existing valid signature and restore it to session_state."""
    if not LOCAL_STORAGE_AVAILABLE or localS is None:
        return False
    
    if not st.session_state.get('affidavit_signed', False):
        try:
            raw_data = localS.getItem(LOCAL_STORAGE_KEY)
            if raw_data is None:
                return False
            
            if isinstance(raw_data, str):
                try:
                    saved_data = json.loads(raw_data)
                except json.JSONDecodeError:
                    return False
            elif isinstance(raw_data, dict):
                saved_data = raw_data
            else:
                return False
            
            required_keys = ['signature_hash', 'timestamp', 'display_name', 'coc_hash']
            if all(k in saved_data for k in required_keys):
                st.session_state['affidavit_signed'] = True
                st.session_state['affidavit_signer_name'] = saved_data['display_name']
                st.session_state['affidavit_timestamp'] = saved_data['timestamp']
                st.session_state['affidavit_signature_hash'] = saved_data['signature_hash']
                st.session_state['affidavit_coc_hash'] = saved_data['coc_hash']
                st.session_state['affidavit_restored'] = True
                return True
        except Exception:
            pass
    return False


def render_affidavit_gate() -> bool:
    """
    Render the affidavit gate UI and return True if signed.
    
    This should be called at the top of protected pages.
    Returns True if the user has signed and can access the page.
    Returns False if the user needs to sign first.
    """
    # Check local storage for existing signature
    if load_persisted_affidavit():
        return True

    if is_affidavit_signed():
        return True
    
    st.warning("🔒 **Access Restricted:** This page requires a signed Affidavit of Integrity.")
    
    st.markdown("""
> *"We are a digital grand jury. If you want to see the foreign wires and file FARA reports, 
> you must stand in the light yourself. Sign the oath. Own the evidence. Protect the mission."*
    """)
    
    st.divider()
    
    st.subheader("📜 Affidavit of Integrity")
    st.caption("Required for access to Foreign Influence Tracker and FARA Reporter")
    
    st.markdown("**Before proceeding, you must affirm the following clauses:**")
    
    for clause in AFFIDAVIT_CLAUSES:
        st.markdown(f"""
**Clause {clause['number']}:**
> {clause['text']}

*Legal Basis: {clause['legal_basis']}*
        """)
    
    st.divider()
    
    st.subheader("✍️ Digital Signature")
    
    signer_name = st.text_input("Type your full legal name to sign:", key="affidavit_name_input")
    
    agree_checkbox = st.checkbox(
        "I AGREE to this Oath and affirm all clauses above are true and correct.",
        key="affidavit_agree_checkbox"
    )
    
    if st.button("🔐 Sign Affidavit", use_container_width=True, type="primary"):
        if signer_name and agree_checkbox:
            timestamp = datetime.now().isoformat()
            coc_hash = get_code_of_conduct_hash()
            signature_hash = generate_signature_hash(signer_name, timestamp, coc_hash)
            
            st.session_state['affidavit_signed'] = True
            st.session_state['affidavit_signer_name'] = signer_name
            st.session_state['affidavit_timestamp'] = timestamp
            st.session_state['affidavit_signature_hash'] = signature_hash
            st.session_state['affidavit_coc_hash'] = coc_hash
            
            if LOCAL_STORAGE_AVAILABLE and localS is not None:
                display_name = f"{signer_name[:2]}***{signer_name[-2:]}" if len(signer_name) > 4 else "***"
                name_hash = hashlib.sha256(signer_name.encode()).hexdigest()
                
                local_data = {
                    "signature_hash": signature_hash,
                    "timestamp": timestamp,
                    "display_name": display_name,
                    "name_hash": name_hash,
                    "coc_hash": coc_hash
                }
                
                try:
                    localS.setItem(LOCAL_STORAGE_KEY, json.dumps(local_data))
                except Exception:
                    pass
            
            st.success(f"✅ Affidavit signed successfully!")
            st.info(f"**Signature Hash:** `{signature_hash[:16]}...`")
            st.info(f"**Timestamp:** {timestamp}")
            
            st.rerun()
        else:
            if not signer_name:
                st.error("Please type your full legal name to sign.")
            if not agree_checkbox:
                st.error("You must check the agreement box to proceed.")
    
    return False


def render_signature_badge():
    """Render a badge showing the user's affidavit status."""
    if is_affidavit_signed():
        details = get_signature_details()
        st.success(f"✅ **Affidavit Signed:** {details['signer_name']} on {details['timestamp'][:10]}")
    else:
        st.warning("🔒 **Unsigned:** Complete the Affidavit of Integrity to unlock full features.")


def require_affidavit(page_function):
    """
    Decorator to require affidavit signature before accessing a page.
    
    Usage:
        @require_affidavit
        def page_foreign_influence():
            # Page content here
            pass
    """
    def wrapper(*args, **kwargs):
        if render_affidavit_gate():
            return page_function(*args, **kwargs)
        return None
    return wrapper


def render_affidavit_status_sidebar():
    """Render affidavit status in the sidebar."""
    if is_affidavit_signed():
        details = get_signature_details()
        st.sidebar.success(f"✅ Oath: {details['signer_name'][:15]}...")
    else:
        st.sidebar.warning("🔒 Affidavit: Unsigned")
