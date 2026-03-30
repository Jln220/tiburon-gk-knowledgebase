# Blue Tiburon — Test Car
## 2003 Hyundai Tiburon GK | 24 Hours of Lemons

**Role:** Lower-tech test car / primary race car
**Engine:** 2.7L V6 Delta (G6BA) — naturally aspirated, "junkyard engine" (unknown miles, sourced from junkyard, running well ~2 years)

---

## Engine & Drivetrain

### Engine
- Stock 2.7L V6 Delta (G6BA), naturally aspirated
- Port matched intake manifolds
- Cold air intake with box bracket
- 170°F thermostat (low-temp for track use)
- Gates timing belt kit (recently installed)
- Original wasted spark ignition coils (no individual coils)
- Stock fuel injectors (Kefico 9260930004, 194cc @ 45psi, 14.2Ω)
- ECCPP eBay headers with exhaust wrap (not equal length, budget option)
- NGK spark plug wires

### Exhaust
- ECCPP headers (eBay, wrapped)
- *(remainder of exhaust TBD)*

### Transmission & Clutch
- **6-speed Aisin** manual transmission (stock)
- **Phantom Grip** block-style LSD
- ClutchMasters FX500 clutch (recently installed)
- Fidanza aluminum flywheel (recently installed)
- Torque Solutions shifter bushings

### Fuel System
- Stock fuel injectors
- Cheap Amazon fuel pressure regulator

### ECU & Tuning
- **Stock Siemens ECU** (no aftermarket ECU)
- **No PDM** (no AIM power distribution module)
- Tuning via **GKFlasher** (see `/Knowledgebase/opengk/gkflasher.md`)
- All sensors are OpenGK recommended types (see `/Knowledgebase/opengk/sensor-information.md`)
- ECU variant: Siemens 5WY15 or 5WY17/18/1F (SIMK43 4MBit MAF) — verify from ECU label

### Deleted Systems
- AC system deleted
- Charcoal canister (EVAP) deleted
- Ignition switch deleted (start button replaces it)
- **No wheel speed sensors** — TC and ABS are not possible on either car.

---

## Electrical

### Starting & Kill Switch
- **No ignition switch** — starts with a start button
- **OMP 6-pole kill switch**
- Immobiliser: V6 uses BCM-based system (BCM asks ECM for start permission) — may need bypass/programming for start button setup

### Battery & Grounding
- Battery relocated to **rear right** of car, in a battery box
- **2 AWG cable** from battery to kill switch
- Battery connected to chassis ground
- Engine grounded with:
  - Ground strap
  - 2 AWG cable to chassis

### Wiring
- Simpler wiring (stock harness, deletions only — no added complexity)
- No PDM, no Haltech, no aftermarket ECU

### Gauges & Instrumentation
- OEM instrument cluster retained
- AEM oil temperature gauge
- AEM oil pressure gauge
- AEM air/fuel ratio (AFR) gauge

---

## Suspension, Steering & Chassis

### Coilovers
- **KSport Kontrol Pro** (CHY050-KP)
- Front spring rate: 7.5 kg/mm
- Rear spring rate: 4 kg/mm
- 36 levels of damping adjustment
- Product: https://ksportusa.com/product/hyundai-tiburon-kontrol-pro-coilovers-chy050-kp/

### Front Suspension
- **Moog OE-style control arms** with **SuperPro SPF3133K-SPRO** bushings (additional positive caster)
- Strut-to-knuckle bolts: **Belmetric BFD14X1.5X70YLW** (M14x1.5x70mm, Class 10.9, DIN 6921 hex flange, yellow zinc)
  - 34mm threaded / 36mm unthreaded, 18mm hex drive, 30.5mm flange
  - Spec sheet: https://belmetric.com/content/A-PDF_Drawings/BFD14X1.5X70YLW.pdf
- Strut-to-knuckle washers: **Nord-Lock WNORD14** (M14, 23mm OD, 15.2mm ID, 3.4mm thick, zinc flake, wedge dual-lock)
  - Spec sheet: https://belmetric.com/content/A-PDF_Drawings/WNORD14.pdf
