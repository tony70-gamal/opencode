# -*- coding: utf-8 -*-
"""Packages the social kit: download gallery page + per-group zips.

Run:  python campaign/social/package_kit.py
Deploy root becomes campaign/social (index.html + images/ + videos/ + captions/ + zips).
"""
import html
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "images"
VID = ROOT / "videos"
CAP = ROOT / "captions"

# Zips are derived artefacts and are not committed to git, so the download
# buttons point at the published host instead of a relative path. That keeps
# the gallery working from the GitHub CDN mirror as well as from Surge.
ZIP_BASE = "https://smart-biogas-social.surge.sh/"

GROUPS = [
    ("Carousel A — WASTE to ENERGY (IG 1080x1350)", "ig01_waste_to_energy", "carousel"),
    ("Carousel B — the real 18 L build (IG 1080x1350)", "ig05_real_build", "carousel"),
    ("Carousel C — why it pays back (IG 1080x1350)", "ig07_value", "carousel"),
    ("Square feed cards 1080x1080", "squares", "square"),
    ("Vertical 9:16 statics (Stories / TikTok)", "vertical", "vertical"),
    ("Reel cover frames 1080x1920", "reels", "vertical"),
    ("Landscape 16:9 (LinkedIn / YouTube)", "landscape", "wide"),
    ("Facebook link cards 1200x630", "facebook", "wide"),
    ("YouTube thumbnail", "youtube", "wide"),
]

CSS = """
:root{--green:#0F3D2E;--teal:#0E9F6E;--amber:#F59E0B;--bg:#F8FAF9;--line:#E5E7EB;--muted:#6B7280}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",system-ui,Arial,sans-serif;background:var(--bg);color:#111827}
header{background:linear-gradient(135deg,#0F3D2E,#0E9F6E);color:#fff;padding:38px 24px}
header .in{max-width:1180px;margin:0 auto}
h1{margin:0 0 6px;font-size:34px;letter-spacing:-.5px}
h1 span{color:var(--amber)}
header p{margin:0;color:#D1FAE5;font-size:16px;max-width:760px}
.bar{max-width:1180px;margin:22px auto 0;display:flex;gap:10px;flex-wrap:wrap}
a.btn{display:inline-block;background:var(--amber);color:#111827;font-weight:700;text-decoration:none;
padding:12px 20px;border-radius:10px;font-size:15px}
a.btn.ghost{background:rgba(255,255,255,.14);color:#fff}
main{max-width:1180px;margin:26px auto 60px;padding:0 24px}
h2{font-size:19px;margin:34px 0 4px;color:var(--green)}
.note{color:var(--muted);font-size:14px;margin:0 0 14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px}
.tile{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;
flex-direction:column;text-decoration:none;color:inherit}
.tile:hover{border-color:var(--teal);box-shadow:0 6px 18px rgba(15,61,46,.12)}
.tile .ph{aspect-ratio:1/1;background:linear-gradient(135deg,#0F3D2E,#0E9F6E);display:flex;
align-items:center;justify-content:center;overflow:hidden}
.tile .ph img{width:100%;height:100%;object-fit:cover}
.tile .ph.v{aspect-ratio:9/16}
.tile .ph.w{aspect-ratio:16/9}
.tile .meta{padding:10px 12px;font-size:13px;line-height:1.35}
.tile .meta b{display:block;color:var(--green);font-size:13px}
.tile .meta span{color:var(--muted);font-size:12px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{padding:11px 14px;text-align:left;font-size:14px;border-bottom:1px solid var(--line)}
th{background:#ECFDF5;color:var(--green);font-size:13px;text-transform:uppercase;letter-spacing:.4px}
td code{font-size:12px;color:#0B7A56}
a{color:var(--teal)}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 24px;color:var(--muted);font-size:13px;text-align:center}
"""


def size_str(n):
    return "%.1f MB" % (n / 1048576) if n > 1048576 else "%.0f KB" % (n / 1024)


def make_zip(pattern_dir, dest, skip_zips=False):
    files = [p for p in sorted(pattern_dir.rglob("*"))
             if p.is_file() and not (skip_zips and p.suffix == ".zip")]
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files:
            z.write(p, p.relative_to(pattern_dir.parent).as_posix())
    return dest, sum(p.stat().st_size for p in files), dest.stat().st_size


def tile(rel, label, sub, cls, is_video=False):
    if cls == "v":
        ph = '<div class="ph v"><video src="%s" muted playsinline preload="metadata"></video></div>' % rel
    elif cls == "w":
        ph = '<div class="ph w"><img loading="lazy" src="%s" alt=""></div>' % rel
    elif cls == "s":
        ph = '<div class="ph"><img loading="lazy" src="%s" alt=""></div>' % rel
    else:
        ph = '<div class="ph"><img loading="lazy" src="%s" alt=""></div>' % rel
    return ('<a class="tile" href="%s" download>%s<div class="meta"><b>%s</b>'
            '<span>%s</span></div></a>' % (rel, ph, html.escape(label), html.escape(sub)))


