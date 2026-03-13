# White Tiburon — Weekend Build Tasks
## Haltech + AIM PDM Integration | Physical Switch Panel

**Target:** PDM fully installed and running with stock ECU for next track day. Haltech wired with Lowdoller sensors and MAP vacuum for data logging + CAN communication test. Injector/coil harnesses left ready to plug in the following weekend.

> **Separate reference files:**
> - Race Studio 3 config: `guides/pdm-config.md`
> - Bench test procedures: `guides/bench-test.md`
> - Signal routing: `signal-routing.md`

---

## Current State (March 2026)

| System | Status |
|--------|--------|
| Haltech bench | Cam ✅ Crank ✅ COP fire ✅ — Knock: **next** |
| PDM Race Studio config | ✅ Updated — physical switch panel (no keypad) |
| PDM car connection | Spade connectors → fuse box pin 87 (non-destructive) |
| Physical switch panel | 6 toggles + 1 momentary starter — **not yet wired to PDM** |
| Stock ECU | Connected and running |

---

## GOAL 1 — PDM + Camera + Podium + AFR

Everything needed to run the car on PDM with stock ECU, plus AIM data/video/telemetry and wideband AFR.

### 1.1 PDM Output Configuration (Race Studio 3)

- [ ] Load updated config per `guides/pdm-config.md` (physical switches, no keypad)
- [ ] Configure all power outputs: HP1–HP3, MP1–MP8, LP1–LP7
- [ ] Configure status variables: ENGINE_RUNNING, FUEL_PRIME, FAN_TEMP bands, STARTER_SAFE, MULTI_WARNING
- [ ] Configure wiper priority logic: MP3 (low) = Ch02 AND NOT Ch03; MP6 (high) = Ch03
- [ ] Transmit config to PDM via USB

> **✓ TEST:** Force-test each output in Race Studio Live Measures

### 1.2 PDM CAN Expansion Bus (CAN0) — AIM Devices

- [ ] Verify CAN0 expansion cable: A22 (H) / A11 (L) / A33 (+Vb out) / A10 (GND)
- [ ] Connect AIM CAN Data Hub (4-way) to expansion cable Binder
- [ ] Daisy-chain: PDM → Data Hub → GPS-08 → SmartyCam → Podium Micro
- [ ] Power all devices via A33 (+Vb out CAN, 22 AWG — keep total draw reasonable)

### 1.3 Setup Podium Micro (SN: 1QTV5KM)

- [ ] Mount Podium Micro in accessible location
- [ ] Connect to CAN Data Hub
- [ ] Configure in Race Studio 3 — verify device recognized
- [ ] Set up PodiumConnect telemetry channels
- [ ] Verify live data visible in PodiumConnect app

### 1.4 SmartyCam Mount & Config

- [ ] Mount SmartyCam (windshield or roll bar bracket)
- [ ] Connect to CAN Data Hub (LP3 power from A16)
- [ ] Configure SmartyCam Stream in Race Studio 3:
  - RPM, Speed (GPS-08), Gear, Coolant Temp, Oil Pressure, TPS, Lat G, Long G
- [ ] Set video overlay layout
- [ ] Verify recording on power-up

### 1.5 GPS Module

- [ ] Mount GPS-08 (roof or cowl — clear sky view)
- [ ] Connect to CAN Data Hub
- [ ] Verify position lock in Race Studio Live Data

### 1.6 PDM Sensor Inputs

- [ ] Wire track/tire temp sensor → available PDM channel input (Ch06–Ch08)
- [ ] Wire crankcase pressure sensor → available PDM channel input
- [ ] Configure in Race Studio as analog inputs

### 1.7 PDM CAN1 — Haltech ECU Stream

- [ ] Connect Haltech 26-pin pins 23/24 (CAN H/L) → PDM A30/A31 (CAN1)
- [ ] Select Haltech CAN_V2_40 protocol in ECU Stream tab
- [ ] Enable required channels: RPM, ECT, Oil P, Oil T, Fuel P, TPS, Vehicle Speed, Battery V
- [ ] Enable logging channels per `guides/pdm-session-1.md` Step 2c
- [ ] Verify all CAN data visible in Race Studio Live Data

