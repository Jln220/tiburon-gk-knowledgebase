# AIM PDM 32 — Complete Technical Reference

**Source:** `AIM PDM/PDM Pinout.pdf` (AIM PDM 32 User Guide, page 4)
**Full User Guide:** `AIM PDM/PDM32_user_guide.pdf` — complete wiring, CAN keypad setup, protection configuration, Race Studio 3 reference
**Device:** AIM PDM 32 Power Distribution Module
**Application:** White Tiburon (primary race car)

---

## Overview

The AIM PDM 32 is a motorsport Power Distribution Module with 32 configurable outputs.
It replaces a conventional fuse/relay panel, providing programmable current protection,
diagnostics, and CAN bus integration.

---

## Connectors — Summary

The PDM 32 has **6 connectors total**:

| # | Connector | Purpose |
|---|-----------|---------|
| 1 | **Surlok Power Connector** (120A Amphenol Surlok) | +V battery supply (+9–15Vdc from battery) |
| 2 | **Rosenberger LVDS** (4-pin) | Display link — connects 6" or 10" AIM dash |
| 3 | **35-pin AMP** (black connector) | Main I/O — Connector A |
| 4 | **35-pin AMP** (grey connector) | Main I/O — Connector B |
| 5 | **Binder 5-pin** (712 female) | USB port connection |
| 6 | **Binder 3-pin** (712 female) | Video input / analog mirror camera |

---

## LVDS Display Connector (4-pin Rosenberger, external view)

| Pin | Description |
|-----|-------------|
| 1 | Serial data |
| 2 | +V Power |
| 3 | Serial data– |
| 4 | GND |

---

## USB Connector (5-pin Binder 712, female, external view)

| Pin | Description |
|-----|-------------|
| 1 | USB D+ |
| 2 | USB D– |
| 3 | GND |

---

## Video Input Connector (3-pin Binder 712, female, external view)

| Pin | Description |
|-----|-------------|
| 1 | Video input 1 |
| 2 | GND |
| 3 | +Vb output CAM |
| 4 | GND |
| 5 | Video input 2 |

---

## 35-Pin AMP Connector A (BLACK) — Pinout

Panel male connector, external view.

| PIN | DESCRIPTION | PIN | DESCRIPTION |
|-----|-------------|-----|-------------|
| 1  | High power output 1 *(has internal series diode)* | 19 | Low power output 6 |
| 2  | Mid power output 1  | 20 | Low power output 7 |
| 3  | Mid power output 2  | 21 | Low power output 8 |
| 4  | Mid power output 3  | 22 | CAN0 High |
| 5  | Mid power output 4  | 23 | High power output 2 *(has internal freewheeling diode)* |
| 6  | Mid power output 5  | 24 | High power output 3 *(has internal freewheeling diode)* |
| 7  | Mid power output 6  | 25 | High power output 3 *(has internal freewheeling diode)* |
| 8  | Mid power output 7  | 26 | Channel input 11 |
| 9  | Mid power output 8  | 27 | Channel input 12 |
| 10 | GND                 | 28 | CAN2 High |
| 11 | CAN0 Low            | 29 | CAN2 Low |
| 12 | High power output 2 *(has internal freewheeling diode)* | 30 | CAN1 High/RS232TX |
| 13 | High power output 1 *(has internal series diode)* | 31 | CAN1 Low/RS232RX |
| 14 | Low power output 1  | 32 | +Vb ext CAN |
| 15 | Low power output 2  | 33 | +Vb out CAN |
| 16 | Low power output 3  | 34 | High power output 4 *(has internal freewheeling diode)* |
| 17 | Low power output 4  | 35 | High power output 4 *(has internal freewheeling diode)* |
| 18 | Low power output 5  |    |  |

