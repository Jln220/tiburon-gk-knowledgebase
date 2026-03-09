# Hardware — Device Reference Documentation

**Rule:** This directory contains **generic device documentation only** — pinouts, wiring diagrams, and specs that apply to any installation of a given device. Car-specific configuration guides live in `builds/{car}/`.

| What belongs here | What belongs in `builds/{car}/` |
|---|---|
| Haltech Elite 2500 connector pinout | Which Haltech pin connects to which sensor on a specific car |
| AIM PDM 32 connector pinout | Race Studio config guide for a specific car |
| Lowdoller sensor wiring spec | Which AVI input a specific sensor is assigned to |
| Toyota COP coil connector pinout | COP wiring for a specific ignition setup |

---

## Contents

### `haltech/` — Haltech Elite 2500

| File | Contents |
|---|---|
| `main-connector-26-pin-elite2500.md` | Full 26-pin connector reference: triggers, AVI, DPO, CAN, signal grounds |
| `main-connector-34-pin-elite2500.md` | Full 34-pin connector reference: ignition (IGN1–6), injectors (INJ1–6), sensor supply, AVI |
| `elite-2500-wiring-diagram--rev-6.md` | Rev 6 wiring diagram highlights (fuse block, power pins, CAN, ignition outputs) |
| `rem-harness-diagram.md` | Remote harness (REM) wiring diagram |

### `aim-pdm/` — AIM PDM 32

| File | Contents |
|---|---|
| `pdm-pinout.md` | Full 35-pin ×2 connector pinout (Connector A and B), built-in channels |
| `pdm-configuration-guide.md` | Logic architecture: keypads → status variables → triggers → outputs; PWM fan example |

### `sensors/` — Sensors & Actuators

| File | Contents |
|---|---|
| `lowdoller-sensors.md` | Combo sensor specs (Lowdoller 899402–899409): PTC thermistor, pressure range, wiring, +5V supply |
| `cop-ignition.md` | Toyota 90919-A2005 COP: connector pinout (A=GND, B=trigger, C=feedback, D=12V), dwell, NSP settings |

---

## Car-Specific Config Lives Here

| Car | Config files |
|---|---|
| White Tiburon | `builds/white-tiburon/pdm/` — Race Studio config guide + session 1 walkthrough |
| White Tiburon | `builds/white-tiburon/cluster-integration.md` — OEM cluster wiring into Haltech |
