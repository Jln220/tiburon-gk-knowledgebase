# OEM Instrument Cluster Integration — White Tiburon (Haltech + AIM PDM)

**Goal:** Keep the factory gauge cluster operational for RPM, speed, fuel level, and coolant temp while running the Haltech Elite 2500 and AIM PDM 32.

**Status:** RESEARCH — needs bench/on-car testing to confirm
**Data Sources:** Shop manual body-electrical (BE-60–65), electrical manual schematic diagrams (SD-48–49, SD-120–122), OpenGK ECM pinouts, Haltech pinout docs
**Confidence:** Signal types and specs from factory manual = HIGH. Haltech DPO configuration details = MEDIUM (forum-sourced, needs NSP verification).

---

## 1. Cluster Connector Reference

The cluster uses three connectors: **M10-1**, **M10-2**, **M10-3**. The pin numbering visible in the circuit diagram (body-electrical BE-61) labels these gauge-critical signals on the cluster:

| Signal Name | Cluster Connector | Function |
|-------------|-------------------|----------|
| TACHO SIGNAL | M10-1 | RPM display — frequency input from ECM |
| SPEED SIGNAL | M10-1 | Speedometer — pulse input from VSS |
| FUEL UNIT | M10-1 | Fuel gauge — resistance from fuel sender |
| FUEL GND | M10-1 | Fuel gauge — ground return |
| TEMP UNIT | M10-1 | Coolant temp gauge — resistance from CTS sender |
| INJECTION SIGNAL | M10-1 | Instantaneous fuel consumption gauge (multi-gauge unit) |
| BUZZER | M10-1 | Warning buzzer |
| METER FUEL | M10-1 | Fuel meter coil power |

**Power:** Fuse 17 (10A) — IG1 switched, feeds cluster indicator power and gauge coils.
**Fuse 16** (10A) — feeds ECM, multi gauge unit, TCM, vehicle speed sensor.

---

## 2. Signal-by-Signal Analysis

### 2a. TACHOMETER (RPM) — EASIEST

**Stock behavior:**
- Cross-coil type gauge, V6: **3 pulses per revolution**
- ECM (Siemens C133-4 pin 17) outputs an "engine speed signal" — a square wave whose frequency = RPM × 3 / 60
- The cluster tachometer responds to the **frequency** of voltage pulses from the ECM
- Tolerance: ±100 RPM at 1,000 to ±240 RPM at 8,000

**Haltech solution:**
- Assign a **DPO** as "Tacho Output" in Haltech NSP
- **DPO 1** (34-pin, pin 18, wire V/B) is the best choice — it has a user-definable 0–12V pull-up
- NSP settings: Tacho Output function → **3 pulses per revolution** for V6
- Active State: Low, Pull-Up: 12V (cross-coil tachs typically want a 12V swing)
- Wire Haltech DPO 1 → cluster TACHO SIGNAL pin

**Testing plan:**
1. With cluster on the bench (IG1 power from 12V supply + fuse 17), feed a square wave from Haltech DPO 1
2. Verify needle sweep matches RPM in Haltech NSP
3. If needle reads wrong, try adjusting pulses per revolution (2 vs 3) — some aftermarket ECUs count differently

**Confidence:** HIGH — this is a standard Haltech feature, well-documented

---

### 2b. SPEEDOMETER — STRAIGHTFORWARD

**Stock behavior:**
- Cross-coil type gauge
- Input: **Hall IC type, 4 pulses per revolution** from VSS (vehicle speed sensor C109 on transaxle)
- 637 rpm × 4 pulses/rev = 60 km/h indication
- The VSS is on the speedometer driven gear in the transaxle — it physically generates pulses proportional to output shaft speed
- ECM receives VSS on C133-4 pin 39, and the signal also routes to the cluster and BCM

**Haltech solution — Two options:**

