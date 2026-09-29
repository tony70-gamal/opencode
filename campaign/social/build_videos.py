# -*- coding: utf-8 -*-
"""Renders the MP4s for the Smart Biogas social kit from the stills.

Each still gets a slow Ken Burns push and the stills are cross-faded, with a
silent stereo track so every platform accepts the upload.
Run:  python campaign/social/build_videos.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "images"
OUT = ROOT / "videos"
FFMPEG = r"D:\AI\webui\ffmpeg\bin\ffmpeg.exe"
FFPROBE = r"D:\AI\webui\ffmpeg\bin\ffprobe.exe"
FPS = 30
FADE = 0.5
DONE = []

# name, output size, [(stills, seconds), ...]
PLAN = [
    ("reel01_waste_to_energy", (1080, 1920), [
        ("vertical/v01_18m_tons.png", 4.6),
        ("vertical/v02_pay_twice.png", 4.6),
        ("reels/reel01_waste_to_energy.png", 4.6),
        ("vertical/v03_step_feed.png", 4.6),
        ("vertical/v04_step_digest.png", 4.6),
        ("vertical/v06_step_safety.png", 4.6),
        ("vertical/v10_team.png", 4.6),
    ]),
    ("reel02_sensors", (1080, 1920), [
        ("vertical/v07_sensors.png", 7.5),
        ("reels/reel02_sensors.png", 7.5),
        ("vertical/v09_generate.png", 7.5),
        ("vertical/v08_spec.png", 7.5),
    ]),
    ("reel03_safety", (1080, 1920), [
        ("reels/reel03_safety.png", 7.0),
        ("vertical/v06_step_safety.png", 7.0),
        ("stories/story2_bts.png", 7.0),
    ]),
    ("reel04_real_build", (1080, 1920), [
        ("reels/reel04_real_build.png", 8.5),
        ("vertical/v08_spec.png", 8.5),
        ("vertical/v04_step_digest.png", 8.5),
        ("vertical/v10_team.png", 8.5),
    ]),
    ("reel05_calculator_cta", (1080, 1920), [
        ("vertical/v09_generate.png", 6.6),
        ("squares/sq03_loop.png", 6.6),
        ("stories/story3_cta.png", 6.6),
    ]),
    ("feed_square_hero", (1080, 1080), [
        ("squares/sq04_cover.png", 6.4),
        ("squares/sq01_18m_tons.png", 6.4),
        ("squares/sq05_how.png", 6.4),
        ("squares/sq06_safety.png", 6.4),
        ("squares/sq07_team.png", 6.4),
    ]),
    ("landscape_hero_16x9", (1920, 1080), [
        ("landscape/ls01_cover.png", 7.5),
        ("landscape/ls02_problem.png", 7.5),
        ("landscape/ls03_how.png", 7.5),
        ("landscape/ls04_cta.png", 7.5),
    ]),
]


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        tail = (p.stderr or "").strip().splitlines()[-12:]
        print("FAILED:", " ".join(cmd[:6]), "...")
        for t in tail:
            print("   " + t)
        return False
    return True


def build(name, size, clips):
    W, H = size
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / (name + ".mp4")
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error"]
    for rel, dur in clips:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(IMG / rel)]
    cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]

    frames = int(round(dur * FPS))
    chain, labels = [], []
    for i, (rel, dur) in enumerate(clips):
        zoom = 1.0 + 0.11 * min(1.0, i * 0.5 + 0.5)
        vf = ("scale=%d:%d:force_original_aspect_ratio=increase,"
              "crop=%d:%d,"
              "zoompan=z='%f+0.11*on/%d':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
              "d=1:s=%dx%d:fps=%d,setsar=1,fps=%d,format=yuv420p"
              % (int(W * 1.14), int(H * 1.14), int(W * 1.14), int(H * 1.14),
                 zoom, frames, W, H, FPS, FPS))
        if i % 2:
            vf += ",crop=w=iw:h=ih:x=0:y=0"
        chain.append("[%d:v]%s[v%d]" % (i, vf, i))
        labels.append("[v%d]" % i)

    if len(clips) > 1:
        prev = labels[0]
        for i in range(1, len(clips)):
            off = sum(d for _, d in clips[:i]) - i * FADE
            out = "[x%d]" % i
            chain.append("%s%sxfade=transition=fade:duration=%.2f:offset=%.2f%s"
                         % (prev, labels[i], FADE, off, out))
            prev = out
        vlabel = prev
    else:
        vlabel = labels[0]

    cmd += ["-filter_complex", ";".join(chain), "-map", vlabel, "-map",
            "%d:a" % len(clips), "-c:v", "libx264", "-preset", "slow", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "96k",
            "-ar", "44100", "-shortest", "-movflags", "+faststart", str(dest)]
    if not run(cmd):
        return None

    probe = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height,r_frame_rate",
                            "-show_entries", "format=duration,size",
                            "-of", "default=nw=1", str(dest)],
                           capture_output=True, text=True)
    info = dict(l.split("=", 1) for l in probe.stdout.strip().splitlines() if "=" in l)
    dur = float(info.get("duration", 0))
    if abs(int(info.get("width", 0)) - W) > 1 or dur < 3:
        print("VERIFY FAILED %s -> %s" % (name, probe.stdout))
        return None
    DONE.append((name + ".mp4", "%sx%s" % (info["width"], info["height"]),
                 "%.1fs" % dur, "%.1f MB" % (int(info["size"]) / 1048576)))
    return dest


def main():
    if not Path(FFMPEG).exists():
        print("ffmpeg not found at " + FFMPEG)
        return 1
    for name, size, clips in PLAN:
        missing = [c for c, _ in clips if not (IMG / c).exists()]
        if missing:
            print("SKIP %s — missing stills: %s" % (name, missing))
            continue
        build(name, size, clips)
    print("\nrendered %d/%d videos" % (len(DONE), len(PLAN)))
    for n, r, d, s in DONE:
        print("  %-28s %-9s %-7s %s" % (n, r, d, s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
