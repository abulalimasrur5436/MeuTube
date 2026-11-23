"""
Full Generator for fresh, high-definition MeuTube screenshots.
Composites real thumbnails with MeuTube's Liquid Glass & AMOLED UI.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS_DIR = 'C:/Windows/Fonts/'
RAW_DIR = 'C:/Users/Administrator/Downloads/meetube-src/assets_raw'
OUT_SCREENS = 'C:/Users/Administrator/Downloads/meetube-src/.github/assets/meutube/screens'
OUT_ROOT = 'C:/Users/Administrator/Downloads/meetube-src/.github/assets/meutube'

os.makedirs(OUT_SCREENS, exist_ok=True)
os.makedirs(OUT_ROOT, exist_ok=True)

W, H = 632, 1390

def get_font(name='segoeui.ttf', size=24):
    try:
        return ImageFont.truetype(os.path.join(FONTS_DIR, name), size)
    except:
        return ImageFont.load_default()

F_TITLE = get_font('segoeuib.ttf', 24)
F_TITLE_LG = get_font('segoeuib.ttf', 27)
F_SUB = get_font('segoeui.ttf', 19)
F_SM = get_font('segoeui.ttf', 16)
F_BOLD = get_font('segoeuib.ttf', 20)
F_BADGE = get_font('segoeuib.ttf', 15)
F_HEAD = get_font('segoeuib.ttf', 32)
F_LYRIC_ACT = get_font('segoeuib.ttf', 24)
F_LYRIC_INACT = get_font('segoeui.ttf', 22)

def raw_img(name):
    return Image.open(os.path.join(RAW_DIR, name)).convert('RGB')

def rounded_mask(size, radius):
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0]-1, size[1]-1), radius, fill=255)
    return mask

def crop_rounded(img, size, radius):
    resized = img.resize(size, Image.LANCZOS)
    if radius == 0:
        return resized
    out = Image.new('RGBA', size, (0, 0, 0, 0))
    out.paste(resized, (0, 0), rounded_mask(size, radius))
    return out

def draw_pill(draw, bbox, fill, outline=None, width=1):
    r = (bbox[3] - bbox[1]) // 2
    draw.rounded_rectangle(bbox, r, fill=fill, outline=outline, width=width)

def draw_glass_card(img, bbox, radius=24, tint=(255, 255, 255, 28), outline=(255, 255, 255, 45)):
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle((0, 0, w-1, h-1), radius, fill=tint, outline=outline, width=1)
    img.alpha_composite(overlay, (bbox[0], bbox[1]))

def draw_glass_pill(img, bbox, tint=(255, 255, 255, 28), outline=(255, 255, 255, 45)):
    return draw_glass_card(img, bbox, (bbox[3] - bbox[1]) // 2, tint, outline)

# Vector Icons
def icon_home(d, cx, cy, col):
    d.polygon([(cx, cy - 14), (cx - 14, cy - 1), (cx + 14, cy - 1)], fill=col)
    d.rectangle((cx - 10, cy - 2, cx + 10, cy + 12), fill=col)
    d.rectangle((cx - 3, cy + 3, cx + 3, cy + 12), fill=(18, 18, 22))

def icon_shorts(d, cx, cy, col):
    d.rounded_rectangle((cx - 9, cy - 13, cx + 9, cy + 13), 5, outline=col, width=2)
    d.polygon([(cx - 3, cy - 5), (cx + 4, cy), (cx - 3, cy + 5)], fill=col)

def icon_search(d, cx, cy, col):
    d.ellipse((cx - 11, cy - 11, cx + 4, cy + 4), outline=col, width=2)
    d.line((cx + 2, cy + 2, cx + 11, cy + 11), fill=col, width=3)

def icon_subs(d, cx, cy, col):
    d.rectangle((cx - 13, cy - 8, cx + 13, cy + 10), outline=col, width=2)
    d.line((cx - 9, cy - 12, cx + 9, cy - 12), fill=col, width=2)
    d.polygon([(cx - 3, cy - 3), (cx + 4, cy + 1), (cx - 3, cy + 5)], fill=col)

def icon_you(d, cx, cy, col):
    d.ellipse((cx - 6, cy - 12, cx + 6, cy), fill=col)
    d.arc((cx - 12, cy + 2, cx + 12, cy + 18), 180, 360, fill=col, width=3)

def icon_like(d, cx, cy, col):
    d.rectangle((cx - 6, cy - 2, cx + 6, cy + 9), fill=col)
    d.polygon([(cx - 6, cy - 2), (cx - 6, cy - 10), (cx - 1, cy - 10), (cx - 1, cy - 2)], fill=col)
    d.rectangle((cx - 11, cy - 2, cx - 8, cy + 9), fill=col)

def icon_dislike(d, cx, cy, col):
    d.rectangle((cx - 6, cy - 9, cx + 6, cy + 2), fill=col)
    d.polygon([(cx - 6, cy + 2), (cx - 6, cy + 10), (cx - 1, cy + 10), (cx - 1, cy + 2)], fill=col)
    d.rectangle((cx - 11, cy - 9, cx - 8, cy + 2), fill=col)

def icon_share(d, cx, cy, col):
    d.ellipse((cx - 10, cy - 3, cx - 4, cy + 3), fill=col)
    d.ellipse((cx + 5, cy - 10, cx + 11, cy - 4), fill=col)
    d.ellipse((cx + 5, cy + 4, cx + 11, cy + 10), fill=col)
    d.line((cx - 6, cy - 1, cx + 7, cy - 7), fill=col, width=2)
    d.line((cx - 6, cy + 1, cx + 7, cy + 7), fill=col, width=2)

def icon_download(d, cx, cy, col):
    d.line((cx, cy - 10, cx, cy + 4), fill=col, width=3)
    d.polygon([(cx - 6, cy + 2), (cx + 6, cy + 2), (cx, cy + 8)], fill=col)
    d.line((cx - 9, cy + 11, cx + 9, cy + 11), fill=col, width=2)

def icon_cast(d, cx, cy, col):
    d.rectangle((cx - 12, cy - 9, cx + 12, cy + 9), outline=col, width=2)
    d.arc((cx - 12, cy + 1, cx - 4, cy + 9), 270, 360, fill=col, width=2)
    d.arc((cx - 12, cy - 3, cx + 1, cy + 9), 270, 360, fill=col, width=2)
    d.ellipse((cx - 13, cy + 6, cx - 9, cy + 10), fill=col)

def icon_queue(d, cx, cy, col):
    d.line((cx - 10, cy - 7, cx + 10, cy - 7), fill=col, width=2)
    d.line((cx - 10, cy, cx + 10, cy), fill=col, width=2)
    d.line((cx - 10, cy + 7, cx + 5, cy + 7), fill=col, width=2)
    d.polygon([(cx + 6, cy + 4), (cx + 12, cy + 7), (cx + 6, cy + 10)], fill=col)

def icon_lyrics(d, cx, cy, col):
    d.rounded_rectangle((cx - 11, cy - 9, cx + 11, cy + 9), 4, outline=col, width=2)
    d.line((cx - 7, cy - 3, cx + 7, cy - 3), fill=col, width=2)
    d.line((cx - 7, cy + 3, cx + 4, cy + 3), fill=col, width=2)

def draw_status_bar(img, time_str="9:41"):
    d = ImageDraw.Draw(img)
    d.text((36, 16), time_str, font=F_SM, fill=(255, 255, 255))
    d.ellipse((W - 95, 20, W - 83, 32), fill=(255, 255, 255))
    d.rectangle((W - 75, 18, W - 42, 32), outline=(255, 255, 255), width=2)
    d.rectangle((W - 71, 22, W - 48, 28), fill=(255, 255, 255))
    d.rectangle((W - 41, 21, W - 39, 29), fill=(255, 255, 255))

def draw_nav_bar(img, active_idx=0, mode='glass'):
    if mode == 'glass':
        bw, bh = 580, 84
        bx, by = (W - bw) // 2, H - bh - 24
        
        # Subtle glow underneath active tab
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        act_x = bx + 58 + active_idx * 116
        gd.ellipse((act_x - 55, by + 5, act_x + 55, by + 75), fill=(255, 55, 55, 120))
        glow = glow.filter(ImageFilter.GaussianBlur(28))
        img.alpha_composite(glow)
        
        # Frosted glass body
        overlay = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle((0, 0, bw-1, bh-1), 42, fill=(22, 22, 28, 225), outline=(255, 255, 255, 45), width=1)
        img.alpha_composite(overlay, (bx, by))
        
        d = ImageDraw.Draw(img)
        nav_fns = [icon_home, icon_shorts, icon_search, icon_subs, icon_you]
        for i, fn in enumerate(nav_fns):
            cx = bx + 58 + i * 116
            cy = by + 42
            if i == active_idx:
                draw_pill(d, (cx - 36, cy - 28, cx + 36, cy + 28), fill=(255, 255, 255, 30))
                fn(d, cx, cy, (255, 60, 60))
            else:
                fn(d, cx, cy, (160, 160, 175))
    else:
        d = ImageDraw.Draw(img)
        d.rectangle((0, H - 76, W, H), fill=(12, 12, 14))
        nav_fns = [icon_home, icon_shorts, icon_search, icon_subs, icon_you]
        for i, fn in enumerate(nav_fns):
            cx = 63 + i * 126
            cy = H - 38
            if i == active_idx:
                fn(d, cx, cy, (255, 0, 0))
            else:
                fn(d, cx, cy, (140, 140, 145))

def draw_top_bar(img, show_logo=True):
    d = ImageDraw.Draw(img)
    if show_logo:
        # MeuTube Red 'M' Icon + Brand Name
        draw_pill(d, (30, 56, 74, 96), fill=(255, 45, 45))
        d.text((43, 63), "M", font=F_BOLD, fill=(255, 255, 255))
        d.text((84, 62), "MeuTube", font=F_HEAD, fill=(255, 255, 255))
    icon_cast(d, W - 80, 76, (255, 255, 255))
    icon_search(d, W - 40, 76, (255, 255, 255))

def draw_chips(img, y=110, active_chip=0, chips=None):
    if chips is None:
        chips = ["All", "Space", "Technology", "AI & Robotics", "Nature 4K"]
    d = ImageDraw.Draw(img)
    x = 24
    for i, c in enumerate(chips):
        tw = int(d.textlength(c, font=F_SM)) + 30
        if i == active_chip:
            draw_pill(d, (x, y, x + tw, y + 42), fill=(255, 255, 255))
            d.text((x + 15, y + 10), c, font=F_SM, fill=(0, 0, 0))
        else:
            draw_pill(d, (x, y, x + tw, y + 42), fill=(38, 38, 44))
            d.text((x + 15, y + 10), c, font=F_SM, fill=(235, 235, 235))
        x += tw + 12

def save_both(img, name):
    p1 = os.path.join(OUT_SCREENS, name)
    p2 = os.path.join(OUT_ROOT, name)
    img_rgb = img.convert('RGB')
    img_rgb.save(p1, quality=94)
    img_rgb.save(p2, quality=94)
    print(f"Saved: {name}")

# -------------------------------------------------------------
# 1. Compact Player (screens/compact_player.jpg & watch.jpg)
# -------------------------------------------------------------
def gen_compact_player():
    img = Image.new('RGBA', (W, H), (14, 14, 18, 255))
    starship = raw_img('starship.jpg')
    
    # Ambient backlight glow
    ambient = starship.resize((W, 850), Image.LANCZOS).filter(ImageFilter.GaussianBlur(85))
    img.paste(ambient, (0, 0))
    
    # Smooth dark gradient overlay
    grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        a = min(255, int(130 + y * 0.14))
        gd.line((0, y, W, y), fill=(10, 10, 12, a))
    img.alpha_composite(grad)
    
    draw_status_bar(img)
    
    # Video player area
    v_h = 356
    video_crop = starship.resize((W, v_h), Image.LANCZOS)
    img.paste(video_crop, (0, 68))
    
    # Scrubber with SponsorBlock segments
    d = ImageDraw.Draw(img)
    d.line((0, 68 + v_h - 4, W, 68 + v_h - 4), fill=(60, 60, 65), width=4)
    d.line((0, 68 + v_h - 4, 90, 68 + v_h - 4), fill=(0, 215, 80), width=4)    # intro skipped (green)
    d.line((90, 68 + v_h - 4, 380, 68 + v_h - 4), fill=(255, 45, 45), width=4) # played (red)
    d.ellipse((374, 68 + v_h - 10, 386, 68 + v_h + 2), fill=(255, 45, 45))
    
    # Duration badge
    draw_pill(d, (W - 85, 68 + v_h - 38, W - 18, 68 + v_h - 14), fill=(0, 0, 0, 190))
    d.text((W - 74, 68 + v_h - 36), "14:49", font=F_BADGE, fill=(255, 255, 255))
    
    # Title & Metadata
    y = 68 + v_h + 20
    d.text((24, y), "Starship Flight 5: The Historic Catch", font=F_TITLE_LG, fill=(255, 255, 255))
    d.text((24, y + 42), "SpaceX • 18M views • 2 weeks ago", font=F_SUB, fill=(180, 180, 190))
    
    # Action buttons row
    y += 88
    # Channel avatar
    d.ellipse((24, y, 74, y + 50), fill=(20, 20, 24))
    d.text((38, y + 12), "X", font=F_BOLD, fill=(255, 255, 255))
    draw_pill(d, (86, y + 4, 215, y + 46), fill=(240, 240, 245))
    d.text((106, y + 14), "Subscribed", font=F_BOLD, fill=(15, 15, 15))
    
    # Likes / Dislikes (Return YouTube Dislike)
    draw_pill(d, (230, y + 4, 385, y + 46), fill=(38, 38, 44))
    icon_like(d, 252, y + 25, (255, 255, 255))
    d.text((268, y + 14), "1.4M", font=F_BOLD, fill=(255, 255, 255))
    d.line((320, y + 12, 320, y + 38), fill=(100, 100, 110), width=1)
    icon_dislike(d, 350, y + 25, (255, 255, 255))
    
    # Share & Download
    draw_pill(d, (400, y + 4, 480, y + 46), fill=(38, 38, 44))
    icon_share(d, 440, y + 25, (255, 255, 255))
    
    draw_pill(d, (495, y + 4, 608, y + 46), fill=(38, 38, 44))
    icon_download(d, 525, y + 25, (255, 255, 255))
    d.text((545, y + 14), "4K", font=F_BOLD, fill=(255, 255, 255))
    
    # Comments glass card
    y += 68
    draw_glass_pill(img, (20, y, W - 20, y + 92), tint=(32, 32, 38, 190), outline=(255, 255, 255, 35))
    d = ImageDraw.Draw(img)
    d.text((40, y + 14), "Comments  184K", font=F_BOLD, fill=(255, 255, 255))
    d.text((W - 55, y + 14), ">", font=F_BOLD, fill=(180, 180, 180))
    d.ellipse((40, y + 48, 68, y + 76), fill=(120, 70, 210))
    d.text((80, y + 52), "Catching a 250-foot booster in mid-air is pure history.", font=F_SM, fill=(225, 225, 230))
    
    # Up Next section
    y += 114
    d.text((24, y), "Up next", font=F_BOLD, fill=(255, 255, 255))
    chips = ["All", "From SpaceX", "Spaceflight", "New to you"]
    draw_chips(img, y + 36, 0, chips)
    
    # Next video card
    y += 94
    v_card = raw_img('vision_pro.jpg')
    c_img = crop_rounded(v_card, (W - 48, 280), 22)
    img.paste(c_img, (24, y), c_img)
    draw_pill(d, (W - 95, y + 236, W - 38, y + 266), fill=(0, 0, 0, 190))
    d.text((W - 84, y + 242), "16:21", font=F_BADGE, fill=(255, 255, 255))
    
    d.text((24, y + 294), "Apple Vision Pro: A Look into the Future", font=F_TITLE, fill=(255, 255, 255))
    d.text((24, y + 328), "Marques Brownlee • 7.8M views • 3 months ago", font=F_SUB, fill=(170, 170, 180))
    
    save_both(img, "compact_player.jpg")
    img.convert('RGB').save(os.path.join(OUT_ROOT, "watch.jpg"), quality=94)

# -------------------------------------------------------------
# 2. Home Screen (screens/home.jpg & home.jpg)
# -------------------------------------------------------------
def gen_home():
    img = Image.new('RGBA', (W, H), (8, 8, 10, 255))
    draw_status_bar(img)
    draw_top_bar(img, show_logo=True)
    draw_chips(img, y=114, active_chip=0, chips=["All", "Space", "Technology", "AI", "Nature 4K"])
    
    d = ImageDraw.Draw(img)
    
    # Video Card 1
    y = 175
    starship = raw_img('starship.jpg')
    c_star = crop_rounded(starship, (W, 355), 0)
    img.paste(c_star, (0, y))
    
    draw_pill(d, (W - 85, y + 355 - 40, W - 18, y + 355 - 16), fill=(0, 0, 0, 190))
    d.text((W - 74, y + 355 - 38), "14:49", font=F_BADGE, fill=(255, 255, 255))
    
    # Channel avatar & Info
    y += 370
    d.ellipse((24, y, 76, y + 52), fill=(25, 25, 30))
    d.text((42, y + 14), "X", font=F_BOLD, fill=(255, 255, 255))
    d.text((92, y), "Starship Flight 5: The Historic Catch", font=F_TITLE, fill=(255, 255, 255))
    d.text((92, y + 32), "SpaceX • 18M views • 2 weeks ago", font=F_SUB, fill=(170, 170, 180))
    
    # Video Card 2
    y += 82
    kurz = raw_img('kurzgesagt.jpg')
    c_kurz = crop_rounded(kurz, (W, 355), 0)
    img.paste(c_kurz, (0, y))
    
    draw_pill(d, (W - 85, y + 355 - 40, W - 18, y + 355 - 16), fill=(0, 0, 0, 190))
    d.text((W - 74, y + 355 - 38), "10:48", font=F_BADGE, fill=(255, 255, 255))
    
    y += 370
    d.ellipse((24, y, 76, y + 52), fill=(180, 50, 50))
    d.text((42, y + 14), "K", font=F_BOLD, fill=(255, 255, 255))
    d.text((92, y), "The Last Human on Earth: What Happens Next?", font=F_TITLE, fill=(255, 255, 255))
    d.text((92, y + 32), "Kurzgesagt – In a Nutshell • 6.2M views • 5 days ago", font=F_SUB, fill=(170, 170, 180))
    
    # Video Card 3 (peek)
    y += 82
    costa = raw_img('costa_rica.jpg')
    img.paste(costa.resize((W, 355)), (0, y))
    
    # Bottom Navigation
    draw_nav_bar(img, active_idx=0, mode='glass')
    save_both(img, "home.jpg")

# -------------------------------------------------------------
# 3. MeeTune Now Playing (screens/meetune_now_playing.jpg)
# -------------------------------------------------------------
def gen_meetune_now_playing():
    img = Image.new('RGBA', (W, H), (16, 16, 22, 255))
    starboy = raw_img('starboy.jpg')
    
    # Vibrant neon ambient background
    amb = starboy.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(95))
    img.paste(amb, (0, 0))
    
    # Gradient overlay
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        a = min(255, int(110 + y * 0.12))
        od.line((0, y, W, y), fill=(12, 10, 18, a))
    img.alpha_composite(overlay)
    
    draw_status_bar(img)
    d = ImageDraw.Draw(img)
    
    # Top pull handle
    draw_pill(d, (W//2 - 40, 60, W//2 + 40, 68), fill=(255, 255, 255, 90))
    
    # Album art (square)
    art_sz = 440
    ax = (W - art_sz) // 2
    ay = 110
    c_art = crop_rounded(starboy, (art_sz, art_sz), 34)
    img.paste(c_art, (ax, ay), c_art)
    
    # Track title & artist
    y = ay + art_sz + 44
    d.text((45, y), "Starboy", font=F_HEAD, fill=(255, 255, 255))
    d.text((45, y + 46), "The Weeknd ft. Daft Punk", font=F_TITLE, fill=(200, 200, 215))
    
    # Heart icon & 3-dots
    d.ellipse((W - 140, y + 10, W - 92, y + 58), outline=(255, 255, 255, 120), width=2)
    d.polygon([(W - 116, y + 26), (W - 124, y + 34), (W - 116, y + 44), (W - 108, y + 34)], fill=(255, 60, 80))
    d.ellipse((W - 124, y + 24, W - 116, y + 34), fill=(255, 60, 80))
    d.ellipse((W - 116, y + 24, W - 108, y + 34), fill=(255, 60, 80))
    
    d.ellipse((W - 80, y + 10, W - 32, y + 58), outline=(255, 255, 255, 120), width=2)
    d.ellipse((W - 64, y + 32, W - 60, y + 36), fill=(255, 255, 255))
    d.ellipse((W - 56, y + 32, W - 52, y + 36), fill=(255, 255, 255))
    d.ellipse((W - 48, y + 32, W - 44, y + 36), fill=(255, 255, 255))
    
    # Synced lyrics preview pill
    y += 110
    draw_glass_pill(img, (40, y, W - 40, y + 58), tint=(255, 255, 255, 25), outline=(255, 255, 255, 40))
    d = ImageDraw.Draw(img)
    d.text((64, y + 16), "Look what you've done... I'm a starboy", font=F_BOLD, fill=(255, 255, 255))
    d.text((W - 75, y + 16), ">", font=F_BOLD, fill=(200, 200, 200))
    
    # Seek bar
    y += 90
    d.line((45, y, W - 45, y), fill=(255, 255, 255, 70), width=5)
    d.line((45, y, 360, y), fill=(255, 255, 255), width=5)
    d.ellipse((352, y - 8, 368, y + 8), fill=(255, 255, 255))
    d.text((45, y + 16), "2:14", font=F_SM, fill=(200, 200, 210))
    d.text((W - 95, y + 16), "-1:36", font=F_SM, fill=(200, 200, 210))
    
    # Playback Controls
    y += 80
    cx = W // 2
    # Prev
    d.polygon([(cx - 150, y + 35), (cx - 120, y + 15), (cx - 120, y + 55)], fill=(255, 255, 255))
    d.polygon([(cx - 120, y + 35), (cx - 90, y + 15), (cx - 90, y + 55)], fill=(255, 255, 255))
    # Big Pause circle
    d.ellipse((cx - 45, y - 10, cx + 45, y + 80), fill=(255, 255, 255))
    d.rectangle((cx - 18, y + 14, cx - 8, y + 56), fill=(15, 15, 18))
    d.rectangle((cx + 8, y + 14, cx + 18, y + 56), fill=(15, 15, 18))
    # Next
    d.polygon([(cx + 90, y + 15), (cx + 90, y + 55), (cx + 120, y + 35)], fill=(255, 255, 255))
    d.polygon([(cx + 120, y + 15), (cx + 120, y + 55), (cx + 150, y + 35)], fill=(255, 255, 255))
    
    # Audio Quality Pill
    y += 140
    bw = 420
    draw_glass_pill(img, ((W - bw)//2, y, (W + bw)//2, y + 46), tint=(255, 255, 255, 30), outline=(255, 255, 255, 60))
    d = ImageDraw.Draw(img)
    d.text(((W - bw)//2 + 25, y + 11), "[||||]  OPUS • 320 kbps • 48 kHz • Spatial", font=F_BADGE, fill=(255, 255, 255))
    
    # Bottom Actions with vector icons
    y += 85
    d.ellipse((80, y, 136, y + 56), outline=(255, 255, 255, 90), width=2)
    icon_lyrics(d, 108, y + 28, (255, 255, 255))
    
    d.ellipse((cx - 28, y, cx + 28, y + 56), outline=(255, 255, 255, 90), width=2)
    icon_cast(d, cx, y + 28, (255, 255, 255))
    
    d.ellipse((W - 136, y, W - 80, y + 56), outline=(255, 255, 255, 90), width=2)
    icon_queue(d, W - 108, y + 28, (255, 255, 255))
    
    save_both(img, "meetune_now_playing.jpg")

# -------------------------------------------------------------
# 4. MeeTune Home (screens/meetune_home.jpg)
# -------------------------------------------------------------
def gen_meetune_home():
    img = Image.new('RGBA', (W, H), (10, 10, 14, 255))
    draw_status_bar(img)
    
    d = ImageDraw.Draw(img)
    # Top bar with heart logo
    d.ellipse((30, 56, 76, 102), fill=(30, 24, 28))
    d.polygon([(53, 72), (45, 80), (53, 90), (61, 80)], fill=(255, 50, 70))
    d.ellipse((45, 70, 53, 80), fill=(255, 50, 70))
    d.ellipse((53, 70, 61, 80), fill=(255, 50, 70))
    
    d.ellipse((W - 76, 56, W - 30, 102), fill=(40, 40, 50))
    icon_you(d, W - 53, 79, (255, 255, 255))
    
    # Section: New releases
    y = 125
    d.text((28, y), "New releases", font=F_HEAD, fill=(255, 255, 255))
    d.text((W - 110, y + 8), "Show all", font=F_BOLD, fill=(180, 180, 180))
    
    y += 50
    starboy = raw_img('starboy.jpg')
    c_sb = crop_rounded(starboy, (280, 280), 28)
    img.paste(c_sb, (28, y), c_sb)
    
    inter = raw_img('interstellar.jpg')
    c_in = crop_rounded(inter, (280, 280), 28)
    img.paste(c_in, (324, y), c_in)
    
    y += 295
    d.text((28, y), "Starboy (Deluxe)", font=F_BOLD, fill=(255, 255, 255))
    d.text((28, y + 28), "The Weeknd", font=F_SUB, fill=(170, 170, 170))
    d.text((324, y), "Interstellar (OST)", font=F_BOLD, fill=(255, 255, 255))
    d.text((324, y + 28), "Hans Zimmer", font=F_SUB, fill=(170, 170, 170))
    
    # Section: Song mixes
    y += 75
    d.text((28, y), "Song mixes", font=F_HEAD, fill=(255, 255, 255))
    
    mixes = [
        ('coldplay.jpg', 'Viva La Vida', 'Coldplay • 1.2B plays'),
        ('lofi.jpg', 'Synthwave & Coding Beats', 'Lofi Girl • 85M plays'),
        ('costa_rica.jpg', 'Deep Ambient Chillout', 'Nature Sounds • 42M plays'),
    ]
    
    y += 50
    for img_name, title, sub in mixes:
        m_img = raw_img(img_name)
        c_m = crop_rounded(m_img, (76, 76), 16)
        img.paste(c_m, (28, y), c_m)
        d.text((120, y + 10), title, font=F_BOLD, fill=(255, 255, 255))
        d.text((120, y + 40), sub, font=F_SUB, fill=(160, 160, 170))
        d.ellipse((W - 55, y + 36, W - 51, y + 40), fill=(170, 170, 170))
        d.ellipse((W - 45, y + 36, W - 41, y + 40), fill=(170, 170, 170))
        d.ellipse((W - 35, y + 36, W - 31, y + 40), fill=(170, 170, 170))
        y += 96
        
    # Floating Mini-player
    y = H - 195
    draw_glass_pill(img, (24, y, W - 24, y + 76), tint=(28, 26, 36, 235), outline=(255, 255, 255, 50))
    c_mini = crop_rounded(starboy, (56, 56), 14)
    img.paste(c_mini, (36, y + 10), c_mini)
    d = ImageDraw.Draw(img)
    d.text((105, y + 14), "Starboy", font=F_BOLD, fill=(255, 255, 255))
    d.text((105, y + 42), "The Weeknd", font=F_SM, fill=(180, 180, 190))
    
    # Pause button
    d.rectangle((W - 110, y + 26, W - 104, y + 50), fill=(255, 255, 255))
    d.rectangle((W - 98, y + 26, W - 92, y + 50), fill=(255, 255, 255))
    # Next button
    d.polygon([(W - 70, y + 26), (W - 70, y + 50), (W - 54, y + 38)], fill=(255, 255, 255))
    d.line((W - 52, y + 26, W - 52, y + 50), fill=(255, 255, 255), width=3)
    
    draw_nav_bar(img, active_idx=0, mode='glass')
    save_both(img, "meetune_home.jpg")

# -------------------------------------------------------------
# 5. Synced Lyrics (lyrics.jpg)
# -------------------------------------------------------------
def gen_lyrics():
    img = Image.new('RGBA', (W, H), (14, 14, 18, 255))
    coldplay = raw_img('coldplay.jpg')
    
    v_h = 360
    c_vid = coldplay.resize((W, v_h), Image.LANCZOS)
    img.paste(c_vid, (0, 0))
    
    d = ImageDraw.Draw(img)
    d.line((0, v_h - 4, W, v_h - 4), fill=(60, 60, 65), width=4)
    d.line((0, v_h - 4, 210, v_h - 4), fill=(255, 50, 50), width=4)
    
    y_sheet = 345
    overlay = Image.new('RGBA', (W, H - y_sheet), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((0, 0, W-1, H - y_sheet - 1), 32, fill=(18, 24, 34, 240), outline=(255, 255, 255, 40), width=1)
    img.alpha_composite(overlay, (0, y_sheet))
    
    d = ImageDraw.Draw(img)
    draw_pill(d, (W//2 - 36, y_sheet + 14, W//2 + 36, y_sheet + 20), fill=(255, 255, 255, 80))
    
    y = y_sheet + 44
    d.text((36, y), "Lyrics", font=F_HEAD, fill=(255, 255, 255))
    d.text((W - 150, y + 8), "lrc.red v", font=F_SUB, fill=(170, 180, 200))
    d.line((W - 55, y + 14, W - 43, y + 26), fill=(255, 255, 255), width=2)
    d.line((W - 43, y + 14, W - 55, y + 26), fill=(255, 255, 255), width=2)
    
    lines = [
        ("I used to rule the world", False),
        ("Seas would rise when I gave the word", False),
        ("Now in the morning I sleep alone", True),  # ACTIVE
        ("Sweep the streets I used to own", False),
        ("I used to roll the dice", False),
        ("Feel the fear in my enemy's eyes", False),
        ("Listen as the crowd would sing", False),
        ("Now the old king is dead! Long live the king!", False),
        ("One minute I held the key", False),
        ("Next the walls were closed on me", False),
        ("And I discovered that my castles stand", False),
        ("Upon pillars of salt and pillars of sand", False),
    ]
    
    y += 68
    for text, is_active in lines:
        if is_active:
            glow = Image.new('RGBA', (W, 70), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            gd.rounded_rectangle((24, 0, W - 24, 60), 16, fill=(140, 80, 255, 75))
            glow = glow.filter(ImageFilter.GaussianBlur(16))
            img.alpha_composite(glow, (0, y - 8))
            
            d = ImageDraw.Draw(img)
            d.text((36, y), text, font=F_HEAD, fill=(255, 255, 255))
            y += 66
        else:
            d.text((36, y), text, font=F_LYRIC_INACT, fill=(160, 165, 185))
            y += 56
            
    save_both(img, "lyrics.jpg")

# -------------------------------------------------------------
# 6. Most Replayed Graph (screens/most_replayed.jpg)
# -------------------------------------------------------------
def gen_most_replayed():
    img = Image.new('RGBA', (W, H), (14, 14, 18, 255))
    inter = raw_img('interstellar.jpg')
    
    draw_status_bar(img)
    v_h = 356
    c_in = inter.resize((W, v_h), Image.LANCZOS)
    img.paste(c_in, (0, 68))
    
    d = ImageDraw.Draw(img)
    draw_pill(d, (W//2 - 65, 68 + 120, W//2 + 65, 68 + 165), fill=(0, 0, 0, 200))
    d.text((W//2 - 46, 68 + 132), "2:45 / 4:18", font=F_BOLD, fill=(255, 255, 255))
    
    # Most Replayed Waveform
    wave_pts = []
    base_y = 68 + v_h - 6
    for x in range(0, W, 4):
        peak = math.exp(-((x - 360)/90)**2) * 58
        jitter = math.sin(x * 0.1) * 4
        wave_pts.append((x, int(base_y - peak - jitter - 6)))
        
    for i in range(len(wave_pts)-1):
        d.line([wave_pts[i], wave_pts[i+1]], fill=(255, 255, 255, 210), width=3)
        
    d.line((0, base_y, W, base_y), fill=(60, 60, 65), width=5)
    d.line((0, base_y, 80, base_y), fill=(0, 215, 80), width=5)
    d.line((80, base_y, 360, base_y), fill=(255, 45, 45), width=5)
    d.ellipse((352, base_y - 8, 368, base_y + 8), fill=(255, 45, 45))
    
    y = 68 + v_h + 20
    d.text((24, y), "Interstellar - Docking Scene (No Time For Caution)", font=F_TITLE, fill=(255, 255, 255))
    d.text((24, y + 38), "Warner Bros. Entertainment • 45M views • 9 years ago", font=F_SUB, fill=(170, 170, 180))
    
    # Actions
    y += 84
    d.ellipse((24, y, 74, y + 50), fill=(25, 40, 70))
    d.text((38, y + 12), "WB", font=F_BOLD, fill=(255, 255, 255))
    draw_pill(d, (86, y + 4, 210, y + 46), fill=(240, 240, 245))
    d.text((106, y + 14), "Subscribe", font=F_BOLD, fill=(15, 15, 15))
    
    draw_pill(d, (225, y + 4, 375, y + 46), fill=(38, 38, 44))
    icon_like(d, 248, y + 25, (255, 255, 255))
    d.text((264, y + 14), "1.8M", font=F_BOLD, fill=(255, 255, 255))
    d.line((315, y + 12, 315, y + 38), fill=(100, 100, 110), width=1)
    icon_dislike(d, 342, y + 25, (255, 255, 255))
    
    # Comment
    y += 66
    draw_glass_pill(img, (20, y, W - 20, y + 92), tint=(32, 32, 38, 190), outline=(255, 255, 255, 35))
    d = ImageDraw.Draw(img)
    d.text((40, y + 14), "Comments  320K", font=F_BOLD, fill=(255, 255, 255))
    d.ellipse((40, y + 48, 68, y + 76), fill=(80, 160, 220))
    d.text((80, y + 52), "This docking scene with Hans Zimmer's organ is pure perfection.", font=F_SM, fill=(225, 225, 230))
    
    y += 114
    d.text((24, y), "Up next", font=F_BOLD, fill=(255, 255, 255))
    chips = ["All", "Hans Zimmer", "Sci-Fi IMAX", "Soundtracks"]
    draw_chips(img, y + 36, 0, chips)
    
    y += 94
    v_star = raw_img('starship.jpg')
    c_s = crop_rounded(v_star, (W - 48, 280), 22)
    img.paste(c_s, (24, y), c_s)
    
    save_both(img, "most_replayed.jpg")

# -------------------------------------------------------------
# 7. Equalizer & Playback Menu (screens/equalizer.jpg)
# -------------------------------------------------------------
def gen_equalizer():
    img = Image.new('RGBA', (W, H), (10, 10, 12, 255))
    costa = raw_img('costa_rica.jpg')
    
    bg = costa.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(15))
    img.paste(bg, (0, 0))
    
    vign = Image.new('RGBA', (W, H), (0, 0, 0, 170))
    img.alpha_composite(vign)
    
    draw_status_bar(img)
    
    sheet_y = 480
    overlay = Image.new('RGBA', (W, H - sheet_y), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((0, 0, W-1, H - sheet_y - 1), 36, fill=(24, 26, 32, 240), outline=(255, 255, 255, 45), width=1)
    img.alpha_composite(overlay, (0, sheet_y))
    
    d = ImageDraw.Draw(img)
    draw_pill(d, (W//2 - 36, sheet_y + 14, W//2 + 36, sheet_y + 20), fill=(255, 255, 255, 90))
    
    menu_items = [
        ("Quality", "Auto (2160p60 HDR) >"),
        ("Subtitles", "Off >"),
        ("Playback speed", "Normal >"),
        ("Equalizer", "Spatial Bass & Clear Vocal >"),
        ("Autoplay", "On"),
        ("Sleep timer", "Off >"),
        ("Picture-in-picture", "Active"),
        ("Ambient mode", "On"),
        ("True AMOLED Black", "Enabled"),
        ("Auto-scroll", "On"),
        ("More settings", ">"),
    ]
    
    y = sheet_y + 44
    for title, val in menu_items:
        d.text((40, y), title, font=F_TITLE, fill=(255, 255, 255))
        d.text((W - 35 - int(d.textlength(val, font=F_SUB)), y + 4), val, font=F_SUB, fill=(180, 190, 215))
        y += 66
        
    save_both(img, "equalizer.jpg")

# -------------------------------------------------------------
# 8. Channel Page (screens/channel.jpg & channel.jpg)
# -------------------------------------------------------------
def gen_channel():
    img = Image.new('RGBA', (W, H), (10, 10, 14, 255))
    draw_status_bar(img)
    
    d = ImageDraw.Draw(img)
    d.text((28, 60), "← Veritasium", font=F_HEAD, fill=(255, 255, 255))
    draw_pill(d, (W - 195, 58, W - 90, 100), fill=(34, 34, 40))
    d.text((W - 170, 68), "Posts", font=F_BOLD, fill=(255, 255, 255))
    d.ellipse((W - 52, 70, W - 48, 74), fill=(255, 255, 255))
    d.ellipse((W - 52, 78, W - 48, 82), fill=(255, 255, 255))
    d.ellipse((W - 52, 86, W - 48, 90), fill=(255, 255, 255))
    
    y = 115
    banner = raw_img('interstellar.jpg').resize((W, 160), Image.LANCZOS)
    img.paste(banner, (0, y))
    
    y += 180
    d.ellipse((28, y, 108, y + 80), fill=(30, 80, 180))
    d.text((54, y + 20), "V", font=F_HEAD, fill=(255, 255, 255))
    
    d.text((125, y + 6), "Veritasium", font=F_HEAD, fill=(255, 255, 255))
    d.text((125, y + 46), "@veritasium • 16.8M subs • 420 videos", font=F_SUB, fill=(170, 170, 180))
    
    y += 105
    draw_pill(d, (28, y, W - 28, y + 54), fill=(245, 245, 250))
    d.text((W//2 - 50, y + 14), "Subscribed", font=F_BOLD, fill=(15, 15, 15))
    
    y += 76
    tabs = ["Videos", "Shorts", "Live", "Playlists", "Community"]
    x = 28
    for i, t in enumerate(tabs):
        tw = int(d.textlength(t, font=F_BOLD))
        if i == 0:
            d.text((x, y), t, font=F_BOLD, fill=(255, 255, 255))
            d.line((x, y + 32, x + tw, y + 32), fill=(255, 50, 50), width=4)
        else:
            d.text((x, y), t, font=F_BOLD, fill=(160, 160, 170))
        x += tw + 34
        
    y += 56
    veri = raw_img('veritasium.jpg')
    c_v = crop_rounded(veri, (W, 355), 0)
    img.paste(c_v, (0, y))
    draw_pill(d, (W - 85, y + 355 - 40, W - 18, y + 355 - 16), fill=(0, 0, 0, 190))
    d.text((W - 74, y + 355 - 38), "18:42", font=F_BADGE, fill=(255, 255, 255))
    
    y += 368
    d.text((28, y), "The Universe is Hostile to Computers", font=F_TITLE, fill=(255, 255, 255))
    d.text((28, y + 32), "Veritasium • 14M views • 2 weeks ago", font=F_SUB, fill=(170, 170, 180))
    
    draw_nav_bar(img, active_idx=3, mode='glass')
    save_both(img, "channel.jpg")

# -------------------------------------------------------------
# 9. Posts (screens/posts.jpg)
# -------------------------------------------------------------
def gen_posts():
    img = Image.new('RGBA', (W, H), (10, 10, 14, 255))
    draw_status_bar(img)
    
    d = ImageDraw.Draw(img)
    d.text((28, 60), "← Veritasium posts", font=F_HEAD, fill=(255, 255, 255))
    
    y = 120
    draw_glass_card(img, (20, y, W - 20, y + 490), radius=24, tint=(26, 28, 34, 210), outline=(255, 255, 255, 40))
    d = ImageDraw.Draw(img)
    d.ellipse((40, y + 20, 92, y + 72), fill=(30, 80, 180))
    d.text((58, y + 34), "V", font=F_BOLD, fill=(255, 255, 255))
    d.text((106, y + 24), "Veritasium", font=F_BOLD, fill=(255, 255, 255))
    d.text((106, y + 50), "2 days ago", font=F_SM, fill=(160, 160, 170))
    
    d.text((40, y + 92), "Which frontier of physics do you find most mind-bending?", font=F_TITLE, fill=(255, 255, 255))
    
    py = y + 144
    opts = [
        ("Quantum Entanglement & Non-locality", "44%", True),
        ("General Relativity & Black Holes", "34%", False),
        ("Dark Matter & Dark Energy", "15%", False),
        ("String Theory & Multiverse", "7%", False),
    ]
    for opt, pct, is_top in opts:
        fill_bg = (40, 50, 75) if is_top else (32, 34, 40)
        draw_pill(d, (40, py, W - 40, py + 54), fill=fill_bg, outline=(255, 255, 255, 50) if is_top else None)
        d.text((60, py + 14), opt, font=F_BOLD, fill=(255, 255, 255))
        d.text((W - 105, py + 14), pct, font=F_BOLD, fill=(255, 255, 255))
        py += 68
        
    d.text((40, py + 10), "240K votes • 18K likes • 1.4K comments", font=F_SUB, fill=(180, 180, 190))
    
    y += 520
    draw_glass_card(img, (20, y, W - 20, y + 420), radius=24, tint=(26, 28, 34, 210), outline=(255, 255, 255, 40))
    d = ImageDraw.Draw(img)
    d.ellipse((40, y + 20, 92, y + 72), fill=(30, 80, 180))
    d.text((58, y + 34), "V", font=F_BOLD, fill=(255, 255, 255))
    d.text((106, y + 24), "Veritasium", font=F_BOLD, fill=(255, 255, 255))
    d.text((106, y + 50), "1 week ago", font=F_SM, fill=(160, 160, 170))
    d.text((40, y + 90), "Behind the scenes on our upcoming documentary!", font=F_TITLE, fill=(255, 255, 255))
    
    save_both(img, "posts.jpg")

# -------------------------------------------------------------
# 10. YouTube Mode (screens/youtube_mode.jpg)
# -------------------------------------------------------------
def gen_youtube_mode():
    img = Image.new('RGBA', (W, H), (12, 12, 14, 255))
    draw_status_bar(img)
    draw_top_bar(img, show_logo=True)
    draw_chips(img, y=114, active_chip=0, chips=["All", "Music", "Gaming", "News", "4K HDR"])
    
    d = ImageDraw.Draw(img)
    
    y = 175
    costa = raw_img('costa_rica.jpg')
    c_c = crop_rounded(costa, (W, 355), 0)
    img.paste(c_c, (0, y))
    draw_pill(d, (W - 85, y + 355 - 40, W - 18, y + 355 - 16), fill=(0, 0, 0, 190))
    d.text((W - 74, y + 355 - 38), "08:15", font=F_BADGE, fill=(255, 255, 255))
    
    y += 370
    d.ellipse((24, y, 76, y + 52), fill=(40, 120, 60))
    d.text((42, y + 14), "CR", font=F_BOLD, fill=(255, 255, 255))
    d.text((92, y), "Costa Rica in 4K 60fps HDR (Ultra HD)", font=F_TITLE, fill=(255, 255, 255))
    d.text((92, y + 32), "Jacob + Katie Schwarz • 98M views • 1 year ago", font=F_SUB, fill=(170, 170, 180))
    
    y += 82
    boston = raw_img('boston.jpg')
    c_b = crop_rounded(boston, (W, 355), 0)
    img.paste(c_b, (0, y))
    draw_pill(d, (W - 85, y + 355 - 40, W - 18, y + 355 - 16), fill=(0, 0, 0, 190))
    d.text((W - 74, y + 355 - 38), "03:40", font=F_BADGE, fill=(255, 255, 255))
    
    y += 370
    d.ellipse((24, y, 76, y + 52), fill=(20, 70, 140))
    d.text((42, y + 14), "BD", font=F_BOLD, fill=(255, 255, 255))
    d.text((92, y), "Atlas Electric: Next Gen Mobility & Testing", font=F_TITLE, fill=(255, 255, 255))
    d.text((92, y + 32), "Boston Dynamics • 11M views • 2 months ago", font=F_SUB, fill=(170, 170, 180))
    
    draw_nav_bar(img, active_idx=0, mode='flat')
    save_both(img, "youtube_mode.jpg")

# -------------------------------------------------------------
# 11. Subscriptions (screens/subscriptions.jpg)
# -------------------------------------------------------------
def gen_subscriptions():
    img = Image.new('RGBA', (W, H), (10, 10, 14, 255))
    draw_status_bar(img)
    draw_top_bar(img, show_logo=True)
    
    d = ImageDraw.Draw(img)
    y = 115
    channels = [
        ("All", (40, 40, 48), "☰"),
        ("SpaceX", (20, 20, 25), "X"),
        ("Veritasium", (30, 80, 180), "V"),
        ("Kurzgesagt", (190, 50, 50), "K"),
        ("MKBHD", (180, 40, 30), "M"),
        ("Boston", (20, 70, 140), "BD"),
    ]
    x = 24
    for name, col, icon in channels:
        d.ellipse((x, y, x + 68, y + 68), fill=col, outline=(255, 50, 50) if name == "SpaceX" else None, width=2)
        if name == "All":
            d.line((x + 22, y + 26, x + 46, y + 26), fill=(255, 255, 255), width=2)
            d.line((x + 22, y + 34, x + 46, y + 34), fill=(255, 255, 255), width=2)
            d.line((x + 22, y + 42, x + 46, y + 42), fill=(255, 255, 255), width=2)
        else:
            d.text((x + 22, y + 20), icon, font=F_BOLD, fill=(255, 255, 255))
        d.text((x + 6, y + 76), name[:6], font=F_SM, fill=(200, 200, 210))
        x += 98
        
    y = 230
    starship = raw_img('starship.jpg')
    img.paste(crop_rounded(starship, (W, 355), 0), (0, y))
    draw_pill(d, (W - 85, y + 355 - 40, W - 18, y + 355 - 16), fill=(0, 0, 0, 190))
    d.text((W - 74, y + 355 - 38), "14:49", font=F_BADGE, fill=(255, 255, 255))
    
    y += 370
    d.ellipse((24, y, 76, y + 52), fill=(25, 25, 30))
    d.text((42, y + 14), "X", font=F_BOLD, fill=(255, 255, 255))
    d.text((92, y), "Starship's Fifth Flight Test - Official 4K", font=F_TITLE, fill=(255, 255, 255))
    d.text((92, y + 32), "SpaceX • 18M views • 2 weeks ago", font=F_SUB, fill=(170, 170, 180))
    
    y += 82
    kurz = raw_img('kurzgesagt.jpg')
    img.paste(crop_rounded(kurz, (W, 355), 0), (0, y))
    draw_pill(d, (W - 85, y + 355 - 40, W - 18, y + 355 - 16), fill=(0, 0, 0, 190))
    d.text((W - 74, y + 355 - 38), "10:48", font=F_BADGE, fill=(255, 255, 255))
    
    y += 370
    d.ellipse((24, y, 76, y + 52), fill=(180, 50, 50))
    d.text((42, y + 14), "K", font=F_BOLD, fill=(255, 255, 255))
    d.text((92, y), "Can We Terraform Mars? The Harsh Reality", font=F_TITLE, fill=(255, 255, 255))
    d.text((92, y + 32), "Kurzgesagt – In a Nutshell • 4.8M views • 1 week ago", font=F_SUB, fill=(170, 170, 180))
    
    draw_nav_bar(img, active_idx=3, mode='glass')
    save_both(img, "subscriptions.jpg")

# -------------------------------------------------------------
# 12. Search (screens/search.jpg & search.jpg)
# -------------------------------------------------------------
def gen_search():
    img = Image.new('RGBA', (W, H), (10, 10, 14, 255))
    draw_status_bar(img)
    
    y = 60
    draw_glass_pill(img, (20, y, W - 20, y + 64), tint=(28, 30, 38, 220), outline=(255, 255, 255, 45))
    d = ImageDraw.Draw(img)
    d.text((40, y + 16), "←", font=F_HEAD, fill=(255, 255, 255))
    d.text((80, y + 18), "4K HDR OLED Nature", font=F_TITLE, fill=(255, 255, 255))
    d.line((W - 65, y + 24, W - 51, y + 38), fill=(200, 200, 210), width=2)
    d.line((W - 51, y + 24, W - 65, y + 38), fill=(200, 200, 210), width=2)
    
    draw_chips(img, y=140, active_chip=0, chips=["All", "Videos", "Shorts", "4K 60fps", "Channels"])
    
    y = 205
    costa = raw_img('costa_rica.jpg')
    c_c = crop_rounded(costa, (282, 390), 24)
    img.paste(c_c, (24, y), c_c)
    
    inter = raw_img('interstellar.jpg')
    c_i = crop_rounded(inter, (282, 390), 24)
    img.paste(c_i, (326, y), c_i)
    
    y += 405
    starboy = raw_img('starboy.jpg')
    c_s = crop_rounded(starboy, (282, 390), 24)
    img.paste(c_s, (24, y), c_s)
    
    lofi = raw_img('lofi.jpg')
    c_l = crop_rounded(lofi, (282, 390), 24)
    img.paste(c_l, (326, y), c_l)
    
    draw_nav_bar(img, active_idx=2, mode='glass')
    save_both(img, "search.jpg")

# -------------------------------------------------------------
# 13. You / Offline (screens/you.jpg)
# -------------------------------------------------------------
def gen_you():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255)) # True AMOLED
    draw_status_bar(img)
    draw_top_bar(img, show_logo=True)
    
    d = ImageDraw.Draw(img)
    y = 125
    d.ellipse((36, y, 126, y + 90), outline=(255, 255, 255, 70), width=2)
    icon_you(d, 81, y + 45, (255, 255, 255))
    
    d.text((150, y + 14), "MeuTube User", font=F_HEAD, fill=(255, 255, 255))
    d.text((150, y + 54), "Entrepreneur Mode (AMOLED)", font=F_SUB, fill=(0, 215, 90))
    
    y += 115
    draw_pill(d, (36, y, W//2 - 10, y + 52), fill=(26, 26, 32))
    d.text((70, y + 14), "Switch account", font=F_BOLD, fill=(255, 255, 255))
    draw_pill(d, (W//2 + 10, y, W - 36, y + 52), fill=(26, 26, 32))
    d.text((W//2 + 55, y + 14), "Settings", font=F_BOLD, fill=(255, 255, 255))
    
    y += 85
    d.text((36, y), "Library", font=F_HEAD, fill=(255, 255, 255))
    
    items = [
        ("Downloads", "4K Smart downloads active"),
        ("History", "Seamless playback memory"),
        ("Playlists", "12 saved playlists"),
        ("Liked videos", "340 videos"),
        ("SponsorBlock", "Saved 6.4 hours of ads"),
    ]
    
    y += 50
    for title, desc in items:
        draw_glass_pill(img, (28, y, W - 28, y + 78), tint=(20, 20, 26, 220), outline=(255, 255, 255, 30))
        d = ImageDraw.Draw(img)
        d.text((50, y + 14), title, font=F_BOLD, fill=(255, 255, 255))
        d.text((50, y + 44), desc, font=F_SM, fill=(160, 160, 170))
        d.text((W - 65, y + 26), ">", font=F_BOLD, fill=(150, 150, 160))
        y += 92
        
    draw_nav_bar(img, active_idx=4, mode='glass')
    save_both(img, "you.jpg")

# -------------------------------------------------------------
# 14. Downloads (downloads.jpg)
# -------------------------------------------------------------
def gen_downloads():
    img = Image.new('RGBA', (W, H), (8, 8, 12, 255))
    draw_status_bar(img)
    
    d = ImageDraw.Draw(img)
    d.text((32, 60), "← Downloads", font=F_HEAD, fill=(255, 255, 255))
    icon_cast(d, W - 50, 76, (255, 255, 255))
    
    dls = [
        ('starship.jpg', "Starship Flight 5 - SpaceX", "4K 2160p • 1.4 GB • Downloaded"),
        ('starboy.jpg', "Starboy - The Weeknd", "Audio FLAC • 42 MB • Downloaded"),
        ('costa_rica.jpg', "Costa Rica in 4K HDR", "4K 2160p • 1.8 GB • Downloaded"),
        ('kurzgesagt.jpg', "Can We Terraform Mars?", "1080p60 • 320 MB • Downloaded"),
    ]
    
    y = 135
    for img_name, title, meta in dls:
        raw = raw_img(img_name)
        c_i = crop_rounded(raw, (W - 48, 260), 22)
        img.paste(c_i, (24, y), c_i)
        draw_pill(d, (W - 95, y + 215, W - 38, y + 245), fill=(0, 200, 80))
        d.text((W - 80, y + 221), "✓", font=F_BOLD, fill=(255, 255, 255))
        
        y += 275
        d.text((28, y), title, font=F_TITLE, fill=(255, 255, 255))
        d.text((28, y + 32), meta, font=F_SUB, fill=(160, 160, 175))
        y += 72
        
    draw_nav_bar(img, active_idx=4, mode='glass')
    img_rgb = img.convert('RGB')
    img_rgb.save(os.path.join(OUT_ROOT, "downloads.jpg"), quality=94)
    print("Saved downloads.jpg")

# -------------------------------------------------------------
# 15. Shorts (shorts.jpg)
# -------------------------------------------------------------
def gen_shorts():
    img = Image.new('RGBA', (W, H), (10, 10, 14, 255))
    boston = raw_img('boston.jpg')
    
    bg = boston.resize((W, H), Image.LANCZOS)
    img.paste(bg, (0, 0))
    
    d = ImageDraw.Draw(img)
    draw_status_bar(img)
    d.text((32, 55), "← Shorts", font=F_HEAD, fill=(255, 255, 255))
    
    actions = [
        (icon_like, "840K"),
        (icon_dislike, "Dislike"),
        (icon_queue, "14K"),
        (icon_share, "Share"),
        (icon_download, "Save"),
    ]
    
    y = H - 560
    for fn, label in actions:
        d.ellipse((W - 75, y, W - 25, y + 50), fill=(0, 0, 0, 140))
        fn(d, W - 50, y + 25, (255, 255, 255))
        d.text((W - 65, y + 56), label, font=F_SM, fill=(255, 255, 255))
        y += 88
        
    y = H - 180
    d.ellipse((28, y, 76, y + 48), fill=(20, 70, 140))
    d.text((42, y + 12), "BD", font=F_BOLD, fill=(255, 255, 255))
    d.text((90, y + 10), "@BostonDynamics", font=F_BOLD, fill=(255, 255, 255))
    draw_pill(d, (290, y + 6, 400, y + 44), fill=(255, 0, 0))
    d.text((308, y + 14), "Subscribe", font=F_BOLD, fill=(255, 255, 255))
    
    d.text((28, y + 62), "Testing agility and balance on our new electric Atlas! 🤖", font=F_SUB, fill=(255, 255, 255))
    
    img_rgb = img.convert('RGB')
    img_rgb.save(os.path.join(OUT_ROOT, "shorts.jpg"), quality=94)
    print("Saved shorts.jpg")

if __name__ == '__main__':
    print("Generating all fresh screenshots...")
    gen_compact_player()
    gen_home()
    gen_meetune_now_playing()
    gen_meetune_home()
    gen_lyrics()
    gen_most_replayed()
    gen_equalizer()
    gen_channel()
    gen_posts()
    gen_youtube_mode()
    gen_subscriptions()
    gen_search()
    gen_you()
    gen_downloads()
    gen_shorts()
    print("All screenshots generated successfully!")
