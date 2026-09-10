# PDM Sensor Harness — Current Race Config (PDM Only, No ECU)
## White Tiburon — AIM PDM 32 reading sensors directly, stock ECU runs the engine

**Purpose: clean, working gauges for next weekend's race — not a permanent
architecture decision.** Stock ECU keeps running the car exactly as it does today;
this is just getting the Lowdoller/tire/trans sensors off temporary Wago splices
and onto a real PDM-read harness so the dash shows good data. The full Haltech
takeover (Phase 2/3 in the older docs) is explicitly deferred, not abandoned —
this doc and the finalized Deutsch harness below are meant to be easy to build on
top of when that happens, not something that has to be undone first.

**Status: this is the active plan for the upcoming race.** It supersedes the combined
PDM + Haltech architecture described in `harness-design.md`, `pdm-build-guide.md`,
`signal-routing.md`, and `hardware/sensors/lowdoller-sensors.md` — those documents
describe a shelved Phase 2/3 plan (Haltech running the engine, PDM doing full power
distribution) that is not part of this build for now. Revisit them if that plan is
picked back up later.

**What changed from the old plan:**
- Stock ECU continues to run the engine — no Haltech engine control, no Haltech in
  the sensor path at all.
- Relay box stays in as-is; only the ECU relay is being replaced. PDM does not
  distribute power to anything else.
- **PDM's only job is reading sensors** and broadcasting them over CAN to the AIM
  dash / SmartyCam / Podium for display and logging. No switch panel, no power
  output logic tied to these channels.
- MAP sensor removed (was AVI9 on the old Haltech plan — not carried over).
- Coolant sensor dropped. The old coolant bypass loops (throttle body feed, heater
  core loop) are being capped — heater core is removed and the TB is already
  blocked internally, so neither loop serves a function anymore. OE coolant sender
  + stock ECU remains the coolant temp reference.
- Tire temp (front left only) and transmission fluid pressure/temp added.

---

## Sensor List

| Sensor | Model | Signals | Location |
|---|---|---|---|
| Fuel pressure/temp | Lowdoller 899404 (150 PSI combo) | 2 (P + T) | On regulator, strut tower mount — right side |
| Transmission pressure/temp | Lowdoller 899404 (150 PSI combo) | 2 (P + T) | Right side, grouped with fuel/tire |
| Tire temp | 6–24VDC supply / 0–5V output sensor (non-Lowdoller) | 1 (T only) | Front left tire only |
| Oil pressure/temp | Lowdoller 899404 (150 PSI combo) | 2 (P + T) | Left side of engine |

Coolant: **excluded.** MAP: **removed.**

---

## PDM Channel Map

The AIM PDM 32 has 12 total channel inputs but only **8 are true analog-capable
(0–5V/0–12V)** — Ch01–Ch08. Ch09–Ch12 are digital-only and unused here. Since the
PDM isn't driving a switch panel or output logic in this build, all 8 analog
channels are free for sensors.

| Channel | Signal | Notes |
|---|---|---|
| Ch01 | Fuel pressure | 899404, 0.5–4.5V ratiometric |
| Ch02 | Fuel temp | 899404, PTC resistive — needs custom sensor calibration in Race Studio (raw element swings only ~84–198Ω across full range; do not rely on the 10kΩ digital pull-up used for switch inputs) |
| Ch03 | Oil pressure | 899404, 0.5–4.5V ratiometric |
| Ch04 | Oil temp | 899404, PTC — custom sensor cal in Race Studio |
| Ch05 | Trans pressure | 899404, 0.5–4.5V ratiometric |
| Ch06 | Trans temp | 899404, PTC — custom sensor cal in Race Studio |
| Ch07 | Tire temp (FL) | 0–5V output |
| Ch08 | **Spare** | Headroom for later (2nd tire zone, brake sensor, etc.) |

> PTC calibration table (same for all Lowdoller temp elements) is in
> `hardware/sensors/lowdoller-sensors.md` — reuse those resistance-vs-temperature
> values when building the custom sensor cal in Race Studio, just pointed at PDM
> channels instead of Haltech AVIs.

