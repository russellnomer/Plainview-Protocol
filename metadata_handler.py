"""
Metadata Handler for The Plainview Protocol V8.4

Injects Open Graph meta tags for viral SEO and social sharing.
Supports dynamic Battle Card sharing with query parameter routing.
"""

import streamlit as st
import streamlit.components.v1 as components
import os


OG_TITLE = "Plainview Protocol: Transparency & Accountability"
OG_DESCRIPTION = "Facts on grift, tools to act. Bipartisan corruption tracking for 3,143 counties."
OG_IMAGE = "https://i.imgur.com/PlainviewProtocol.png"
OG_URL = "https://plainview-protocol.replit.app"


def get_base_url():
    """Get the base URL for the deployed app."""
    domain = os.environ.get('REPLIT_DEV_DOMAIN', '')
    if domain:
        return f"https://{domain}"
    return OG_URL


def get_battlecard_image_url(card_id: str) -> str:
    """Get the full URL for a battle card image."""
    base_url = get_base_url()
    card_filename = f"battlecard_{card_id}.png"
    card_path = os.path.join('static', 'battlecards', card_filename)
    
    if os.path.exists(card_path):
        return f"{base_url}/static/battlecards/{card_filename}"
    return f"{base_url}/static/battlecards/default_battlecard.png"


def inject_og_meta_tags(card_id: str = None):
    """Inject Open Graph meta tags into the page head for social sharing."""
    
    if card_id:
        title = "My Plainview Battle Card"
        description = "I just audited my representative. The numbers don't lie. #PlainviewProtocol"
        image = get_battlecard_image_url(card_id)
        url = f"{get_base_url()}/?page=share&id={card_id}"
    else:
        title = OG_TITLE
        description = OG_DESCRIPTION
        image = OG_IMAGE
        url = OG_URL
    
    og_tags = f"""
    <script>
        // Inject OG meta tags into document head
        (function() {{
            var head = document.head || document.getElementsByTagName('head')[0];
            
            // Remove existing OG tags first
            var existingMetas = head.querySelectorAll('meta[property^="og:"], meta[name^="twitter:"]');
            existingMetas.forEach(function(m) {{ m.remove(); }});
            
            var metas = [
                {{ property: 'og:title', content: '{title}' }},
                {{ property: 'og:description', content: '{description}' }},
                {{ property: 'og:type', content: 'website' }},
                {{ property: 'og:url', content: '{url}' }},
                {{ property: 'og:image', content: '{image}' }},
                {{ property: 'og:image:width', content: '1080' }},
                {{ property: 'og:image:height', content: '1080' }},
                {{ name: 'twitter:card', content: 'summary_large_image' }},
                {{ name: 'twitter:title', content: '{title}' }},
                {{ name: 'twitter:description', content: '{description}' }},
                {{ name: 'twitter:image', content: '{image}' }},
                {{ name: 'description', content: '{description}' }}
            ];
            
            metas.forEach(function(m) {{
                var meta = document.createElement('meta');
                if (m.property) meta.setAttribute('property', m.property);
                if (m.name) meta.setAttribute('name', m.name);
                meta.setAttribute('content', m.content);
                head.appendChild(meta);
            }});
        }})();
    </script>
    """
    components.html(og_tags, height=0, width=0)


def get_page_config():
    """Return the page configuration for st.set_page_config."""
    return {
        "page_title": "Plainview Protocol: Transparency & Accountability",
        "page_icon": "🔱",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }


def get_share_url(page_name: str, custom_text: str = "") -> str:
    """Generate a pre-filled X (Twitter) share URL."""
    base_text = custom_text or f"I'm using the Plainview Protocol to track grift and demand transparency. Facts on grift, tools to act."
    hashtags = "#PlainviewProtocol #Transparency #Accountability"
    full_text = f"{base_text} {hashtags} {OG_URL}"
    encoded = full_text.replace(' ', '%20').replace('#', '%23').replace(':', '%3A').replace('\n', '%0A')
    return f"https://twitter.com/intent/tweet?text={encoded}"
