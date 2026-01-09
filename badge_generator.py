"""
Badge Generator - V6.27
The Plainview Protocol

Generates digital support badges using PIL/Pillow.
"""

from PIL import Image, ImageDraw, ImageFont
import io
from typing import Tuple

BADGE_SIZE = (1200, 1200)
NAVY_BLUE = (26, 26, 46)
ROYAL_BLUE = (74, 144, 217)
SILVER = (192, 192, 192)
WHITE = (255, 255, 255)
DARK_BLUE = (15, 52, 96)

def create_shield_badge() -> bytes:
    """Generate the Stand with ICE digital badge."""
    img = Image.new('RGBA', BADGE_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x = BADGE_SIZE[0] // 2
    center_y = BADGE_SIZE[1] // 2
    
    shield_points = [
        (center_x, 100),
        (center_x + 400, 200),
        (center_x + 400, 600),
        (center_x, 1050),
        (center_x - 400, 600),
        (center_x - 400, 200),
    ]
    
    draw.polygon(shield_points, fill=NAVY_BLUE, outline=SILVER)
    
    draw.polygon(shield_points, outline=SILVER, width=8)
    
    inner_points = [
        (center_x, 130),
        (center_x + 370, 220),
        (center_x + 370, 580),
        (center_x, 1000),
        (center_x - 370, 580),
        (center_x - 370, 220),
    ]
    draw.polygon(inner_points, outline=ROYAL_BLUE, width=4)
    
    stripe_y = 500
    stripe_height = 40
    draw.rectangle(
        [(center_x - 350, stripe_y), (center_x + 350, stripe_y + stripe_height)],
        fill=ROYAL_BLUE
    )
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        url_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
    
    title_text = "I STAND WITH"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(
        (center_x - title_width // 2, 280),
        title_text,
        fill=WHITE,
        font=title_font
    )
    
    ice_text = "ICE"
    ice_bbox = draw.textbbox((0, 0), ice_text, font=title_font)
    ice_width = ice_bbox[2] - ice_bbox[0]
    draw.text(
        (center_x - ice_width // 2, 370),
        ice_text,
        fill=ROYAL_BLUE,
        font=title_font
    )
    
    tagline1 = "RULE OF LAW"
    tagline1_bbox = draw.textbbox((0, 0), tagline1, font=subtitle_font)
    tagline1_width = tagline1_bbox[2] - tagline1_bbox[0]
    draw.text(
        (center_x - tagline1_width // 2, 600),
        tagline1,
        fill=SILVER,
        font=subtitle_font
    )
    
    tagline2 = "SECURE BORDERS"
    tagline2_bbox = draw.textbbox((0, 0), tagline2, font=subtitle_font)
    tagline2_width = tagline2_bbox[2] - tagline2_bbox[0]
    draw.text(
        (center_x - tagline2_width // 2, 660),
        tagline2,
        fill=SILVER,
        font=subtitle_font
    )
    
    tagline3 = "SAFE AMERICA"
    tagline3_bbox = draw.textbbox((0, 0), tagline3, font=subtitle_font)
    tagline3_width = tagline3_bbox[2] - tagline3_bbox[0]
    draw.text(
        (center_x - tagline3_width // 2, 720),
        tagline3,
        fill=SILVER,
        font=subtitle_font
    )
    
    star_center = (center_x, 850)
    star_size = 60
    draw_star(draw, star_center, star_size, ROYAL_BLUE, SILVER)
    
    url_text = "plainviewprotocol.com"
    url_bbox = draw.textbbox((0, 0), url_text, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    draw.text(
        (center_x - url_width // 2, 930),
        url_text,
        fill=SILVER,
        font=url_font
    )
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG', quality=95)
    buffer.seek(0)
    
    return buffer.getvalue()

def draw_star(draw: ImageDraw, center: Tuple[int, int], size: int, fill_color: Tuple, outline_color: Tuple):
    """Draw a 5-pointed star."""
    import math
    
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