**Notes on Connector A:**
- Pin 1 and Pin 13 are both labeled "High power output 1" — these are the two pins of the same high-current output (dual-pin for current capacity)
- Pin 12 and Pin 23 appear as dual-pin outputs for High power output 2
- Pin 34 and Pin 35 are dual-pin for High power output 4
- High Power Out 1 has an **internal series diode**
- High Power Outs 1, 2, 3, 4 have **internal freewheeling diode** (except #1 which has series diode)

---

## 35-Pin AMP Connector B (GREY) — Pinout

Panel male connector, external view.

| PIN | DESCRIPTION | PIN | DESCRIPTION |
|-----|-------------|-----|-------------|
| 1  | Half bridge power output 1  | 19 | Speed 2 input |
| 2  | Half bridge power output 1  | 20 | Speed 1 input |
| 3  | Low power output 9          | 21 | Channel input 9 |
| 4  | Mid power output 9          | 22 | Channel input 10 |
| 5  | Mid power output 10         | 23 | Ignition |
| 6  | Low power output 10         | 24 | Half bridge power output 3 |
| 7  | Low power output 11         | 25 | Half bridge power output 3 |
| 8  | Mid power output 11         | 26 | Channel input 1 |
| 9  | Mid power output 12         | 27 | Channel input 2 |
| 10 | Low power output 12         | 28 | Channel input 3 |
| 11 | Half bridge power output 2  | 29 | Channel input 4 |
| 12 | Half bridge power output 2  | 30 | Channel input 5 |
| 13 | P GND                       | 31 | Channel input 6 |
| 14 | P GND                       | 32 | Channel input 7 |
| 15 | LIN                         | 33 | Channel input 8 |
| 16 | +5V Analog Vreference       | 34 | Half bridge power output 4 |
| 17 | +Vb output                  | 35 | Half bridge power output 4 |
| 18 | GND                         |    |  |

**Notes on Connector B:**
- Half bridge outputs use **dual pins** for current capacity:
  - Half bridge output 1: pins 1 + 2
  - Half bridge output 2: pins 11 + 12
  - Half bridge output 3: pins 24 + 25
  - Half bridge output 4: pins 34 + 35
- Pin 13: P GND = Power Ground
- Pin 14: P GND = Power Ground
- Pin 15: LIN bus connection
- Pin 16: +5V Analog reference (for sensors)
- Pin 17: +Vb output (switched battery voltage)
- Pin 23: Ignition input

---

## Output Channel Classification

Based on the pinout, the PDM 32 outputs fall into these categories:

### High Power Outputs (Connector A)
| Output | Pins (Conn A) | Note |
|--------|--------------|------|
| High power output 1 | A1, A13 (dual pin) | Internal series diode |
| High power output 2 | A12, A23 (dual pin) | Internal freewheeling diode |
| High power output 3 | A24, A25 (dual pin) | Internal freewheeling diode |
| High power output 4 | A34, A35 (dual pin) | Internal freewheeling diode |

### Half Bridge Power Outputs (Connector B)
| Output | Pins (Conn B) | Note |
|--------|--------------|------|
| Half bridge power output 1 | B1, B2 (dual pin) | |
| Half bridge power output 2 | B11, B12 (dual pin) | |
| Half bridge power output 3 | B24, B25 (dual pin) | |
| Half bridge power output 4 | B34, B35 (dual pin) | |

### Mid Power Outputs
| Output | Pin |
|--------|-----|
| Mid power output 1  | A2  |
| Mid power output 2  | A3  |
| Mid power output 3  | A4  |
| Mid power output 4  | A5  |
| Mid power output 5  | A6  |
| Mid power output 6  | A7  |
| Mid power output 7  | A8  |
| Mid power output 8  | A9  |
| Mid power output 9  | B4  |
| Mid power output 10 | B5  |
| Mid power output 11 | B8  |
| Mid power output 12 | B9  |

### Low Power Outputs
| Output | Pin |
|--------|-----|
| Low power output 1  | A14 |
| Low power output 2  | A15 |
| Low power output 3  | A16 |
| Low power output 4  | A17 |
| Low power output 5  | A18 |
| Low power output 6  | A19 |
| Low power output 7  | A20 |
| Low power output 8  | A21 |
| Low power output 9  | B3  |
| Low power output 10 | B6  |
| Low power output 11 | B7  |
| Low power output 12 | B10 |

---

## Input Channels

### Digital/Analog Channel Inputs (Connector B)
| Input | Pin |
|-------|-----|
| Channel input 1  | B26 |
| Channel input 2  | B27 |
| Channel input 3  | B28 |
| Channel input 4  | B29 |
| Channel input 5  | B30 |
| Channel input 6  | B31 |
| Channel input 7  | B32 |
| Channel input 8  | B33 |
| Channel input 9  | B21 |
| Channel input 10 | B22 |
| Channel input 11 | A26 |
| Channel input 12 | A27 |

### Speed Inputs (Connector B)
| Input | Pin |
|-------|-----|
| Speed 1 input | B20 |
| Speed 2 input | B19 |

### Special Inputs
| Input | Pin | Connector |
|-------|-----|-----------|
| Ignition    | B23 | B |
| LIN bus     | B15 | B |

### Built-In Internal Channels (Software Only — No Pin)
| Channel | Description |
|---------|-------------|
| `SafeIgnition` | ON when PDM activated via IGN input (B23). OFF when activated via CH_IN11/12. Use as master permissive for all engine outputs. |
| `POTotCurrent` | Sum of all current drawn by power outputs — useful for monitoring total load |
| IMU 9-axis | Internal 3-axis accelerometer + magnetometer + gyro |
| Internal temperature | PDM internal temperature sensor |

> **Source:** PDM32 User Guide §11.5 — these channels appear automatically in Race Studio 3 and do not require wiring.

---

## Communication Buses

### CAN Bus (Connector A)

| Signal | Pin | Harness Wire Color | Twisted With | Device |
|--------|-----|--------------------|--------------|--------|
| CAN0 High    | A22 | (expansion cable) | A11 | AIM DataHub / GPS / SmartyCam |
| CAN0 Low     | A11 | (expansion cable) | A22 | AIM DataHub / GPS / SmartyCam |
| CAN1 High / RS232 TX | A30 | **White** | A31 | Haltech Elite 2500 |
| CAN1 Low  / RS232 RX | A31 | **Blue**  | A30 | Haltech Elite 2500 |
| CAN2 High    | A28 | **White** | A29 | AIM CAN Keypad 12 |
| CAN2 Low     | A29 | **Black** | A28 | AIM CAN Keypad 12 |
| +Vb ext CAN  | A32 | (expansion cable) | — | — |
| +Vb out CAN  | A33 | (expansion cable) | — | — |

**Three CAN buses total:** CAN0, CAN1 (also configurable as RS232), CAN2

> **CAN1 pair:** A30 White (H) + A31 Blue (L) — twisted, → Haltech 26-pin pin 23/24
> **CAN2 pair:** A28 White (H) + A29 Black (L) — twisted, → Keypad Deutsch
> **A28 and A30 are both White** — different twisted pairs, adjacent pins. Label both ends clearly before routing.

### CAN Expansion Cable (AIM Device Bus — CAN0)

The PDM ships with a dedicated harness labeled **"CAN expansion"** that plugs into the **black connector (Connector A)** and breaks CAN0 plus its power rails out to a **5-pin Binder connector** for connecting AIM devices (GPS-08, SmartyCAM, CAN Data Hub, etc.).

Binder pin layout (front/mating face view):

```
  5  1
 4    2
   3
```

| Binder Pin | Signal | PDM Pin (Conn A) | Wire Gauge | Notes |
|-----------|--------|-----------------|------------|-------|
| 1 | +Vb ext CAN | A32 | 22 AWG | Power IN from external device to PDM (typically unused) |
| 2 | CAN0 Low | A11 | 22 AWG | AIM device bus data − |
| 3 | +Vb out CAN | A33 | 22 AWG | Power OUT from PDM to AIM devices (powers hub/GPS/cam) |
| 4 | GND | A10 | 22 AWG | Logic ground |
| 5 | CAN0 High | A22 | 22 AWG | AIM device bus data + — **see fault note below** |

> **Wire gauge: 22 AWG throughout** — all five conductors in the expansion cable are 22 ga. The +Vb out CAN line (A33) powers connected AIM devices; keep total device current draw modest given this gauge. Do not splice high-current loads onto this line.

> ~~⚠️ Known fault — Binder pin 5 (CAN0 High / A22): no continuity found~~ — **resolved: loose connection in test setup. All 5 pins confirmed good.**

### CAN2 Bus (A28/A29) — Available for Future CAN Device

CAN2 pins (A28 H / A29 L) are available for a future CAN device such as the AIM CAN Keypad 12, additional ECU, or data logger. CAN2 runs at 125 kbps.

> **⚠️ Do not wire CAN2 devices to CAN0 (A11/A22).** CAN0 runs AIM expansion devices at 1 Mbps. Mixing bus speeds = both buses fail.

#### CAN Keypad 12 Cable Pinout (for future keypad connection)

| Deutsch Pin | Colour | Function |
|------------|--------|----------|
| 1 | Blue | CAN L |
| 2 | White | CAN H |
| 3 | Black | GND |
| 4 | Red | Vbatt (12–24V) |

**Binder pin layout (front/mating face view):**

```
  5  1
 4    2
   3
```

**Full color map — PDM harness → Binder cable → Deutsch (keypad side):**

| PDM Harness Color | PDM Pin | Connector | Binder Pin | Binder Cable Color | Deutsch Pin | Keypad Color | Signal |
|------------------|---------|-----------|------------|-------------------|------------|-------------|--------|
| — | A21 (LP8) | Black | 1 | Red | 4 | Red | Vbatt |
| **White** | A28 (CAN2 H) | Black | 2 | White | 2 | White | CAN H |
| — | — | — | 3 | Yellow | — | — | Spare — not connected |
| **Black** | A29 (CAN2 L) | Black | 4 | Green | 1 | Blue | CAN L |
| — | **B18 (GND)** | **Grey** | 5 | Black | 3 | Black | GND |

> **CAN H path:** PDM harness White (A28) → Binder White → Keypad White (Deutsch pin 2) — White throughout
> **CAN L path:** PDM harness Black (A29) → Binder Green → Keypad Blue (Deutsch pin 1) — three different colors, label all junctions
> **A10 (GND) is committed** to the CAN0 expansion cable — keypad GND uses B18 (grey connector), same ground plane

> **⚠️ Do not wire keypad to CAN0 (A11/A22).** CAN0 runs AIM expansion devices at 1 Mbps. Keypad runs at 125 kbps on CAN2 only. Mixed bus = both buses fail.

> **LP8 (A21) — "Keypad" power output:** OVC Protected, 5A max, trigger = `SafeIgnition`. Keypad draws <1A.

### LIN Bus (Connector B)
| Signal | Pin |
|--------|-----|
| LIN | B15 |

### RS232 (Connector A, shared with CAN1)
| Signal | Pin |
|--------|-----|
| RS232 TX | A30 (shared with CAN1 High) |
| RS232 RX | A31 (shared with CAN1 Low) |

---

## Power Supply

| Parameter | Value |
|-----------|-------|
| Main supply | +9–15Vdc from battery (via Surlok connector) |
| Max current | 120A (Amphenol Surlok connector rating) |
| +5V Analog Vref output | B16 (for connected sensors) |
| +Vb output | B17 (switched battery voltage) |
| +Vb out CAN | A33 |
| +Vb ext CAN | A32 |

---

## Ground Pins

| Signal | Pin | Connector |
|--------|-----|-----------|
| GND             | A10 | A |
| P GND           | B13 | B |
| P GND           | B14 | B |
| GND             | B18 | B |

---

## Output Count Summary

| Type | Count |
|------|-------|
| High power outputs | 4 (dual-pin each) |
| Half bridge power outputs | 4 (dual-pin each) |
| Mid power outputs | 12 |
| Low power outputs | 12 |
| **Total outputs** | **32** |

---

## Input Count Summary

| Type | Count |
|------|-------|
| Channel inputs (digital/analog) | 12 |
| Speed inputs | 2 |
| Ignition input | 1 |
| **Total inputs** | **15** |

---

## Diode Notes

- **High Power Out 1:** Has internal **series diode** (prevents backfeed; load sees Vbatt minus diode drop)
- **High Power Outs 1, 2, 3, 4:** Have internal **freewheeling diode** (suppresses inductive kickback; required for relay coils, solenoids, motors)

---

## Physical Layout Notes

- Both 35-pin AMP connectors are **panel male** (pins face outward from PDM body)
- Black connector = Connector A (left side when viewing unit face-on)
- Grey connector = Connector B (right side when viewing unit face-on)
- Pin 1 is top-left on each connector (row numbering proceeds left-to-right, top-to-bottom in a 4-row arrangement: rows of approximately 5, 11, 11, 8 pins)

---

## Software / Configuration

- Configured via **AiM Race Studio** software
- USB connection via 5-pin Binder connector
- Firmware updates and configuration files loaded over USB
- Display (6" or 10" AIM MXP/MXG) connects via LVDS link; display can show PDM channel status, current draw, fault codes

---

## Related Files

| File | Contents |
|------|----------|
| `AIM PDM/PDM Pinout.pdf` | Source PDF (User Guide page 4) — connector diagram + full pinout tables |
| `Knowledgebase/cars/white-tiburon.md` | White car wiring integration — which PDM channels are assigned to what |
| `Knowledgebase/aim-pdm/pdm-pinout.md` | This file |
