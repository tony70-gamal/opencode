# -*- coding: utf-8 -*-
"""Generates every static asset for the Smart Biogas social kit.

Copy is taken from campaign/biogas (website) so the pics/videos explain the
same project. Run:  python campaign/social/build_social.py
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sk import *  # noqa

PHOTO = Image.open(ASSETS / "prototype_main.jpg").convert("RGB")
LOGO = Image.open(ASSETS / "logo_placeholder.png").convert("RGB")

MADE = []
BOXES = []
CURRENT = [""]


class AuditDraw:
    """Proxy that records every text box so overlaps can be detected."""

    def __init__(self, img):
        self._d = ImageDraw.Draw(img)

    def __getattr__(self, name):
        return getattr(self._d, name)

    def text(self, xy, text, *a, **k):
        font = k.get("font")
        if font is None:
            return self._d.text(xy, text, *a, **k)
        bb = font.getbbox(text)
        BOXES.append((xy[0] + bb[0], xy[1] + bb[1], xy[0] + bb[2], xy[1] + bb[3],
                      text[:30], CURRENT[0]))
        return self._d.text(xy, text, *a, **k)


def overlaps():
    bad = []
    for i in range(len(BOXES)):
        x1, y1, x2, y2, t1, c1 = BOXES[i]
        if (x2 - x1) < 2 or (y2 - y1) < 2:
            continue
        a1 = (x2 - x1) * (y2 - y1)
        for j in range(i + 1, len(BOXES)):
            u1, v1, u2, v2, t2, c2 = BOXES[j]
            if c1 != c2:
                continue
            ox = min(x2, u2) - max(x1, u1)
            oy = min(y2, v2) - max(y1, v1)
            if ox <= 2 or oy <= 2:
                continue
            a2 = (u2 - u1) * (v2 - v1)
            frac = (ox * oy) / max(1, min(a1, a2))
            if frac > 0.10:
                bad.append("%s :: %r <> %r (%.0f%%)" % (c1, t1, t2, frac * 100))
    return bad


def save(img, rel, fmt="PNG"):
    p = IMG_DIR / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if fmt.upper() == "JPG":
        img.convert("RGB").save(p, quality=92, subsampling=1, optimize=True)
    else:
        img.save(p, optimize=True)
    MADE.append((rel, img.size, p.stat().st_size))
    return p


# ------------------------------------------------------------------ chrome ---
def header(d, W, dark=True, label=None, right=None):
    fg = WHITE if dark else GREEN
    f = F(F_BOLD, 27)
    d.ellipse((MARGIN, 62, MARGIN + 20, 82), fill=AMBER)
    d.text((MARGIN + 34, 60), BRAND, font=f, fill=fg)
    d.text((MARGIN + 34, 92), SUBBRAND, font=F(F_REG, 21), fill=LIME if dark else MUTED)
    if right:
        f2 = F(F_MONO, 22)
        d.text((W - MARGIN - d.textlength(right, font=f2), 66), right, font=f2,
               fill=AMBER if dark else AMBER2)
    if label:
        return pill(d, MARGIN, 150, label, F(F_BOLD, 24),
                    INK if dark else WHITE, AMBER, padx=24, pady=12)[1] + 150
    return 150


def footer(d, W, H, dark=True, note="WASTE HAS ENERGY."):
    y = H - 74
    d.line((MARGIN, y - 22, W - MARGIN, y - 22), fill=(31, 58, 46) if dark else LINE, width=2)
    f = F(F_BLACK, 30)
    d.text((MARGIN, y), note, font=f, fill=AMBER if dark else GREEN)
    f2 = F(F_REG, 21)
    d.text((W - MARGIN - d.textlength("sut.edu.eg", font=f2), y + 8), "sut.edu.eg",
           font=f2, fill=MINT2 if dark else MUTED)


def base(size, style="dark"):
    W, H = size
    MARGIN = int(W * 0.075)
    globals()["MARGIN"] = MARGIN
    if style == "photo":
        img = cover(PHOTO, size, 0.4).filter(ImageFilter.GaussianBlur(1.2))
        scrim(img, (0, 0, W, H), (4, 20, 15), 40, 215)
    elif style == "light":
        img = vgrad(size, WHITE, MINT)
    elif style == "teal":
        img = dgrad(size, TEAL, TEAL2)
    elif style == "amber":
        img = dgrad(size, AMBER, AMBER2)
    else:
        img = dgrad(size, GREEN, DARK)
    CURRENT[0] = "card#%d" % len(MADE)
    return img, AuditDraw(img), W, H, MARGIN


def bullets(d, x, y, w, items, font, color, dot=AMBER, gap=0.20, lh_pad=16):
    lh = line_h(font, gap)
    for it in items:
        d.ellipse((x, y + font.size * 0.42, x + 13, y + font.size * 0.42 + 13), fill=dot)
        lines = wrap(d, it, font, w - 34)
        for i, ln in enumerate(lines):
            d.text((x + 34, y + i * lh), ln, font=font, fill=color)
        y += len(lines) * lh + lh_pad
    return y


def headline(d, x, y, w, text, size, color=WHITE, path=F_BLACK, max_lines=3, min_size=30):
    f, lines = fit(d, text, path, w, size, min_size, max_lines)
    lh = line_h(f, 0.10)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=color)
    return y + len(lines) * lh, f


def kicker(d, x, y, text, color=AMBER, size=25):
    f = F(F_BOLD, size)
    tracked(d, (x, y), text.upper(), f, color, track=2)
    return y + int(size * 1.6)


# ============================================================ CAROUSEL 1 =====
def carousel_waste_to_energy():
    D = "ig01_waste_to_energy"
    W, H = 1080, 1350

    # 1 -- cover
    img, d, W, H, M = base((W, H), "photo")
    header(d, W, True, "SMART FOOD WASTE-TO-BIOGAS", "01/07")
    y = kicker(d, M, 190, "el sewedy university of technology")
    y, fh = headline(d, M, y, W - 2 * M, "WASTE → ENERGY?", 132, WHITE, max_lines=2)
    y = para(d, M, y + 10, "Organic waste is a disposal problem. We turn it into a "
                           "measurable energy resource.", F(F_SEMI, 34), MINT2,
             W - 2 * M, 0.20) + 40
    chips = [("18 L", "digester"), ("100×50×70", "cm mobile frame"), ("18M t/yr", "Egypt food waste")]
    cw = (W - 2 * M - 2 * 20) / 3
    for i, (big, small) in enumerate(chips):
        x = M + i * (cw + 20)
        card(img, (int(x), int(y), int(x + cw), int(y + 132)), fill=(9, 32, 24), r=18)
        fb = F(F_BLACK, 42)
        d.text((x + (cw - d.textlength(big, font=fb)) / 2, y + 22), big, font=fb, fill=AMBER)
        fs = F(F_REG, 23)
        d.text((x + (cw - d.textlength(small, font=fs)) / 2, y + 78), small, font=fs, fill=MINT2)
    footer(d, W, H, True, "SWIPE →")
    save(img, D + "/01_cover.png")

    # 2 -- problem
    img, d, W, H, M = base((W, H), "light")
    header(d, W, False, "THE PROBLEM", "02/07")
    y = kicker(d, M, 190, "egypt throws away 18 million tons a year", AMBER2)
    y, fh = headline(d, M, y, W - 2 * M, "WE PAY TWICE.", 108, GREEN, max_lines=1)
    y = bullets(d, M, y + 34, W - 2 * M, [
        "18M tons of food waste every year in Egypt (UNEP 2024).",
        "80–88% of it ends up in open dumps: methane, disease vectors, lost value.",
        "81–82% of Egypt's electricity runs on imported natural gas.",
        "So we pay to throw waste away — then pay again to import the energy that waste could have made.",
    ], F(F_REG, 31), GRAY, lh_pad=22)
    card(img, (M, y + 10, W - M, y + 190), fill=GREEN, r=22)
    d.text((M + 34, y + 44), "ONE CLOSED LOOP FIXES BOTH", font=F(F_BOLD, 30), fill=AMBER)
    para(d, M + 34, y + 88, "FOOD WASTE → BIOGAS → ENERGY → DATA", F(F_MONO, 30),
         WHITE, W - 2 * M - 68, 0.20)
    footer(d, W, H, False)
    save(img, D + "/02_problem.png")

    steps = [
        ("01", "SHRED + FEED", "Waste is shredded and dropped into the sealed feed hopper. "
         "Nothing touches open air — no smell, no flies, no leachate.",
         "FOOD WASTE → HOPPER"),
        ("02", "DIGEST AT 35°C", "An 18 L gas-tight HDPE digester holds 12–14 L of slurry at a "
         "constant 35°C. A gear motor and paddle keep it mixed; a heater holds temperature.",
         "SEALED · MIXED · 35°C"),
        ("03", "COLLECT BIOGAS", "Gas pushes into a 5–10 L bladder, then through a filter and "
         "regulator. Pressure is watched continuously by an analog sensor.",
         "BLADDER → FILTER → REGULATOR"),
        ("04", "SAFETY IS LAYERED", "Mechanical relief valve, non-return valve, flame arrestor, "
         "MQ methane/H2S alarms, ventilation, PPE and a fire extinguisher.",
         "SOFTWARE NEVER REPLACES A VALVE"),
    ]
    for i, (num, head, body, tag) in enumerate(steps):
        img, d, W, H, M = base((W, H), "dark" if i % 2 == 0 else "teal")
        header(d, W, True, "HOW IT WORKS", "%02d/07" % (i + 3))
        d.text((M, 190), num, font=F(F_BLACK, 150), fill=AMBER)
        y = 190 + 150
        y, fh = headline(d, M, y + 6, W - 2 * M, head, 74, WHITE, max_lines=2)
        y = para(d, M, y + 20, body, F(F_REG, 32), MINT2, W - 2 * M, 0.22) + 34
        paste_round(img, PHOTO, (M, y, W - 2 * M, 430), 26, 0.35)
        scrim(img, (M, y + 250, W - 2 * M, 180), (5, 22, 17), 0, 215)
        f = F(F_MONO, 30)
        d.text((M + 30, y + 320), tag, font=f, fill=AMBER)
        footer(d, W, H, True)
        save(img, "%s/%02d_%s.png" % (D, i + 3, head.split()[0].lower()))

    # 7 -- generate + data + CTA
    img, d, W, H, M = base((W, H), "photo")
    header(d, W, True, "ENERGY + DATA", "07/07")
    y = kicker(d, M, 190, "step 5 and 6")
    y, _ = headline(d, M, y, W - 2 * M, "GENERATE. MEASURE. OPTIMIZE.", 74, WHITE, max_lines=2)
    y = bullets(d, M, y + 26, W - 2 * M, [
        "Biogas runs a generator or heats and cooks — off-grid or standby.",
        "2× ESP32 log temperature, pH, pressure and CH4/H2S every cycle.",
        "The AI layer pauses feeding when pH or pressure drifts, and auto-vents.",
        "Every kWh is auditable: kg/day, m3/kg, kWh/kg, EGP/m3, uptime.",
    ], F(F_REG, 30), MINT, lh_pad=18)
    y = chip_flow(d, M, y + 10, W - 2 * M,
                  ["SENSORS", "ESP32", "MQTT/TLS", "TIMESCALEDB", "GRAFANA", "AI CONTROL"],
                  F(F_BOLD, 25), WHITE, (17, 37, 30), (31, 58, 46))
    card(img, (M, H - 300, W - M, H - 100), fill=AMBER, r=24)
    d.text((M + 34, H - 262), "SEE THE 18 L PROTOTYPE", font=F(F_BOLD, 30), fill=INK)
    d.text((M + 34, H - 216), "smart-biogas2026.surge.sh", font=F(F_MONO, 30), fill=GREEN)
    footer(d, W, H, True, "SWIPE BACK")
    save(img, D + "/07_cta.png")


# ============================================================ CAROUSEL 2 =====
def carousel_real_build():
    D = "ig05_real_build"
    W, H = 1080, 1350

    img, d, W, H, M = base((W, H), "photo")
    header(d, W, True, "PROTOTYPE", "01/06")
    y = kicker(d, M, 190, "18 litre mobile rig · 100×50×70 cm")
    y, _ = headline(d, M, y, W - 2 * M, "NOT A RENDER. A WORKING BUILD.", 92, WHITE, max_lines=2)
    y = para(d, M, y + 16, "Hopper → digester → gas storage → control cabinet, on casters, "
             "built and tested by the team.", F(F_SEMI, 32), MINT2, W - 2 * M, 0.20) + 30
    for i, (k, v) in enumerate([("18 L", "digester"), ("2×", "ESP32"), ("35°C", "held")]):
        x = M + i * ((W - 2 * M - 40) / 3 + 20)
        cw = (W - 2 * M - 40) / 3
        card(img, (int(x), int(y), int(x + cw), int(y + 124)), fill=(9, 32, 24), r=18)
        fb = F(F_BLACK, 52)
        d.text((x + (cw - d.textlength(k, font=fb)) / 2, y + 18), k, font=fb, fill=AMBER)
        fs = F(F_REG, 24)
        d.text((x + (cw - d.textlength(v, font=fs)) / 2, y + 82), v, font=fs, fill=MINT2)
    footer(d, W, H, True, "SWIPE →")
    save(img, D + "/01_cover.png")

    img, d, W, H, M = base((W, H), "dark")
    header(d, W, True, "SPECIFICATION", "02/06")
    y = kicker(d, M, 190, "current build")
    y, _ = headline(d, M, y, W - 2 * M, "18 L SPEC", 104, WHITE, max_lines=1)
    y = spec_table(d, M, y + 20, W - 2 * M, [
        ("Digester", "18 L HDPE, gas-tight, insulated"),
        ("Working volume", "12–14 L"),
        ("Mix / heat", "Gear motor + paddle, heater, 35°C"),
        ("Gas", "5–10 L bladder, non-return, relief, arrestor"),
        ("Sensors", "DS18B20 ×2, MQ-4, MQ-136, MPX5010, JSN-SR04T, pH, NDIR"),
        ("Control", "2× ESP32-WROOM-32, relay, solenoid, buck"),
        ("Frame", "100×50×70 cm, casters"),
        ("Scale", "18 L → 60 L → 500 L+ (S/M/L)"),
    ]) + 24
    if y > H - 120:
        warn("spec table too tall: %d" % y)
    card(img, (M, H - 260, W - M, H - 120), fill=AMBER, r=20)
    d.text((M + 30, H - 232), "Prototype ≈ 10,900 EGP", font=F(F_BOLD, 34), fill=INK)
    d.text((M + 30, H - 186), "provisional — pending quotations. Not a commercial price.",
           font=F(F_REG, 24), fill=RUST)
    footer(d, W, H, True)
    save(img, D + "/02_spec.png")

    img, d, W, H, M = base((W, H), "teal")
    header(d, W, True, "SENSORS", "03/06")
    y = kicker(d, M, 190, "every vital sign, logged")
    y, _ = headline(d, M, y, W - 2 * M, "SENSORS THAT TALK", 82, WHITE, max_lines=2)
    y += 30
    tiles = [
        ("DS18B20 ×2", "Digester and gas temperature"),
        ("MQ-4", "Methane leak alarm"),
        ("MQ-136", "H2S hydrogen-sulfide alarm"),
        ("MPX5010", "Analog gas pressure"),
        ("JSN-SR04T", "Waterproof level / distance"),
        ("pH probe", "Acidity of the slurry"),
        ("NDIR module", "Optional CO2 cross-check"),
        ("DS + relay", "Heater and mixer switching"),
    ]
    tw = (W - 2 * M - 20) / 2
    for i, (h, b) in enumerate(tiles):
        x = M + (i % 2) * (tw + 20)
        yy = y + (i // 2) * 168
        numbered_tile(img, (int(x), int(yy), int(x + tw), int(yy + 152)),
                      i + 1, h, b, dark=True, accent=AMBER)
    footer(d, W, H, True)
    save(img, D + "/03_sensors.png")

    img, d, W, H, M = base((W, H), "dark")
    header(d, W, True, "CONTROL STACK", "04/06")
    y = kicker(d, M, 190, "closed-loop control")
    y, _ = headline(d, M, y, W - 2 * M, "IT DOESN'T JUST MONITOR. IT DECIDES.", 76,
                    WHITE, max_lines=2)
    y += 26
    stack = [
        ("SENSORS", "DS18B20 · MQ-4/136 · MPX5010 · JSN-SR04T · pH"),
        ("2× ESP32-WROOM-32", "control, telemetry, watchdog, signed OTA"),
        ("MQTT over TLS", "Mosquitto + Node.js/Express, ACLs and auth"),
        ("PostgreSQL + TimescaleDB", "hypertables, historian, calibration logs"),
        ("React + Grafana + Python AI", "live dashboards, alerts, anomaly, auto-vent"),
    ]
    for i, (h, b) in enumerate(stack):
        hgt = 112
        card(img, (M, y, W - M, y + hgt), fill=(17, 37, 30), outline=(31, 58, 46), r=18)
        d.text((M + 28, y + 18), h, font=F(F_BOLD, 31), fill=AMBER)
        d.text((M + 28, y + 62), b, font=F(F_REG, 25), fill=MINT2)
        if i < len(stack) - 1:
            d.text((W / 2 - 14, y + hgt + 3), "↓", font=F(F_BOLD, 32), fill=TEAL)
        y += hgt + 40
    if y > H - 110:
        warn("control stack too tall: %d" % y)
    footer(d, W, H, True)
    save(img, D + "/04_control.png")

    img, d, W, H, M = base((W, H), "dark")
    header(d, W, True, "SAFETY", "05/06")
    y = kicker(d, M, 190, "appendix c · 7 layers")
    y, _ = headline(d, M, y, W - 2 * M, "7 LAYERS BEFORE YOU FLAME IT", 82, WHITE, max_lines=2)
    y += 26
    y = bullets(d, M, y, W - 2 * M, [
        "1. Mechanical relief valve — independent of all software.",
        "2. Non-return valve — blocks backflow into the digester.",
        "3. Flame arrestor — kills ignition sources in the gas line.",
        "4. MQ-4 methane and MQ-136 H2S alarms with load shedding.",
        "5. Forced ventilation at the cabinet and rig.",
        "6. PPE kit and a CO2 extinguisher mounted on the frame.",
        "7. Watchdog + signed OTA so a failed update cannot brick safety control.",
    ], F(F_REG, 28), MINT, lh_pad=12)
    card(img, (M, H - 250, W - M, H - 120), fill=(17, 37, 30), outline=AMBER, r=20)
    d.text((M + 28, H - 222), "MECHANICAL RELIEF NEVER DEPENDS ON SOFTWARE",
           font=F(F_BOLD, 27), fill=AMBER)
    footer(d, W, H, True)
    save(img, D + "/05_safety.png")

    img, d, W, H, M = base((W, H), "photo")
    header(d, W, True, "WHAT'S NEXT", "06/06")
    y = kicker(d, M, 190, "from 18 litres to commercial")
    y, _ = headline(d, M, y, W - 2 * M, "18 → 60 → 500+ LITRES", 96, WHITE, max_lines=1)
    y += 40
    for i, (k, v) in enumerate([("18 L", "prototype · built now"),
                                ("60 L", "pilot · 30–90 day measured data"),
                                ("500 L+", "commercial · S/M/L per waste stream")]):
        hgt = 150
        card(img, (M, y, W - M, y + hgt), fill=(9, 32, 24), outline=(31, 58, 46), r=20)
        d.text((M + 30, y + 26), k, font=F(F_BLACK, 52), fill=AMBER)
        d.text((M + 300, y + 48), v, font=F(F_REG, 28), fill=MINT)
        y += hgt + 20
    card(img, (M, y + 16, W - M, H - 116), fill=AMBER, r=22)
    d.text((M + 32, y + 48), "BOOK A 30-DAY PILOT ASSESSMENT", font=F(F_BOLD, 32), fill=INK)
    d.text((M + 32, y + 96), "smart-biogas2026.surge.sh", font=F(F_MONO, 30), fill=GREEN)
    footer(d, W, H, True, "SWIPE BACK")
    save(img, D + "/06_scale_cta.png")


# ============================================================ CAROUSEL 3 =====
def carousel_value():
    D = "ig07_value"
    W, H = 1080, 1350

    img, d, W, H, M = base((W, H), "teal")
    header(d, W, True, "WHY IT PAYS BACK", "01/05")
    y = kicker(d, M, 190, "four value pillars")
    y, _ = headline(d, M, y, W - 2 * M, "ONE RIG. FOUR REVENUES.", 86, WHITE, max_lines=2)
    y += 34
    pillars = [("Waste value", "Diverted from landfill and quantified in kg/day."),
               ("Energy value", "Biogas for cooking, heating or electricity."),
               ("Data value", "Temp, pH, pressure, CH4/H2S, alerts, history."),
               ("Sustainability value", "Waste processed and GHG avoided, measured.")]
    tw = (W - 2 * M - 20) / 2
    for i, (h, b) in enumerate(pillars):
        x = M + (i % 2) * (tw + 20)
        yy = y + (i // 2) * 300
        numbered_tile(img, (int(x), int(yy), int(x + tw), int(yy + 280)),
                      i + 1, h, b, dark=True, accent=AMBER)
    footer(d, W, H, True, "SWIPE →")
    save(img, D + "/01_pillars.png")

    img, d, W, H, M = base((W, H), "light")
    header(d, W, False, "BUSINESS MODEL", "02/05")
    y = kicker(d, M, 190, "not a one-time sale", AMBER2)
    y, _ = headline(d, M, y, W - 2 * M, "6 REVENUE STREAMS", 76, GREEN, max_lines=1)
    y += 26
    streams = [("System sales", "S / M / L sized to the waste stream"),
               ("Installation", "Assessment, install and training"),
               ("Maintenance", "Calibration and SLA contracts"),
               ("IoT subscription", "Cloud hosting and analytics"),
               ("Upgrades", "Extra sensors and gas storage"),
               ("Engineering", "Custom design for your site")]
    for i, (h, b) in enumerate(streams):
        yy = y + i * 112
        card(img, (M, yy, W - M, yy + 96), fill=WHITE, outline=LINE, r=18)
        d.ellipse((M + 26, yy + 26, M + 70, yy + 70), fill=AMBER)
        d.text((M + 38, yy + 33), str(i + 1), font=F(F_BLACK, 30), fill=INK)
        d.text((M + 96, yy + 18), h, font=F(F_BOLD, 31), fill=GREEN)
        d.text((M + 96, yy + 56), b, font=F(F_REG, 25), fill=GRAY)
    y2 = y + 6 * 112 + 10
    if y2 > H - 190:
        warn("revenue grid too tall: %d" % y2)
    card(img, (M, y2, W - M, y2 + 118), fill=GREEN, r=20)
    d.text((M + 30, y2 + 26), "LTV ≈ 2.5× the hardware alone", font=F(F_BOLD, 30), fill=AMBER)
    d.text((M + 30, y2 + 70), "3 years of care, data and uptime on top of every unit.",
           font=F(F_REG, 25), fill=MINT2)
    footer(d, W, H, False)
    save(img, D + "/02_revenue.png")

    img, d, W, H, M = base((W, H), "dark")
    header(d, W, True, "WHO FIRST", "03/05")
    y = kicker(d, M, 190, "validate speed, then revenue")
    y, _ = headline(d, M, y, W - 2 * M, "WHO GETS PILOT NUMBER ONE?", 78, WHITE, max_lines=2)
    y += 30
    tiers = [("1", "Universities", "Cafeteria waste, fast measurement, great for research data."),
             ("2", "Restaurants & hotels", "High organic load, high disposal cost, quick payback."),
             ("3", "Food processing", "Steady tonnes per day, ideal for commercial scale."),
             ("4", "Agricultural operations", "Largest volumes, longest payback horizon.")]
    for i, (n, h, b) in enumerate(tiers):
        hgt = 168
        card(img, (M, y, W - M, y + hgt), fill=(17, 37, 30), outline=(31, 58, 46), r=20)
        d.text((M + 30, y + 34), n, font=F(F_BLACK, 88), fill=AMBER)
        d.text((M + 150, y + 26), h, font=F(F_BOLD, 34), fill=WHITE)
        para(d, M + 150, y + 76, b, F(F_REG, 25), MINT2, W - 2 * M - 180, 0.20)
        y += hgt + 20
    if y > H - 120:
        warn("tier list too tall: %d" % y)
    footer(d, W, H, True, "SWIPE →")
    save(img, D + "/03_pyramid.png")

    img, d, W, H, M = base((W, H), "amber")
    header(d, W, False, "SALES FUNNEL", "04/05")
    y = kicker(d, M, 190, "how a lead becomes a plant", RUST)
    y, _ = headline(d, M, y, W - 2 * M, "FROM CLICK TO COMMERCIAL", 78, INK, max_lines=2)
    y += 30
    steps = ["Awareness", "Interest", "Demonstration", "Waste data", "Pilot 30–90 d",
             "Commercial unit"]
    for i, s in enumerate(steps):
        hgt = 96
        inset = i * 22
        card(img, (M + inset, y, W - M - inset, y + hgt), fill=GREEN, r=18)
        f = F(F_BOLD, 31)
        d.text((M + inset + (W - 2 * M - 2 * inset - d.textlength(s, font=f)) / 2, y + 30),
               s, font=f, fill=WHITE)
        d.text((M + inset + 20, y + 34), str(i + 1), font=F(F_BOLD, 26), fill=AMBER)
        y += hgt + 16
    if y > H - 130:
        warn("funnel too tall: %d" % y)
    d.text((M, y + 10), "Ten validation steps before we quote a single ROI number.",
           font=F(F_REG, 27), fill=RUST)
    footer(d, W, H, False, "MEASURE, THEN MONETIZE.")
    save(img, D + "/04_funnel.png")

    img, d, W, H, M = base((W, H), "photo")
    header(d, W, True, "NEXT STEP", "05/05")
    y = kicker(d, M, 200, "waste assessment")
    y, _ = headline(d, M, y + 10, W - 2 * M, "START WITH DATA, NOT A QUOTE.", 84,
                    WHITE, max_lines=2)
    y = para(d, M, y + 24, "Tell us how much organic waste you generate a day. We pilot, "
             "measure, then propose ROI from real numbers.", F(F_SEMI, 32), MINT,
             W - 2 * M, 0.22) + 40
    for i, (k, v) in enumerate([("kg / day", "your waste volume"),
                                ("EGP / kg", "your disposal cost"),
                                ("kWh / month", "your energy use"),
                                ("30 days", "our pilot window")]):
        tw = (W - 2 * M - 20) / 2
        x = M + (i % 2) * (tw + 20)
        yy = y + (i // 2) * 150
        card(img, (int(x), int(yy), int(x + tw), int(yy + 130)), fill=(9, 32, 24), r=18)
        d.text((x + 24, yy + 22), k, font=F(F_BLACK, 38), fill=AMBER)
        d.text((x + 24, yy + 80), v, font=F(F_REG, 25), fill=MINT2)
    card(img, (M, H - 300, W - M, H - 108), fill=AMBER, r=24)
    d.text((M + 32, H - 262), "REQUEST A PILOT ASSESSMENT", font=F(F_BOLD, 31), fill=INK)
    d.text((M + 32, H - 214), "smart-biogas2026.surge.sh", font=F(F_MONO, 31), fill=GREEN)
    d.text((M + 32, H - 168), "hamza250102724@sut.edu.eg", font=F(F_REG, 25), fill=RUST)
    footer(d, W, H, True, "SWIPE BACK")
    save(img, D + "/05_cta.png")


# ================================================================== SQUARES ==
def squares():
    specs = [
        ("sq01_18m_tons", "18M", "TONS OF FOOD WASTE", "generated in Egypt every year "
         "(UNEP 2024). 80–88% still ends up in open dumps.", "18M TONS / YEAR"),
        ("sq02_81pct", "81–82%", "OF EGYPT'S POWER", "runs on imported natural gas — so we "
         "import the energy our own waste could have made.", "THE IMPORT PROBLEM"),
        ("sq03_loop", "1", "CLOSED LOOP", "FOOD WASTE → PRE-PROCESSING → DIGESTER → BIOGAS → "
         "ENERGY → IoT+AI DATA. Waste becomes auditable kWh.", "WASTE → ENERGY"),
    ]
    for name, big, mid, body, tag in specs:
        W = H = 1080
        img, d, W, H, M = base((W, H), "dark")
        header(d, W, True, tag, None)
        fb = F(F_BLACK, 250)
        d.text((M, 210), big, font=fb, fill=AMBER)
        f_mid = F(F_BOLD, 56)
        y = 210 + 250
        d.text((M, y), mid, font=f_mid, fill=WHITE)
        para(d, M, y + 84, body, F(F_REG, 34), MINT2, W - 2 * M, 0.24)
        paste_round(img, PHOTO, (M, H - 430, W - 2 * M, 250), 24, 0.35)
        footer(d, W, H, True)
        save(img, "squares/" + name + ".png")


# =================================================================== STORIES ==
def stories():
    W, H = 1080, 1920
    img, d, W, H, M = base((W, H), "dark")
    d.ellipse((M, 120, M + 20, 140), fill=AMBER)
    d.text((M + 34, 118), BRAND, font=F(F_BOLD, 30), fill=WHITE)
    y = kicker(d, M, 300, "story 1 of 3 · poll")
    y, _ = headline(d, M, y, W - 2 * M, "HOW MUCH FOOD WASTE DO YOU MAKE?", 92, WHITE, max_lines=3)
    y += 60
    for i, (k, v) in enumerate([("0–20", "kg per day"), ("20–50", "kg per day"),
                                ("50–100", "kg per day"), ("100+", "kg per day")]):
        card(img, (M, y, W - M, y + 150), fill=(17, 37, 30), outline=(31, 58, 46), r=22)
        f = F(F_BLACK, 64)
        d.text((M + 40, y + 40), k, font=f, fill=AMBER)
        d.text((M + 40, y + 108), v, font=F(F_REG, 28), fill=MINT2)
        d.text((W - M - 60, y + 60), "›", font=F(F_BOLD, 40), fill=TEAL)
        y += 168
    card(img, (M, H - 250, W - M, H - 120), fill=AMBER, r=24)
    d.text((M + 32, H - 210), "VOTE BY TAPPING ABOVE", font=F(F_BOLD, 34), fill=INK)
    d.text((M + 32, H - 160), "we build the right size for your answer", font=F(F_REG, 27), fill=RUST)
    save(img, "stories/story1_poll.png")

    img, d, W, H, M = base((W, H), "photo")
    d.ellipse((M, 120, M + 20, 140), fill=AMBER)
    d.text((M + 34, 118), BRAND, font=F(F_BOLD, 30), fill=WHITE)
    y = kicker(d, M, 300, "story 2 of 3 · behind the scenes")
    y, _ = headline(d, M, y, W - 2 * M, "pH CALIBRATION DAY", 104, WHITE, max_lines=2)
    y = para(d, M, y + 20, "Two solutions, one probe. Buffer 4.0, buffer 7.0, rinse, slope "
             "check, then the slurry. If the number drifts, the whole loop is wrong.",
             F(F_SEMI, 34), MINT, W - 2 * M, 0.22) + 40
    for i, (k, v) in enumerate([("4.00", "buffer pH 4"), ("7.00", "buffer pH 7"),
                                ("6.4", "slurry reading"), ("±0.2", "target band")]):
        tw = (W - 2 * M - 20) / 2
        x = M + (i % 2) * (tw + 20)
        yy = y + (i // 2) * 190
        card(img, (int(x), int(yy), int(x + tw), int(yy + 170)), fill=(9, 32, 24), r=20)
        d.text((x + 28, yy + 28), k, font=F(F_BLACK, 56), fill=AMBER)
        d.text((x + 28, yy + 108), v, font=F(F_REG, 27), fill=MINT2)
    card(img, (M, H - 250, W - M, H - 120), fill=AMBER, r=24)
    d.text((M + 32, H - 210), "REAL R&D > PERFECT RENDERS", font=F(F_BOLD, 32), fill=INK)
    d.text((M + 32, H - 160), "comment LAB for the full build log", font=F(F_REG, 27), fill=RUST)
    save(img, "stories/story2_bts.png")

    img, d, W, H, M = base((W, H), "teal")
    d.ellipse((M, 120, M + 20, 140), fill=AMBER)
    d.text((M + 34, 118), BRAND, font=F(F_BOLD, 30), fill=WHITE)
    y = kicker(d, M, 320, "story 3 of 3 · your turn")
    y, _ = headline(d, M, y, W - 2 * M, "SWIPE UP. GET A FREE WASTE ASSESSMENT.", 88,
                    WHITE, max_lines=3)
    y = para(d, M, y + 24, "One question: how much organic waste per day? We come back with a "
             "sizing, a payback estimate and a 30-day pilot plan.",
             F(F_SEMI, 34), MINT, W - 2 * M, 0.22) + 50
    for i, (k, v) in enumerate([("Universities", "cafeteria + lab data"),
                                ("Restaurants", "kitchen and hotel waste"),
                                ("Food processors", "steady tonnes per day"),
                                ("Farms", "agricultural residues")]):
        yy = y + i * 132
        card(img, (M, yy, W - M, yy + 112), fill=(9, 60, 42), outline=(20, 110, 78), r=20)
        d.text((M + 32, yy + 20), k, font=F(F_BOLD, 36), fill=WHITE)
        d.text((M + 32, yy + 68), v, font=F(F_REG, 27), fill=MINT2)
    card(img, (M, H - 260, W - M, H - 120), fill=AMBER, r=24)
    d.text((M + 32, H - 220), "smart-biogas2026.surge.sh", font=F(F_MONO, 36), fill=INK)
    d.text((M + 32, H - 166), "SUT Energy Engineering · 2025/2026", font=F(F_REG, 27), fill=RUST)
    save(img, "stories/story3_cta.png")


# ============================================================= REEL COVERS ===
def reel_covers():
    W, H = 1080, 1920
    covers = [
        ("reel01_waste_to_energy", "photo", "30s REEL", "WASTE →\nENERGY?", 118,
         "The whole project in 30 seconds — problem, process, prototype.",
         ["18M tons/yr wasted in Egypt", "18 L working mobile rig", "2× ESP32 + AI closed loop"]),
        ("reel02_sensors", "dark", "30s REEL", "SENSORS\nTHAT TALK", 112,
         "Every vital sign logged, every anomaly caught.",
         ["DS18B20 ×2 · MQ-4 · MQ-136", "MPX5010 pressure · pH · level",
          "MQTT/TLS → TimescaleDB → Grafana"]),
        ("reel03_safety", "teal", "20s REEL", "SAFETY IS\nLAYERED", 116,
         "Seven layers before you light anything.",
         ["mechanical relief (independent)", "non-return + flame arrestor",
          "CH4/H2S alarms, vent, PPE, extinguisher"]),
        ("reel04_real_build", "photo", "35s REEL", "NOT A\nRENDER", 122,
         "A real build, filmed on the rig.",
         ["100×50×70 cm on casters", "hopper → digester → bladder → cabinet",
          "18 → 60 → 500+ litres planned"]),
    ]
    for name, style, tag, title, size, sub, pts in covers:
        img, d, W, H, M = base((W, H), style)
        d.ellipse((M, 120, M + 20, 140), fill=AMBER)
        d.text((M + 34, 118), BRAND, font=F(F_BOLD, 30), fill=WHITE)
        pill(d, W - M - 210, 112, tag, F(F_BOLD, 26), INK, AMBER, padx=24, pady=13)
        y = kicker(d, M, 340, "smart food waste-to-biogas")
        f = F(F_BLACK, size)
        lh = int(size * 1.06)
        for i, ln in enumerate(title.split("\n")):
            d.text((M, y + i * lh), ln, font=f, fill=WHITE)
        y += len(title.split("\n")) * lh + 20
        y = para(d, M, y, sub, F(F_SEMI, 36), MINT, W - 2 * M, 0.22) + 50
        if name == "reel04_real_build":
            paste_round(img, PHOTO, (M, y - 20, W - 2 * M, 420), 26, 0.35)
            y += 440
        for p in pts:
            card(img, (M, y, W - M, y + 150), fill=(9, 32, 24) if style != "teal" else (9, 60, 42),
                 outline=(31, 58, 46) if style != "teal" else (20, 110, 78), r=20)
            d.ellipse((M + 30, y + 62, M + 44, y + 76), fill=AMBER)
            d.text((M + 66, y + 52), p, font=F(F_BOLD, 33), fill=WHITE)
            y += 168
        if y > H - 150:
            warn("%s content overflows: %d" % (name, y))
        footer(d, W, H, True)
        save(img, "reels/" + name + ".png")


# ============================================================== FB / THUMB ===
def fb_and_thumb():
    W, H = 1200, 630
    img, d, W, H, M = base((W, H), "photo")
    M = 70
    scrim(img, (0, 0, 620, H), (4, 20, 15), 120, 235)
    d.text((M, 70), "SMART BIOGAS · SUT", font=F(F_BOLD, 30), fill=LIME)
    d.text((M, 118), "WASTE", font=F(F_BLACK, 96), fill=WHITE)
    d.text((M, 216), "→ ENERGY?", font=F(F_BLACK, 96), fill=AMBER)
    para(d, M, 330, "18M tons of food waste a year in Egypt — turned into measurable clean "
         "energy by an 18 L digester with IoT sensors and AI control.",
         F(F_REG, 28), MINT, 500, 0.24)
    d.text((M, 552), "smart-biogas2026.surge.sh", font=F(F_MONO, 30), fill=AMBER)
    save(img, "facebook/fb_link_cover.jpg", "JPG")

    img, d, W, H, M = base((W, H), "teal")
    M = 70
    d.text((M, 70), "SUT ENERGY ENGINEERING", font=F(F_BOLD, 30), fill=MINT)
    d.text((M, 120), "6 REVENUE", font=F(F_BLACK, 86), fill=WHITE)
    d.text((M, 206), "STREAMS", font=F(F_BLACK, 86), fill=AMBER)
    para(d, M, 300, "System sales · Installation · Maintenance · IoT subscription · "
         "Upgrades · Custom engineering. LTV ≈ 2.5× the hardware alone.",
         F(F_REG, 28), WHITE, 540, 0.24)
    d.text((M, 524), "Book a 30-day pilot → smart-biogas2026.surge.sh", font=F(F_BOLD, 29),
           fill=AMBER)
    save(img, "facebook/fb_link_business.jpg", "JPG")

    W, H = 1280, 720
    img, d, W, H, M = base((W, H), "photo")
    scrim(img, (0, 0, 760, H), (4, 20, 15), 100, 240)
    d.text((70, 92), "SUT · SMART BIOGAS", font=F(F_BOLD, 32), fill=LIME)
    d.text((70, 160), "WASTE HAS", font=F(F_BLACK, 118), fill=WHITE)
    d.text((70, 272), "ENERGY.", font=F(F_BLACK, 118), fill=AMBER)
    para(d, 70, 428, "18 million tons thrown away every year. We built an 18 litre rig that "
         "digests it, cleans the gas and logs every sensor.",
         F(F_REG, 34), MINT, 620, 0.24)
    save(img, "youtube/thumb_problem.png")


# ================================================= EXTRA SQUARE + 16:9 STILL ==
def extra_formats():
    W = H = 1080
    # -- 1:1 cover
    img, d, W, H, M = base((W, H), "photo")
    header(d, W, True, None, None)
    y = kicker(d, M, 160, "sut energy engineering")
    y, _ = headline(d, M, y, W - 2 * M, "WASTE → ENERGY?", 104, WHITE, max_lines=2)
    paste_round(img, PHOTO, (M, y + 24, W - 2 * M, 330), 24, 0.35)
    y += 386
    for i, (k, v) in enumerate([("18 L", "digester"), ("2×", "ESP32"), ("18M t", "EG waste/yr")]):
        cw = (W - 2 * M - 40) / 3
        x = M + i * (cw + 20)
        card(img, (int(x), int(y), int(x + cw), int(y + 120)), fill=(9, 32, 24), r=18)
        fb = F(F_BLACK, 40)
        d.text((x + (cw - d.textlength(k, font=fb)) / 2, y + 18), k, font=fb, fill=AMBER)
        fs = F(F_REG, 23)
        d.text((x + (cw - d.textlength(v, font=fs)) / 2, y + 74), v, font=fs, fill=MINT2)
    footer(d, W, H, True)
    save(img, "squares/sq04_cover.png")

    # -- 1:1 how it works
    img, d, W, H, M = base((W, H), "dark")
    header(d, W, True, None, None)
    y = kicker(d, M, 160, "six steps, one closed loop")
    y, _ = headline(d, M, y, W - 2 * M, "WASTE TO WATTS", 88, WHITE, max_lines=1)
    y = chip_flow(d, M, y + 20, W - 2 * M,
                  ["FOOD WASTE", "PRE-PROCESS", "DIGESTER 35°C", "BIOGAS",
                   "GENERATOR", "ELECTRICITY", "IoT+AI DATA"],
                  F(F_BOLD, 26), WHITE, (17, 37, 30), (31, 58, 46)) + 40
    y = bullets(d, M, y, W - 2 * M, [
        "The digester is sealed: no smell, no flies, no leachate.",
        "A paddle mixes and a heater holds 35°C automatically.",
        "The bladder stores gas, the filter cleans it, the regulator meters it.",
        "Relief valve, non-return and flame arrestor sit in the gas line.",
        "2× ESP32 log everything and pause feeding when pH drifts.",
    ], F(F_REG, 28), MINT, lh_pad=12)
    if y > H - 110:
        warn("square how-it-works overflow: %d" % y)
    footer(d, W, H, True)
    save(img, "squares/sq05_how.png")

    # -- 1:1 safety
    img, d, W, H, M = base((W, H), "teal")
    header(d, W, True, None, None)
    y = kicker(d, M, 160, "appendix c")
    y, _ = headline(d, M, y, W - 2 * M, "SAFETY IS LAYERED", 82, WHITE, max_lines=1)
    y += 24
    y = spec_table(d, M, y, W - 2 * M, [
        ("1. Mechanical relief", "independent of all software"),
        ("2. Non-return valve", "no backflow into the digester"),
        ("3. Flame arrestor", "no ignition source in the gas line"),
        ("4. MQ-4 / MQ-136", "methane and H2S alarms with load shedding"),
        ("5. Ventilation", "forced air at cabinet and rig"),
        ("6. PPE + extinguisher", "mounted on the frame"),
    ], rh=62) + 20
    if y > H - 150:
        warn("square safety overflow: %d" % y)
    card(img, (M, H - 240, W - M, H - 110), fill=AMBER, r=20)
    d.text((M + 28, H - 208), "SOFTWARE NEVER REPLACES", font=F(F_BOLD, 28), fill=INK)
    d.text((M + 28, H - 166), "A MECHANICAL RELIEF VALVE", font=F(F_BOLD, 28), fill=INK)
    footer(d, W, H, True)
    save(img, "squares/sq06_safety.png")

    # -- 1:1 team + CTA
    img, d, W, H, M = base((W, H), "dark")
    header(d, W, True, None, None)
    y = kicker(d, M, 160, "el sewedy university of technology")
    y, _ = headline(d, M, y, W - 2 * M, "BUILT BY 5 ENGINEERS", 78, WHITE, max_lines=2)
    y += 20
    for i, n in enumerate(["Zeyad Mohamed AbdelAleem", "Hamza Ahmed AbdelFattah",
                           "Ahmed Sayed", "Nour Gamal Ahmed", "Caren George Samir"]):
        yy = y + i * 82
        card(img, (M, yy, W - M, yy + 68), fill=(17, 37, 30), outline=(31, 58, 46), r=16)
        d.text((M + 26, yy + 18), n, font=F(F_BOLD, 29), fill=WHITE)
    y += 5 * 82 + 14
    d.text((M, y), "Supervisor: Dr. Mariam Ahmed Sameh", font=F(F_REG, 27), fill=LIME)
    card(img, (M, H - 210, W - M, H - 104), fill=AMBER, r=20)
    d.text((M + 28, H - 178), "smart-biogas2026.surge.sh", font=F(F_MONO, 30), fill=INK)
    footer(d, W, H, True)
    save(img, "squares/sq07_team.png")

    # -- 16:9 stills
    W, H = 1280, 720
    for name, kick, head, body, style in [
        ("ls01_cover", "smart food waste-to-biogas", "WASTE HAS ENERGY.",
         "18M tons of food waste a year in Egypt. An 18 litre digester, IoT sensors and AI "
         "control turn it into measurable clean energy.", "photo"),
        ("ls02_problem", "two national problems", "WE PAY TWICE.",
         "18M tons wasted every year, 80–88% in open dumps. Meanwhile 81–82% of our "
         "electricity runs on imported gas. One loop fixes both.", "dark"),
        ("ls03_how", "six steps, one closed loop", "FOOD WASTE TO WATERTS",
         "Shred, feed, digest at 35°C, collect biogas, generate power, log everything. "
         "Software never replaces a mechanical relief valve.", "teal"),
    ]:
        img, d, W, H, M = base((W, H), style)
        M = 84
        if style == "photo":
            paste_round(img, PHOTO, (760, 96, 428, 528), 22, 0.35)
            d.text((760, 636), "REAL 18 L BUILD — NOT A RENDER", font=F(F_BOLD, 26), fill=AMBER)
        y = kicker(d, M, 96, kick)
        y, _ = headline(d, M, y, 720 if style == "photo" else W - 2 * M, head, 92,
                        WHITE, max_lines=2)
        y = para(d, M, y + 20, body, F(F_REG, 32), MINT2, 700, 0.22) + 26
        d.text((M, H - 96), "smart-biogas2026.surge.sh", font=F(F_MONO, 30), fill=AMBER)
        d.text((M, H - 52), "SUT · Energy Engineering · 2025/2026", font=F(F_REG, 24), fill=MINT2)
        if y > H - 120:
            warn("%s overflow: %d" % (name, y))
        save(img, "landscape/" + name + ".png")

    img, d, W, H, M = base((W, H), "amber")
    M = 84
    y = kicker(d, M, 110, "next step", RUST)
    y, _ = headline(d, M, y, W - 2 * M, "BOOK A 30-DAY PILOT", 96, INK, max_lines=1)
    y = para(d, M, y + 16, "Tell us your kg/day and we come back with sizing, payback and a "
         "measured pilot plan. Universities → restaurants → food processing → farms.",
             F(F_REG, 32), INK, 1000, 0.22) + 30
    for i, (k, v) in enumerate([("kg / day", "waste volume"), ("EGP / kg", "disposal cost"),
                                ("kWh / mo", "energy use"), ("30 days", "pilot window")]):
        tw = (W - 2 * M - 60) / 4
        x = M + i * (tw + 20)
        card(img, (int(x), int(y), int(x + tw), int(y + 140)), fill=WHITE, outline=None, r=18)
        d.text((x + 26, y + 26), k, font=F(F_BLACK, 40), fill=GREEN)
        d.text((x + 26, y + 88), v, font=F(F_REG, 26), fill=GRAY)
    d.text((M, H - 96), "smart-biogas2026.surge.sh", font=F(F_MONO, 30), fill=INK)
    d.text((M, H - 52), "hamza250102724@sut.edu.eg", font=F(F_REG, 24), fill=RUST)
    if y + 145 > H - 110:
        warn("ls04_cta overflow: %d" % (y + 140))
    save(img, "landscape/ls04_cta.png")



# ============================================================ 9:16 VIDEO ====
def vertical():
    W, H = 1080, 1920
    SPECS = [
        ("v01_18m_tons", "dark", "the problem", "18M TONS", "of food waste generated in Egypt "
         "every year. 80–88% still ends up in open dumps: methane, disease vectors and a "
         "resource we paid to throw away.", "chips",
         [("18M t", "wasted / yr"), ("80–88%", "in open dumps"), ("UNEP", "2024 report")]),
        ("v02_pay_twice", "teal", "two national problems", "WE PAY TWICE.",
         "Egypt throws away 18 million tons of food a year while importing the gas that "
         "generates 81–82% of its electricity. One closed loop answers both.", "tiles",
         [("PAY TO DISPOSE", "landfill fees, transport, lost resource"),
          ("PAY FOR ENERGY", "imported gas, price volatility, carbon risk")]),
        ("v03_step_feed", "photo", "step 1 of 4", "SHRED + FEED",
         "Waste is shredded and dropped into the sealed feed hopper. Nothing touches open "
         "air — no smell, no flies, no leachate.", "photo", None),
        ("v04_step_digest", "photo", "step 2 of 4", "DIGEST AT 35°C",
         "An 18 L gas-tight HDPE digester holds 12–14 L of slurry at a constant 35°C. A "
         "gear motor and paddle keep it mixed; a heater holds temperature.", "photo", None),
        ("v05_step_collect", "photo", "step 3 of 4", "COLLECT BIOGAS",
         "Gas pushes into a 5–10 L bladder, then through a filter and a regulator. Pressure "
         "is watched continuously by an analog sensor.", "photo", None),
        ("v06_step_safety", "dark", "step 4 of 4", "SAFETY IS LAYERED",
         "Biogas is fuel, so the gas line gets the same respect as any industrial "
         "installation.", "list",
         ["Mechanical relief valve — independent of all software",
          "Non-return valve — blocks backflow into the digester",
          "Flame arrestor — no ignition source in the line",
          "MQ-4 methane and MQ-136 H2S alarms with load shedding",
          "Forced ventilation, PPE kit and a mounted extinguisher"]),
        ("v07_sensors", "dark", "closed-loop control", "SENSORS THAT TALK",
         "Every vital sign is logged every cycle. When something drifts, the system acts "
         "before a human has to.", "list",
         ["DS18B20 ×2 — digester and gas temperature",
          "MQ-4 — methane leak alarm · MQ-136 — H2S alarm",
          "MPX5010 — analog gas pressure",
          "JSN-SR04T — waterproof level sensor",
          "pH probe — acidity of the slurry"]),
        ("v08_spec", "dark", "18 litre mobile rig", "REAL SPECS",
         "A working build on casters, not a render. 100×50×70 cm and it rolls out the door.",
         "spec", [("Digester", "18 L HDPE, gas-tight"), ("Working", "12–14 L"),
                  ("Mix / heat", "paddle + heater, 35°C"), ("Gas", "5–10 L bladder"),
                  ("Control", "2× ESP32-WROOM-32"), ("Cost", "≈ 10,900 EGP")]),
        ("v09_generate", "teal", "steps 5 and 6", "GENERATE. MEASURE. OPTIMIZE.",
         "Biogas runs a generator or heats and cooks. The AI layer pauses feeding when pH or "
         "pressure drifts, and every kWh stays auditable.", "chips",
         [("2× ESP32", "control"), ("MQTT/TLS", "telemetry"),
          ("TIMESCALE", "history"), ("GRAFANA", "live view")]),
        ("v10_team", "dark", "who we are", "BUILT BY 5 ENGINEERS",
         "El Sewedy University of Technology — Energy Engineering 2025/2026. We are looking "
         "for pilot partners who generate organic waste every day.", "cta", None),
    ]
    for name, style, kick, head, body, kind, data in SPECS:
        img, d, W, H, M = base((W, H), style)
        d.ellipse((M, 120, M + 20, 140), fill=AMBER)
        d.text((M + 34, 118), BRAND, font=F(F_BOLD, 30), fill=WHITE)
        y = kicker(d, M, 240, kick)
        y, _ = headline(d, M, y, W - 2 * M, head, 104, WHITE, max_lines=3)
        y = para(d, M, y + 18, body, F(F_SEMI, 33), MINT, W - 2 * M, 0.22) + 40
        if kind == "photo":
            paste_round(img, PHOTO, (M, y, W - 2 * M, 560), 26, 0.35)
            y += 600
        elif kind == "chips":
            for k, v in data:
                card(img, (M, y, W - M, y + 168), fill=(9, 32, 24) if style != "teal" else (9, 60, 42),
                     outline=(31, 58, 46) if style != "teal" else (20, 110, 78), r=20)
                d.text((M + 32, y + 30), k, font=F(F_BLACK, 52), fill=AMBER)
                d.text((M + 32, y + 104), v, font=F(F_REG, 28), fill=MINT2)
                y += 188
        elif kind == "tiles":
            for k, v in data:
                card(img, (M, y, W - M, y + 210), fill=(9, 60, 42), outline=(20, 110, 78), r=20)
                d.text((M + 32, y + 32), k, font=F(F_BOLD, 40), fill=AMBER)
                para(d, M + 32, y + 100, v, F(F_REG, 28), MINT, W - 2 * M - 64, 0.20)
                y += 230
        elif kind == "list":
            y = bullets(d, M, y, W - 2 * M, data, F(F_REG, 30), MINT, lh_pad=16)
        elif kind == "spec":
            y = spec_table(d, M, y, W - 2 * M, data, rh=64) + 20
        elif kind == "cta":
            y = bullets(d, M, y, W - 2 * M, [
                "Zeyad Mohamed AbdelAleem · Hamza Ahmed AbdelFattah",
                "Ahmed Sayed · Nour Gamal Ahmed · Caren George Samir",
                "Supervisor: Dr. Mariam Ahmed Sameh",
            ], F(F_REG, 30), MINT, lh_pad=16)
            card(img, (M, y + 20, W - M, y + 170), fill=AMBER, r=22)
            d.text((M + 32, y + 54), "REQUEST A PILOT ASSESSMENT", font=F(F_BOLD, 31), fill=INK)
            d.text((M + 32, y + 108), "smart-biogas2026.surge.sh", font=F(F_MONO, 29), fill=GREEN)
            y += 190
        if y > H - 130:
            warn("%s overflows: %d" % (name, y))
        footer(d, W, H, True)
        save(img, "vertical/" + name + ".png")


# ===================================================================== main ==
def main():
    carousel_waste_to_energy()
    carousel_real_build()
    carousel_value()
    squares()
    stories()
    reel_covers()
    fb_and_thumb()
    extra_formats()
    vertical()
    print("generated %d images" % len(MADE))
    bad = 0
    for rel, size, n in MADE:
        flag = ""
        if n < 15000:
            flag = "  <-- SUSPICIOUSLY SMALL"
            bad += 1
        print("  %-46s %sx%s %6.1f KB%s" % (rel, size[0], size[1], n / 1024, flag))
    if WARNINGS:
        print("\nLAYOUT WARNINGS (%d):" % len(WARNINGS))
        for w in WARNINGS:
            print("  ! " + w)
    else:
        print("\nno layout warnings")
    ov = overlaps()
    if ov:
        print("\nTEXT OVERLAPS (%d):" % len(ov))
        for o in ov:
            print("  x " + o)
    else:
        print("no text overlaps")
    oob = []
    for x1, y1, x2, y2, t, c in BOXES:
        rel, size, _ = MADE[int(c.split("#")[1])]
        if x1 < 2 or y1 < 2 or x2 > size[0] - 2 or y2 > size[1] - 2:
            oob.append("%s %r box=%s" % (rel, t, [int(v) for v in (x1, y1, x2, y2)]))
    if oob:
        print("\nTEXT OUT OF BOUNDS (%d):" % len(oob))
        for o in oob:
            print("  > " + o)
    else:
        print("no text out of bounds")
    print("small/blank files: %d" % bad)


if __name__ == "__main__":
    main()
