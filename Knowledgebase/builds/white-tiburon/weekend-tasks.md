# White Tiburon — Build Procedure
## Haltech + AIM PDM Integration | Phase-Based with Test Gates

---

## Current State (March 2026)

| System | Status |
|--------|--------|
| Haltech bench setup | Cam ✅ Crank ✅ — Knock: **next** |
| Toyota COP coil (90919-A2005) | **Bench tested with Haltech ✅ — firing confirmed** |
| PDM Race Studio config | Base map loaded; keypad, outputs, triggers configured |
| PDM car connection | Spade connectors → fuse box pin 87 (alongside stock ECU — non-destructive) |
| CAN Keypad 12 | Connected to PDM CAN2 at 125 kbps |
| Stock ECU | Connected and running — **do NOT disturb until Phase 3** |

**Rule:** Complete each phase and pass its TEST before moving to the next. Do not skip tests to save time — we are trying to avoid redoing work.

---

## PHASE 0 — Haltech Bench Tests
*ECU on bench with spare sensors. Complete before any car work.*

### P0.1 Knock Sensors
- [ ] Wire knock sensor 1 → Haltech 26-pin pin 21 (GY/G)
- [ ] Wire knock sensor 2 → Haltech 26-pin pin 22 (GY/L)
- [ ] In NSP: confirm knock channels show signal (noise floor OK; just needs ADC activity — no "no signal" fault)

> **✓ TEST P0.1:** NSP knock channels show activity (noise floor), no sensor fault

### P0.2 Lowdoller Sensor Signals
- [ ] Bench-power all sensors (+5V from 34-pin pin 9, GND to signal ground)
- [ ] Measure yellow wire at each AVI input: expect ~0.5V at zero pressure
- [ ] Confirm all AVI 1–8 reading in NSP with expected resting voltage

> **✓ TEST P0.2:** All AVIs show 0.5–0.6V resting (zero pressure); green-temp channels read room temp (~1.8–2.2V on PTC table)

### P0.3 CAN Data Broadcast → PDM
- [ ] Connect Haltech 26-pin pins 23/24 (CAN H/L) → PDM CAN0 (A22/A11)
- [ ] Power both units; open Race Studio 3 → Live Data
- [ ] Confirm PDM receives: RPM, Coolant Temp, Oil Pressure, Oil Temp, Fuel Pressure, TPS
- [ ] Simulate RPM > 50 in NSP (bench) → confirm `ENGINE_RUNNING` var activates in Race Studio

> **✓ TEST P0.3:** All 6 CAN channels visible with valid values in Race Studio Live Data

---

## PHASE 1 — PDM Logic Tests (Stock ECU Running)
*PDM powered via fuse box pin 87 spade connectors. Stock ECU manages engine. Work from outside — no irreversible changes yet.*

### P1.1 PDM Power-Up Sequence
- [ ] Turn ignition switch (PDM B23) ON
- [ ] Confirm `SafeIgnition` = active in Race Studio Live Data
- [ ] Confirm LP1–LP6 outputs come on (ECU, dash, SmartyCam, GPS, wideband, cluster)
- [ ] Confirm CAN keypad LEDs illuminate with correct base colors

> **✓ TEST P1.1:** All IGN-gated outputs active; keypad shows correct resting LED colors; no faults

### P1.2 CAN Keypad — All Buttons
Work through each key. Watch status variable in Race Studio Live Data.

| Key | Expected | Pass? |
|-----|----------|-------|
| 01 Start | `StarterKYD` latches on | |
| 02 Horn | `SirenKYD` on while held, off on release | |
| 03 Lights | `LightsKYD` toggles; MP5 (A6) state follows | |
| 04 Coolsuit | `CoolsuitKYD` toggles; MP7 (A8) state follows | |
| 05 Fan+ | `FanKYD` override; HP2 duty jumps to 98% | |
| 06 Fuel+ | `FuelOverride` on; HP3 runs | |
| 07 Pit | `PITLIMITER_SAFE` only active if speed < 60 mph | |
| 08 Wiper | Wiper output activates | |
| 09 Yes/No | `COMMS_YN` toggles green LED | |
| 10 Pit# | `PITIN_LAPS` cycles 0→1→2→3→0; LED brightness increases | |
| Backup Ch09 | `StarterKYD` also activates (OR logic) | |

