# White Tiburon — Session Start

**2003 Hyundai Tiburon GK | G6BA 2.7L V6 | Haltech Elite 2500 + AIM PDM 32 | 24 Hours of Lemons**

> **LLM: Load this file first, then `build-profile.json`, then ask your question.**

---

## Build Phase Status (March 2026)

| Phase | System | Status |
|---|---|---|
| P0 | Haltech bench — cam/crank/COP | ✅ Complete |
| P0 | Haltech bench — knock sensors | ⬜ Next |
| P0 | Haltech bench — Lowdoller sensor signals | ⬜ |
| P0 | Haltech → PDM CAN data verified | ⬜ |
| P1 | PDM connected to car (non-destructive) | ✅ Spade connectors on fuse box |
| P1 | Race Studio base config loaded | ✅ |
| P1 | CAN Keypad 12 connected | ✅ 125 kbps on PDM CAN2 |
| P2 | Mechanical installation | ⬜ |
| P3 | Full Haltech integration (stock ECU out) | ⬜ |

---

## Files — Load in This Order for a Work Session

| # | File | What It Covers |
|---|---|---|
| 1 | `README.md` ← *you are here* | Phase status, key facts, file index |
| 2 | `build-profile.json` | Machine-readable config: all 10 AVI pins, PDM output map, ignition type, CAN buses |
| 3 | `signal-routing.md` | End-to-end wire traces for every signal (confidence: ✅ verified / ⚠️ forum / 🔲 planned) |
| 4 | `weekend-tasks.md` | Phased build procedure with test gates — current active work |
| 5 | `guides/pdm-session-1.md` | Race Studio 3 step-by-step config walkthrough (from webinar starting point) |
| 6 | `guides/pdm-config.md` | PDM control scheme overview (keypad map, status variables, output logic) |
| 7 | `guides/bench-test.md` | Consolidated bench test procedure: fuel pump, fuse box tap, alt exciter, starter |
| 8 | `cluster-integration.md` | OEM cluster wiring into Haltech (tach, speedo, fuel, coolant) |
| 9 | `build-profile.md` | Narrative build profile: parts list, mods, history |
| 10 | `build-knowledge-graph.json` | Component/signal relationship graph for programmatic lookup |
| 11 | `diagrams/fuel-pump.md` | Mermaid fuel pump power + control path diagram |

---

## Key Confirmed Facts (Load These Into Context)

> **LLM:** Modifications below override factory specs in `common/shop-manual/` and `common/opengk/`. Check this section first, then reference manuals for anything not listed here.

### Modifications — OEM Values That Do NOT Apply
| System | OEM Spec | **This Car** |
|---|---|---|
| Thermostat | 82°C (180°F) | **77°C (170°F) aftermarket unit installed** |
| Ignition | Wasted spark, 3 coil packs | **Sequential COP — Toyota 90919-A2005 ×6** |
| ECU | Siemens SIMK43 | **Haltech Elite 2500** |
| Power dist. | OEM fuse/relay box | **AIM PDM 32** |
| Fan control | OEM fan thermoswitch | **PDM PWM — 25/50/75/100% at 77/82/87/92°C** |

---

### ECU — Haltech Elite 2500
| Detail | Value |
|---|---|
| Sensor supply +5V | 34-pin **pin 9** (O wire) — ratiometric sensors (Lowdoller, MAP, TPS) |
| Sensor supply +8V | 34-pin **pin 12** (O/W wire) — NOT pin 3 |
| CAN0 to PDM | 26-pin **pin 23** (W) = CAN H → PDM A22; **pin 24** (L) = CAN L → PDM A11 |
| VSS (speed) | 26-pin **pin 8** (SPI 1) ← transaxle Hall IC, 4 pulses/rev |
| Tacho output | 34-pin **pin 18** (DPO 1, V/B) — 3 ppr, 12V active low |

### Ignition — COP (confirmed bench-tested ✅)
| Detail | Value |
|---|---|
| Coil | Toyota **90919-A2005** ×6, sequential |
| IGN outputs | Haltech 34-pin pins 3–8 (IGN1–IGN6, Y/B Y/R Y/O Y/G Y/BR Y/L) |
| Coil connector | A=GND (block), B=trigger (Haltech IGN), C=feedback (open), D=12V (PDM MP2) |
| Dwell | ~2.1 ms |