> **✓ TEST:** Simulate RPM > 50 in NSP → confirm ENGINE_RUNNING activates in Race Studio

### 1.8 Install PDM + Electronics Plate (Passenger Footwell)

All electronics mounted on a single plate in the passenger footwell: PDM, Haltech Elite 2500, Podium Micro (SN: 1QTV5KM), Innovate LM2.

- [ ] Fabricate/source mounting plate for passenger footwell
- [ ] Mount PDM on plate (vibration-isolated)
- [ ] Mount Haltech Elite 2500 on plate
- [ ] Mount Podium Micro on plate
- [ ] Mount Innovate LM2 on plate
- [ ] Route PDM engine bay harness through firewall grommet
- [ ] Route cockpit harness (dash LVDS, switch panel, CAN buses — short runs)
- [ ] Connect Surlok power: 4 AWG from kill switch → 120A breaker → PDM Surlok (+)
- [ ] Connect PDM grounds (B13, B14, B18 to chassis)

### 1.9 Kill Switch Wiring (4-Pole, Already Mounted)

Kill switch is already mounted left of steering wheel. 2 AWG cable already run to it.

```
Battery (+) ─── 2 AWG ─── Kill Switch [Large Terminal A]
                                │
                          [Jumper] to [Small Terminal A]
                                │
                     Kill Switch [Large Terminal B] ───┬─── 2 AWG ─── 150A Breaker ─── Starter B+ / Alternator B+
                                │                      │
                                │                      └─── 4 AWG ─── 120A Breaker ─── PDM Surlok (+)
                                │
                     Kill Switch [Small Terminal B] ─── IGN toggle switch ─── PDM Conn B pin 23 (IGN input)
                                                                         └─── Haltech 34-pin pin 13 (ECU IGN)
```

- [ ] Verify jumper from large terminal A to small terminal A
- [ ] Wire large terminal B → 150A breaker → starter B+ / alternator B+ (2 AWG)
- [ ] Wire large terminal B → 120A breaker → PDM Surlok (+) (4 AWG)
- [ ] Wire small terminal B → IGN toggle switch → PDM B23 + Haltech 34-pin pin 13
- [ ] Test: kill switch OFF → all power drops, `SafeIgnition` = 0, all outputs off
- [ ] Test: kill switch ON, IGN toggle OFF → PDM has Surlok power but `SafeIgnition` = 0

### 1.10 Dash Screen Mount

- [ ] Mount AIM 10" dash (visible from driver position)
- [ ] Connect LVDS cable from PDM to dash
- [ ] Configure dash pages in Race Studio

### 1.11 Connect Switch Panel

- [ ] Wire ignition toggle → PDM Conn B pin 23 (also splice to Haltech 34-pin pin 13, P wire)
- [ ] Wire start button → Ch09 (B21), momentary, active = GND
- [ ] Wire fan override toggle → Ch01 (B26), active = 12V
- [ ] Wire wiper low toggle → Ch02 (B27), active = 12V
- [ ] Wire wiper high toggle → Ch03 (B28), active = 12V
- [ ] Wire coolsuit toggle → Ch04 (B29), active = 12V
- [ ] Wire defogger toggle → Ch05 (B30), active = 12V
- [ ] Wire brake light switch → Ch11 (A26), closed on press
- [ ] Wire warning LED → LP7 (A20)

> **✓ TEST:** Flip each switch → correct output activates in Race Studio Live Measures

### 1.12 Innovate Motorsports Wideband AFR

- [ ] Mount Innovate LM2 controller
- [ ] Wire LM2 power → PDM LP5 (A18)
- [ ] Wire LM2 analog output → available Haltech AVI
- [ ] Install wideband O2 sensor in exhaust
- [ ] Verify AFR reading in Haltech NSP and on AIM dash

### 1.13 Check Haltech CAN Communication

