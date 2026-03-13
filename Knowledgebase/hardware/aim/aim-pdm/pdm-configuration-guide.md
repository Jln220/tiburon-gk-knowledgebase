# AIM PDM 32 — Configuration Guide
**Source:** AIM Sports webinar "3-27 I Have an AIM PDM, Now What?" — Robbie Yeoman (CTO) & Roger Caddell (National Training Manager), 8/30/2022
**YouTube:** https://www.youtube.com/watch?v=sResCgHlDYI
**Software:** AiM Race Studio (USB connection via 5-pin Binder on PDM)
**Sample RS3 Config:** https://www.aimsports.com/webinars/Co... (see video description for full link)

---

## Hardware Specifications

### PDM 32

| Spec | Value |
|------|-------|
| Dimensions | 234.5 × 94.6 × 49.5 mm |
| Weight | 761 g |
| Body | Anodized aluminum |
| Waterproof | IP65 |
| Power supply | 9–15V DC |
| Total max current | 120A |
| Internal memory | 4 GB (data logging) |
| CAN buses | 3 (CAN AiM, CAN ECU, CAN2) |
| LIN bus | 1 |
| Analog camera inputs | 2 |
| Inputs | 14 fully configurable (8 analog 0–5V/0–12V or digital, 2 speed, 4 digital), max 500 Hz each |
| LEDs | 32 RGB + 1 PDM ON + 1 PDM STS (Status) |
| Remote display | LVDS (4-pin Rosenberger) — 5", 6", or 10" dash |

**Compatible AIM expansions:** GPS09c, Channel Expansion, TC Hub, Lambda Controller (LCU-One CAN), SmartyCam 3 Series, Formula Steering Wheel, Memory Module, K Keypads

**Part number (bare PDM, no GPS, no display):** `XC1PDM3201`
**CAN expansion cable (female Binder, 150 cm):** `V02579030`
**USB cable (3M712, 250 cm):** `V02563030`

### AIM PDM Dash 10"

| Spec | Value |
|------|-------|
| Display | 10" TFT |
| Resolution | 1280 × 480 pixels |
| Brightness | 800 cd/m² |
| Contrast | 1100:1 |
| Dimensions | 278.0 × 135.0 × 26.2 mm |
| Weight | 1000 g |
| Waterproof | IP65 |
| Shift light LEDs | 10 |
| Status info LEDs | 6 |
| Power consumption | 250 mA |
| Ambient light sensor | Yes |
| Connector | LVDS Link, 4-pin Rosenberger male |

**LVDS connector pinout (external view):**

| Pin | Signal |
|-----|--------|
| 1 | GND |
| 2 | Serial Data + |
| 3 | +V Power |
| 4 | Serial Data − |

