# Campaign — Smart Food Waste-to-Biogas — Full Launch Pack
**Goal:** General Awareness — **Platforms:** Omnichannel (LinkedIn + Instagram + TikTok/Reels + Landing) — **Language:** English Professional — **Version:** v1 17 Sep 2026 — **Source:** `Smart_Food_Waste_to_Biogas_Business_Marketing_Financial_Plan_No_Videos.pdf` v2.1 FIXED

## What you got
- `index.html` — Landing page (hero with your rig, problem, 4 pillars, prototype specs, tech stack, **savings calculator**, business model, waste assessment form)
- `style.css` — Palette deep green #0F3D2E + teal #0E9F6E + amber #F59E0B, responsive, Inter
- `calculator.js` — Biogas Savings Calculator (§13, §18) — inputs kg/day, days, disposal cost, kWh price, yield, CH4%, eff. → outputs annual waste, biogas, kWh theoretical/actual, savings, benefit. Illustrative yield 0.10 m3/kg until BMP replaces.
- `assets/` — Drop **prototype_main.jpg** (your photo) here + optional `dashboard.png`, `team.jpg`. See `assets/README.txt`.
- `content/calendar.csv` — 30-day omnichannel calendar (Days 1-30, funnel Awareness→Pilot, pillars, format, hook, copy, visual brief, hashtags, CTA, KPI) — import to Notion/Sheets.
- `content/linkedin_12.md` — 12 LinkedIn posts ready to paste (1200-700 chars, professional, cited §).
- `content/instagram_12.md` — 12 Instagram posts/reels/carousels.
- `content/tiktok_4.md` — 4 vertical scripts 15-40s with shot lists.
- `content/press_release.md` — One-page press release for SUT / Innovators Support Fund / competitions.
- `content/waste_assessment_form.html` — Standalone lead form (copy to Google Form or keep as HTML). Fields per §12.
- `content/ad_copy.md` — LinkedIn + IG ad sets + UTM + A/B headlines.

## How to preview locally (like server.py:25)
```pwsh
# From C:\Users\Nour\Documents\opencode
python server.py --port 8000
# then open http://localhost:8000/campaign/biogas/
# and http://localhost:8000/campaign/biogas/content/calendar.csv
```
Or double-click `index.html`. Ensure `assets/prototype_main.jpg` is in place (copy from chat hero).

## Where to put the hero image
Save the image you just sent as:
- `campaign/biogas/assets/prototype_main.jpg`  (for the campaign site)
- `assets/biogas/prototype_main.jpg`           (optional, for repo-wide reuse)

PowerShell:
```pwsh
Copy-Item "C:\Users\Nour\Downloads\hero.jpg" "C:\Users\Nour\Documents\opencode\campaign\biogas\assets\prototype_main.jpg" -Force
Copy-Item "C:\Users\Nour\Documents\opencode\campaign\biogas\assets\prototype_main.jpg" "C:\Users\Nour\Documents\opencode\assets\biogas\prototype_main.jpg" -Force
```

## 6-stage funnel (pdf:6) mapping
1 Awareness Days 1-3  | 2 Interest 4-6 | 3 Demonstration 7-10 | 4 Data 11-12 | 5 Pilot 16-18 | 6 Commercial 20-27 | Evergreen 29-30

## Business truth to keep in every post
- Prototype ≈10,900 EGP provisional — pending dated quotations (Appendix A)
- Yield 0.10 m3/kg wet illustrative — mid-range (§B) — replace with BMP per VDI 4630
- No ROI claim before 10-step validation + ≥30d pilot (§23)
- Safety: mech. relief independent, software never replaces valve (Appendix C)

## Next steps
1. Drop hero jpg → verify `index.html` shows it.
2. Review `calendar.csv` in Sheets — adjust dates to your launch.
3. Schedule LI 1-3 + IG 1-2 for Week 1.
4. Wire form to Formspree/Google Form or `mailto:hamza250102724@sut.edu.eg` (send_email.py:22).
5. For paid boost: use `ad_copy.md` UTM + A/B test.

## Hosting options
- Local: `server.py` stdlib (zero deps)
- Cloud: `render.yaml` / `docker-compose.yml` already in repo — add `/campaign/biogas` as static route.

— Generated 17 Sep 2026 — Team: Zeyad/Hamza/Ahmed/Nour/Caren — Supervisor Dr. Mariam — SUT
