"""
Badge Generator - V6.27
The Plainview Protocol

Generates digital support badges using PIL/Pillow.
Optimized for X/Instagram at 1080x1080.
"""

from PIL import Image, ImageDraw, ImageFont
import io
import math
from typing import Tuple

BADGE_SIZE = (1080, 1080)
NAVY_BLUE = (26, 26, 46)
ROYAL_BLUE = (74, 144, 217)
SILVER = (192, 192, 192)
WHITE = (255, 255, 255)
DARK_BLUE = (15, 52, 96)

SCALE = 0.9

def create_shield_badge() -> bytes:
    """Generate the Stand with ICE digital badge at 1080x1080."""
    img = Image.new('RGBA', BADGE_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x = BADGE_SIZE[0] // 2
    center_y = BADGE_SIZE[1] // 2
    
    shield_points = [
        (center_x, int(90 * SCALE)),
        (center_x + int(360 * SCALE), int(180 * SCALE)),
        (center_x + int(360 * SCALE), int(540 * SCALE)),
        (center_x, int(945 * SCALE)),
        (center_x - int(360 * SCALE), int(540 * SCALE)),
        (center_x - int(360 * SCALE), int(180 * SCALE)),
    ]
    
    draw.polygon(shield_points, fill=NAVY_BLUE, outline=SILVER)
    draw.polygon(shield_points, outline=SILVER, width=7)
    
    inner_points = [
        (center_x, int(117 * SCALE)),
        (center_x + int(333 * SCALE), int(198 * SCALE)),
        (center_x + int(333 * SCALE), int(522 * SCALE)),
        (center_x, int(900 * SCALE)),
        (center_x - int(333 * SCALE), int(522 * SCALE)),
        (center_x - int(333 * SCALE), int(198 * SCALE)),
    ]
    draw.polygon(inner_points, outline=ROYAL_BLUE, width=4)
    
    stripe_y = int(450 * SCALE)
    stripe_height = int(36 * SCALE)
    draw.rectangle(
        [(center_x - int(315 * SCALE), stripe_y), (center_x + int(315 * SCALE), stripe_y + stripe_height)],
        fill=ROYAL_BLUE
    )
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(65 * SCALE))
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(41 * SCALE))
        url_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(25 * SCALE))
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
    
    title_text = "I STAND WITH"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(
        (center_x - title_width // 2, int(252 * SCALE)),
        title_text,
        fill=WHITE,
        font=title_font
    )
    
    ice_text = "ICE"
    ice_bbox = draw.textbbox((0, 0), ice_text, font=title_font)
    ice_width = ice_bbox[2] - ice_bbox[0]
    draw.text(
        (center_x - ice_width // 2, int(333 * SCALE)),
        ice_text,
        fill=ROYAL_BLUE,
        font=title_font
    )
    
    tagline1 = "RULE OF LAW"
    tagline1_bbox = draw.textbbox((0, 0), tagline1, font=subtitle_font)
    tagline1_width = tagline1_bbox[2] - tagline1_bbox[0]
    draw.text(
        (center_x - tagline1_width // 2, int(540 * SCALE)),
        tagline1,
        fill=SILVER,
        font=subtitle_font
    )
    
    tagline2 = "SECURE BORDERS"
    tagline2_bbox = draw.textbbox((0, 0), tagline2, font=subtitle_font)
    tagline2_width = tagline2_bbox[2] - tagline2_bbox[0]
    draw.text(
        (center_x - tagline2_width // 2, int(594 * SCALE)),
        tagline2,
        fill=SILVER,
        font=subtitle_font
    )
    
    tagline3 = "SAFE AMERICA"
    tagline3_bbox = draw.textbbox((0, 0), tagline3, font=subtitle_font)
    tagline3_width = tagline3_bbox[2] - tagline3_bbox[0]
    draw.text(
        (center_x - tagline3_width // 2, int(648 * SCALE)),
        tagline3,
        fill=SILVER,
        font=subtitle_font
    )
    
    star_center = (center_x, int(765 * SCALE))
    star_size = int(54 * SCALE)
    draw_star(draw, star_center, star_size, ROYAL_BLUE, SILVER)
    
    url_text = "plainviewprotocol.com"
    url_bbox = draw.textbbox((0, 0), url_text, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    draw.text(
        (center_x - url_width // 2, int(837 * SCALE)),
        url_text,
        fill=SILVER,
        font=url_font
    )
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG', optimize=True)
    buffer.seek(0)
    
    return buffer.getvalue()

def draw_star(draw: ImageDraw.ImageDraw, center: Tuple[int, int], size: int, fill_color: Tuple, outline_color: Tuple):
    """Draw a 5-pointed star."""
    cx, cy = center
    points = []
    
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        if i % 2 == 0:
            r = size
        else:
            r = size * 0.4
        
        x = cx + r * math.cos(angle)
        y = cy - r * math.sin(angle)
        points.append((x, y))
    
    draw.polygon(points, fill=fill_color, outline=outline_color)

def get_badge_bytes() -> bytes:
    """Get the badge as bytes for download."""
    return create_shield_badge()