### AVI Assignments (Lowdoller combo sensors — PTC thermistor, NOT NTC)
| AVI | Signal | Pin | Wire |
|---|---|---|---|
| AVI 1 | Fuel pressure | 26-pin-13 | GY/Y shielded |
| AVI 2 | Fuel temp | 34-pin-16 | O/B |
| AVI 3 | Oil pressure | 34-pin-17 | O/R |
| AVI 4 | Oil temp | 34-pin-2 | O/Y |
| AVI 5 | Coolant pressure | 26-pin-20 | O/G |
| AVI 6 | Coolant temp | 26-pin-12 | GY/O shielded |
| AVI 7 | Brake pressure | 26-pin-3 | GY |
| AVI 8 | Brake temp | 26-pin-4 | V |
| AVI 9 | MAP | 34-pin-15 | Y |
| AVI 10 | TPS | 34-pin-14 | W |

### PDM — AIM PDM 32
| Output | Name | Trigger |
|---|---|---|
| HP1 (A1+A13) | Starter | STARTER_SAFE |
| HP2 (A12+A23) | Fan | ECT temp bands + FanKYD override |
| HP3 (A24+A25) | FuelPump | FUEL_PRIME OR ENGINE_RUNNING OR FuelOverride |
| MP1 (A2) | InjectorPwr | SafeIgnition |
| MP2 (A3) | CoilPwr | SafeIgnition |
| MP3 (A4) | Horn | HornKYD |
| MP4 (A5) | BrakeLights | BRAKE_SWITCH (Ch11) |
| MP5 (A6) | TailLights | LightsKYD |
| MP6 (A7) | AltExciter | SafeIgnition |
| MP7 (A8) | Coolsuit | CoolsuitKYD |
| LP1–LP6 (A14–A19) | ECUPwr/Dash/SmartyCam/GPS/Wideband/Cluster | SafeIgnition |
| LP7 (A20) | WarningLED | MULTI_WARNING |

### Physical Switches
| Input | PDM Connection | Function |
|---|---|---|
| IGN toggle | PDM B23 (built-in IGN input) | Master power / SafeIgnition |
| Start backup button | Ch09 (B21) | Physical backup for keypad Start |
| Brake switch | Ch11 (B28) | Brake lights (always active) |

### CAN Keypad 12 (CAN2, 125 kbps) Button Map
| Key | Function | Type |
|---|---|---|
| K01 | Start | Latching toggle |
| K02 | Horn | Momentary |
| K03 | Lights | Latching toggle |
| K04 | Coolsuit | Latching toggle |
| K05 | Fan override | Latching toggle |
| K06 | Fuel override | Latching toggle |
| K07 | Pit limiter (speed-gated <60 mph) | Latching toggle |
| K08 | Wiper | Latching toggle |
| K09 | Comms Yes/No (PodiumConnect) | Latching toggle |
| K10 | Pit-in 1/2/3 laps (PodiumConnect) | Multi-position |
| K11–12 | Spare | — |

---

## Platform Knowledge (Common to All GK Tiburons)

| Need | File |
|---|---|
| Chassis specs, gear ratios, alignment | `common/chassis/gk-chassis-specs.md` |
| OEM ECU pinouts (SIMK43 5WY) | `common/opengk/ecm-pinouts.md` |
| K-Line / immobiliser / GKFlasher | `common/opengk/k-line.md`, `gkflasher.md`, `smartra.md` |
| CAN bus messages (DME1–5, ASC1–2) | `common/opengk/can-bus-messages.md` |
| BCM pinouts | `common/opengk/body-control-module.md` |
| ETM (electrical manual index) | `common/electrical-manual/index.md` |
| Shop manual (factory OCR) | `common/shop-manual/` |

## Hardware Device Reference

| Device | Reference File |
|---|---|
| Haltech Elite 2500 — 26-pin connector | `hardware/haltech/main-connector-26-pin-elite2500.md` |
| Haltech Elite 2500 — 34-pin connector | `hardware/haltech/main-connector-34-pin-elite2500.md` |
| AIM PDM 32 — full pinout | `hardware/aim-pdm/pdm-pinout.md` |
| AIM PDM 32 — logic & configuration theory | `hardware/aim-pdm/pdm-configuration-guide.md` |
| Lowdoller combo sensors | `hardware/sensors/lowdoller-sensors.md` |
| Toyota COP coil 90919-A2005 | `hardware/sensors/cop-ignition.md` |