**Option A (Preferred): Keep VSS wired to cluster directly**
- The VSS output goes to three places: ECM, cluster, BCM-JM (for speed-dependent features)
- Simply keep the existing VSS → cluster wire intact
- Wire VSS signal to a Haltech **SPI input** (26-pin, SPI 1–4, 50kHz max) for the ECU to read speed
- This requires NO Haltech output — the cluster gets its signal straight from the physical sensor
- The only question is whether the BCM needs the speed signal (it uses it for over-speed warning, intermittent wiper speed sensitivity, and auto-lock)

**Option B: Haltech generates speed output via DPO**
- If you need to reroute through Haltech (e.g., speed correction, gear ratio change), configure a DPO as speed output
- DPO 2 (34-pin, pin 1, wire V/BR) — fixed 5V pull-up, good for Hall IC type input
- NSP: Signal Type = Frequency, Mode = Table, map Vehicle Speed → output frequency
- The cluster expects 4 pulses/rev from the transaxle, so you'd need to match the expected frequency at each speed
- Formula: freq (Hz) = (speed_kmh / 60) × 637 × 4 / 60 ≈ speed_kmh × 0.7078 Hz

**Testing plan:**
1. Option A first — confirm the existing VSS wire to the cluster still works with the Haltech spliced in on an SPI input
2. Drive at known speed (GPS reference from AIM), confirm speedometer accuracy
3. If the speedo is off, switch to Option B and calibrate in NSP table

**Confidence:** HIGH for Option A (no change needed), MEDIUM for Option B (needs frequency calibration)

---

### 2c. FUEL GAUGE — NEEDS CREATIVE SOLUTION

**Stock behavior:**
- Cross-coil type (magnetic, two coils at right angles)
- Driven by **variable resistance** from fuel sender (M55, in fuel tank)
- Fuel sender is a float-arm rheostat:
  - Full (F): **6 Ω**
  - Half (1/2): **32.5 Ω**
  - Empty (E): **97 Ω**
- Powered through Fuse 17 (IG1), current through gauge coils varies with sender resistance
- Low fuel warning: separate thermistor sensor in the sender unit
- The ECM is NOT in this circuit — it's a direct analog loop: Battery → Fuse 17 → gauge coil → FUEL UNIT wire → fuel sender → FUEL GND → ground

**Challenge with Haltech/PDM:**
- The fuel gauge is purely resistive — it's not driven by a signal the ECU generates
- The stock fuel sender in the tank physically varies resistance as fuel level changes
- If you keep the OEM fuel sender wired to the cluster, **the fuel gauge will work with zero changes**
- The Lowdoller fuel pressure/temp sensor is on the fuel return line — it does NOT replace the tank sender

**Solution: Keep the OEM fuel sender wired to the cluster**
- The fuel sender (M55) has its own connector — FUEL UNIT and FUEL GND go directly to the cluster
- This circuit is independent of the ECM entirely
- Just keep these two wires connected between the tank sender and cluster
- The Haltech doesn't need to be involved at all

**If the OEM sender is removed in the future:**
- You'd need to simulate the 6–97 Ω resistance range
- AIM PDM half-bridge outputs (35A, PWM capable) could theoretically drive a gauge, but simulating variable resistance is non-trivial — you'd need a resistor ladder or a digital potentiometer controlled by the PDM
- More practical: just display fuel level on the AIM 10" dash from the Lowdoller fuel pressure sensor and abandon the OEM fuel gauge
- OR: keep the OEM sender as a dedicated fuel level sensor and wire it to both the cluster AND a Haltech AVI (through a voltage divider/buffer to convert resistance to 0-5V)

**Testing plan:**
1. Confirm the OEM fuel sender connector is still intact and wired
2. IG1 on → fuel gauge should move to its resting position with the sender connected
3. If the sender is disconnected, gauge will peg to Full (low resistance path = more current)

**Confidence:** HIGH that OEM sender → cluster will work as-is. LOW confidence on simulating it electronically if needed later.

---

