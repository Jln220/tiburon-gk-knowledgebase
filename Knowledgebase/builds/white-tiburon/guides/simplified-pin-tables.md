# Simplified Pin Tables — White Tiburon Final Install
## Only the wires you need at each connector

**Car:** White 2003 Tiburon GK | Haltech Elite 2500 + AIM PDM 32
**Purpose:** Strip the harnesses down to just what's wired. If a pin isn't listed, leave it empty.

> **Naming convention:** PDM docs call the connectors A (Black) and B (Grey). The signal-routing doc uses B=Black and G=Grey. This file uses the **A/B standard** with color labels.

---

## 1. Haltech 34-Pin Connector (A) — 25 of 34 pins used

| Pin | Wire | Function | Destination |
|-----|------|----------|-------------|
| 2 | O/Y | AVI 4 — Oil temp | D4 pin 4 → Lowdoller 899404 green wire |
| 3 | Y/B | IGN 1 | D2 pin 1 → Coil 1 pin B (cyl 1) |
| 4 | Y/R | IGN 2 | D3 pin 1 → Coil 2 pin B (cyl 2) |
| 5 | Y/O | IGN 3 | D2 pin 2 → Coil 3 pin B (cyl 3) |
| 6 | Y/G | IGN 4 | D3 pin 2 → Coil 4 pin B (cyl 4) |
| 7 | Y/BR | IGN 5 | D2 pin 3 → Coil 5 pin B (cyl 5) |
| 8 | Y/L | IGN 6 | D3 pin 3 → Coil 6 pin B (cyl 6) |
| **9** | **O** | **+5V sensor supply** | D4 pin 7 → all Lowdoller red wires (100 mA max) |
| 10 | B | Battery ground | Battery negative terminal |
| 11 | B | Battery ground | Battery negative terminal |
| **12** | **O/W** | **+8V sensor supply** | D1 pin 10 → MAP sensor power (1A max) |
| 13 | P | 12V ignition input | Splice from PDM ignition switch (Grey B23) |
| 14 | W | AVI 10 — TPS | D1 pin 9 → throttle body TPS signal |
| 15 | Y | AVI 9 — Crankcase pressure | D1 pin 8 → vacuum tee sensor (future) |
| 16 | O/B | AVI 2 — Fuel temp | D4 pin 2 → Lowdoller 899404 green wire |
| 17 | O/R | AVI 3 — Oil pressure | D4 pin 3 → Lowdoller 899404 yellow wire |
| 18 | V/B | DPO 1 — Tacho output | OEM cluster M10-1 tacho signal |
| 19 | L | INJ 1 | D2 pin 4 → Injector 1 (cyl 1) |
| 20 | L/B | INJ 2 | D3 pin 4 → Injector 2 (cyl 2) |
| 21 | L/BR | INJ 3 | D2 pin 5 → Injector 3 (cyl 3) |
| 22 | L/R | INJ 4 | D3 pin 5 → Injector 4 (cyl 4) |
| 24 | B/Y | DPO 5 — Fuel pump trigger | PDM channel input (HP3 prime/RPM logic) |
| **26** | **R/L** | **Injector power input** | Splice from PDM MP1 (A2) — 12V required |
| 27 | L/O | INJ 5 | D2 pin 6 → Injector 5 (cyl 5) |
| 28 | L/Y | INJ 6 | D3 pin 6 → Injector 6 (cyl 6) |

**Unused (leave empty):** 1, 23, 25, 29, 30, 31, 32, 33, 34

---

## 2. Haltech 26-Pin Connector (B) — 18 of 26 pins used