- **Reason for bolts/nordlocks:** resolves sliding issue with factory camber bolts
- Front wheel bearings replaced **Fall 2024**

### Rear Suspension
- **SuperPro bushings** in rear trailing arms (shared with white car)
- Rear wheel bearings replaced **Fall 2024**

### Sway Bars & Links
- **Adjustable sway bar links** front and rear
- **Stock sway bars** front and rear

### Axles
- **GSP axles** with **Timken axle seals**

### Wheel Spacers
- **25mm spacers** — testing effect on wheel bearing life
- Survived: 3× 16-hour races + ~8 track days so far

### Wheels & Tires
- 3 sets of OEM 17x7 wheels
- Tire size: 215/45/17
- Tire options:
  - Hankook RS4 (performance/grip)
  - Continental ExtremeContact Endurance (endurance/longevity)

### Steering
- **Momo detachable steering wheel** (quick release)
- *(No front/rear strut bars on blue car)*

---

## Interior & Safety

### Seating
- **Sparco Sprint L** seat (non-containment)
- 16 gauge steel plate welded over driver's side floor
- Exhaust tunnel cut to lower seat height (improved seating position relative to cage)
- **Crow Safety 6-point Enduro harness**

### Controls
- Wiper motor rewired to **rotary switch** (avoids hitting column stalk while racing)

### Visibility
- **FrostFighter heated windshield** (for defogging)

### Fire Suppression
- **Lifeline 2020** fire suppression system
- New bottle purchased **September 2024**

### Driver Cooling
- **Paragon Viking CoolSuit** system

### Data & Timing
- **Garmin Catalyst** (video + lap timing)

---

## Maintenance Log

### Oil Analysis — Blackstone Labs

**Unit ID:** APRSPLS CRAB | **Lab:** Blackstone Laboratories, Fort Wayne IN
**Oil:** Kirkland 5W/30 Full Synthetic | **Engine:** Hyundai 2.7L V6 (G6BA)
**Original reports:** `cars/oil-analysis/`

#### Test 1 — Sampled 4/3/2025 (Lab# S240847)
**Context:** After two HPDEs, Mar–Jun 2024 season. 2,000 miles on oil. Unit at 143,500 mi. 0 qts makeup oil.

| Element | Result (ppm) | Unit Avg | Universal Avg | Status |
|---------|-------------|----------|---------------|--------|
| Aluminum | 6 | 6 | 4 | Slightly above avg |
| Chromium | 1 | 1 | 1 | Normal |
| **Iron** | **11** | **11** | **10** | **Watch — accelerated per-mile wear** |
| Copper | 4 | 4 | 7 | Good (below avg) |
| Lead | 1 | 1 | 1 | Normal |
| Tin | 3 | 3 | 1 | Slightly elevated |
| Molybdenum | 67 | 67 | 78 | Normal (additive) |
| **Silicon** | **39** | **39** | **15** | **High — check air intake for leaks** |
| Sodium | 5 | 5 | 40 | Good |
| Boron | 170 | 170 | 68 | Additive package |
| Calcium | 1201 | 1201 | 1655 | Additive package |
| Magnesium | 445 | 445 | 332 | Additive package |
| Phosphorus | 578 | 578 | 698 | Additive package |
| Zinc | 700 | 700 | 824 | Additive package |

| Property | Result | Should Be |
|----------|--------|-----------|
| SUS Viscosity @ 210°F | 54.6 | 56–63 |
| cSt Viscosity @ 100°C | 8.66 | 9.1–11.3 |
| Flashpoint °F | 375 | >385 |
| Fuel % | 0.5 | <2.0 |
| Antifreeze % | 0.0 | 0.0 |
| Water % | 0.0 | 0.0 |
| Insolubles % | 0.3 | <0.6 |

**Blackstone comments:** Iron at 11 ppm shows accelerated steel wear on a per-mile basis (sample run shorter than 5K universal avg baseline). Other metals look good. Check for air intake leaks in case silicon is dirt. Thin viscosity and minor fuel (0.5%) are fine. Check back in 2K miles.

---

