# Reels / TikTok / Shorts captions + beat sheets — Smart Biogas social kit
Timings match the actual renders (`build_videos.py`). Silent video + silent track, so add
music in the app: pick an "upbeat / documentary" track at low volume under the voiceover.

---

## reel01_waste_to_energy.mp4 — 1080x1920, 29.2s
Beat sheet: `0:00` 18M tons (v01) → `0:04.1` we pay twice (v02) → `0:08.2` title (reel01)
→ `0:12.3` shred + feed (v03) → `0:16.4` digest 35°C (v04) → `0:20.5` safety layers (v06)
→ `0:24.5` the team + link (v10)

**Voiceover script**
Egypt throws away 18 million tons of food a year. We pay to dispose of it, then import gas
for 81% of our electricity. So we built a loop: shred, feed a sealed 18 litre digester at
35 degrees, collect the biogas, generate, and log every sensor. Real build, real sensors,
mechanical safety always independent of software. Full project: smart-biogas2026.surge.sh

**Caption**
18M tons wasted a year. 81% of our power imported. One loop fixes both — and we already
built the 18 L rig. smart-biogas2026.surge.sh

#SmartBiogas #WasteToEnergy #FoodWaste #Egypt #Engineering #Sustainability #Reels
#AnaerobicDigestion #CleanEnergy #TikTok #FYP #IoT #SUT

---

## reel02_sensors.mp4 — 1080x1920, 28.5s
Beat sheet: `0:00` sensors that talk (v07) → `0:07.0` title (reel02) → `0:14.0` generate and
optimize (v09) → `0:21.0` real specs (v08)

**Voiceover script**
This is not a machine that makes gas and hopes for the best. Two ESP32s read temperature,
methane, hydrogen sulfide, pressure, level and pH. Everything goes over MQTT with TLS into
TimescaleDB, and a Python model watches for drift. If pH or pressure leaves the band, the
system pauses feeding before a human has to react.

**Caption**
It doesn't just monitor. It decides. 2× ESP32 → MQTT/TLS → TimescaleDB → Grafana → AI
control. 7 safety layers, and software never replaces a relief valve.
smart-biogas2026.surge.sh

#IoT #ESP32 #Sensors #SmartBiogas #Engineering #DataPillar #SUT #Tech

---

## reel03_safety.mp4 — 1080x1920, 20.0s
Beat sheet: `0:00` title (reel03) → `0:06.5` the 7 layers (v06) → `0:13.0` pH calibration BTS
(story2)

**Voiceover script**
Biogas is fuel, so the gas line gets treated like an industrial installation. Mechanical
relief valve, independent of all software. Non-return valve. Flame arrestor. Methane and
hydrogen sulfide alarms. Forced ventilation, PPE, and an extinguisher mounted on the frame.
The rule is simple: software never replaces a valve.

**Caption**
7 safety layers. Mechanical relief is independent of the software by design.
Share this with your lab safety officer. smart-biogas2026.surge.sh

#Safety #SmartBiogas #Biogas #LabSafety #Engineering #RiskManagement #SUT

---

## reel04_real_build.mp4 — 1080x1920, 32.5s
Beat sheet: `0:00` not a render (reel04) → `0:08.0` real specs (v08) → `0:16.0` digest
(v04) → `0:24.0` the team + link (v10)

**Voiceover script**
This is a real build, not a render. Eighteen litre sealed digester, twelve to fourteen
litres working, held at 35 degrees by a heater and mixed by a paddle. Gas goes into a five to
ten litre bladder, through a filter and a regulator, with a relief valve and a flame arrestor
in the line. Two ESP32s in the cabinet. A hundred by fifty by seventy centimetres, on
casters. Prototype cost around 10,900 EGP. Next stop: a 60 litre pilot with 30 days of
measured data.

**Caption**
A working mobile rig, filmed on the build. 18 L → 60 L pilot → 500 L+ commercial.
Comment SPEC for the full build sheet. smart-biogas2026.surge.sh

#Prototype #Engineering #BuildInPublic #SmartBiogas #MechanicalEngineering #Lab #SUT #Reels

---

## reel05_calculator_cta.mp4 — 1080x1920, 18.8s
Beat sheet: `0:00` generate and measure (v09) → `0:06.1` the closed loop (sq03)
→ `0:12.2` CTA (story3)

**Voiceover script**
Every number in this project comes back to the same question: how much waste do you make a
day? At 100 kilos a day and 300 operating days, that is 30 tonnes a year, and at a biogas
yield of 0.1 cubic metres per kilo, 3,000 cubic metres of gas. Those are illustrative. Our
30-day pilot replaces them with measured yield, so the business case is built on your data,
not our guess.

**Caption**
Try your own number instead of ours: smart-biogas2026.surge.sh
Tell us your kg/day and we size the rig and model the payback.

#SmartBiogas #WasteToEnergy #ROI #SolarPowersBusiness #Calculators #Egypt #SUT

---

## feed_square_hero.mp4 — 1080x1080, 30.0s
Beat sheet: `0:00` cover (sq04) → `0:05.9` 18M tons (sq01) → `0:11.8` how it works (sq05)
→ `0:17.7` safety (sq06) → `0:23.6` the team (sq07)
Use for Instagram feed, Facebook feed, LinkedIn native video (all 1:1 safe).

**Caption**
The whole project in 30 seconds: 18 million tons wasted, one closed loop, seven safety
layers, five engineering students. smart-biogas2026.surge.sh

#SmartBiogas #WasteToEnergy #Egypt #Sustainability #Engineering #CleanEnergy #SUT

---

## landscape_hero_16x9.mp4 — 1920x1080, 28.5s
Beat sheet: `0:00` cover (ls01) → `0:07.0` the problem (ls02) → `0:14.0` how it works (ls03)
→ `0:21.0` CTA (ls04)
Use for YouTube, Facebook wide, LinkedIn, website hero embed.

**Caption**
18 million tons of food waste a year in Egypt. An 18 litre digester, IoT sensors and AI
control turn it into measurable clean energy. Book a 30-day pilot:
smart-biogas2026.surge.sh

#SmartBiogas #WasteToEnergy #Egypt #CleanEnergy #Engineering #Sustainability #SUT