| Pin | Wire | Function | Destination |
|-----|------|----------|-------------|
| 1 | Y (shd) | Crank trigger (+) | D1 pin 1 → CKP sensor, lower block driver side |
| 2 | Y (shd) | Cam home (+) | D1 pin 3 → CMP sensor, front of engine |
| 3 | GY | AVI 7 — IAT | D1 pin 7 → IAT sensor, back of plenum |
| 4 | V | AVI 8 — Wideband O2 | LM2 cable 3811 lime green wire (cockpit run) |
| 5 | G (shd) | Crank trigger (−) | D1 pin 2 → CKP signal ground ref |
| 6 | G (shd) | Cam home (−) | D1 pin 4 → CMP signal ground ref |
| 8 | GY (shd) | SPI 1 — VSS | Splice from transaxle VSS (C109 Hall IC) |
| **11** | **R/W** | **ECU power (13.8V)** | From PDM LP1 (A14) |
| 12 | GY/O (shd) | AVI 6 — Coolant temp | D4 pin 6 → Lowdoller LDM899TP100 green wire |
| 13 | GY/Y (shd) | AVI 1 — Fuel pressure | D4 pin 1 → Lowdoller 899404 yellow wire |
| 14 | B/W | Signal ground | D1 pin 11 + D4 pin 8 — all sensor grounds |
| 15 | B/W | Signal ground | (paralleled with pin 14) |
| 16 | B/W | Signal ground | (paralleled with pin 14) |
| 20 | O/G | AVI 5 — Coolant pressure | D4 pin 5 → Lowdoller LDM899TP100 yellow wire |
| 21 | GY/G | Knock 1 | D1 pin 5 → knock sensor, driver side block |
| 22 | GY/L | Knock 2 | D1 pin 6 → knock sensor, driver side block |
| **23** | **W** | **CAN H** | PDM Connector A pin 30 (white, 500 kbps) |
| **24** | **L** | **CAN L** | PDM Connector A pin 31 (blue, 500 kbps) |

**Unused (leave empty):** 7, 9, 10, 17, 18, 19, 25, 26

---

## 3. PDM Connector A — Black (35-pin) — 27 of 35 pins used

All power outputs (HP, MP1–8, LP1–8), CAN buses, and Ch11/Ch12 inputs are on this connector.

| Pin | Function | Destination |
|-----|----------|-------------|
| **1** | **HP1 — Starter (pin 1 of 2)** | Starter solenoid S-terminal (10 AWG, ring terminal) |
| 2 | MP1 — Injector power | 3-way splice → D2 pin 8 + D3 pin 8 + Haltech 34-pin 26 |
| 3 | MP2 — Coil power | 2-way splice → D2 pin 7 + D3 pin 7 |
| 4 | MP3 — Horn | Horn (Phase 2+, triggered by Ch12) |
| 5 | MP4 — Brake lights | Brake light circuit (triggered by Ch09) |
| 6 | MP5 — Tail lights | Tail light circuit (on with SafeIgnition) |
| 7 | MP6 — Headlights | Headlight circuit (Phase 2+, Ch04 + SafeIgnition) |
| 8 | MP7 — Coolsuit pump | Coolsuit pump motor (Ch10 + SafeIgnition) |
| 9 | MP8 — Defogger | Rear window defogger element (Ch11 + SafeIgnition) |
| 10 | GND | Ground — CAN0 expansion cable |
| 11 | CAN0 Low | AIM expansion devices (GPS, SmartyCam, DataHub) |
| **13** | **HP1 — Starter (pin 2 of 2)** | (paralleled with A1) |
| 14 | LP1 — ECU power | Haltech 26-pin pin 11 (R/W, 13.8V) |
| 15 | LP2 — Dash | AIM 10" dash power |
| 16 | LP3 — SmartyCam | SmartyCam power |
| 17 | LP4 — GPS | AIM GPS-08 power |
| 18 | LP5 — Wideband | Innovate LM2 power |
| 19 | LP6 — Cluster | OEM instrument cluster power |
| 20 | LP7 — Warning LED | Warning LED (low oil P / high ECT / high oil T / low fuel P) |
| 21 | LP8 — Alt exciter | Alternator D+ field wire splice |
| 22 | CAN0 High | AIM expansion devices (GPS, SmartyCam, DataHub) |
| **24** | **HP3 — Fuel pump (pin 1 of 2)** | Fuel pump + (14 AWG) |
| **25** | **HP3 — Fuel pump (pin 2 of 2)** | (paralleled with A24) |
| 26 | Ch11 input — Defogger toggle | Latching switch, 12V when ON |
| 27 | Ch12 input — Horn button | Momentary switch, active = GND |
| **30** | **CAN1 High** | Haltech 26-pin pin 23 (white wire, 500 kbps) |
| **31** | **CAN1 Low** | Haltech 26-pin pin 24 (blue wire, 500 kbps) |
| 33 | +Vb out CAN | Powers AIM devices on CAN0 bus |

