#!/usr/bin/env python3
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def draw_newspaper():
    # Canvas dimensions: 1024 x 1024
    width, height = 1024, 1024
    bg_color = (246, 243, 236)  # Warm newsprint cream
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    font_dir = "assets"
    reg_path = os.path.join(font_dir, "DejaVuSans.ttf")
    bold_path = os.path.join(font_dir, "DejaVuSans-Bold.ttf")

    def get_font(size, bold=False):
        path = bold_path if bold else reg_path
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()

    font_masthead = get_font(36, bold=True)
    font_subdate = get_font(12, bold=False)
    font_sec_title = get_font(13, bold=True)
    font_headline = get_font(16, bold=True)
    font_lead_headline = get_font(20, bold=True)
    font_body = get_font(10.5, bold=False)
    font_lead_body = get_font(12, bold=False)
    font_tag = get_font(10, bold=True)
    font_keyfact = get_font(10, bold=True)

    # Helper: draw text with wrapping
    def draw_wrapped_text(draw, text, box, font, fill=(30, 30, 30), spacing=3):
        x, y, max_w, max_h = box
        words = text.split(" ")
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            try:
                w = font.getlength(test_line)
            except AttributeError:
                bbox = font.getbbox(test_line)
                w = bbox[2] - bbox[0]
            if w <= max_w:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        if current_line:
            lines.append(" ".join(current_line))

        cur_y = y
        line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1] + spacing
        for line in lines:
            if cur_y + line_height > y + max_h:
                break
            draw.text((x, cur_y), line, font=font, fill=fill)
            cur_y += line_height
        return cur_y

    # Helper: draw headline with automatic sizing and wrapping to fit box
    def draw_heading(draw, text, box, initial_size, bold=True, max_lines=2, fill=(20, 20, 20), spacing=2):
        x, y, max_w, max_h = box
        size = initial_size
        while size >= 10:
            font = get_font(size, bold=bold)
            words = text.split(" ")
            lines = []
            current_line = []
            possible = True
            for word in words:
                test_line = " ".join(current_line + [word])
                try:
                    w = font.getlength(test_line)
                except AttributeError:
                    bbox = font.getbbox(test_line)
                    w = bbox[2] - bbox[0]
                if w <= max_w:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        possible = False
                        break
            if current_line:
                lines.append(" ".join(current_line))
            
            if possible and len(lines) <= max_lines:
                break
            size -= 1

        cur_y = y
        line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1] + spacing
        for line in lines:
            draw.text((x, cur_y), line, font=font, fill=fill)
            cur_y += line_height
        return cur_y

    # --- 1. MASTHEAD ---
    draw.rectangle([16, 12, 1008, 85], fill=(240, 235, 224), outline=(180, 175, 165), width=1)
    draw.text((28, 18), "THE WORLD", font=font_masthead, fill=(20, 20, 20))
    draw.text((28, 58), "TUESDAY, 17 NOVEMBER 2026", font=font_subdate, fill=(100, 95, 90))
    draw.text((780, 58), "EDITION: GLOBAL BRIEFING", font=font_subdate, fill=(100, 95, 90))
    draw.line([16, 88, 1008, 88], fill=(40, 40, 40), width=3)
    draw.line([16, 92, 1008, 92], fill=(40, 40, 40), width=1)

    # --- 2. LEAD STORY (KERCH BRIDGE) ---
    # Y: 98 to 380
    lead_box = [16, 98, 1008, 382]
    draw.rectangle(lead_box, fill=(250, 248, 242), outline=(190, 185, 175), width=1)
    
    # Accent bar for lead
    draw.rectangle([16, 98, 1008, 114], fill=(180, 40, 40))
    draw.text((24, 100), "SPECIAL REPORT • LEAD STORY", font=font_tag, fill=(255, 255, 255))
    draw.text((880, 100), "UKRAINE / RUSSIA", font=font_tag, fill=(255, 255, 255))

    # Left side of lead: Illustration (Kerch bridge with broken span, water, smoke)
    ill_x, ill_y, ill_w, ill_h = 28, 124, 420, 212
    draw.rectangle([ill_x, ill_y, ill_x + ill_w, ill_y + ill_h], fill=(210, 225, 235), outline=(160, 175, 185))
    # Sea
    draw.rectangle([ill_x, ill_y + 110, ill_x + ill_w, ill_y + ill_h], fill=(70, 110, 140))
    # Waves
    for wx in range(ill_x + 10, ill_x + ill_w - 20, 30):
        draw.arc([wx, ill_y + 130, wx + 20, ill_y + 150], 0, 180, fill=(100, 140, 170), width=2)
    # Bridge piers & left deck
    draw.line([ill_x + 20, ill_y + 100, ill_x + 160, ill_y + 100], fill=(90, 90, 90), width=12)
    draw.line([ill_x + 60, ill_y + 100, ill_x + 60, ill_y + ill_h], fill=(70, 70, 70), width=6)
    draw.line([ill_x + 130, ill_y + 100, ill_x + 130, ill_y + ill_h], fill=(70, 70, 70), width=6)
    # Right deck
    draw.line([ill_x + 260, ill_y + 100, ill_x + ill_w - 20, ill_y + 100], fill=(90, 90, 90), width=12)
    draw.line([ill_x + 320, ill_y + 100, ill_x + 320, ill_y + ill_h], fill=(70, 70, 70), width=6)
    draw.line([ill_x + 380, ill_y + 100, ill_x + 380, ill_y + ill_h], fill=(70, 70, 70), width=6)
    # Broken middle span (angled down into gap)
    draw.line([ill_x + 160, ill_y + 100, ill_x + 210, ill_y + 130], fill=(110, 110, 110), width=10)
    draw.line([ill_x + 210, ill_y + 130, ill_x + 260, ill_y + 100], fill=(110, 110, 110), width=10)
    # Smoke plume / explosion
    draw.ellipse([ill_x + 180, ill_y + 40, ill_x + 230, ill_y + 90], fill=(140, 140, 140))
    draw.ellipse([ill_x + 210, ill_y + 20, ill_x + 270, ill_y + 80], fill=(110, 110, 110))
    draw.ellipse([ill_x + 160, ill_y + 50, ill_x + 205, ill_y + 95], fill=(210, 130, 50))
    
    # Illustration caption/label below illustration box
    draw.text((ill_x, ill_y + ill_h + 4), "Kerch Bridge: Span collapsed into sea after overnight strike", font=font_subdate, fill=(80, 80, 80))

    # Right side of lead: Headline & Body & Key Fact
    text_x = ill_x + ill_w + 16
    text_w = 1008 - text_x - 16
    
    lead_head = "UKRAINE STRIKES KERCH BRIDGE; RUSSIA HITS KYIV"
    next_y = draw_heading(draw, lead_head, [text_x, 124, text_w, 55], 20, bold=True, max_lines=2)
    
    lead_summary = (
        "Ukraine struck the strategic Kerch Bridge linking Russia to occupied Crimea overnight in what "
        "President Zelensky called an 'unprecedented operation.' A major road span collapsed into the sea, "
        "halting vehicle traffic while some trains resumed. Two people were killed in Crimea. "
        "Hours earlier, Russian ballistic missiles hit the South and North bridges over the Dnipro in Kyiv, "
        "severing crucial heating lines to hundreds of buildings across the capital."
    )
    next_y = draw_wrapped_text(draw, lead_summary, [text_x, next_y + 6, text_w, 140], font_lead_body, fill=(40, 40, 40), spacing=4)
    
    # Key fact line for lead
    draw.text((text_x, next_y + 4), "• Key Fact: Two people were killed in Crimea during the strike.", font=font_keyfact, fill=(150, 30, 30))


    # --- 3. SECOND ROW (2 PANELS: GULF & MANILA) ---
    # Y: 392 to 625
    row2_y = 392
    panel_w2 = 492
    panel_h2 = 233

    # Panel 1: Gulf
    p1_x = 16
    draw.rectangle([p1_x, row2_y, p1_x + panel_w2, row2_y + panel_h2], fill=(250, 248, 242), outline=(190, 185, 175), width=1)
    draw.rectangle([p1_x, row2_y, p1_x + panel_w2, row2_y + 18], fill=(40, 90, 140))
    draw.text((p1_x + 8, row2_y + 2), "GULF CRISIS", font=font_tag, fill=(255, 255, 255))
    draw.text((p1_x + panel_w2 - 70, row2_y + 2), "BAHRAIN", font=font_tag, fill=(255, 255, 255))

    # Gulf illustration (Radar dish + 2 small drone silhouettes + tanker with mine)
    g_ill_x, g_ill_y, g_ill_w, g_ill_h = p1_x + 12, row2_y + 24, 160, 165
    draw.rectangle([g_ill_x, g_ill_y, g_ill_x + g_ill_w, g_ill_y + g_ill_h], fill=(225, 220, 210), outline=(180, 175, 165))
    # Water at bottom of Gulf illustration
    draw.rectangle([g_ill_x, g_ill_y + 120, g_ill_x + g_ill_w, g_ill_y + g_ill_h], fill=(70, 110, 140))
    # Waves
    for wx in range(g_ill_x + 10, g_ill_x + g_ill_w - 20, 30):
        draw.arc([wx, g_ill_y + 140, wx + 20, g_ill_y + 160], 0, 180, fill=(100, 140, 170), width=2)
    # Radar dish on left
    draw.arc([g_ill_x + 10, g_ill_y + 25, g_ill_x + 55, g_ill_y + 70], 180, 360, fill=(50, 50, 50), width=3)
    draw.line([g_ill_x + 32, g_ill_y + 47, g_ill_x + 32, g_ill_y + 120], fill=(50, 50, 50), width=3)
    # 2 Small drone silhouettes in sky
    draw.line([g_ill_x + 50, g_ill_y + 20, g_ill_x + 75, g_ill_y + 20], fill=(30, 30, 30), width=2)
    draw.line([g_ill_x + 62, g_ill_y + 16, g_ill_x + 62, g_ill_y + 24], fill=(30, 30, 30), width=2)
    draw.line([g_ill_x + 85, g_ill_y + 30, g_ill_x + 110, g_ill_y + 30], fill=(30, 30, 30), width=2)
    draw.line([g_ill_x + 97, g_ill_y + 26, g_ill_x + 97, g_ill_y + 34], fill=(30, 30, 30), width=2)
    # Tanker with fire / mine on right
    draw.rectangle([g_ill_x + 90, g_ill_y + 95, g_ill_x + 145, g_ill_y + 115], fill=(100, 100, 100)) # hull
    draw.ellipse([g_ill_x + 115, g_ill_y + 70, g_ill_x + 135, g_ill_y + 100], fill=(180, 50, 30)) # fire
    draw.ellipse([g_ill_x + 100, g_ill_y + 110, g_ill_x + 112, g_ill_y + 122], fill=(40, 40, 40)) # mine

    # Gulf caption strictly below illustration (clear of body text)
    draw.text((g_ill_x, g_ill_y + g_ill_h + 4), "Radar target & Tanker mine", font=font_subdate, fill=(80, 80, 80))

    gulf_text_x = p1_x + 180
    gulf_text_w = panel_w2 - 192
    gulf_head = "IRAN DRONES TARGET US RADAR; 4TH TANKER HIT"
    gulf_next_y = draw_heading(draw, gulf_head, [gulf_text_x, row2_y + 24, gulf_text_w, 45], 13, bold=True, max_lines=2)

    gulf_body = (
        "Iran's Revolutionary Guard fired drones at a US military radar at Sheikh Isa air base in Bahrain; "
        "Bahrain reported the attack was intercepted with no casualties. Meanwhile, a fourth oil tanker "
        "caught fire within 24 hours in the Strait of Hormuz after striking a naval mine."
    )
    gulf_next_y = draw_wrapped_text(draw, gulf_body, [gulf_text_x, gulf_next_y + 4, gulf_text_w, 110], font_body, fill=(40, 40, 40), spacing=3)
    draw.text((gulf_text_x, row2_y + 212), "• Fact: Attack intercepted with no casualties.", font=font_keyfact, fill=(150, 30, 30))


    # Panel 2: Manila / ASEAN
    p2_x = 516
    draw.rectangle([p2_x, row2_y, p2_x + panel_w2, row2_y + panel_h2], fill=(250, 248, 242), outline=(190, 185, 175), width=1)
    draw.rectangle([p2_x, row2_y, p2_x + panel_w2, row2_y + 18], fill=(90, 50, 120))
    draw.text((p2_x + 8, row2_y + 2), "ASEAN SUMMIT", font=font_tag, fill=(255, 255, 255))
    draw.text((p2_x + panel_w2 - 64, row2_y + 2), "MANILA", font=font_tag, fill=(255, 255, 255))

    # ASEAN illustration (Manila skyline + 4 small flags for Quad: US, JP, IN, AU)
    m_ill_x, m_ill_y, m_ill_w, m_ill_h = p2_x + 12, row2_y + 24, 160, 165
    draw.rectangle([m_ill_x, m_ill_y, m_ill_x + m_ill_w, m_ill_y + m_ill_h], fill=(225, 220, 210), outline=(180, 175, 165))
    # Skyline buildings
    draw.rectangle([m_ill_x + 15, m_ill_y + 70, m_ill_x + 40, m_ill_y + 165], fill=(130, 130, 140))
    draw.rectangle([m_ill_x + 42, m_ill_y + 50, m_ill_x + 75, m_ill_y + 165], fill=(110, 110, 120))
    draw.rectangle([m_ill_x + 78, m_ill_y + 80, m_ill_x + 105, m_ill_y + 165], fill=(140, 140, 150))
    # 4 small Quad flags on poles
    for fi, fx in enumerate([m_ill_x + 20, m_ill_x + 55, m_ill_x + 90, m_ill_x + 125]):
        draw.line([fx, m_ill_y + 35, fx, m_ill_y + 75], fill=(60, 60, 60), width=2)
        draw.rectangle([fx, m_ill_y + 25, fx + 14, m_ill_y + 37], fill=(180 - fi*30, 50 + fi*30, 100))

    draw.text((m_ill_x, m_ill_y + m_ill_h + 4), "Manila skyline & Quad flags", font=font_subdate, fill=(80, 80, 80))

    asean_text_x = p2_x + 180
    asean_text_w = panel_w2 - 192
    asean_head = "TRUMP MEETS QUAD LEADERS; 1,500 PROTEST"
    asean_next_y = draw_heading(draw, asean_head, [asean_text_x, row2_y + 24, asean_text_w, 45], 13, bold=True, max_lines=2)

    asean_body = (
        "Donald Trump arrived in Manila for the ASEAN summit and met Quad leaders for the first time "
        "since returning to office. About 1,500 protesters rallied outside. Trump is scheduled to "
        "travel to Shenzhen on Thursday to meet Xi Jinping and Vladimir Putin."
    )
    asean_next_y = draw_wrapped_text(draw, asean_body, [asean_text_x, asean_next_y + 4, asean_text_w, 110], font_body, fill=(40, 40, 40), spacing=3)
    draw.text((asean_text_x, row2_y + 212), "• Fact: Traveling to Shenzhen to meet Xi & Putin.", font=font_keyfact, fill=(150, 30, 30))


    # --- 4. THIRD ROW (3 PANELS: GAZA, JAPAN, YEMEN) ---
    # Y: 637 to 865
    row3_y = 637
    panel_w3 = 320
    panel_h3 = 228

    # Panel 1: Gaza
    gza_x = 16
    draw.rectangle([gza_x, row3_y, gza_x + panel_w3, row3_y + panel_h3], fill=(250, 248, 242), outline=(190, 185, 175), width=1)
    draw.rectangle([gza_x, row3_y, gza_x + panel_w3, row3_y + 18], fill=(160, 90, 40))
    draw.text((gza_x + 8, row3_y + 2), "HUMANITARIAN", font=font_tag, fill=(255, 255, 255))
    draw.text((gza_x + panel_w3 - 48, row3_y + 2), "GAZA", font=font_tag, fill=(255, 255, 255))

    gaza_head = "WEST URGES GAZA BORDER OPENING"
    gaza_next_y = draw_heading(draw, gaza_head, [gza_x + 12, row3_y + 24, panel_w3 - 24, 38], 13, bold=True, max_lines=2)

    gaza_body = (
        "The UK, Australia, Canada and Italy jointly urged Israel to open Gaza crossings for humanitarian "
        "aid, describing the ongoing civilian situation as catastrophic."
    )
    gaza_next_y = draw_wrapped_text(draw, gaza_body, [gza_x + 12, gaza_next_y + 4, panel_w3 - 24, 75], font_body, fill=(40, 40, 40), spacing=3)

    # Gaza Illustration: Aid trucks at crossing gate
    gz_ill_x, gz_ill_y, gz_ill_w, gz_ill_h = gza_x + 12, row3_y + 142, 296, 60
    draw.rectangle([gz_ill_x, gz_ill_y, gz_ill_x + gz_ill_w, gz_ill_y + gz_ill_h], fill=(225, 220, 210), outline=(170, 165, 155))
    # Gate barrier poles
    draw.rectangle([gz_ill_x + 20, gz_ill_y + 15, gz_ill_x + 30, gz_ill_y + 55], fill=(120, 120, 120))
    draw.line([gz_ill_x + 30, gz_ill_y + 25, gz_ill_x + 100, gz_ill_y + 25], fill=(180, 50, 40), width=4) # barrier arm
    # Aid trucks
    draw.rectangle([gz_ill_x + 120, gz_ill_y + 25, gz_ill_x + 180, gz_ill_y + 50], fill=(200, 190, 170))
    draw.rectangle([gz_ill_x + 185, gz_ill_y + 28, gz_ill_x + 230, gz_ill_y + 50], fill=(160, 150, 130))
    draw.ellipse([gz_ill_x + 135, gz_ill_y + 45, gz_ill_x + 150, gz_ill_y + 58], fill=(40, 40, 40))
    draw.ellipse([gz_ill_x + 200, gz_ill_y + 45, gz_ill_x + 215, gz_ill_y + 58], fill=(40, 40, 40))
    draw.text((gz_ill_x + 4, gz_ill_y + 46), "Aid Crossing Gate", font=font_subdate, fill=(80, 80, 80))
    draw.text((gza_x + 12, row3_y + 208), "• Fact: Situation described as catastrophic.", font=font_keyfact, fill=(150, 30, 30))


    # Panel 2: Japan
    jap_x = 352
    draw.rectangle([jap_x, row3_y, jap_x + panel_w3, row3_y + panel_h3], fill=(250, 248, 242), outline=(190, 185, 175), width=1)
    draw.rectangle([jap_x, row3_y, jap_x + panel_w3, row3_y + 18], fill=(50, 110, 80))
    draw.text((jap_x + 8, row3_y + 2), "DEFENSE", font=font_tag, fill=(255, 255, 255))
    draw.text((jap_x + panel_w3 - 52, row3_y + 2), "JAPAN", font=font_tag, fill=(255, 255, 255))

    japan_head = "JAPAN JETS SCRAMBLED OVER RUSSIAN AIRCRAFT"
    japan_next_y = draw_heading(draw, japan_head, [jap_x + 12, row3_y + 24, panel_w3 - 24, 38], 13, bold=True, max_lines=2)

    japan_body = (
        "Japan scrambled fighter jets after two suspected Russian aircraft violated its airspace. "
        "Tokyo lodged a strong diplomatic protest following the interception."
    )
    japan_next_y = draw_wrapped_text(draw, japan_body, [jap_x + 12, japan_next_y + 4, panel_w3 - 24, 75], font_body, fill=(40, 40, 40), spacing=3)

    # Japan Illustration: 2 fighter jets in sky with contrails
    jp_ill_x, jp_ill_y, jp_ill_w, jp_ill_h = jap_x + 12, row3_y + 142, 296, 60
    draw.rectangle([jp_ill_x, jp_ill_y, jp_ill_x + jp_ill_w, jp_ill_y + jp_ill_h], fill=(215, 225, 235), outline=(170, 175, 185))
    # Contrails
    draw.line([jp_ill_x + 20, jp_ill_y + 20, jp_ill_x + 130, jp_ill_y + 25], fill=(240, 240, 240), width=2)
    draw.line([jp_ill_x + 30, jp_ill_y + 40, jp_ill_x + 140, jp_ill_y + 45], fill=(240, 240, 240), width=2)
    # Jets (polygons)
    draw.polygon([(jp_ill_x + 120, jp_ill_y + 22), (jp_ill_x + 140, jp_ill_y + 25), (jp_ill_x + 115, jp_ill_y + 28)], fill=(100, 110, 120))
    draw.polygon([(jp_ill_x + 130, jp_ill_y + 42), (jp_ill_x + 150, jp_ill_y + 45), (jp_ill_x + 125, jp_ill_y + 48)], fill=(100, 110, 120))
    draw.text((jp_ill_x + 4, jp_ill_y + 46), "Fighter Jets Intercept", font=font_subdate, fill=(80, 80, 80))
    draw.text((jap_x + 12, row3_y + 208), "• Fact: Lodged strong diplomatic protest.", font=font_keyfact, fill=(150, 30, 30))


    # Panel 3: Yemen
    yem_x = 688
    draw.rectangle([yem_x, row3_y, yem_x + panel_w3, row3_y + panel_h3], fill=(250, 248, 242), outline=(190, 185, 175), width=1)
    draw.rectangle([yem_x, row3_y, yem_x + panel_w3, row3_y + 18], fill=(120, 40, 80))
    draw.text((yem_x + 8, row3_y + 2), "CONFLICT", font=font_tag, fill=(255, 255, 255))
    draw.text((yem_x + panel_w3 - 60, row3_y + 2), "YEMEN", font=font_tag, fill=(255, 255, 255))

    yemen_head = "HOUTHIS ADVANCE TO ADEN; SAUDI COMMANDER"
    yemen_next_y = draw_heading(draw, yemen_head, [yem_x + 12, row3_y + 24, panel_w3 - 24, 38], 13, bold=True, max_lines=2)

    yemen_body = (
        "Houthi fighters advanced to about 60 km from Aden. Government forces retreated from the Red Sea coast "
        "to defend the southern port city, while Saudi Arabia replaced its coalition commander."
    )
    yemen_next_y = draw_wrapped_text(draw, yemen_body, [yem_x + 12, yemen_next_y + 4, panel_w3 - 24, 75], font_body, fill=(40, 40, 40), spacing=3)

    # Yemen Illustration: Desert dunes + column/arrow advancing toward labelled "ADEN"
    ym_ill_x, ym_ill_y, ym_ill_w, ym_ill_h = yem_x + 12, row3_y + 142, 296, 60
    draw.rectangle([ym_ill_x, ym_ill_y, ym_ill_x + ym_ill_w, ym_ill_y + ym_ill_h], fill=(235, 225, 205), outline=(180, 170, 150))
    # Desert dunes (arcs/curves)
    draw.arc([ym_ill_x + 10, ym_ill_y + 20, ym_ill_x + 120, ym_ill_y + 70], 180, 360, fill=(200, 180, 140), width=3)
    draw.arc([ym_ill_x + 90, ym_ill_y + 30, ym_ill_x + 200, ym_ill_y + 80], 180, 360, fill=(190, 170, 130), width=3)
    # Advancing arrow / column
    draw.line([ym_ill_x + 30, ym_ill_y + 35, ym_ill_x + 180, ym_ill_y + 35], fill=(180, 40, 40), width=3)
    draw.polygon([(ym_ill_x + 180, ym_ill_y + 28), (ym_ill_x + 195, ym_ill_y + 35), (ym_ill_x + 180, ym_ill_y + 42)], fill=(180, 40, 40))
    # ADEN label box
    draw.rectangle([ym_ill_x + 220, ym_ill_y + 15, ym_ill_x + 280, ym_ill_y + 45], fill=(80, 80, 80), outline=(50, 50, 50))
    draw.text((ym_ill_x + 233, ym_ill_y + 22), "ADEN", font=font_tag, fill=(255, 255, 255))
    
    draw.text((ym_ill_x + 4, ym_ill_y + 46), "Houthi Advance on Aden", font=font_subdate, fill=(80, 80, 80))
    draw.text((yem_x + 12, row3_y + 208), "• Fact: Forces retreated from Red Sea coast.", font=font_keyfact, fill=(150, 30, 30))


    # --- 5. BOTTOM STRIP: ALSO TODAY ---
    # Y: 874 to 1012
    bot_y = 874
    draw.rectangle([16, bot_y, 1008, 1012], fill=(240, 235, 224), outline=(180, 175, 165), width=1)
    draw.rectangle([16, bot_y, 1008, bot_y + 20], fill=(50, 50, 50))
    draw.text((24, bot_y + 3), "ALSO TODAY — GLOBAL BRIEFS", font=font_tag, fill=(255, 255, 255))

    briefs_y = bot_y + 26
    col_w = 236
    col_gap = 12
    start_x = 24

    briefs = [
        ("EU-RWANDA MIGRANT HUB", "Austria, Denmark, Germany, Greece and Netherlands plan a migrant return hub in Rwanda for rejected asylum seekers (~100 pilot in 2027)."),
        ("DEPARDIEU PLEADS GUILTY", "French actor Gérard Depardieu pleaded guilty to sexual assault and dropped his appeal in a Paris court ruling."),
        ("PATTINSON IS JAMES BOND", "Robert Pattinson was officially named the next James Bond by Amazon MGM, with Denis Villeneuve directing."),
        ("BITCOIN STALLS <$65K", "Cryptocurrency markets remain subdued, with Bitcoin stalled below $65,000, down more than 15% this month.")
    ]

    for i, (b_title, b_desc) in enumerate(briefs):
        cx = start_x + i * (col_w + col_gap)
        draw.text((cx, briefs_y), b_title, font=font_tag, fill=(150, 30, 30))
        draw_wrapped_text(draw, b_desc, [cx, briefs_y + 16, col_w, 90], font_body, fill=(30, 30, 30), spacing=2)

    # Save output
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, "PNG")
    print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    draw_newspaper()