def main():
    total_img = sum(p.stat().st_size for p in IMG.rglob("*") if p.is_file())
    total_vid = sum(p.stat().st_size for p in VID.rglob("*") if p.is_file())

    z1, raw1, z1s = make_zip(IMG, ROOT / "Smart_Biogas_Social_IMAGES.zip")
    z2, raw2, z2s = make_zip(VID, ROOT / "Smart_Biogas_Social_VIDEOS.zip")
    z3, raw3, z3s = make_zip(ROOT, ROOT / "Smart_Biogas_Social_KIT.zip", skip_zips=True)

    parts = ["<!DOCTYPE html><html lang=en><head><meta charset=utf-8>",
             '<meta name=viewport content="width=device-width,initial-scale=1">',
             "<title>Smart Biogas — social media kit (images + videos)</title>",
             "<style>%s</style></head><body>" % CSS]
    parts.append(
        '<header><div class="in"><h1>SMART BIOGAS <span>SOCIAL KIT</span></h1>'
        "<p>49 images and 7 videos explaining the project — the same numbers, specs and "
        "brand as the website, as plain files you can upload straight to Facebook, Instagram, "
        "TikTok, Reels, Shorts and LinkedIn. Tap any file to download it.</p>"
        '<div class=bar><a class=btn href="%sSmart_Biogas_Social_IMAGES.zip" download>Download '
        "all images (%s)</a>"
        '<a class=btn href="%sSmart_Biogas_Social_VIDEOS.zip" download>Download all videos '
        "(%s)</a>"
        '<a class=btn ghost href="%sSmart_Biogas_Social_KIT.zip" download>Full kit including '
        "captions (%s)</a></div></div></header>"
        % (ZIP_BASE, size_str(z1s), ZIP_BASE, size_str(z2s), ZIP_BASE, size_str(z3s)))
    parts.append("<main>")

    for title, folder, cls in GROUPS:
        d = IMG / folder
        if not d.exists():
            continue
        files = sorted(p for p in d.iterdir() if p.is_file())
        parts.append("<h2>%s</h2>" % html.escape(title))
        parts.append('<p class=note>%d files · tap to download · post in this order</p>' % len(files))
        parts.append('<div class=grid>')
        for i, p in enumerate(files, 1):
            rel = p.relative_to(ROOT).as_posix()
            sub = "%d of %d · %s" % (i, len(files), size_str(p.stat().st_size))
            parts.append(tile(rel, p.stem.replace("_", " "), sub, cls))
        parts.append("</div>")

    parts.append("<h2>Videos</h2>")
    parts.append('<p class=note">H.264 + AAC · 30fps · silent track so every platform accepts '
                 "the upload · add music and voiceover in the app</p>")
    parts.append("<table><tr><th>File</th><th>Resolution</th><th>Length</th><th>Size</th>"
                 "<th>Download</th></tr>")
    RES = {"reel01_waste_to_energy.mp4": ("1080x1920", "29.2s"),
           "reel02_sensors.mp4": ("1080x1920", "28.5s"),
           "reel03_safety.mp4": ("1080x1920", "20.0s"),
           "reel04_real_build.mp4": ("1080x1920", "32.5s"),
           "reel05_calculator_cta.mp4": ("1080x1920", "18.8s"),
           "feed_square_hero.mp4": ("1080x1080", "30.0s"),
           "landscape_hero_16x9.mp4": ("1920x1080", "28.5s")}
    for p in sorted(VID.glob("*.mp4")):
        r, dur = RES.get(p.name, ("?", "?"))
        parts.append('<tr><td><code>%s</code></td><td>%s</td><td>%s</td><td>%s</td>'
                     '<td><a href="videos/%s" download>get</a></td></tr>'
                     % (p.name, r, dur, size_str(p.stat().st_size), p.name))
    parts.append("</table>")

    parts.append("<h2>Captions and the 30-day plan</h2><table>"
                 "<tr><th>File</th><th>What is in it</th><th>Download</th></tr>")
    DESC = {
        "INSTAGRAM_FACEBOOK.md": "3 carousel captions, stat cards, Stories sequence, FB link posts",
        "REELS_TIKTOK.md": "beat sheet + voiceover + caption + hashtags for all 7 videos",
        "FACEBOOK.md": "3 Facebook posts incl. a text-only version for groups",
        "POSTING_PLAN.md": "all 30 days mapped to a specific file, with platform notes",
    }
    for p in sorted(CAP.glob("*.md")):
        parts.append('<tr><td><code>%s</code></td><td>%s</td>'
                     '<td><a href="captions/%s" download>get</a></td></tr>'
                     % (p.name, html.escape(DESC.get(p.name, "")), p.name))
    parts.append("</table>")
    parts.append("</main>")
    parts.append("<footer>SUT · Energy Engineering 2025/2026 · project: "
                 "<a href=https://smart-biogas2026.surge.sh>smart-biogas2026.surge.sh</a> · "
                 "prototype figures are provisional pending pilot data</footer></body></html>")

    (ROOT / "index.html").write_text("\n".join(parts), encoding="utf-8")

    print("images: %d files, %s" % (len(list(IMG.rglob('*'))), size_str(total_img)))
    print("videos: %d files, %s" % (len(list(VID.glob('*.mp4'))), size_str(total_vid)))
    print("%s  raw %s -> %s" % (z1.name, size_str(raw1), size_str(z1s)))
    print("%s  raw %s -> %s" % (z2.name, size_str(raw2), size_str(z2s)))
    print("%s  -> %s" % (z3.name, size_str(z3s)))
    print("index.html: %.0f KB" % ((ROOT / "index.html").stat().st_size / 1024))


if __name__ == "__main__":
    main()
