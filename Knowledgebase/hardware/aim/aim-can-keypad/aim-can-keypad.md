# AIM CAN Keypad 12 (Blink Marine PKP-2600-SI)

**Manufacturer:** Blink Marine (AIM resells as "AIM CAN Keypad 12" — same hardware)
**Model:** PKP-2600-SI
**Datasheet:** `AIM PDM/PKP_2600_SI_Datasheet_REV1.pdf`
**Application:** White Tiburon — primary cockpit control panel, CAN2 bus

---

## Overview

12-key CAN keypad with RGB LED indicators and interchangeable 15 mm icon inserts.
IP67/IP69K rated — suitable for open cockpit / race car use.
CANopen / J1939 protocol. Connected to PDM CAN2 bus at 125 kbps.

---

## Electrical Specifications

| Parameter | Value |
|---|---|
| Supply voltage | 12–24V nominal (8–32V range) |
| Standby current | < 50 mA |
| Communication | CANopen, J1939 |
| MTBF | 204,291 hours (MIL-HDBK-217, ground mobile) |
| Operating temp | −40°C to +70°C |
| Storage temp | −40°C to +85°C |
| Ingress protection | IP67 / IP69K |
| Weight | 230 g (inserts excluded) |
| Switch life | 3 million operations per key |

---

## Connector — Deutsch DT04-4P

Standard 4-pin Deutsch connector, wire-side view:

```
  4   3
  1   2
```

| Pin | Wire Color | Function |
|---|---|---|
| 1 | Blue | CAN L |
| 2 | White | CAN H |
| 3 | Black | GND (negative battery) |
| 4 | Red | Vbatt (12–24V) |

> The device is polarity protected.

---

## PDM Wiring (White Tiburon)

Custom **5-pin Binder 712 female → 4-pin Deutsch DT04-4P male** cable.
Binder end plugs into PDM Connector A (black). Deutsch end plugs into keypad.

| PDM Pin | Connector | Signal | Binder Pin | Cable Color | Deutsch Pin | Keypad Color |
|---|---|---|---|---|---|---|
| **A21** | Black | LP8 (keypad power) | 1 | Red | 4 | Red (Vbatt) |
| **A28** | Black | CAN2 High (White) | 2 | White | 2 | White (CAN H) |
| — | — | Spare | 3 | Yellow | — | — |
| **A29** | Black | CAN2 Low (Black) | 4 | Green | 1 | Blue (CAN L) |
| **B18** | **Grey** | GND | 5 | Black | 3 | Black (GND) |

> **CAN H:** White all the way — PDM harness White (A28) → Binder White → Keypad White. No color change.
> **CAN L:** Color changes twice — PDM harness Black (A29) → Binder Green → Keypad Blue. Label all three junctions.
> **GND note:** A10 is committed to the CAN0 expansion cable. Keypad GND uses B18 (grey connector) — same ground plane, different physical pin.
> **Do NOT use CAN0 (A11/A22)** — that bus is AIM expansion at 1 Mbps. Keypad requires CAN2 at 125 kbps.

### LP8 Power Output Config (Race Studio 3)

| Setting | Value |
|---|---|
| Output | LP8 (A21) |
| Name | `Keypad` |
| Mode | OVC Protected |
| Max load | 5A |
| Trigger | `SafeIgnition` |

---

## Physical Layout

**Dimensions:** 181.5 mm × 70.0 mm × 15.2 mm (7.15" × 2.76" × 0.60")
**Mounting footprint:** 135.5 mm (5.33") between studs × 16.3 mm (0.64") inset from edge
**Body depth:** 165.0 mm (6.50") along long axis
**Mounting:** 2× #10-32 UNC steel studs — max torque **1.8 Nm (16 lbf-in)**
**Gasket:** Rubber molded on backside acts as panel gasket — no separate seal required.

### Key Numbering (physical, face-on view)

Race Studio 3 numbers left-to-right, top-to-bottom — confirmed in RS3 CAN2 Keypad tab:

```
[ 1 ][ 2 ][ 3 ][ 4 ][ 5 ][ 6 ]   ← top row
[ 7 ][ 8 ][ 9 ][10 ][11 ][12 ]   ← bottom row
```

Key 1 = top-left, Key 12 = bottom-right.

### Race Studio 3 Button Assignment (White Tiburon) — CONFIRMED

**CAN ID: 0x19**

| Key N. | Variable Name | Work As | LED Colors (rest → active states) |
|---|---|---|---|
| 1 | `StarterKYD` | Momentary | White → Green |
| 2 | `HornKYD` | Momentary | White → Orange |
| 3 | `LightsKYD` | Multistatus (3-pos) | White → Cyan → Blue |
| 4 | `CoolsuitKYD` | Toggle | White → (confirm color) |
| 5 | `FanKYD` | Toggle | White → Red |
| 6 | `FuelOverrideKYD` | Toggle | White → Red |
| 7 | `PitLimiterKYD` | Toggle | White → Green (armed) → Red (active) |
| 8 | `CommsKYD` | Toggle | White → Green |
| 9 | `PitInKYD` | Multistatus (4-pos) | White → Red → … (confirm remaining) |
| 10 | `WiperKYD` | Multistatus (3-pos) | White → Cyan → Blue |
| 11 | K43 (spare) | Momentary | White |
| 12 | K44 (spare) | Momentary | White |

> **Variable name changes from draft:** `FuelOverrideKYD` (not `FuelOverride`), `PitLimiterKYD` (not `PitLimiter_KYD`), `CommsKYD` (not `COMMS_YN`), `PitInKYD` (not `PITIN_LAPS`). These names must match exactly in Math Channels.

---

## CAN Bus Settings

| Setting | Value |
|---|---|
| Bus | CAN2 (PDM A28 H / A29 L) |
| Speed | 125 kbps |
| Protocol | CANopen (Device Profile 401d) / J1939 |
| Address | Configurable via Race Studio 3 or J1939 address claim |

---

## Mechanical Notes

- Vertical or horizontal mount — symmetrical design
- Inserts are interchangeable 15 mm; thousands of stock icons at blinkmarine.com
- Membrane compensation valve self-balances internal pressure with temperature changes
- Rubber backside gasket seals mounting holes against liquid intrusion
- Polarity protected — reversed power connection will not damage the device

---

## Related Files

| File | Contents |
|---|---|
| `AIM PDM/PKP_2600_SI_Datasheet_REV1.pdf` | Source datasheet (Blink Marine) |
| `hardware/aim/aim-pdm/pdm-pinout.md` | PDM connector pinout — CAN2, LP8, B18 locations |
| `builds/white-tiburon/guides/pdm-config.md` | Full PDM configuration including keypad button logic |
| `builds/white-tiburon/guides/pdm-session-1.md` | Step-by-step RS3 setup for CAN2 Keypad tab |