- [ ] Power Haltech from PDM LP1 (A14) — or from stock circuit initially
- [ ] Verify bidirectional CAN: Haltech broadcasts to PDM, PDM reads all enabled channels
- [ ] Confirm fan temp bands react to live coolant temp on CAN
- [ ] Confirm warning LED triggers when sensor thresholds crossed

### 1.14 Alternator Exciter via PDM LP8 (A21)

- [ ] Locate OEM alternator D+ exciter wire (thin ~18 AWG at alternator Yazaki connector)
- [ ] Cut exciter wire at convenient point near fuse box (leave length on both ends)
- [ ] Fuse box side → wire to PDM LP8 (A21, Connector A)
- [ ] Alternator D+ side → remains connected to alternator (load side)
- [ ] LP8 trigger = SafeIgnition, OVC Protected, 5A max (actual draw < 1A)
- [ ] Bench test first: connect 12V indicator lamp to LP8, verify on/off with IGN toggle
- [ ] Verify in car: IGN on + engine running → alternator charges (13.8–14.4V)
- [ ] Verify: IGN off or kill switch → LP8 drops → charging stops immediately

> See `guides/bench-test.md` Section 5 for detailed procedure

### 1.15 OE Main Relay → PDM MP1/MP2 (Phase 1)

MP1 and MP2 temporarily power the stock ECU via the OE main relay socket. Same `SafeIgnition` trigger — no Race Studio change needed when switching to Haltech later.

- [ ] Locate OE main relay in underhood fuse box
- [ ] Pull the OE main relay
- [ ] Insert PDM MP1 (A2) wire into relay socket pin 87 (power out)
- [ ] Insert PDM MP2 (A3) wire into same pin 87 socket (parallel)
- [ ] IGN on → verify stock ECU powers up via PDM
- [ ] IGN off → verify stock ECU loses power

> **Phase 2 switchover:** Disconnect MP1/MP2 from relay socket. Reroute MP1 → injector rail + Haltech 34-pin pin 26 (R/L). Reroute MP2 → COP coil Pin D common bus. No Race Studio config change.

### 1.16 Test Fuel Pump + Starter + Alternator with Stock ECU

- [ ] Wire HP3 (A24+A25) to fuel pump via fuse box pin 87 (pull OEM fuel pump relay)
- [ ] IGN on → verify 3-second fuel prime, then off
- [ ] Wire HP1 (A1+A13) to starter solenoid (fuse box pin 87 or direct)
- [ ] Press START button (Ch09) → engine cranks; release → stops
- [ ] While running: press START → should NOT engage (RPM interlock)
- [ ] Confirm alternator charging (13.8–14.4V) with engine running

> **✓ TEST:** Engine starts and runs on stock ECU with PDM controlling starter, fuel pump, and alternator field

### 1.17 Test OE Cluster with Haltech

- [ ] Confirm tach signal: Haltech DPO 1 (34-pin pin 18, V/B) → cluster TACHO
- [ ] Confirm speedo: OEM VSS (C109) → cluster + Haltech SPI 1 (26-pin pin 8)
- [ ] Fuel gauge: direct OEM circuit (no ECU involvement) — verify still works
- [ ] Coolant gauge: direct OEM circuit — verify still works

---

## GOAL 2 — Sensors + Seat Bracket + Suspension + Brakes

Mechanical work that can happen concurrently with electrical.

### 2.1 MAP Sensor — Intake Plenum

- [ ] Drill and tap threaded hole in intake plenum (standard boss)
- [ ] Install MAP sensor
- [ ] Connect vacuum tube to plenum
- [ ] Wire MAP → Haltech AVI 9 (34-pin pin 15, Y); power from +8V (pin 12, O/W)
- [ ] Verify MAP reading in NSP at idle vacuum

### 2.2 Install Lowdoller Sensors

