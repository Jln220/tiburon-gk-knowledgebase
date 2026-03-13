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
| Kill switch | Mounted left of steering wheel, 2 AWG cable run |
| Seat panel | Needs welding (~3 hrs) — **must do before electronics install** |

**Removed from this weekend:** Suspension (coilovers → fab shop Wednesday), front brakes + bearings (fab shop).

---

## FRIDAY AT HOME — Race Studio Config (Workday)

PDM at home with laptop. All software work — no car needed.

### F.1 Finalize PDM Configuration

- [ ] Open Race Studio 3, load `Tiburon_White_v1_base.zconfig`
- [ ] Configure all power outputs per `guides/pdm-config.md`:
  - HP1–HP3 (starter, fan, fuel pump)
  - MP1–MP8 (injector/coil pwr, wiper low/high, brake/tail lights, coolsuit, defogger)
  - LP1–LP8 (ECU, dash, SmartyCam, GPS, wideband, cluster, warning LED, alt exciter)
- [ ] Configure status variables: ENGINE_RUNNING, FUEL_PRIME, FAN_TEMP bands (77/82/87/92°C), FAN_FAILSAFE, STARTER_SAFE, MULTI_WARNING
- [ ] Configure wiper priority logic: MP3 = Ch02 AND NOT Ch03; MP6 = Ch03
- [ ] Configure channel inputs: Ch01–Ch05 (toggles), Ch09 (starter), Ch11 (brake)
- [ ] Disable CAN2 keypad, remove all `*KYD` status variables
- [ ] Configure ECU Stream tab: Haltech CAN_V2_40 protocol on CAN1 (A30/A31), 500 kbps
  - Enable channels: RPM, ECT, Oil P, Oil T, Fuel P, TPS, Vehicle Speed, Battery V
- [ ] Configure SmartyCam Stream: RPM, Speed (GPS-08), Gear, Coolant Temp, Oil P, TPS, Lat G, Long G
- [ ] Transmit config to PDM via USB

> **✓ TEST:** Force-test each output in Race Studio Live Measures (no loads — just verify logic triggers)

### F.2 Prep Work (While Config Compiles/Transmits)

- [ ] Label all PDM harness wires with destination (use wiring summary tables below)
- [ ] Inventory parts: breakers (150A, 120A), spade connectors, ring terminals, wire (2/4/14/18 AWG)
- [ ] Inventory sensors: Lowdoller fuel/oil/coolant, MAP, wideband O2 bung
- [ ] Pack laptop + USB cable for shop

---

## FRIDAY EVENING — Welding + Mechanical Prep (Shop, 5pm+)

**Welding first — sparks and heat cannot coexist with electronics.** Do all hot work before any electronics go near the car.

### FE.1 Weld Seat Panel (~3 hours)

- [ ] Remove seat and loose interior trim from passenger footwell area
- [ ] Weld in floor panel for seat mount
- [ ] Grind and finish welds
- [ ] Clean area thoroughly (metal shavings, sparks, slag)

### FE.2 Mechanical Prep (While Panel Cools / After Welding)

- [ ] Test-fit electronics mounting plate in passenger footwell — mark bolt holes
- [ ] Drill mounting holes in plate and floor (if not using adhesive/rivets)
- [ ] Drain oil for oil sensor install tomorrow (let it drain overnight = cleaner)
- [ ] Prep oil sensor port: verify 1/8" NPT thread, have Teflon tape ready
- [ ] Lay out PDM harness along planned routes (engine bay through firewall, cockpit runs)

---

## SATURDAY — PDM Install + Power System (Shop, All Day)

**Goal by end of Saturday:** PDM installed, powered, all switches working, car starts and runs on stock ECU with PDM controlling starter, fuel pump, and alternator exciter.

### S.1 Install Electronics Mounting Plate (First Thing)

All electronics on a single plate in passenger footwell: PDM, Haltech Elite 2500, Podium Micro (SN: 1QTV5KM), Innovate LM2.