### 2d. COOLANT TEMPERATURE GAUGE — KEEP OEM SENDER

**Stock behavior:**
- Cross-coil type (same as fuel gauge — magnetic, two perpendicular coils)
- Driven by **variable resistance** from the coolant temperature sender (C111 for 2.7L)
- CTS sender is a **NTC thermistor** (negative temperature coefficient — resistance drops as temp rises):
  - 60°C: **143.4 Ω**
  - 85°C: **58.1 Ω**
  - 110°C: **26.9 Ω**
  - 125°C (red zone): **17.5 Ω**
- Gauge angles: 0° at 60°C, 38° at 85–110°C, 90° at red zone (125°C+)
- Powered through Fuse 17, same principle as fuel gauge
- The ECM has its OWN coolant temp sensor (separate from the gauge sender on the 2.7L) — C111 is a combination sensor with both ECM input and gauge sender

**Important: Two-function sensor (C111)**
- The 2.7L coolant temp sensor/sender (C111) has multiple pins:
  - ECM coolant temp input (goes to ECM C133-3)
  - Gauge sender output (goes to cluster TEMP UNIT)
- The ECM signal and gauge sender are electrically separate circuits sharing a physical housing

**Solution: Keep the OEM CTS gauge sender wired to the cluster**
- Same as fuel gauge — this is a direct resistive circuit, no ECM involvement
- Battery → Fuse 17 → gauge coil → TEMP UNIT → CTS sender → ground
- The Haltech reads coolant temp on its own AVI input (26-pin pin 4, AVI 8) from either the OEM ECT sensor or a Lowdoller coolant sensor
- The cluster gauge reads from the OEM sender — completely independent circuit

**If you replace the OEM CTS with a Lowdoller sensor only:**
- The Lowdoller coolant sensor (LDM899TP100) has both pressure (0.5–4.5V) and temp (PTC resistive)
- The Lowdoller temp output is a PTC thermistor (resistance INCREASES with temp) — opposite of OEM NTC
- You CANNOT wire the Lowdoller PTC temp to the OEM gauge — it would read backwards
- To keep the OEM gauge, you'd need to keep the OEM sender in the coolant circuit as well
- Most practical: keep both sensors. OEM sender for gauge, Lowdoller for Haltech/AIM data

**Testing plan:**
1. Confirm the OEM CTS gauge sender wire to the cluster is intact (separate from the ECM temp wire)
2. IG1 on, engine cold → gauge should show cool
3. Warm engine → gauge should rise toward center
4. If gauge doesn't work, check Fuse 17 and TEMP UNIT continuity

**Confidence:** HIGH — the gauge circuit is independent of the ECM

---

## 3. Summary — What to Test Tomorrow

| Gauge | Signal Type | Source | Haltech Involved? | Difficulty | Expected Result |
|-------|------------|--------|-------------------|------------|-----------------|
| **Tachometer** | Frequency (3 pulses/rev) | Haltech DPO 1 | YES — Tacho Output | Easy | Configure in NSP, wire DPO 1 → TACHO SIGNAL |
| **Speedometer** | Frequency (Hall IC, 4 pulses/rev) | VSS on transaxle (direct) | NO (keep stock wiring) | Easy | Just keep VSS wire to cluster, add SPI tap to Haltech |
| **Fuel Level** | Resistance (6–97 Ω) | OEM fuel sender in tank | NO | None | Keep OEM sender wired to cluster, works as-is |
| **Coolant Temp** | Resistance (NTC, 17.5–143.4 Ω) | OEM CTS gauge sender | NO | None | Keep OEM sender wired to cluster, works as-is |

### Minimal Changes Required:
1. **Tach:** Wire Haltech DPO 1 (34-pin pin 18, V/B) → cluster TACHO SIGNAL. Configure as Tacho Output, 3 pulses/rev, 12V pull-up, active low.
2. **Speed:** Keep the existing VSS → cluster wire. Add a splice/T from VSS to Haltech SPI 1 (26-pin pin 8) for the ECU to read speed.
3. **Fuel:** No changes. OEM sender → cluster is a standalone circuit.
4. **Temp:** No changes. OEM CTS sender → cluster is a standalone circuit.

