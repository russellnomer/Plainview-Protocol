"""
Fact Check Builder - V6.28
The Plainview Protocol

Generates "Narrative Shield" fact-check graphics using PIL/Pillow.
1200x675px optimized for X/Facebook sharing.

"The lie travels halfway around the world while the truth is putting on its shoes.
We gave the truth a Ferrari."
"""

from PIL import Image, ImageDraw, ImageFont
import io
import math
from typing import Tuple

CARD_SIZE = (1200, 675)
NAVY_BLUE = (26, 26, 46)
DARK_RED = (178, 34, 34)
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
ROYAL_BLUE = (74, 144, 217)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (60, 60, 60)

HASHTAGS = "#FactCheck #RuleOfLaw #SupportICE #PlainviewProtocol"

def create_fact_check_card() -> bytes:
    """Generate the Narrative Shield fact-check card."""
    img = Image.new('RGB', CARD_SIZE, NAVY_BLUE)
    draw = ImageDraw.Draw(img)
    
    try:
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        verdict_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        header_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        verdict_font = ImageFont.load_default()
    
    draw.rectangle([(0, 0), (1200, 70)], fill=DARK_RED)
    
    header_text = 'FACT CHECK: "SHE WAS JUST DRIVING AWAY"'
    header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
    header_width = header_bbox[2] - header_bbox[0]
    draw.text(
        ((CARD_SIZE[0] - header_width) // 2, 18),
        header_text,
        fill=WHITE,
        font=header_font
    )
    
    panel_a_x = 0
    panel_a_width = 500
    panel_b_x = 520
    panel_b_width = 680
    
    draw.rectangle([(20, 90), (500, 550)], fill=(40, 40, 60), outline=SILVER, width=2)
    
    draw_vehicle_silhouette(draw, 260, 280)
    
    draw.polygon([
        (350, 380),
        (450, 380),
        (450, 370),
        (480, 390),
        (450, 410),
        (450, 400),
        (350, 400)
    ], fill=DARK_RED)
    
    force_text = "Force Multiplier:"
    force_bbox = draw.textbbox((0, 0), force_text, font=body_font)
    draw.text((280, 420), force_text, fill=WHITE, font=body_font)
    
    weight_text = "4,300 lbs @ Acceleration"
    draw.text((260, 445), weight_text, fill=ROYAL_BLUE, font=title_font)
    
    draw.text((180, 500), "Honda Pilot SUV", fill=SILVER, font=small_font)
    
    draw.rectangle([(520, 90), (1180, 550)], fill=(30, 30, 50), outline=SILVER, width=2)
    
    claim_y = 110
    draw.text((540, claim_y), "THE CLAIM:", fill=SILVER, font=title_font)
    draw.text((540, claim_y + 35), '"Peaceful exit from a traffic stop."', fill=WHITE, font=body_font)
    
    reality_y = 190
    draw.rectangle([(540, reality_y), (1160, reality_y + 120)], fill=DARK_RED, outline=None)
    draw.text((560, reality_y + 10), "THE REALITY:", fill=WHITE, font=title_font)
    draw.text((560, reality_y + 45), "Vehicle = Deadly Weapon", fill=WHITE, font=body_font)
    draw.text((560, reality_y + 70), "Impact force exceeds firearm round", fill=WHITE, font=body_font)
    draw.text((560, reality_y + 95), "at typical acceleration speeds.", fill=WHITE, font=body_font)
    
    law_y = 330
    draw.text((540, law_y), "THE LAW:", fill=ROYAL_BLUE, font=title_font)
    draw.text((540, law_y + 35), "8 CFR 287.8 authorizes deadly force", fill=WHITE, font=body_font)
    draw.text((540, law_y + 60), "against vehicular assault on officers.", fill=WHITE, font=body_font)
    
    source_y = 420
    draw.text((540, source_y), "SOURCE:", fill=SILVER, font=small_font)
    draw.text((540, source_y + 20), "Code of Federal Regulations, Title 8", fill=SILVER, font=small_font)
    draw.text((540, source_y + 40), "Graham v. Connor, 490 U.S. 386 (1989)", fill=SILVER, font=small_font)
    draw.text((540, source_y + 60), "Standard physics: KE = ½mv²", fill=SILVER, font=small_font)
    
    draw.rectangle([(0, 560), (1200, 675)], fill=(20, 20, 35))
    
    verdict_text = "VERDICT: FALSE"
    verdict_bbox = draw.textbbox((0, 0), verdict_text, font=verdict_font)
    verdict_width = verdict_bbox[2] - verdict_bbox[0]
    
    stamp_x = 80
    stamp_y = 580
    draw.rectangle(
        [(stamp_x - 10, stamp_y - 5), (stamp_x + verdict_width + 10, stamp_y + 55)],
        outline=DARK_RED,
        width=4
    )
    draw.text((stamp_x, stamp_y), verdict_text, fill=DARK_RED, font=verdict_font)
    
    draw_shield_icon(draw, 1100, 615, 40)
    
    url_text = "plainviewprotocol.com"
    url_bbox = draw.textbbox((0, 0), url_text, font=small_font)
    draw.text((1020, 650), url_text, fill=SILVER, font=small_font)
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG', optimize=True)
    buffer.seek(0)
    
    return buffer.getvalue()

def draw_vehicle_silhouette(draw: ImageDraw.ImageDraw, cx: int, cy: int):
    """Draw a simplified SUV silhouette."""
    body_points = [
        (cx - 120, cy + 40),
        (cx - 120, cy - 10),
        (cx - 100, cy - 10),
        (cx - 80, cy - 50),
        (cx + 60, cy - 50),
        (cx + 100, cy - 10),
        (cx + 120, cy - 10),
        (cx + 120, cy + 40),
    ]
    draw.polygon(body_points, fill=DARK_GRAY, outline=SILVER)
    
    draw.ellipse([(cx - 90, cy + 20), (cx - 50, cy + 60)], fill=(30, 30, 30), outline=SILVER)
    draw.ellipse([(cx + 50, cy + 20), (cx + 90, cy + 60)], fill=(30, 30, 30), outline=SILVER)
    
    draw.rectangle([(cx - 70, cy - 40), (cx - 30, cy - 15)], fill=(100, 150, 200), outline=SILVER)
    draw.rectangle([(cx + 10, cy - 40), (cx + 50, cy - 15)], fill=(100, 150, 200), outline=SILVER)

def draw_shield_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int):
    """Draw the Plainview Protocol shield icon."""
    shield_points = [
        (cx, cy - size),
        (cx + size * 0.8, cy - size * 0.6),
        (cx + size * 0.8, cy + size * 0.3),
        (cx, cy + size),
        (cx - size * 0.8, cy + size * 0.3),
        (cx - size * 0.8, cy - size * 0.6),
    ]
    draw.polygon(shield_points, fill=NAVY_BLUE, outline=ROYAL_BLUE, width=2)
    
    draw.line([(cx - size * 0.6, cy), (cx + size * 0.6, cy)], fill=ROYAL_BLUE, width=2)

def get_fact_check_card() -> bytes:
    """Get the fact check card as bytes for download."""
    return create_fact_check_card()

def get_hashtags() -> str:
    """Get the approved hashtags for sharing."""
    return HASHTAGS
