# Instagram + Facebook captions — Smart Biogas social kit
Paste as-is. Line 1 is the hook (visible before "more").

---

## 1. Carousel A — "WASTE → ENERGY?" (7 slides, 1080x1350)
Files: `images/ig01_waste_to_energy/01_cover.png` → `07_cta.png`
Slide order: cover → problem → shred+feed → digest 35C → collect biogas → safety → generate+data+CTA

**Caption**
WASTE → ENERGY?

Egypt throws away about 18 million tons of food waste every year. 80–88% of it ends up in open
dumps while 81–82% of our electricity runs on imported gas. We pay to throw waste away, then
pay again to import the energy that waste could have made.

We built the loop that closes both gaps: shred and feed a sealed 18 litre digester at 35°C,
collect the biogas, generate, and log every sensor through 2× ESP32 into a live dashboard.

Not a concept. A working mobile rig on casters — 100×50×70 cm, real sensors, real gas
handling, real mechanical safety backups. Software never replaces a relief valve.

Swipe through all 7 slides, then open the live project: smart-biogas2026.surge.sh

Which slide surprised you most? Tell us 1–7 below.

#SmartBiogas #WasteToEnergy #FoodWaste #Egypt #Sustainability #Engineering
#AnaerobicDigestion #CleanEnergy #CircularEconomy #IoT #ESP32 #SUT #EnergyEngineering
#EgyptianEngineering #RenewableEnergy #Prototype

---

## 2. Carousel B — "The real 18 L build" (6 slides, 1080x1350)
Files: `images/ig05_real_build/01_cover.png` → `06_scale_cta.png`
Slide order: not-a-render cover → 18 L spec table → sensors → control stack → 7 safety layers → scale + CTA

**Caption**
Not a render. A working build.

18 L HDPE digester, 12–14 L working volume, held at 35°C with a gear motor and paddle.
5–10 L gas bladder with filter, regulator, non-return and flame arrestor. Control cabinet
with 2× ESP32-WROOM-32, relays and a buck converter. Frame 100×50×70 cm on casters.

Sensors: DS18B20 ×2, MQ-4, MQ-136, MPX5010, JSN-SR04T, pH, optional NDIR.
Control path: sensors → ESP32 → MQTT over TLS → Mosquitto/Node.js → PostgreSQL + TimescaleDB
→ React + Grafana + Python AI.

Prototype cost ≈ 10,900 EGP, provisional pending quotations. A prototype price is not a
commercial price, and we will not pretend otherwise.

Next scale: 18 L → 60 L pilot → 500 L+ commercial, sized per waste stream.

See the live project: smart-biogas2026.surge.sh

Comment SPEC and we will send you the full build sheet.

#SmartBiogas #Prototype #Engineering #ESP32 #IoT #Sensor #MechanicalEngineering
#WasteToEnergy #SUT #EnergyEngineering #Biogas #EngineeringStudent #Tech

---

## 3. Carousel C — "Why it pays back" (5 slides, 1080x1350)
Files: `images/ig07_value/01_pillars.png` → `05_cta.png`
Slide order: 4 value pillars → 6 revenue streams → priority pyramid → sales funnel → CTA

**Caption**
One rig. Four values. Six revenue streams.

Value: waste diverted and quantified in kg/day. Energy from biogas. Data you can audit in
kWh/kg and EGP/m3. Sustainability you can report instead of claim.

Revenue: system sales, installation, maintenance, IoT subscription, upgrades, and custom
engineering. Lifetime value ≈ 2.5× the hardware alone once care, data and uptime are counted.

Who goes first? Universities for fast validation, then restaurants and hotels, then food
processing, then agricultural operations. Validate speed, then chase revenue.

Ten validation steps before we quote a single ROI number. Measure, then monetize.

Start with data, not a quote: smart-biogas2026.surge.sh

Comment your tier 1–4 and we will reply.

#SmartBiogas #BusinessModel #Sustainability #WasteToEnergy #Startup #Revenue
#CircularEconomy #Egypt #SUT #EnergyEngineering #Biogas #ROI #B2B

---

## 4. Square stat cards (1080x1080) — use one per post, or as a 3-post sequence
Files: `squares/sq01_18m_tons.png`, `sq02_81pct.png`, `sq03_loop.png`

**sq01 — 18M tons**
18 million tons of food waste generated in Egypt every year. 80–88% still ends up in open
dumps: methane, disease vectors and a resource we paid to throw away.

Egypt has the waste AND the energy problem. The fix is the same loop.

Save this stat, and send it to someone who still throws food away.

#FoodWaste #Egypt #SmartBiogas #WasteToEnergy #Sustainability #18MillionTons

**sq02 — 81–82%**
81–82% of Egypt's electricity runs on imported natural gas. Meanwhile we bury the exact
energy source that could replace part of those imports.

Organic waste is not a disposal problem. It is a fuel supply that is already paid for.

#EnergySecurity #Egypt #SmartBiogas #ImportedGas #WasteToEnergy #EnergyTransition

**sq03 — one closed loop**
FOOD WASTE → PRE-PROCESSING → ANAEROBIC DIGESTION → BIOGAS → ENERGY → IoT + AI DATA.

Six steps turn an unmanaged disposal stream into auditable kWh, m3/kg and EGP/m3.

That is the whole project in one line. Everything else is engineering.

#SmartBiogas #AnaerobicDigestion #CircularEconomy #IoT #WasteToEnergy #SUT

---

## 5. Stories (1080x1920) — post as a 3-frame sequence
Files: `stories/story1_poll.png`, `story2_bts.png`, `story3_cta.png`

**Frame 1 — poll**
Use the built-in POLL sticker: "How much food waste do you generate?" Options:
0–20 kg/day · 20–50 kg/day · 50–100 kg/day · 100+ kg/day
Caption: Tap your answer — it tells us which rig size you need.

**Frame 2 — behind the scenes**
Text: pH calibration day. Two buffers, one probe, rinse, slope check, then the slurry.
If the number drifts, the whole loop is wrong.
Sticker: POLL "Have you calibrated a pH probe this week?"
Caption: Real R&D beats perfect renders. Comment LAB for the full build log.

**Frame 3 — CTA**
Use the LINK sticker → smart-biogas2026.surge.sh
Text: Swipe up. One question: how much organic waste per day? We come back with sizing,
payback and a 30-day pilot plan.

---

## 6. Reel covers (1080x1920) — the first frame you can also post as a static
Files: `reels/reel01_waste_to_energy.png`, `reel02_sensors.png`, `reel03_safety.png`,
`reel04_real_build.png`
Captions for the matching videos are in `REELS_TIKTOK.md`.