**Part number (10" with icons):** `XC1D10000`
**LVDS cable 200 cm:** `FCCA682000`

---

## Core Configuration Concepts

The PDM uses a layered logic system. Think of it as a state machine:

```
Physical Inputs (switches/buttons)
        ↓
    [Keypads] — defines how an input behaves
        ↓
 [Status Variables] — tracks the current state
        ↓
  [Trigger Commands] — IF condition THEN action (with timers)
        ↓
  [Power Outputs] — what actually switches the load on/off
```

---

## 1. Keypads (Input Definitions)

**What they are:** Named definitions for each physical button or switch input connected to a PDM channel input.

### Button/Switch Types

| Type | Behavior | Use Case |
|------|----------|----------|
| **Momentary** | On only while pressed; off when released | Starter, horn, momentary trigger |
| **Latching / Toggle** | Two defined positions; stays in last position | Kill switch, light on/off |
| **Multi-position** | 3+ defined positions (0=rest, 1=pos1, 2=pos2, ...) | Light dimmer, fan speed selector |

**Rest status = Position 0** — this is the state the PDM boots into on power-up. Design your logic assuming the PDM will always start at rest.

### Naming Convention (Best Practice)
Name keypads descriptively, including where they came from:
- `Keypad_Starter` not just `Starter`
- `Keypad_FanHigh` not just `FanHigh`

This becomes critical when troubleshooting power output triggers — without the source in the name, you have to click into each trigger to find where an input came from.

### Feedback Indicators
The display can show keypad status color:
- **Green** = active/on as expected
- **Red** = activated (input on) but output not working → fault condition

This lets the driver know "I pushed the button but nothing happened — there's a fault."

---

## 2. Status Variables

**What they are:** Named state-tracking variables that hold the current condition (on/off/fault) of a logical function.

- Each function in the car should have a status variable
- Variables are updated by Trigger Commands (see below)
- Variables can be displayed on the AIM 10" dash
- Used as conditions in other trigger commands (variables referencing variables)

**Example:** `FuelPump_Status` variable is set to ACTIVE by:
- Timer (3-second startup prime)
- RPM condition (engine running)

Set to REST by:
- Timer expiry
- Engine off

---

## 3. Trigger Commands

**What they are:** IF/THEN rules that change Status Variables and control Power Outputs.

Each trigger has:
- **Condition:** What must be true to fire (keypad state, RPM, temp, timer, "always true", etc.)
- **Action:** What to do when condition is met (set variable to active/rest, turn output on/off)
- **Timer:** Optional delay before action executes

### Key Condition Types
| Condition | Example | Use |
|-----------|---------|-----|
| Keypad state | `Keypad_Starter = on` | Button-driven |
| Channel value | `RPM > 50` | Sensor-driven |
| Timer | `after 3 seconds` | Time-based sequencing |
| Variable state | `FuelPump_Status = active` | Cascaded logic |
| Always true | — | Unconditional (output always on) |
| Always false | — | Disable output |

### Fuel Pump Logic Example (from webinar)
This mimics how every production car handles fuel pump priming:

```
Trigger 1 (startup prime):
  CONDITION: System boots (timer starts)
  ACTION:    FuelPump_Status → ACTIVE
  TIMER:     3 seconds, then → REST

Trigger 2 (engine running):
  CONDITION: RPM > 50
  ACTION:    FuelPump_Status → ACTIVE immediately
```

Result:
- On key-on: pump runs for 3 seconds to build fuel pressure, then shuts off
- On engine crank/start: pump turns on immediately as soon as engine fires (RPM > 50)
- Engine stall: RPM drops below 50 → pump stops (safety)

### Starter Logic Example
```
Trigger:
  CONDITION: Keypad_Starter = on (momentary while button held)
  ACTION:    Starter output → ON (continuous power, inductive)
```

Note: Use "continuous power, inductive load" output type for the starter — it has the freewheeling diode needed for relay coil/motor protection.

---

## 4. Power Outputs

**What they are:** The actual PDM output channels that switch voltage to loads.

### Output Configuration for Each Channel
1. **Output type** — determines driver behavior:
   - `Continuous power` — always on while condition true
   - `Inductive load` — for motors, solenoids, relays (uses freewheeling diode)
   - `PWM` — pulse-width modulated for variable-speed control
2. **Trigger condition** — references a Status Variable or Keypad state
3. **Overcurrent protection** — set trip current for each output (PDM will cut if exceeded and flag a fault)

### Output Current Ratings (from pdm-pinout.md)
| Output Type | Count | Notes |
|-------------|-------|-------|
| High power | 4 (dual-pin) | For high-current loads: fan motors, etc. High Power Out 1 has series diode |
| Half bridge | 4 (dual-pin, Conn B) | Bidirectional drive — useful for reversible loads |
| Mid power | 12 (single pin) | Relays, moderate loads |
| Low power | 12 (single pin) | Logic-level outputs, small loads |

---

## 5. PWM (Pulse Width Modulation) for Fan Control

**Use case:** Controlling brushless fan speed automatically based on coolant temperature.

**Setup:**
- Fan wired directly to battery (gets its own power)
- PDM PWM output controls the fan speed signal (0–100% duty cycle)
- Create a table: `Coolant Temp → PWM duty cycle`
  - e.g., 180°F → 20%, 200°F → 60%, 220°F → 100%
- Fully automated — driver does not need to manage it

**Why automate:** Drivers have enough to manage; fan control should be transparent. Also produces data: the PDM logs current draw over time, so post-race analysis can show when the fan was working hardest.

**Post-race data value:** PDM current data on fan/pump channels shows:
- Peak thermal events during the session
- Whether cooling system is keeping up
- Pump health (current draw change = wear indicator)

---

## 6. Multi-Position Example (Lights)

```
Keypad: Lights
  Position 0 (rest) = off
  Position 1 = running lights
  Position 2 = full bright
```

Triggers:
- `Lights = position 0` → all light outputs OFF
- `Lights = position 1` → running light outputs ON
- `Lights = position 2` → all light outputs ON

---

## White Tiburon — Finalized PDM Configuration

> Full Race Studio 3 setup (status variables, trigger logic, protection settings, step-by-step): `builds/white-tiburon/guides/pdm-config.md`
>
> **CAN keypad excluded from this build.** All driver controls use a physical switch panel. CAN2 bus unused.

### Physical Inputs (8 inputs — physical switch panel)

| Input | PDM Connection | Type | Purpose |
|-------|----------------|------|---------|
| **Ignition switch** | Conn B pin 23 (Ignition input) | Latching toggle | Master power state (`SafeIgnition`). Also spliced to Haltech 34-pin pin 13 (ECU IGN enable). |
| **Fan override** | Ch01 — B26 | Latching toggle, 12V | Manual fan 98% override |
| **Wiper Low** | Ch02 — B27 | Latching toggle, 12V | Wiper motor low speed |
| **Wiper High** | Ch03 — B28 | Latching toggle, 12V | Wiper motor high speed (overrides low) |
| **Coolsuit** | Ch04 — B29 | Latching toggle, 12V | Coolsuit pump on/off |
| **Defogger** | Ch05 — B30 | Latching toggle, 12V | Rear window defogger |
| **Start button** | Ch09 — B21 | Momentary, active = GND | Crank engine — gated by ignition + RPM interlock |
| **Brake switch** | Ch11 — A26 | Closed on press | Brake lights — always active, independent of ignition |

### Power Output Map (Finalized)

| Output | Name | PDM Pins | Mode | Limit | Trigger |
|--------|------|----------|------|-------|---------|
| HP1 | Starter | A1 + A13 | OVC Protected | 20A | `STARTER_SAFE` = Ch09 AND IGN AND NOT RPM |
| HP2 | Fan | A12 + A23 | Fused, PWM 100Hz | 35A | ECT 4-band PWM (77–92°C) + Ch01 override |
| HP3 | Fuel Pump | A24 + A25 | OVC Protected | 15A | 3s IGN prime OR RPM > 50 |
| HP4 | Spare | A34 + A35 | — | — | — |
| MP1 | InjectorPwr | A2 | OVC Protected | 15A | `SafeIgnition` |
| MP2 | CoilPwr | A3 | OVC Protected | 15A | `SafeIgnition` |
| MP3 | WiperLow | A4 | OVC Protected | 10A | Ch02 AND NOT Ch03 |
| MP4 | BrakeLights | A5 | Fused | 10A | Ch11 brake switch |
| MP5 | TailLights | A6 | Fused | 10A | `SafeIgnition` (always on) |
| MP6 | WiperHigh | A7 | OVC Protected | 10A | Ch03 |
| MP7 | Coolsuit | A8 | OVC Protected | 10A | Ch04 AND SafeIgnition |
| MP8 | Defogger | A9 | OVC Protected | 10A | Ch05 AND SafeIgnition |
| LP1 | ECU Power | A14 | OVC Protected | 10A | `SafeIgnition` |
| LP2 | Dash | A15 | OVC Protected | 10A | `SafeIgnition` |
| LP3 | SmartyCam | A16 | OVC Protected | 10A | `SafeIgnition` |
| LP4 | GPS | A17 | OVC Protected | 10A | `SafeIgnition` |
| LP5 | Wideband | A18 | OVC Protected | 10A | `SafeIgnition` |
| LP6 | Cluster | A19 | OVC Protected | 10A | `SafeIgnition` |
| LP7 | WarningLED | A20 | OVC Protected | 5A | `MULTI_WARNING` |
| LP8 | AltExciter | A21 | OVC Protected | 5A | `SafeIgnition` — OEM alternator D+ field wire |

> **MP1/MP2 Phase 1 (stock ECU):** Wired to OE relay box main relay pin 87 (relay pulled). Provides switched 12V to stock ECU. **Phase 2 (Haltech):** MP1 → injector rail + Haltech pin 26; MP2 → COP Pin D bus. No Race Studio change.

### CAN Bus Configuration

AIM's official pin labels (from PDM32 tech sheet Ver. 1.17):

| Bus Label | PDM Pins | Device | Speed | RS3 Tab | Notes |
|-----------|----------|--------|-------|---------|-------|
| **CAN AiM** | A22 (H) / A11 (L) | AIM expansion bus | 1 Mbps | SmartyCam Stream / Channels | GPS-08, SmartyCam, Podium via 4-way Data Hub. Pre-wired expansion cable. Pins A10/A11/A22/A32/A33 reserved. |
| **CAN ECU** | A30 (H) / A31 (L) | Haltech Elite 2500 | 500 kbps | ECU Stream | RPM, ECT, Oil P, Oil T, Fuel P → fuel pump, fan PWM, alarms. Shared with RS232 TX/RX — RS232 unavailable when CAN ECU active. |
| **CAN2** | A28 (H) / A29 (L) | **Unused** | — | — | CAN keypad excluded. Available for future expansion. |

> **Note on RS3 tab naming:** The RS3 "ECU Stream" tab controls the **CAN ECU** bus (A30/A31). The "CAN AiM" expansion bus (A22/A11) is configured through the SmartyCam Stream tab and is where the GPS-08 auto-broadcasts. There is no dedicated "CAN AiM" tab — the expansion bus is always-on at 1 Mbps.

---

## Configuration Tips (from Robbie Yeoman)

1. **Label everything from the source** — `Keypad_Starter` not just `Starter`
2. **Rest state = boot state** — design all logic assuming rest = key-off / engine-off condition
3. **Use timers for sequencing** — startup priming, cooldown fans, etc.
4. **Leverage CAN data** — don't duplicate analog signals; use ECU CAN broadcast for RPM/temp/speed
5. **Monitor current data post-race** — PDM logs current per channel; spikes indicate faults
6. **Test each output in Race Studio** — you can manually toggle outputs before wiring to verify logic
7. **Fault indicators on dash** — configure display to show output status; red = triggered but not responding

---

## Related Files
| File | Contents |
|------|----------|
| `aim-pdm/pdm-pinout.md` | Full connector pinout (both 35-pin connectors) |
| `builds/white-tiburon/guides/pdm-config.md` | Full Race Studio 3 config: status vars, triggers, LED colors, step-by-step setup |
| `cars/white-tiburon-weekend-tasks.md` | Wiring bundle assignments and build task list |
| `haltech/main-connector-26-pin-elite2500.md` | Haltech CAN bus pins (23=H, 24=L) |