- [ ] Bolt/rivet mounting plate into passenger footwell
- [ ] Mount PDM on plate (vibration-isolated)
- [ ] Mount Haltech Elite 2500 on plate
- [ ] Mount Podium Micro on plate
- [ ] Mount Innovate LM2 on plate

### S.2 Kill Switch Wiring

Kill switch already mounted. 2 AWG cable already run from battery (+) to large terminal A.

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
- [ ] Wire small terminal B → IGN toggle switch (new)
- [ ] Connect PDM Surlok power cable
- [ ] Connect PDM grounds (B13, B14, B18 to chassis)

### S.3 Switch Panel + IGN Wiring

- [ ] Wire IGN toggle → PDM Conn B pin 23 AND splice to Haltech 34-pin pin 13 (P wire)
- [ ] Wire start button → Ch09 (B21), momentary, active = GND
- [ ] Wire fan override toggle → Ch01 (B26), active = 12V
- [ ] Wire wiper low toggle → Ch02 (B27), active = 12V
- [ ] Wire wiper high toggle → Ch03 (B28), active = 12V
- [ ] Wire coolsuit toggle → Ch04 (B29), active = 12V
- [ ] Wire defogger toggle → Ch05 (B30), active = 12V
- [ ] Wire brake light switch → Ch11 (A26), closed on press
- [ ] Wire warning LED → LP7 (A20)

### S.4 First Power-Up in Car

- [ ] Kill switch ON, IGN toggle ON → PDM powers up
- [ ] Connect laptop USB → Race Studio Live Data
- [ ] Verify `SafeIgnition` = 1
- [ ] Flip each toggle → verify correct channel input activates in Live Data
- [ ] Press START button → verify `STARTER_SAFE` logic (should activate with ENGINE_RUNNING = 0)
- [ ] IGN toggle OFF → verify `SafeIgnition` = 0, all outputs drop
- [ ] Kill switch OFF → verify total power loss

> **✓ GATE:** All switches verified before connecting any loads.

### S.5 Dash + LVDS

- [ ] Mount AIM 10" dash (visible from driver position)
- [ ] Connect LVDS cable from PDM to dash
- [ ] Verify dash powers up and shows live data

### S.6 PDM → Fuse Box Connections (Engine Bay)

**OE Main Relay (MP1/MP2):**
- [ ] Locate OE main relay in underhood fuse box
- [ ] Pull the OE main relay
- [ ] Insert PDM MP1 (A2) wire into relay socket pin 87 (power out)
- [ ] Insert PDM MP2 (A3) wire into same pin 87 socket (parallel)
- [ ] IGN on → verify stock ECU powers up via PDM; IGN off → stock ECU loses power

> **Phase 2 switchover:** Disconnect MP1/MP2 from relay socket. Reroute MP1 → injector rail + Haltech 34-pin pin 26 (R/L). Reroute MP2 → COP coil Pin D common bus. No Race Studio config change.

**Fuel Pump Relay (HP3):**
- [ ] Pull OEM fuel pump relay
- [ ] Insert PDM HP3 (A24+A25) wire into pin 87 socket
- [ ] IGN on → verify 3-second fuel prime (listen for pump), then off
- [ ] Verify in Race Studio: `FUEL_PRIME` timer fires, `FuelSV` active → inactive

**Starter (HP1):**
- [ ] Wire HP1 (A1+A13) to starter — fuse box pin 87 (try first) or direct to solenoid S terminal
- [ ] Press START button (Ch09) → engine cranks; release → stops
- [ ] While engine running: press START → should NOT engage (RPM interlock)

### S.7 Alternator Exciter (LP8)

- [ ] Locate OEM alternator D+ exciter wire (thin ~18 AWG at alternator Yazaki connector)
- [ ] Cut exciter wire at convenient point near fuse box (leave length on both ends)
- [ ] Fuse box side → wire to PDM LP8 (A21, Connector A)
- [ ] Alternator D+ side → remains connected to alternator (load side)