**Future (wire but don't connect yet):**

| Pin | Function | Destination |
|-----|----------|-------------|
| 28 | CAN2 High | CAN keypad (125 kbps) — Phase 3 |
| 29 | CAN2 Low | CAN keypad (125 kbps) — Phase 3 |

**Unused (leave empty):** 12, 23, 32, 34, 35

---

## 4. PDM Connector B — Grey (35-pin) — 18 of 35 pins used

Half-bridge outputs, wiper outputs, channel inputs 1–10, ignition input, and grounds are on this connector.

| Pin | Function | Destination |
|-----|----------|-------------|
| **1** | **HB1 — Cooling fan (pin 1 of 2)** | Radiator fan motor (12 AWG, PWM 4-band) |
| **2** | **HB1 — Cooling fan (pin 2 of 2)** | (paralleled with B1) |
| 3 | LP9 — Wiper park sweep | Wiper motor brown wire |
| 4 | MP9 — Wiper low | Wiper motor green wire |
| 5 | MP10 — Wiper high | Wiper motor yellow wire |
| 13 | P GND | Power ground |
| 14 | P GND | Power ground |
| 18 | GND | Signal/logic ground |
| 21 | Ch09 input — Brake light switch | Switch closes to GND on pedal press |
| 22 | Ch10 input — Coolsuit toggle | Latching switch, 12V when ON |
| **23** | **Ignition input** | **Ignition toggle switch → also spliced to Haltech 34-pin 13** |
| 26 | Ch01 input — Start button | Momentary, active = GND |
| 27 | Ch02 input — Fan low override | Latching switch, 12V when ON |
| 28 | Ch03 input — Fan high override | Latching switch, 12V when ON |
| 29 | Ch04 input — Headlights toggle | Latching switch, 12V when ON |
| 30 | Ch05 input — Wiper low toggle | Latching switch, 12V when ON |
| 31 | Ch06 input — Wiper high toggle | Latching switch, 12V when ON |
| 33 | Ch08 input — (spare) | Available — Ch07 (B32) also spare |

**Unused (leave empty):** 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 19, 20, 24, 25, 32, 34, 35

---

## Wire Count Summary

| Connector | Total Pins | Pins Used | Empty |
|-----------|-----------|-----------|-------|
| Haltech 34-pin (A) | 34 | 25 | 9 |
| Haltech 26-pin (B) | 26 | 18 | 8 |
| PDM Conn A (Black) | 35 | 27 (+2 future) | 6 |
| PDM Conn B (Grey) | 35 | 18 | 17 |
| **Totals** | **130** | **88** | **40** |

> **34% of pins are empty.** That's your harness simplification — 40 wires you don't need to run.

---

## Cross-References

| File | Contents |
|------|----------|
| `harness-design.md` | Deutsch connector pinouts (D1–D4), physical routing, build order |
| `../signal-routing.md` | Full end-to-end signal trace with AVI/DPO assignments |
| `pdm-build-guide.md` | PDM output config, Race Studio settings, phase build plan |
| `../../hardware/haltech/main-connector-34-pin-elite2500.md` | Full 34-pin reference |
| `../../hardware/haltech/main-connector-26-pin-elite2500.md` | Full 26-pin reference |
| `../../hardware/aim/aim-pdm/pdm-pinout.md` | Full PDM pinout reference |

---

*Generated: 2026-03-23*