---

## Supply / Ground — PDM's Own Pins

No Haltech pins are used anywhere in this harness. Reference pins are on PDM
Connector B (Grey):

| Function | PDM Pin | Used By |
|---|---|---|
| +5V Analog Vref | B16 | Shared bus — all 3 Lowdoller combo sensors' red wires |
| Signal/clean GND | B18 | Shared bus — Lowdoller black+white returns, tire temp black wire |
| +Vb switched 12V | B17 | Tire temp red wire only (needs 6–24V, can't share the 5V bus) |

**Tire temp sensor pinout** (per sensor datasheet):

| Wire | Function | Destination |
|---|---|---|
| Red | Supply, 6–24VDC | PDM B17 (+Vb) |
| Black | Clean sensor ground | PDM B18 (shared clean GND bus) |
| White | Output signal, 0–5VDC | Ch07 |
| Clear (shield) | Chassis ground | Chassis, **not** the clean-GND bus — kept separate to avoid coupling shield-return noise into the shared analog sensor signals |

---

## Deutsch Connector Groups

Grouped by physical location to minimize the number of cable runs converging on
the PDM — two trunks instead of five individual sensor leads.

### Right Side — Fuel + Trans + Tire Temp (12-pin Deutsch)

| Pin | Signal |
|---|---|
| 1 | Fuel pressure (yellow) |
| 2 | Fuel temp (green) |
| 3 | Trans pressure (yellow) |
| 4 | Trans temp (green) |
| 5 | Tire temp signal (white) |
| 6 | Shared +5V (fuel + trans red wires) |
| 7 | Shared clean GND (fuel + trans black/white, tire temp black) |
| 8 | Tire temp +Vb supply (red) |
| 9 | Tire temp shield drain (clear → chassis GND) |
| 10–12 | Spare |

9 of 12 pins used, 3 spare.

### Left Side — Oil Only (4-pin Deutsch)

| Pin | Signal |
|---|---|
| 1 | Oil pressure (yellow) |
| 2 | Oil temp (green) |
| 3 | Shared +5V (red) |
| 4 | Shared clean GND (black/white) |

All 4 pins used — no spares on this one unless you want to size up for future
expansion (a 6-pin leaves room to add something else on this side later).

---

## Bypass Loop Disposition (Coolant)

Both the throttle-body coolant feed and the heater-core loop are being **capped
into dead-legs** rather than left flowing — neither the heater core (removed) nor
the TB coolant passages (blocked) need flow anymore. No sensor is being installed
in either capped stub for now; the OE coolant sender + stock ECU remains the
temperature reference. If a coolant channel is wanted later, threading a sensor
into one of these capped stubs is still on the table — see prior discussion: a
true dead-leg (zero flow) equalizes to actual system pressure, so it's a
reasonably good pressure tap despite being a former bypass branch. Would need a
free PDM analog channel, which there currently isn't one to spare without giving
up the Ch08 headroom.

---

## Open Items

- **PTC resistive sensor reading on PDM channel inputs** — confirmed to be handled
  via custom sensor calibration in Race Studio (per build decision). Worth a bench
  check with one sensor before committing all four temp channels to this scheme.
- Trans sensor confirmed as Lowdoller 899404 combo (same as fuel/oil).

---

## Cross-References

| File | Status |
|---|---|
| `guides/harness-design.md` | Describes shelved PDM+Haltech Deutsch architecture (D1–D4, coil/injector banks) — not current |
| `guides/pdm-build-guide.md` | Describes shelved PDM+Haltech Race Studio config (fan/switch outputs, ECU Stream) — not current |
| `signal-routing.md` | Describes shelved Haltech AVI assignments — not current |
| `hardware/sensors/lowdoller-sensors.md` | Sensor specs/PTC calibration table still accurate — reuse the resistance table, ignore the Haltech AVI assignment section |
| `hardware/aim/aim-pdm/pdm-pinout.md` | PDM connector pinout — still accurate, source for B16/B17/B18 references above |