### S.8 CAN0 Expansion Bus — AIM Devices

- [ ] Verify CAN0 expansion cable: A22 (H) / A11 (L) / A33 (+Vb out) / A10 (GND)
- [ ] Connect AIM CAN Data Hub (4-way) to expansion cable Binder
- [ ] Daisy-chain: PDM → Data Hub → GPS-08 → SmartyCam → Podium Micro
- [ ] Power all devices via A33 (+Vb out CAN)
- [ ] Mount GPS-08 (roof or cowl — clear sky view)
- [ ] Mount SmartyCam (windshield or roll bar bracket)
- [ ] Verify GPS position lock in Race Studio Live Data
- [ ] Verify SmartyCam recording on power-up
- [ ] Verify Podium Micro recognized in Race Studio

### S.9 Full System Test — Start Car on Stock ECU

- [ ] IGN on → fuel prime (3s) → pump off
- [ ] Press START → engine cranks and starts
- [ ] Verify engine running: `ENGINE_RUNNING` = 1 in Race Studio
- [ ] Verify starter interlock: press START while running → no crank
- [ ] Verify alternator charging: 13.8–14.4V at battery posts
- [ ] Verify fan toggle (Ch01) → HP2 at 98%
- [ ] Verify wiper low (Ch02) → MP3 on; wiper high (Ch03) → MP6 on, MP3 off
- [ ] Verify coolsuit (Ch04) → MP7 on
- [ ] Verify defogger (Ch05) → MP8 on
- [ ] Verify brake lights (Ch11) → MP4 on (test with IGN off too)
- [ ] Verify tail lights → MP5 on with IGN (automatic)
- [ ] **Kill switch test:** engine running → flip kill switch → engine dies, all power drops, alternator stops charging

> **✓ GATE:** Car starts, runs, and stops reliably on stock ECU with PDM. Kill switch kills everything.

---

## SUNDAY — Sensors + Haltech Wiring + Harnesses (Shop, All Day)

**Goal by end of Sunday:** All Lowdoller sensors installed and reading, Haltech CAN data flowing to PDM, coil/injector harnesses built and ready to plug in.

### SU.1 Oil Sensor Install (Oil Already Drained Friday)

