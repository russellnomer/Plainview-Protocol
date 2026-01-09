#!/usr/bin/env python3
"""
Share Server for The Plainview Protocol V6.32
Provides Twitter Card meta tags for viral battle card sharing.

This Flask server runs alongside Streamlit to serve Open Graph meta tags
that Twitter/X scrapes for rich card previews.
"""

from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'battlecards')
BASE_URL = os.environ.get('REPLIT_DEV_DOMAIN', 'plainviewprotocol.com')

@app.route('/share/<card_id>')
def share_card(card_id):
    """
    Serve Twitter Card meta tags for battle card sharing.
    Twitter's bot scrapes this page; humans get redirected to main app.
    """
    card_id_clean = card_id.replace('.png', '').replace('battlecard_', '')
    image_filename = f"battlecard_{card_id_clean}.png"
    image_path = os.path.join(STATIC_DIR, image_filename)
    
    if not os.path.exists(image_path):
        image_url = f"https://{BASE_URL}/static/battlecards/default_battlecard.png"
    else:
        image_url = f"https://{BASE_URL}/static/battlecards/{image_filename}"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plainview Protocol Battle Card</title>
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="My Plainview Battle Card">
    <meta property="og:description" content="I just audited my representative. See their score. #PlainviewProtocol">
    <meta property="og:image" content="{image_url}">
    <meta property="og:image:width" content="1080">
    <meta property="og:image:height" content="1080">
    <meta property="og:url" content="https://{BASE_URL}/share/{card_id}">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="My Plainview Battle Card">
    <meta name="twitter:description" content="I just audited my representative. See their score. The numbers don't lie.">
    <meta name="twitter:image" content="{image_url}">
    <meta name="twitter:site" content="@PlainviewProtocol">
    
    <!-- Redirect humans to main app -->
    <script>
        setTimeout(function() {{
            window.location.href = 'https://{BASE_URL}/Scorecard_Generator';
        }}, 100);
    </script>
</head>
<body style="background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; text-align: center; padding: 50px;">
    <h1>Redirecting to The Plainview Protocol...</h1>
    <p>If you are not redirected, <a href="https://{BASE_URL}" style="color: #58a6ff;">click here</a>.</p>
</body>
</html>"""
    
    return html

@app.route('/static/battlecards/<filename>')
def serve_battlecard(filename):
    """Serve battle card images for Twitter scraper."""
    if not filename.endswith('.png'):
        abort(400)
    return send_from_directory(STATIC_DIR, filename)

@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'ok', 'service': 'share_server', 'version': '6.32'}

if __name__ == '__main__':
    os.makedirs(STATIC_DIR, exist_ok=True)
    port = int(os.environ.get('SHARE_SERVER_PORT', 3001))
    app.run(host='0.0.0.0', port=port, debug=False)