> **✓ TEST P1.2:** All 10 keys trigger correct status vars; LED colors match config; no spurious outputs

### P1.3 Fuel Pump Logic
- [ ] Confirm fuel pump wired to HP3 (A24+A25)
- [ ] Cycle ignition switch ON → verify 3-second prime (pump on then off)
- [ ] With engine running (stock ECU): confirm HP3 stays on (RPM > 50 via CAN)
- [ ] Key 06 (Fuel Override) on → pump runs regardless of RPM
- [ ] Turn ignition off → pump stops within 2s

> **✓ TEST P1.3:** 3s prime confirmed; pump tracks RPM; Key 06 override works; pump stops on IGN off

### P1.4 Fan PWM Logic
- [ ] Confirm fan wired to HP2 (A12+A23)
- [ ] In Race Studio: inject simulated ECT via CAN
  - 82°C → HP2 = 25% duty
  - 87°C → 50%
  - 92°C → 75%
  - 96°C → 98%
- [ ] Key 05 (Fan Override) → HP2 immediately jumps to 98%
- [ ] Failsafe: disconnect Haltech CAN → after 5s, HP2 = 98%

> **✓ TEST P1.4:** All 4 temp bands confirmed; manual override confirmed; loss-of-CAN failsafe confirmed

### P1.5 Warning LED Logic
- [ ] Confirm warning LED wired to LP7 (A20)
- [ ] Force CAN oil pressure < 15 PSI → LED activates
- [ ] Force CAN ECT > 105°C → LED activates
- [ ] Force CAN oil temp > 130°C → LED activates
- [ ] Force CAN fuel pressure < 30 PSI → LED activates
- [ ] With RPM < 500: confirm all alarms suppressed (RPM guard active)

> **✓ TEST P1.5:** LED triggers on each condition independently; suppressed below 500 RPM

### P1.6 Start Car — PDM Controls Starter, Stock ECU Runs Engine
⚠️ **Prerequisite:** HP1 (A1+A13) wired to starter solenoid. Stock ECU and injectors connected normally.

- [ ] Wire HP1 to starter solenoid (insert in-line with or replace stock IGN switch starter line)
- [ ] Confirm `STARTER_SAFE`: Key 01 AND IGN on AND RPM < 50
- [ ] Crank with Key 01: engine should start; stock ECU takes over
- [ ] While running: press Key 01 → HP1 should NOT activate (RPM interlock)
- [ ] Test backup Ch09 button: same behavior as Key 01
- [ ] **Start engine** and confirm normal operation with stock ECU

> **✓ TEST P1.6:** Engine starts via Key 01 and physical backup; RPM interlock blocks re-engagement while running

### P1.7 Alternator Exciter via PDM
Cut the OEM alternator exciter wire from the stock ignition circuit and route through a PDM output.

- [ ] Locate OEM alternator exciter wire (IG or D+ terminal on alternator, thin wire ~18 AWG)
- [ ] Cut this wire from stock ignition source
- [ ] Wire one end to a PDM spare mid-power output (use **MP6, A7**) and the other end to alternator D+
- [ ] Configure MP6 in Race Studio: trigger = `SafeIgnition`, continuous, max 5A
- [ ] Start engine → confirm battery voltage rises to 13.8–14.4V
- [ ] Turn ignition off → confirm voltage drops (field collapses, charging stops)

> **✓ TEST P1.7:** Voltmeter reads 13.8–14.4V charging; voltage drops when IGN switch off

### P1.8 Brake Lights
- [ ] Wire brake light switch → Ch11 (Conn B pin 28)
- [ ] Wire brake lights → MP4 (A5)
- [ ] Press brake pedal with ignition off → MP4 activates immediately
- [ ] Confirm independence from keypad (brake lights work regardless of keypad state)