- [ ] Install Lowdoller 150 PSI oil pressure/temp sensor (PN 899404, 1/8" NPT)
- [ ] Refill oil, check for leaks
- [ ] Wire: Yellow → AVI 3 (34-pin pin 17, O/R), Green → AVI 4 (34-pin pin 2, O/Y)

### SU.2 Coolant Sensor Install

- [ ] Full coolant flush (water out, fresh coolant in)
- [ ] Install Lowdoller coolant sensor (LDM899TP100, M12×1.5) on tee with OE coolant temp sender
- [ ] Wire: Yellow → AVI 5 (26-pin pin 20, O/G), Green → AVI 6 (26-pin pin 12, GY/O shielded)

### SU.3 Fuel System + Fuel Sensor

- [ ] Install Radium FPR/damper on fuel rail
- [ ] Route 6AN PTFE lines (collect all fittings first)
- [ ] Cut return line and install line tap + Lowdoller fuel sensor (PN 899404, 1/8" NPT)
- [ ] Wire: Yellow → AVI 1 (26-pin pin 13, GY/Y shielded), Green → AVI 2 (34-pin pin 16, O/B)

### SU.4 MAP Sensor

- [ ] Drill and tap threaded hole in intake plenum (standard boss)
- [ ] Install MAP sensor
- [ ] Connect vacuum tube to plenum
- [ ] Wire MAP → Haltech AVI 9 (34-pin pin 15, Y); power from +8V (pin 12, O/W)

### SU.5 Sensor Common Wiring

- [ ] All red wires → Haltech +5V (34-pin pin 9, O wire)
- [ ] All black + white wires → Haltech signal GND (26-pin pins 14/15/16, B/W)

> **✓ TEST:** All AVIs show 0.5–0.6V resting (zero pressure); temp channels read room temp

### SU.6 Haltech CAN1 → PDM

- [ ] Connect Haltech 26-pin pins 23/24 (CAN H/L) → PDM A30/A31 (CAN1)
- [ ] Power Haltech from PDM LP1 (A14)
- [ ] Verify Haltech CAN_V2_40 protocol active — all enabled channels visible in Race Studio Live Data
- [ ] Confirm fan temp bands react to live coolant temp on CAN
- [ ] Confirm warning LED (LP7) triggers when sensor thresholds crossed (force values in NSP)
- [ ] Verify MAP reading in NSP at idle vacuum

> **✓ TEST:** Start car → RPM > 50 → `ENGINE_RUNNING` activates → fuel pump stays on → all CAN sensor data flowing

### SU.7 Wideband AFR

- [ ] Wire LM2 power → PDM LP5 (A18) — already mounted on plate Saturday
- [ ] Wire LM2 analog output → available Haltech AVI
- [ ] Install wideband O2 sensor bung in exhaust (weld if not already in place)
- [ ] Install O2 sensor
- [ ] Verify AFR reading in Haltech NSP and on AIM dash

### SU.8 OE Cluster Verification

- [ ] Confirm tach signal: Haltech DPO 1 (34-pin pin 18, V/B) → cluster TACHO
- [ ] Confirm speedo: OEM VSS (C109) → cluster + Haltech SPI 1 (26-pin pin 8)
- [ ] Fuel gauge: direct OEM circuit (no ECU involvement) — verify still works
- [ ] Coolant gauge: direct OEM circuit — verify still works

### SU.9 Harness Fabrication (Prep for Haltech Switchover)

Build all harnesses now so switching from stock ECU → Haltech is just plugging in.

**Knock + cam/crank harness (shielded):**
- [ ] Knock 1 → 26-pin pin 21 (GY/G)
- [ ] Knock 2 → 26-pin pin 22 (GY/L)
- [ ] Crank trigger +/− → 26-pin pins 1/5 (Y shielded / G shielded)
- [ ] Cam home +/− → 26-pin pins 2/6 (Y shielded / G shielded)

**Coil harness (Toyota 90919-A2005 ×6):**
- [ ] Pin B (trigger) → Haltech IGN1–6 (34-pin pins 3–8: Y/B, Y/R, Y/O, Y/G, Y/BR, Y/L)
- [ ] Pin D (power) → common bus from PDM MP2 (A3)
- [ ] Pin A (ground) → common bus to engine block
- [ ] Pin C → leave open

**Injector harness:**
- [ ] Injectors 1–6 → Haltech INJ1–6 (34-pin pins 19–22, 27–28: L, L/B, L/BR, L/R, L/O, L/Y)
- [ ] Injector rail 12V → PDM MP1 (A2) + Haltech 34-pin pin 26 (R/L, ECU injector power input)

**Inline disconnects:**
- [ ] Make coil/injector power connectors — inline disconnects so these unplug from stock ECU and plug to Haltech harness

**Sensor harness:**
- [ ] Make sensor harness + 8-pin connector — consolidates all Lowdoller sensor wires to single connector at Haltech end

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
- [ ] Reroute MP1 from OE relay pin 87 → injector rail + Haltech 34-pin pin 26
- [ ] Reroute MP2 from OE relay pin 87 → COP Pin D common bus
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
- [ ] Configure PodiumConnect telemetry channels for race engineer
- [ ] Mount Lowdoller 1500 PSI brake sensor bracket (leave wires terminated, AVI 7+8 reserved)
- [ ] Crankcase pressure sensor (valve cover or PCV port → available PDM/Haltech input)
- [ ] IR tire temp sensor bracket + PDM channel input wiring