**Oil (change oil first):**
- [ ] Drain and change oil
- [ ] Install Lowdoller 150 PSI oil pressure/temp sensor (PN 899404, 1/8" NPT)
- [ ] Wire: Yellow → AVI 3 (34-pin pin 17, O/R), Green → AVI 4 (34-pin pin 2, O/Y)

**Coolant (change coolant, tee with OE sensor):**
- [ ] Full coolant flush (water out, fresh coolant in)
- [ ] Install Lowdoller coolant sensor (LDM899TP100, M12×1.5) on tee with OE coolant temp sender
- [ ] Wire: Yellow → AVI 5 (26-pin pin 20, O/G), Green → AVI 6 (26-pin pin 12, GY/O shielded)

**Fuel:**
- [ ] Install Radium FPR/damper on fuel rail
- [ ] Route 6AN PTFE lines (collect all fittings first)
- [ ] Cut return line and install line tap + Lowdoller fuel sensor (PN 899404, 1/8" NPT)
- [ ] Wire: Yellow → AVI 1 (26-pin pin 13, GY/Y shielded), Green → AVI 2 (34-pin pin 16, O/B)

**Crankcase pressure:**
- [ ] Install crankcase pressure sensor (location TBD — valve cover or PCV port)
- [ ] Wire to available PDM or Haltech input

**All sensors — common wiring:**
- [ ] All red wires → Haltech +5V (34-pin pin 9, O wire)
- [ ] All black + white wires → Haltech signal GND (26-pin pins 14/15/16, B/W)

> **✓ TEST:** All AVIs show 0.5–0.6V resting (zero pressure); temp channels read room temp

### 2.3 Fix Seat Bracket

- [ ] Address Sparco Sprint L mounting / height issue
- [ ] Source correct seat bracket if needed

### 2.4 Front Brakes + Bearings

- [ ] Swap front brake pads
- [ ] Check front wheel bearings for play

---

## GOAL 3 — Haltech Harness Fabrication (Ready for Next Weekend)

Build all harnesses and connectors now so switching from stock ECU → Haltech is just plugging in.

### 3.1 Connectors to Build

**8-pin sensor connector (Lowdoller → Haltech):**
- 6× signal wires (3 pressure + 3 temp from fuel/oil/coolant sensors)
- 2× power/ground (+5V supply, signal GND)

**Injector harness connector:**
- 6× injector signal wires (Haltech INJ1–6)
- 1× PDM power (MP1 → injector rail + Haltech 34-pin pin 26)

**Coil harness connector:**
- 6× coil trigger wires (Haltech IGN1–6)
- 1× PDM power (MP2 → coil Pin D common bus)
- 1× engine ground (coil Pin A common bus)

### 3.2 Make Harnesses

- [ ] **Knock sensor + cam/crank harness** — shielded wiring
  - Knock 1 → 26-pin pin 21 (GY/G)
  - Knock 2 → 26-pin pin 22 (GY/L)
  - Crank trigger +/− → 26-pin pins 1/5 (Y shielded / G shielded)
  - Cam home +/− → 26-pin pins 2/6 (Y shielded / G shielded)
- [ ] **Make coil harness** — Toyota 90919-A2005 ×6
  - Pin B (trigger) → Haltech IGN1–6 (34-pin pins 3–8: Y/B, Y/R, Y/O, Y/G, Y/BR, Y/L)
  - Pin D (power) → common bus from PDM MP2 (A3)
  - Pin A (ground) → common bus to engine block
  - Pin C → leave open
- [ ] **Make injector harness**
  - Injectors 1–6 → Haltech INJ1–6 (34-pin pins 19–22, 27–28: L, L/B, L/BR, L/R, L/O, L/Y)
  - Injector rail 12V → PDM MP1 (A2) + Haltech 34-pin pin 26 (R/L, ECU injector power input)
- [ ] **Coil/injector power connectors** — make inline disconnects so these unplug from stock ECU and plug to Haltech harness
- [ ] **Make sensor harness + 8-pin connector** — consolidates all Lowdoller sensor wires to single connector at Haltech end

### 3.3 Brake Sensor (Leave Ready to Wire)

- [ ] Mount Lowdoller 1500 PSI brake pressure/temp sensor (PN 899405, 1/8" NPT) bracket
- [ ] Leave wires terminated but not connected (AVI 7 + AVI 8 reserved)

### 3.4 Tire Temp Sensor (Mount Bracket)

- [ ] Fabricate/source IR tire temp sensor bracket
- [ ] Wire to PDM channel input

---

## PDM Wiring Summary — Physical Connections

### Engine Bay

| Load | PDM Output | Pin(s) | Notes |
|------|-----------|--------|-------|
| Starter | HP1 | A1 + A13 | Via solenoid; inductive; series diode |
| Fan | HP2 | A12 + A23 | PWM 100Hz; freewheeling diode |
| Fuel Pump | HP3 | A24 + A25 | Via fuse box pin 87; freewheeling diode |
| Injector Power / OE Relay | MP1 | A2 | **Phase 1:** OE relay box pin 87 (pull relay). **Phase 2:** → injector rail + Haltech 34-pin pin 26 |
| Coil Power / OE Relay | MP2 | A3 | **Phase 1:** OE relay box pin 87 (same socket). **Phase 2:** → Pin D all 6 COPs |
| Wiper Low | MP3 | A4 | OEM wiper motor low speed wire |
| Wiper High | MP6 | A7 | OEM wiper motor high speed wire |
| Alternator exciter | LP8 | A21 | D+ field wire cut and routed through LP8; SafeIgnition trigger; < 1A draw |

### Cockpit

| Load | PDM Output | Pin(s) | Notes |
|------|-----------|--------|-------|
| Brake Lights | MP4 | A5 | Always active (Ch11 trigger) |
| Tail Lights | MP5 | A6 | SafeIgnition (always on) |
| Coolsuit | MP7 | A8 | Ch04 AND SafeIgnition |
| Defogger | MP8 | A9 | Ch05 AND SafeIgnition |
| Fuel sender | — | — | OEM direct circuit, no PDM involvement |

### Accessories (SafeIgnition trigger)

| Load | PDM Output | Pin |
|------|-----------|-----|
| ECU Power | LP1 | A14 |
| Dash | LP2 | A15 |
| SmartyCam | LP3 | A16 |
| GPS | LP4 | A17 |
| Wideband | LP5 | A18 |
| Cluster | LP6 | A19 |
| Warning LED | LP7 | A20 |
| AltExciter | LP8 | A21 |

### CAN Buses

| Bus | PDM Pins | Device | Speed |
|-----|----------|--------|-------|
| CAN0 (AIM expansion) | A22 (H) / A11 (L) | Data Hub → GPS, SmartyCam, Podium | 1 Mbps |
| CAN1 (ECU) | A30 (H) / A31 (L) | Haltech Elite 2500 | 500 kbps |
| CAN2 | A28 (H) / A29 (L) | **Unused** — available for future keypad | 125 kbps |

### Switch Panel Inputs

| Switch | PDM Input | Pin | Type |
|--------|----------|-----|------|
| Ignition | IGN input | B23 | Latching toggle, 12V |
| Start | Ch09 | B21 | Momentary, active = GND |
| Fan override | Ch01 | B26 | Latching toggle, 12V |
| Wiper Low | Ch02 | B27 | Latching toggle, 12V |
| Wiper High | Ch03 | B28 | Latching toggle, 12V |
| Coolsuit | Ch04 | B29 | Latching toggle, 12V |
| Defogger | Ch05 | B30 | Latching toggle, 12V |
| Brake switch | Ch11 | A26 | Closed on press |

---

## Haltech Wiring Summary — Sensor + Harness Connections

### Lowdoller Combo Sensors (5-wire each)

| AVI | Signal | Sensor PN | Wire → Pin | Calibration |
|-----|--------|-----------|-----------|-------------|
| AVI 1 | Fuel pressure | 899404 | Yellow → 26-pin pin 13 (GY/Y shld) | PSI = (V−0.5) × 37.5 |
| AVI 2 | Fuel temp | 899404 | Green → 34-pin pin 16 (O/B) | PTC custom table |
| AVI 3 | Oil pressure | 899404 | Yellow → 34-pin pin 17 (O/R) | PSI = (V−0.5) × 37.5 |
| AVI 4 | Oil temp | 899404 | Green → 34-pin pin 2 (O/Y) | PTC custom table |
| AVI 5 | Coolant pressure | LDM899TP100 | Yellow → 26-pin pin 20 (O/G) | PSI = (V−0.5) × 25.0 |
| AVI 6 | Coolant temp | LDM899TP100 | Green → 26-pin pin 12 (GY/O shld) | PTC custom table |
| AVI 7 | Brake pressure | 899405 | *Leave ready* | PSI = (V−0.5) × 375.0 |
| AVI 8 | Brake temp | 899405 | *Leave ready* | PTC custom table |
| AVI 9 | MAP | — | Yellow → 34-pin pin 15 (Y) | Per MAP spec |
| AVI 10 | TPS | OEM | → 34-pin pin 14 (W) | 0–5V |

**+5V supply:** All red wires → 34-pin pin 9 (O, 100mA)
**Signal GND:** All black + white wires → 26-pin pins 14/15/16 (B/W)

### Coil Harness (Toyota 90919-A2005 ×6)

| Coil | Haltech IGN | Pin | Wire Color |
|------|------------|-----|------------|
| Cyl 1 | IGN 1 | 34-pin pin 3 | Y/B |
| Cyl 2 | IGN 2 | 34-pin pin 4 | Y/R |
| Cyl 3 | IGN 3 | 34-pin pin 5 | Y/O |
| Cyl 4 | IGN 4 | 34-pin pin 6 | Y/G |
| Cyl 5 | IGN 5 | 34-pin pin 7 | Y/BR |
| Cyl 6 | IGN 6 | 34-pin pin 8 | Y/L |

Power: PDM MP2 (A3) → Pin D common bus
Ground: Pin A → engine block

### Injector Harness

| Injector | Haltech INJ | Pin | Wire Color |
|----------|------------|-----|------------|
| Cyl 1 | INJ 1 | 34-pin pin 19 | L |
| Cyl 2 | INJ 2 | 34-pin pin 20 | L/B |
| Cyl 3 | INJ 3 | 34-pin pin 21 | L/BR |
| Cyl 4 | INJ 4 | 34-pin pin 22 | L/R |
| Cyl 5 | INJ 5 | 34-pin pin 27 | L/O |
| Cyl 6 | INJ 6 | 34-pin pin 28 | L/Y |

Power: PDM MP1 (A2) → injector rail + Haltech 34-pin pin 26 (R/L)

### ECU Sensitive Bundle (Shielded)

| Signal | Haltech Pin | Wire |
|--------|------------|------|
| Crank trigger + | 26-pin pin 1 | Y (shielded) |
| Crank trigger − | 26-pin pin 5 | G (shielded) |
| Cam home + | 26-pin pin 2 | Y (shielded) |
| Cam home − | 26-pin pin 6 | G (shielded) |
| Knock 1 | 26-pin pin 21 | GY/G |
| Knock 2 | 26-pin pin 22 | GY/L |

---

## NEXT WEEKEND — Haltech Takes Over Engine

After track day with stock ECU + PDM, switch to Haltech running the engine:

- [ ] Disconnect stock ECU injector wiring → plug in Haltech injector harness
- [ ] Disconnect stock ECU coil wiring → plug in Haltech coil harness
- [ ] Move crank/cam/TPS to Haltech (bench-confirmed)
- [ ] Power Haltech ECU from PDM LP1 (A14) — disconnect stock ECU power
- [ ] First fire on Haltech — base tune, confirm idle
- [ ] Verify all PDM tests still pass with Haltech running
- [ ] Connect wideband to Haltech AVI for closed-loop AFR

---

## LATER / ONGOING

- [ ] Rubber-mount ECU and PDM plate (vibration isolation)
- [ ] Clean and label all harnesses
- [ ] Harness routing: confirm no chafing on steering/suspension movement
- [ ] Source correct Sparco seat bracket (Sprint L height issue)
- [ ] Configure PodiumConnect telemetry channels for race engineer