> **✓ TEST P1.8:** Brake lights work with ignition off; instant response

---

## PHASE 2 — Engine Bay Mechanical
*Can be done concurrently with Phase 1 if second person available. No Phase dependencies except sensors go in before Phase 3.*

### P2.1 Oil Change + Oil Sensor
- [ ] Drain and change oil
- [ ] Install Lowdoller 150 PSI oil pressure/temp sensor (PN 899404, 1/8" NPT)
- [ ] Wire: Yellow → AVI 3 (34-pin pin 17, O/R), Green → AVI 4 (34-pin pin 2, O/Y), Red → +5V (pin 9), Black+White → signal GND

### P2.2 Coolant Flush + Coolant Sensor
- [ ] Full coolant flush (water out, fresh coolant in)
- [ ] Install Lowdoller coolant pressure/temp sensor (LDM899TP100, M12×1.5)
- [ ] Wire: Yellow → AVI 5 (26-pin pin 20, O/G), Green → AVI 6 (26-pin pin 12, GY/O shld)
- [ ] Confirm thread fits manifold fitting before final torque

### P2.3 Fuel System — Radium FPR + Fuel Sensor
- [ ] Install Radium FPR/damper on fuel rail
- [ ] Route 6AN PTFE lines (collect all fittings before starting)
- [ ] Install line tap + Lowdoller 150 PSI fuel pressure/temp sensor on return line (1/8" NPT)
- [ ] Wire: Yellow → AVI 1 (26-pin pin 13, GY/Y shld), Green → AVI 2 (34-pin pin 16, O/B)

### P2.4 MAP Sensor
- [ ] Drill and tap intake plenum for MAP sensor (standard boss)
- [ ] Optional: polish plenum interior while accessible
- [ ] Wire MAP → AVI 9 (34-pin pin 15, Y); +8V power from pin 12 (O/W, orange/white)

### P2.5 COP Install (Toyota 90919-A2005 ×6)
- [ ] Test physical fitment on valve covers
- [ ] Confirm cylinder-to-coil assignment for G6BA firing order
- [ ] Wire coils: Pin B (trigger) → Haltech IGN1–6 (34-pin pins 3–8); Pin D (power) → PDM MP2 (A3); Pin A → engine block GND; Pin C → leave open
- Reference: `hardware/sensors/cop-ignition.md`

### P2.6 Front Brakes + Bearings
- [ ] Swap front brake pads
- [ ] Check front wheel bearings for play

### P2.7 Decked Engine Upper Oil Pan
- [ ] Clean mating surface; install upper oil pan on the milled-heads Build 1 engine
- See `builds/white-tiburon/build-profile.md`

---

## PHASE 3 — Full Haltech Integration
*Only after Phase 0 and Phase 1 fully tested. This is the point of no return — stock ECU goes offline.*

- [ ] Move injector wiring from stock ECU → Haltech INJ1–6 (34-pin pins 19–22, 27–28)
- [ ] Move COP trigger wires → Haltech IGN1–6 (already bench-confirmed in P0.x)
- [ ] Move crank/cam to Haltech (bench-confirmed); remove from stock ECU
- [ ] Move TPS wiring → Haltech AVI 10 (34-pin pin 14, W)
- [ ] Power Haltech ECU from PDM LP1 (A14) — disconnect stock ECU power
- [ ] Reconnect IGN switch output → Haltech 34-pin pin 13 (P, purple) in addition to PDM B23
- [ ] **First fire on Haltech** — base tune, confirm idle
- [ ] Verify all Phase 1 tests still pass with Haltech running
- [ ] Connect wideband (Innovate LM2) → available Haltech AVI; power from PDM LP5 (A18)

---

## PHASE 4 — Data/Telemetry System

- [ ] Mount and configure AIM SmartyCam (LP3 power A16, CAN1 daisy-chain)
- [ ] Mount and configure AIM Podium telemetry (LP4 is GPS, confirm Podium power separately)
- [ ] Mount AIM GPS module (CAN1 bus)
- [ ] Confirm full CAN chain: Haltech → PDM → Dash → SmartyCam → GPS → Podium
- [ ] Set up dash pages on AIM 10" display
- [ ] Configure PodiumConnect channels: verify K09/K10 comms buttons trigger visible flags in PodiumConnect
- [ ] Configure video data overlay on SmartyCam

---

## LATER / ONGOING

- [ ] Source correct Sparco seat bracket (Sprint L height issue — see white-tiburon.md)
- [ ] Rubber-mount ECU and PDM plate (vibration isolation)
- [ ] Clean and label harness after Phase 3 integration
- [ ] Harness routing: confirm no chafing on steering/suspension movement

---

## 5. WIRING BUNDLES — Master Reference

These define the logical groupings for how PDM, Haltech, and loads are connected.

### 5a. PDM Physical Inputs (2 only)

| Input | PDM Pin | Type | Notes |
|-------|---------|------|-------|
| **Ignition switch** | Conn B pin 23 | Latching toggle | Keeps PDM powered for engine-off accessories; master IGN state (`SafeIgnition`). Also spliced to Haltech 34-pin pin 13 (P) for ECU IGN enable. |
| **Start button (backup)** | Ch09 — Conn B pin 21 | Momentary | Physical redundancy for CAN keypad Key 01 |
| **Brake light switch** | Ch11 — Conn B pin 28 | Momentary (direct) | Always active; wired independent of keypad |

All other controls (horn, lights, fan, wiper, coolsuit, fuel override) → **AIM CAN Keypad 12 (CAN2, 125 kbps)**. No physical switches for these functions.

### 5b. PDM Cabin Bundle
| Load | PDM Output | Notes |
|------|-----------|-------|
| Coolsuit pump | PDM 12V | Simple on/off |
| Wipers | PDM 12V | Switched from cockpit |

### 5c. PDM Engine Bundle
| Load | PDM Output | Notes |
|------|-----------|-------|
| Starter | PDM 12V | Momentary, high current |
| Alternator field | PDM 12V | |
| Cooling fan(s) | PDM 12V | Haltech DPO trigger or temp-based PDM logic |
| Headlights | PDM 12V | From cockpit switch |
| Horn | PDM 12V | From cockpit switch |

### 5d. Fuel Pump Bundle
| Signal | Device | Pin/Wire | Notes |
|--------|--------|----------|-------|
| 12V power | PDM output | — | PDM provides switched 12V to pump |
| Trigger/control | Haltech DPO 5 | 34-pin pin 24, B/Y wire | Fuel pump trigger (ground-side) |

**Haltech fuse block:** Fuse 4 = 20A fuel pump

### 5e. Injector Bundle
| Signal | Device | Pin/Wire | Notes |
|--------|--------|----------|-------|
| 12V power | PDM output | — | 12V to injector rail common |
| Injector #1 | Haltech INJ 1 | L wire | Ground-side drive, 1A max |
| Injector #2 | Haltech INJ 2 | L/B wire | |
| Injector #3 | Haltech INJ 3 | L/BR wire | |
| Injector #4 | Haltech INJ 4 | L/R wire | |
| Injector #5 | Haltech INJ 5 | L/O wire | |
| Injector #6 | Haltech INJ 6 | L/Y wire | |

**Haltech fuse block:** Fuse 2 = 20A injection
**Haltech note:** ECU injector power input required — pin 26 (R/L) on 34-pin, 12V from injector power relay

### 5f. Coil Bundle
| Signal | Device | Pin/Wire | Notes |
|--------|--------|----------|-------|
| 12V power | PDM output | — | 12V to coil common |
| Ignition #1 | Haltech IGN 1 | Y/B wire | Ground-side drive |
| Ignition #2 | Haltech IGN 2 | Y/R wire | |
| Ignition #3 | Haltech IGN 3 | Y/O wire | |
| Ignition #4 | Haltech IGN 4 | Y/G wire | (available if COP) |
| Ignition #5 | Haltech IGN 5 | Y/BR wire | (available if COP) |
| Ignition #6 | Haltech IGN 6 | Y/L wire | (available if COP) |

**Haltech fuse block:** Fuse 3 = 15A ignition
**Note:** COP confirmed — Toyota 90919-A2005 ×6, sequential COP, all 6 ignition outputs active. See `hardware/sensors/cop-ignition.md`.

### 5g. ECU Sensitive Bundle (Shielded Wiring)
| Signal | Haltech Pin | Wire | Notes |
|--------|------------|------|-------|
| Crank (trigger +) | 26-pin A1 | Y (shielded) | Hall or reluctor |
| Crank (trigger −) | 26-pin A5 | G (shielded) | Ground ref for reluctor |
| Cam (home +) | 26-pin A2 | Y (shielded) | Hall or reluctor |
| Cam (home −) | 26-pin A6 | G (shielded) | Ground ref for reluctor |
| Knock 1 | 26-pin A21 | GY/G | Piezoelectric |
| Knock 2 | 26-pin A22 | GY/L | Piezoelectric |

**Stock sensor reference (OpenGK):**
- CKP: Hyundai 39180-37150 / NTK EH0220
- CMP: Hyundai 39350-37100 / NTK EC0145
- Both are Hall effect type on 2.7L V6

### 5h. ECU Analog Bundle — Lowdoller Combo Sensors

Full specs & calibration: `hardware/sensors/lowdoller-sensors.md`

All Lowdoller sensors: 5-wire (Red=+5V, Black=pressure GND, Yellow=pressure signal, White=temp GND, Green=temp signal)

**5V Supply: 34-pin pin 9 (O, orange) = +5V DC, 100mA.** Already tested and configured in NSP.

| AVI | Assignment | Sensor PN | Wire→AVI | Calibration | Thread |
|-----|-----------|-----------|----------|-------------|--------|
| 1 | Fuel pressure | 899404 | Yellow | PSI = (V−0.5) × 37.5 [0–150] | 1/8" NPT |
| 2 | Fuel temp | 899404 | Green | PTC custom table (see below) | — |
| 3 | Oil pressure | 899404 | Yellow | PSI = (V−0.5) × 37.5 [0–150] | 1/8" NPT |
| 4 | Oil temp | 899404 | Green | PTC custom table | — |
| 5 | Coolant pressure | LDM899TP100 | Yellow | PSI = (V−0.5) × 25.0 [0–100] | M12×1.5 |
| 6 | Coolant temp | LDM899TP100 | Green | PTC custom table | — |
| 7 | Brake pressure | 899405 | Yellow | PSI = (V−0.5) × 375.0 [0–1500] | 1/8" NPT |
| 8 | Brake temp | 899405 | Green | PTC custom table | — |
| **9** | **MAP sensor** | — | — | Per MAP spec | — |
| 10 | Spare / Trans | 899404? | — | If trans, same as fuel/oil | 1/8" NPT |

**Grounds:** All black + white wires → Haltech signal ground pins A14–A16 (B/W) on 26-pin.

**Temp calibration (PTC — all sensors identical):**
`-40°F=84.27Ω, 32°F=100Ω, 104°F=115.54Ω, 212°F=138.51Ω, 320°F=161.05Ω, 500°F=197.71Ω`
**Note:** These are PTC (resistance goes UP with temp) — unusual for automotive. Already configured as custom cal table in NSP.

**Products:**
- 150 PSI (fuel/oil/trans): https://lowdoller-motorsports.com/collections/combo-pressure-and-temp-sensors/products/150-psi-pressure-temperature-combo-150-psi-500-f-pn-899404
- 100 PSI coolant (M12×1.5): https://lowdoller-motorsports.com/collections/combo-pressure-and-temp-sensors/products/m12-x-1-5-coolant-pressure-temperature-combo-100-psi-500-f
- 1500 PSI brake: https://lowdoller-motorsports.com/collections/combo-pressure-and-temp-sensors/products/brake-pressure-temperature-combo-1500-psi-500-f-pn-899405

---

## 6. AIM PDM 32 — Finalized Output/Input Assignments

> Full Race Studio 3 configuration (status variables, trigger logic, protection settings, LED colors) → `builds/white-tiburon/pdm/config-guide.md`; step-by-step walkthrough → `builds/white-tiburon/pdm/session-1.md`

### Physical Inputs to Wire
- [ ] **Conn B pin 23** — Ignition latching toggle switch (master IGN / `SafeIgnition`) — also splice to Haltech 34-pin pin 13 (P)
- [ ] **Ch09 (B21)** — Backup start pushbutton (momentary, active = GND)
- [ ] **Ch11 (B28)** — Brake light switch (momentary, closed on press)

### CAN Bus Devices to Connect
- [ ] **CAN0 (A22/A11)** — Haltech Elite 2500 (500 kbps)
- [ ] **CAN1 (A30/A31)** — AIM Dash / GPS / SmartyCam / Podium (1 Mbps)
- [ ] **CAN2 (A28/A29)** — AIM CAN Keypad 12 (125 kbps)

### High-Priority Power Outputs to Wire
- [ ] **HP1 (A1+A13)** — Starter motor (via solenoid, inductive load)
- [ ] **HP2 (A12+A23)** — Cooling fan (PWM 100Hz)
- [ ] **HP3 (A24+A25)** — Fuel pump (inductive load)
- [ ] **MP1 (A2)** — Injector power supply (→ injector rail + Haltech 34-pin pin 26, R/L)
- [ ] **MP2 (A3)** — COP coil power supply (→ Pin D on all 6 Toyota 90919-A2005 COPs)
- [ ] **MP3 (A4)** — Horn
- [ ] **MP4 (A5)** — Brake lights
- [ ] **MP5 (A6)** — Tail/running lights
- [ ] **MP7 (A8)** — Coolsuit pump

### Accessory Outputs to Wire (IGN-gated, `SafeIgnition`)
- [ ] **LP1 (A14)** — Haltech ECU power (→ 26-pin pin 11, R/W, 13.8V supply)
- [ ] **LP2 (A15)** — AIM 10" dash
- [ ] **LP3 (A16)** — AIM SmartyCam
- [ ] **LP4 (A17)** — AIM GPS module
- [ ] **LP5 (A18)** — Innovate LM2 wideband
- [ ] **LP6 (A19)** — OEM instrument cluster
- [ ] **LP7 (A20)** — Multi-warning red LED (oil P / ECT / oil T / fuel P)

---

## 7. RADIUM FUEL SYSTEM

- [ ] Install Radium fuel pressure regulator/damper
- [ ] Route 6AN PTFE lines to replace soft fuel lines
- [ ] Collect all fittings needed (make a list before starting)
- [ ] Install fuel pressure/temp sensor tap

---

## 8. OTHER

### Move Brake and Fuel Lines
- [ ] Reroute as needed for clearance with new components

### Fix Seat Bracket
- [ ] Address current Sparco Sprint L mounting issues
- [ ] Source full Sparco seat bracket (see 3c)

---

## Quick Reference — Haltech Elite 2500 Pin Summary

### 26-Pin Connector (B) — Sensors, Triggers & CAN
| Pin | Color | Function | Notes |
|-----|-------|----------|-------|
| 1 | Y (shd) | Crank trigger + | Hall or reluctor |
| 2 | Y (shd) | Cam home + | Hall or reluctor |
| 3 | GY | AVI 7 (Air Temp) | 0–5V, 1K pull-up |
| 4 | V | AVI 8 (Coolant Temp) | 0–5V, 1K pull-up |
| 5 | G (shd) | Crank trigger − | Reluctor ground ref |
| 6 | G (shd) | Cam home − | Reluctor ground ref |
| 7 | GY/R (shd) | SPI 4 | 50KHz, 25V max |
| 8 | GY (shd) | SPI 1 | 50KHz, 25V max |
| 9 | GY/B (shd) | SPI 2 | 50KHz, 25V max |
| 10 | GY/BR (shd) | SPI 3 | 50KHz, 25V max |
| 11 | R/W | +13.8V ECU supply | ECU power input |
| 12 | GY/O (shd) | AVI 6 (O2 input 1) | 0–5V, NB O2 compatible |
| 13 | GY/Y (shd) | AVI 1 (O2 input 2) | 0–5V, NB O2 compatible |
| 14 | B/W | Signal ground | Sensor ground |
| 15 | B/W | Signal ground | Sensor ground |
| 16 | B/W | Signal ground | Sensor ground |
| 17 | Y/V | IGN 7 | 1A max |
| 18 | Y/GY | IGN 8 | 1A max |
| 19 | V/O | DPO 4 | Fixed 12V pull-up |
| 20 | O/G | AVI 5 | 0–5V, 1K pull-up |
| 21 | GY/G | Knock 1 | Piezoelectric |
| 22 | GY/L | Knock 2 | Piezoelectric |
| 23 | W | CAN H | ISO 11898 |
| 24 | L | CAN L | ISO 11898 |
| 25 | BR/B | DBW 1 / DPO | 5A peak, 1A avg |
| 26 | BR/R | DBW 2 / DPO | 5A peak, 1A avg |

### 34-Pin Connector (A) — Power, Injectors, Ignition & AVI
| Pin | Color | Function | Notes |
|-----|-------|----------|-------|
| 1 | V/BR | DPO 2 | Fixed 5V pull-up |
| 2 | O/Y | AVI 4 | 0–5V, 1K pull-up |
| 3 | Y/B | IGN 1 | 1A max |
| 4 | Y/R | IGN 2 | 1A max |
| 5 | Y/O | IGN 3 | 1A max |
| 6 | Y/G | IGN 4 | 1A max |
| 7 | Y/BR | IGN 5 | 1A max |
| 8 | Y/L | IGN 6 | 1A max |
| **9** | **O** | **+5V DC sensor supply** | **100mA max — for Lowdoller sensors** |
| 10 | B | Battery ground | To battery negative |
| 11 | B | Battery ground | To battery negative |
| **12** | **O/W** | **+8V DC sensor supply** | **1A max — for OEM sensors/relays/solenoids** |
| 13 | P | 12V ignition input | 12V on IGN + cranking |
| 14 | W | AVI 10 (TPS) | 0–5V, 1K pull-up |
| 15 | Y | AVI 9 (MAP) | 0–5V, 1K pull-up |
| 16 | O/B | AVI 2 | 0–5V, 1K pull-up |
| 17 | O/R | AVI 3 | 0–5V, 1K pull-up |
| 18 | V/B | DPO 1 | User-definable pull-up |
| 19 | L | INJ 1 | 0–8A peak, 0–2A hold |
| 20 | L/B | INJ 2 | 0–8A peak, 0–2A hold |
| 21 | L/BR | INJ 3 | 0–8A peak, 0–2A hold |
| 22 | L/R | INJ 4 | 0–8A peak, 0–2A hold |
| 23 | V/R | DPO 3 | Fixed 12V pull-up |
| 24 | B/Y | DPO 5 (fuel pump trigger) | Fixed 12V pull-up |
| 25 | B/R | DPO 6 (ECR out) | Fixed 12V pull-up |
| **26** | **R/L** | **ECU injector power input** | **REQUIRED — 12V from inj relay** |
| 27 | L/O | INJ 5 | 0–8A peak, 0–2A hold |
| 28 | L/Y | INJ 6 | 0–8A peak, 0–2A hold |
| 29 | L/G | INJ 7 | 0–8A peak, 0–2A hold |
| 30 | L/V | INJ 8 | 0–8A peak, 0–2A hold |
| 31 | G | Stepper 1 P1 / DPO | Hi/Lo 1A |
| 32 | G/B | Stepper 1 P2 / DPO | Hi/Lo 1A |
| 33 | G/BR | Stepper 1 P3 / DPO | Hi/Lo 1A |
| 34 | G/R | Stepper 1 P4 / DPO | Hi/Lo 1A |