#### Test 2 — Sampled 6/13/2025 (Lab# S246709)
**Context:** One HPDE weekend, ~2 months after first test. Unit reported at 200,000 (hours vs miles tracking issue). 1 qt makeup oil added.

| Element | Result (ppm) | Unit Avg | Previous | Universal Avg | Trend |
|---------|-------------|----------|----------|---------------|-------|
| Aluminum | 6 | 6 | 6 | 4 | Stable |
| Chromium | 1 | 1 | 1 | 1 | Stable |
| **Iron** | **10** | **11** | **11** | **10** | **Improved (↓1)** |
| Copper | 3 | 4 | 4 | 7 | Good (↓1) |
| Lead | 0 | 1 | 1 | 1 | Good (↓1) |
| **Tin** | **4** | **4** | **3** | **1** | **Elevated (↑1) — watch** |
| Molybdenum | 90 | 79 | 67 | 79 | Normal (additive) |
| Silicon | 22 | 31 | 39 | 15 | Improved (↓17) but still above avg |
| Sodium | 5 | 5 | 5 | 40 | Good |
| Boron | 109 | 140 | 170 | 68 | Additive package |
| Calcium | 878 | 1040 | 1201 | 1651 | Additive package |
| Magnesium | 664 | 555 | 445 | 334 | Additive package |
| Phosphorus | 701 | 640 | 578 | 698 | Additive package |
| Zinc | 798 | 749 | 700 | 823 | Additive package |

| Property | Result | Should Be | Previous |
|----------|--------|-----------|----------|
| SUS Viscosity @ 210°F | 54.5 | 56–63 | 54.6 |
| cSt Viscosity @ 100°C | 8.61 | 9.1–11.3 | 8.66 |
| Flashpoint °F | 400 | >385 | 375 |
| Fuel % | <0.5 | <2.0 | 0.5 |
| Antifreeze % | 0.0 | 0.0 | 0.0 |
| Water % | 0.0 | 0.0 | 0.0 |
| Insolubles % | 0.3 | <0.6 | 0.3 |

**Blackstone comments:** Results look good next to averages. Tin is a little elevated, but in the absence of other metals reading high (specifically copper from bronze wear), it's probably fine to just check back on tin. Viscosity is still slightly thin for 5W/30, should be harmless. Try ~4,000 miles on next oil. Note: hours reported this time vs miles last time, making direct comparison difficult.

---

#### Trend Summary
| Metric | Test 1 (4/3/25) | Test 2 (6/13/25) | Direction | Notes |
|--------|-----------------|-------------------|-----------|-------|
| Iron | 11 | 10 | ↓ Improving | Was flagged, now at universal avg |
| Silicon | 39 | 22 | ↓ Improving | Still above 15 avg — air intake leak? |
| Tin | 3 | 4 | ↑ Watch | Blackstone says monitor, no bronze wear present |
| Viscosity (cSt) | 8.66 | 8.61 | Stable | Consistently thin for 5W/30, harmless |
| Flashpoint | 375 | 400 | ↑ Improved | Less fuel dilution |
| Fuel % | 0.5 | <0.5 | ↑ Improved | |

**Action items:**
- Monitor tin trend on next sample
- Investigate silicon source — cold air intake box/bracket seal? Filter fitment?
- Next sample at ~4,000 miles per Blackstone recommendation
- Resolve hours vs miles tracking with Blackstone (use miles consistently)

### Service History
| Date | Work Performed | Notes |
|------|---------------|-------|
| ~2024 | Engine installed | Junkyard V6, unknown miles |
| Jul 2025 | ClutchMasters FX500 + Fidanza flywheel | New clutch/flywheel combo |
| Recent | Gates timing belt kit | Full timing belt service |
| Fall 2024 | Front & rear wheel bearings replaced | |
| Sep 2024 | Lifeline 2020 bottle | New fire suppression bottle |

---

## Known Issues & Ongoing Work
- **Seat height relative to cage** — floor drop resolved in both cars; white car now has Momo Daytona, blue car now has Sparco Sprint L
- **25mm wheel spacers** — monitoring for wheel bearing wear; 3 races + 8 track days so far, no issues
- **Amazon fuel pressure regulator** — cheap/temporary; white car getting Radium upgrade
