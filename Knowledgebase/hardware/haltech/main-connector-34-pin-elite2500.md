# Haltech Elite 2500 — 34-Pin Connector (A)
**Source:** `Haltech/main-connector-34-pin-elite2500.pdf` + Haltech Support Center
**Harness:** HT-141304, Elite 2500 Premium Universal Harness 2.5m (8')

---

## Pinout — Looking Into Connector on ECU

| Pin | Wire Color | Connection | Notes |
|-----|-----------|------------|-------|
| 1 | V/BR | DPO 2 | 1A max, output to ground, **fixed 5V pull-up** |
| 2 | O/Y | AVI 4 | 0–5V signal input, switchable 1K pull-up |
| 3 | Y/B | IGN 1 | 1A max current |
| 4 | Y/R | IGN 2 | 1A max current |
| 5 | Y/O | IGN 3 | 1A max current |
| 6 | Y/G | IGN 4 | 1A max current |
| 7 | Y/BR | IGN 5 | 1A max current |
| 8 | Y/L | IGN 6 | 1A max current |
| **9** | **O (orange)** | **+5V DC sensor supply** | **100mA max — for 5V ratiometric sensors** |
| 10 | B | Battery ground | To vehicle battery negative (−) |
| 11 | B | Battery ground | To vehicle battery negative (−) |
| **12** | **O/W (orange/white)** | **+8V DC sensor supply** | **1A max — for 8V sensors, relays, solenoids** |
| 13 | P | 12V ignition input | 12V on IGN and cranking only |
| 14 | W | AVI 10 (TPS) | 0–5V signal input, switchable 1K pull-up |
| 15 | Y | AVI 9 (MAP) | 0–5V signal input, switchable 1K pull-up |
| 16 | O/B | AVI 2 | 0–5V signal input, switchable 1K pull-up |
| 17 | O/R | AVI 3 | 0–5V signal input, switchable 1K pull-up |
| 18 | V/B | DPO 1 | 1A max, output to ground, user-definable pull-up |
| 19 | L | INJ 1 | Current controlled, 0–8A peak, 0–2A hold |
| 20 | L/B | INJ 2 | Current controlled, 0–8A peak, 0–2A hold |
| 21 | L/BR | INJ 3 | Current controlled, 0–8A peak, 0–2A hold |
| 22 | L/R | INJ 4 | Current controlled, 0–8A peak, 0–2A hold |
| 23 | V/R | DPO 3 | 1A max, fixed 12V pull-up |
| 24 | B/Y | DPO 5 (Fuel Pump Trigger) | 1A max, fixed 12V pull-up |
| 25 | B/R | DPO 6 (ECR Out) | 1A max, fixed 12V pull-up |
| **26** | **R/L** | **ECU Injector Power Input** | **REQUIRED — 12V from injector power relay** |
| 27 | L/O | INJ 5 | Current controlled, 0–8A peak, 0–2A hold |
| 28 | L/Y | INJ 6 | Current controlled, 0–8A peak, 0–2A hold |
| 29 | L/G | INJ 7 | Current controlled, 0–8A peak, 0–2A hold |
| 30 | L/V | INJ 8 | Current controlled, 0–8A peak, 0–2A hold |
| 31 | G | Stepper 1 P1 / DPO | Hi/Lo side driver, 1A max |
| 32 | G/B | Stepper 1 P2 / DPO | Hi/Lo side driver, 1A max |
| 33 | G/BR | Stepper 1 P3 / DPO | Hi/Lo side driver, 1A max |
| 34 | G/R | Stepper 1 P4 / DPO | Hi/Lo side driver, 1A max |

## White Tiburon Assignments

| Pin | Wire | Assignment | Notes |
|-----|------|------------|-------|
| 2 | O/Y | AVI 4 — Oil temp | Lowdoller 899404 green wire |
| 3 | Y/B | IGN 1 | COP Cyl 1 — Toyota 90919-A2005 |
| 4 | Y/R | IGN 2 | COP Cyl 2 |
| 5 | Y/O | IGN 3 | COP Cyl 3 |
| 6 | Y/G | IGN 4 | COP Cyl 4 |
| 7 | Y/BR | IGN 5 | COP Cyl 5 |
| 8 | Y/L | IGN 6 | COP Cyl 6 |
| 9 | O | +5V sensor supply | All Lowdoller red wires (100 mA max) |
| 10 | B | Battery ground | Battery negative terminal |
| 11 | B | Battery ground | Battery negative terminal |
| 12 | O/W | +8V sensor supply | MAP sensor power (1A max) |
| 13 | P | 12V ignition input | Splice from PDM ignition switch (Grey B23) |
| 14 | W | AVI 10 — TPS | Throttle body TPS signal |
| 15 | Y | AVI 9 — Crankcase pressure | Vacuum tee sensor (future) |
| 16 | O/B | AVI 2 — Fuel temp | Lowdoller 899404 green wire |
| 17 | O/R | AVI 3 — Oil pressure | Lowdoller 899404 yellow wire |
| 18 | V/B | DPO 1 — Tacho output | OEM cluster tacho signal |
| 19 | L | INJ 1 | Injector 1 (cyl 1) |
| 20 | L/B | INJ 2 | Injector 2 (cyl 2) |
| 21 | L/BR | INJ 3 | Injector 3 (cyl 3) |
| 22 | L/R | INJ 4 | Injector 4 (cyl 4) |
| 24 | B/Y | DPO 5 — Fuel pump trigger | PDM channel input (HP3 prime/RPM logic) |
| 26 | R/L | Injector power input | Splice from PDM MP1 (A2) — 12V required |
| 27 | L/O | INJ 5 | Injector 5 (cyl 5) |
| 28 | L/Y | INJ 6 | Injector 6 (cyl 6) |
| 31 | G | Stepper 1 P1 — IACV phase A | IACV stepper motor (35150-33010) via D5 |
| 32 | G/B | Stepper 1 P2 — IACV phase B | IACV stepper motor via D5 |
| 33 | G/BR | Stepper 1 P3 — IACV phase C | IACV stepper motor via D5 |
| 34 | G/R | Stepper 1 P4 — IACV phase D | IACV stepper motor via D5 |

---

## Key Notes

**Sensor Supplies — Two Different Voltages:**
- **Pin 9 = +5V DC** (100mA) — for all 5V ratiometric sensors (MAP, TPS, Lowdoller pressure sensors)
- **Pin 12 = +8V DC** (1A) — for 8V sensors, relays, solenoids

**Fuse Block (HT-030102):** Fuse 1: 10A ECU | Fuse 2: 20A Injection | Fuse 3: 15A Ignition | Fuse 4: 20A Fuel Pump | Fuse 5–6: Spare. Max 15A continuous / 20A peak per circuit.
