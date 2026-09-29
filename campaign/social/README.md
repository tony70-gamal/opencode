# Smart Biogas — social media kit (pics + videos)

Same project, same numbers and same brand as the website, rendered as static images and
videos for Facebook, Instagram, TikTok, Reels, Shorts, Stories and LinkedIn.
Nothing here is a web app: every file is a normal image or MP4 you upload directly.

- 49 images + 7 MP4 videos
- Built with Pillow (`build_social.py`) and ffmpeg (`build_videos.py`) — both re-runnable
- Verified: no text overflow, no text collisions, no blank files, correct video durations

## Folder map

| Folder | Size | Count | Use for |
|---|---|---|---|
| `images/ig01_waste_to_energy/` | 1080x1350 | 7 | IG carousel A — the whole story, problem to CTA |
| `images/ig05_real_build/` | 1080x1350 | 6 | IG carousel B — the 18 L prototype in detail |
| `images/ig07_value/` | 1080x1350 | 5 | IG carousel C — value pillars, revenue, funnel, CTA |
| `images/squares/` | 1080x1080 | 7 | IG/Facebook feed, LinkedIn single image, stat cards |
| `images/vertical/` | 1080x1920 | 10 | Stories, TikTok image posts, 9:16 video slides |
| `images/reels/` | 1080x1920 | 4 | Reel cover frames (also postable alone) |
| `images/landscape/` | 1280x720 | 4 | LinkedIn + YouTube + website hero |
| `images/facebook/` | 1200x630 | 2 | Facebook link posts (largest feed render) |
| `images/youtube/` | 1280x720 | 1 | YouTube thumbnail |
| `videos/` | 9:16 / 1:1 / 16:9 | 7 | Reels, TikTok, Shorts, feed video, LinkedIn video |
| `captions/` | text | 4 | Ready-to-paste captions, beat sheets, 30-day plan |

## Videos

| File | Resolution | Length | Content |
|---|---|---|---|
| `reel01_waste_to_energy.mp4` | 1080x1920 | 29.2s | 18M tons → we pay twice → 4 steps → team |
| `reel02_sensors.mp4` | 1080x1920 | 28.5s | Sensors → control stack → generate → specs |
| `reel03_safety.mp4` | 1080x1920 | 20.0s | Title → 7 safety layers → pH calibration BTS |
| `reel04_real_build.mp4` | 1080x1920 | 32.5s | Not a render → specs → digester → team |
| `reel05_calculator_cta.mp4` | 1080x1920 | 18.8s | Generate → closed loop → assessment CTA |
| `feed_square_hero.mp4` | 1080x1080 | 30.0s | Full project in 30s, feed-square |
| `landscape_hero_16x9.mp4` | 1920x1080 | 28.5s | Cover → problem → process → CTA |

All MP4s are H.264 + AAC, `yuv420p`, 30fps, `+faststart`, with a silent stereo track so every
platform accepts the upload. Add music and a voiceover in the app using the scripts in
`captions/REELS_TIKTOK.md`.

## Rebuilding

```pwsh
C:\Users\Gamal\AppData\Local\Programs\Python\Python311\python.exe campaign\social\build_social.py
C:\Users\Gamal\AppData\Local\Programs\Python\Python311\python.exe campaign\social\build_videos.py
```

`build_social.py` prints a layout audit at the end: `no layout warnings`, `no text overlaps`,
`no text out of bounds`, `small/blank files: 0`. If you edit copy and a block grows, the
audits will tell you which card broke instead of letting you ship a clipped one.

## Where the copy came from
Every number, spec and claim is taken from the existing campaign:
`campaign/biogas/index.html`, `content/press_release.md`, `content/calendar.csv`,
`content/linkedin_12.md`, `content/instagram_12.md`. Prototype cost is always labelled
provisional and pilot data is always labelled pending, exactly as in the website.