### Wires to Cut from OEM ECM Harness:
- The old ECM C133-4 pin 17 (engine speed signal output to cluster) — this was the stock ECM's tacho signal. Disconnect from old ECM side, leave cluster side intact for Haltech DPO 1 connection.
- Everything else stays.

### What WON'T Work on the OEM Cluster:
- **Check Engine light** — needs ECM ground control (was ECM C133-4). Haltech can drive this via a DPO if you want it.
- **Multi-gauge unit** (torque/fuel consumption/voltage) — torque gauge uses CAN from stock ECM, fuel consumption uses injection signal from stock ECM. These won't work without significant effort. The AIM 10" dash replaces this functionality anyway.
- **Immobilizer light** — BCM controlled, irrelevant for race car
- **ABS/TCS lights** — depends on whether ABS module is retained

---

## 4. Tomorrow's Test Procedure

### Step 1: Bench Power the Cluster
- Connect 12V to Fuse 17 circuit (IG1 power to cluster)
- Confirm cluster illumination and gauge needles at rest position
- Fuel gauge should rest at its "E" park position (pointer doesn't fall below E per spec)

### Step 2: Test Tachometer
- Connect Haltech DPO 1 output to cluster TACHO SIGNAL wire
- Power up Haltech, configure DPO 1 as Tacho Output (3 pulses/rev, 12V pull-up, active low)
- Use Haltech test mode / test RPM to sweep RPM
- Verify needle tracks correctly from 1K–8K RPM

### Step 3: Test Speedometer
- If VSS is accessible, spin the sensor input (or use a signal generator on the VSS wire)
- Verify speedometer responds to pulses
- Alternative: just drive the car with the VSS connected and compare to AIM GPS speed

### Step 4: Verify Fuel & Temp Gauges
- With OEM senders connected, IG1 on:
  - Fuel gauge should show approximate tank level
  - Temp gauge should show cool (engine cold)
- Start engine, confirm temp gauge rises after warmup

---

## 5. Relevant Knowledgebase References

| Topic | File | Key Lines/Sections |
|-------|------|--------------------|
| Cluster circuit diagram | `shop-manual/body-electrical.md` | Lines 3130–3220 (connectors, pin signals) |
| Gauge specs (speedo/tach/fuel/temp) | `shop-manual/body-electrical.md` | Lines 79–213 (all gauge types and tolerances) |
| Gauge troubleshooting | `shop-manual/body-electrical.md` | Lines 285–310 |
| Gauge inspection procedures | `shop-manual/body-electrical.md` | Lines 3257–3362 |
| Indicators & gauges schematic | `electrical-manual/schematic-diagrams.md` | Lines 7383–7466 (circuit descriptions) |
| Vehicle speed sensor schematic | `electrical-manual/schematic-diagrams.md` | Lines 2780–2844 |
| MFI control system (tach source) | `electrical-manual/schematic-diagrams.md` | Lines 4900–4943 |
| Stock ECM pinout (C133-4 pin 17 = tach) | `opengk/ecm-pinouts.md` | Lines 107–119 |
| Haltech 34-pin pinout | `haltech/main-connector-34-pin-elite2500.md` | Full pinout with DPO assignments |
| Haltech 26-pin pinout | `haltech/main-connector-26-pin-elite2500.md` | SPI inputs for VSS |
| Lowdoller sensors | `cars/lowdoller-sensors.md` | PTC vs NTC note for gauge compatibility |

---

*Document created: 2026-03-07*
*Verification level: MANUAL REVIEW of factory PDFs + web research on Haltech DPO config*
*Known caveat: Haltech NSP tacho output settings sourced from forums — verify exact menu path in NSP software*
