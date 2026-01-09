"""
Metadata Handler for The Plainview Protocol V8.4

Injects Open Graph meta tags for viral SEO and social sharing.
"""

import streamlit as st
import streamlit.components.v1 as components


OG_TITLE = "Plainview Protocol: Transparency & Accountability"
OG_DESCRIPTION = "Facts on grift, tools to act. Bipartisan corruption tracking for 3,143 counties."
OG_IMAGE = "https://i.imgur.com/PlainviewProtocol.png"
OG_URL = "https://plainview-protocol.replit.app"


def inject_og_meta_tags():
    """Inject Open Graph meta tags into the page head for social sharing."""
    og_tags = f"""
    <script>
        // Inject OG meta tags into document head
        (function() {{
            var head = document.head || document.getElementsByTagName('head')[0];
            
            var metas = [
                {{ property: 'og:title', content: '{OG_TITLE}' }},
                {{ property: 'og:description', content: '{OG_DESCRIPTION}' }},
                {{ property: 'og:type', content: 'website' }},
                {{ property: 'og:url', content: '{OG_URL}' }},
                {{ name: 'twitter:card', content: 'summary_large_image' }},
                {{ name: 'twitter:title', content: '{OG_TITLE}' }},
                {{ name: 'twitter:description', content: '{OG_DESCRIPTION}' }},
                {{ name: 'description', content: '{OG_DESCRIPTION}' }}
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
