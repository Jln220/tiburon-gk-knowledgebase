# AIM PDM32 Race Studio 3 Configuration Guide — White Tiburon

## Overview

Complete Race Studio 3 configuration for the AIM PDM32 + AIM CAN Keypad 12 in the white 2003 Tiburon GK race car. Based on analysis of the AIM "I Have a PDM Now What" webinar config (`Webinar complete.zconfig`), adapted for the Tiburon's Haltech Elite 2500 + COP ignition + CAN keypad control scheme.

> **`.zconfig` files** use proprietary internal UIDs and cross-referenced channel indices managed by Race Studio 3. The starting-point file `Tiburon_White_v1_base.zconfig` has output names and settings pre-configured but trigger logic must be finalized in Race Studio 3.
>
> **Note:** `Tiburon_White_v1_base.zconfig` and `Webinar complete.zconfig` are Race Studio 3 project files — they live on the laptop running Race Studio, not in this repo. Export a backup copy to `AIM PDM/` after each major config change.

---

## Control Scheme

### Physical Inputs (2 only)

| Input | Type | PDM Connection | Purpose |
|---|---|---|---|
| **Ignition switch** | Toggle (latching) | PDM Ignition Input (Conn B pin 23) | Master power — keeps PDM powered with engine off (for config, testing, accessories) |
| **Start button (backup)** | Momentary push | PDM Channel Input Ch09 | Physical backup for CAN keypad start button |

### CAN Keypad 12 (Primary Controls)

Connected to **PDM CAN2** bus at **125 kbps** (standard AIM keypad baud rate).

```
AIM CAN Keypad 12 — Tiburon Button Layout
==========================================

  [01 START]  [02 HORN ]  [03 LIGHT]  [04 COOL ]
  [05 FAN+ ]  [06 FUEL+]  [07 PIT  ]  [08 WIPER]
  [09 YES  ]  [10 PIT# ]  [11 spare]  [12 spare]

Physical switch panel:
  [IGN toggle]  [START backup pushbutton]  (RED multi-warning LED)

Key 09: Comms Yes/No toggle — sends affirmative/negative to PodiumConnect
Key 10: Pit-in timer — each press cycles: off → 1 lap → 2 laps → 3 laps → off
```

### Warning Light

| Output | Type | Connection | Trigger |
|---|---|---|---|
| **Red LED** | PDM low-power output (LP7 or spare) | Wire to switch panel LED | Multi-warning: Low oil P OR High coolant T OR High oil T OR Low fuel P |

---

## Webinar Config Mapping

The webinar config already implements keypad-driven control with a physical backup starter. Here's how the webinar maps to the Tiburon:

| Webinar Key | Webinar Function | Webinar Status Var | Tiburon Key | Tiburon Function | Changes Needed |
|---|---|---|---|---|---|
| Key 01 | Fan override | FanKYD | **Key 05** | Fan manual 100% | Remap key number |
| Key 02 | Lights | LightsKYD | **Key 03** | Tail/running lights | Remap key number |
| Key 03 | Siren/Horn | SirenKYD | **Key 02** | Horn | Rename siren → horn |
| Key 04 | Starter | StarterKYD | **Key 01** | Start (primary) | Remap key number |
| Key 05 | Ignition relay | IgnitionKYD | *removed* | **Physical switch** | Replace keypad with Conn B pin 23 |
| Key 06 | Spare | K06 | **Key 06** | Fuel pump override | New logic |
| Key 07 | Previous page | PreviousKYD | **Key 07** | Pit limiter (safety-gated) | New logic |
| Key 08 | Next page | NextKYD | **Key 08** | Wiper | New logic |
| *New* | — | — | **Key 09** | Comms Yes/No (PodiumConnect) | New — add COMMS_YN latching toggle |
| *New* | — | — | **Key 10** | Pit-In X Laps (PodiumConnect) | New — add PITIN_LAPS multi-position (4 pos) |
| Ch09 | Backup start button | momentary SW | **Ch09** | Backup start button | **No change** |

### Status Variables Carried Forward

These webinar status variables are directly reusable:

| Variable | Logic | Used By |
|---|---|---|
| `StarterKYD` | Latched toggle from keypad start button | Starter trigger |
| `SirenKYD` | Momentary from keypad horn button | Horn trigger |
| `LightsKYD` | Latched toggle from keypad lights button | Lights trigger |
| `FanKYD` | Latched toggle from keypad fan button | Fan manual override |
| `FuelSV` | Composite: SafeIgnition AND RPM conditions | Fuel pump run logic |
| `SafeIgnition` | Ignition input is ON and stable | Master permissive for engine outputs |
| `FlashSV` | Momentary flash state | High beam flash (if applicable) |
| `FANOFFSV` | Fan override off state | Fan manual disable |

### Status Variables to Add

| Variable | Logic | Used By |
|---|---|---|
| `ENGINE_RUNNING` | CAN RPM > 50 | Starter interlock, fuel pump, oil P alarm |
| `FUEL_PRIME` | 3s one-shot timer on SafeIgnition rising edge | Fuel pump prime |
| `FAN_TEMP_25` | CAN Coolant_T > 80°C AND <= 85°C (hysteresis -5°C) | Fan 25% band |
| `FAN_TEMP_50` | CAN Coolant_T > 85°C AND <= 90°C | Fan 50% band |
| `FAN_TEMP_75` | CAN Coolant_T > 90°C AND <= 95°C | Fan 75% band |
| `FAN_TEMP_100` | CAN Coolant_T > 95°C | Fan 98% band |
| `FAN_FAILSAFE` | CAN coolant_T signal timeout > 5s | Fan 98% failsafe |
| `STARTER_SAFE` | (StarterKYD OR Ch09) AND SafeIgnition AND NOT ENGINE_RUNNING | Safe to crank |
| `LOW_OIL_P` | CAN Oil_P < 15 PSI AND ENGINE_RUNNING AND RPM > 500 | Warning light |
| `HIGH_COOLANT_T` | CAN Coolant_T > 105°C | Warning light |
| `HIGH_OIL_T` | CAN Oil_T > 130°C | Warning light |
| `LOW_FUEL_P` | CAN Fuel_P < 30 PSI AND ENGINE_RUNNING AND RPM > 500 | Warning light |
| `MULTI_WARNING` | LOW_OIL_P OR HIGH_COOLANT_T OR HIGH_OIL_T OR LOW_FUEL_P | Red LED trigger |
| `CoolsuitKYD` | Latched toggle from keypad Key 04 | Coolsuit pump |
| `FuelOverride` | Latched toggle from keypad Key 06 | Manual fuel pump on |
| `PitLimiter_KYD` | Latched toggle from keypad Key 07 | Raw keypad state |
| `PITLIMITER_SAFE` | PitLimiter_KYD AND CAN Speed < 60 mph | Safe to engage — blocks accidental on-track activation |
| `PITLIMITER_ACTIVE` | PITLIMITER_SAFE AND NOT (TPS > 60%) | Active limiter state sent to Haltech; TPS override always available |
| `COMMS_YN` | Latched toggle from keypad Key 09 | PodiumConnect affirmative/negative signal |
| `PITIN_LAPS` | Multi-position from keypad Key 10 (0/1/2/3) | PodiumConnect pit-in request with lap count |

---

## Power Output Configuration

### Output Map

| Output | Name | Mode | MaxLoad | Inductive | PWM | Trigger |
|---|---|---|---|---|---|---|
| **HP1** | Starter | OVC Protected | 20A | **Yes** | DC | STARTER_SAFE |
| **HP2** | Fan | Fused | 35A | No | 100Hz | ECT PWM curve + FanKYD override |
| **HP3** | FuelPump | OVC Protected | 15A | **Yes** | DC | FUEL_PRIME OR ENGINE_RUNNING OR FuelOverride |
| HP4 | Spare | -- | 20A | -- | -- | -- |
| **MP1** | InjectorPwr | OVC Protected | 15A | **Yes** | DC | SafeIgnition |
| **MP2** | CoilPwr | OVC Protected | 15A | No | DC | SafeIgnition |
| **MP3** | Horn | OVC Protected | 15A | No | DC | SirenKYD (Key 02, momentary) |
| **MP4** | BrakeLights | Fused | 10A | No | DC | BRAKE_SWITCH (physical, always active) |
| **MP5** | TailLights | Fused | 10A | No | DC | LightsKYD (Key 03, toggle) |
| MP6 | Spare | -- | 15A | -- | -- | -- |
| **MP7** | Coolsuit | OVC Protected | 10A | **Yes** | DC | CoolsuitKYD (Key 04, toggle) |
| MP8 | Spare | -- | 15A | -- | -- | -- |
| **LP1** | ECU_Power | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP2** | Dash | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP3** | SmartyCam | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP4** | GPS | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP5** | Wideband | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP6** | Cluster | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP7** | WarningLED | OVC Protected | 5A | No | DC | MULTI_WARNING |

### Detailed Output Logic

#### HP1: Starter

```
Trigger: STARTER_SAFE
  = (StarterKYD [Key 01 press] OR Ch09 [physical backup button])
    AND SafeIgnition [IGN switch ON]
    AND NOT ENGINE_RUNNING [CAN RPM < 50]

Properties:
  Mode: OVC Protected
  Max Load: 20A
  Inductive: YES (starter solenoid)
  OVC Retries: 1, Latch Off: 5s

Safety:
  - RPM interlock prevents cranking into running engine
  - HP1 series diode prevents back-EMF to PDM
  - Add 10s timeout: if HP1 ON > 10s → force off (motor protection)
  - Physical backup button on Ch09 works independently of keypad
```

#### HP2: Fan (4-Level Priority PWM)

```
Fan speed is driven by CAN coolant temp from Haltech, with manual override.

Action 1: ON @ 25% duty  | Priority 1 | Trigger: FAN_TEMP_25 (80-85°C)
Action 2: ON @ 50% duty  | Priority 2 | Trigger: FAN_TEMP_50 (85-90°C)
Action 3: ON @ 75% duty  | Priority 3 | Trigger: FAN_TEMP_75 (90-95°C)
Action 4: ON @ 98% duty  | Priority 4 | Trigger: FAN_TEMP_100 (>95°C) OR FAN_FAILSAFE

Manual override: FanKYD (Key 05) → 98% duty, Priority 5 (highest)

Properties:
  Mode: Fused (auto-disable on overcurrent)
  Max Load: 35A
  PWM Freq: 100 Hz
  Soft Start: 1.0s (reduce inrush)

Hysteresis: Each band has 5°C hysteresis (ON at threshold, OFF at threshold - 5°C)
Failsafe: If CAN coolant temp signal lost > 5s → 98% duty
```

#### HP3: Fuel Pump

```
Trigger: FUEL_PRIME OR ENGINE_RUNNING OR FuelOverride

  FUEL_PRIME:   3s one-shot timer on SafeIgnition rising edge
  ENGINE_RUNNING: CAN RPM > 50 (with 2s off-delay for stall protection)
  FuelOverride:  Key 06 toggle (manual override, e.g., for priming/testing)

Properties:
  Mode: OVC Protected
  Max Load: 15A
  Inductive: YES (pump motor)
  OVC Retries: 3 (pump may spike on initial prime)
  Latch Off: 5s

Haltech DPO 5 (34-pin pin 24, B/Y) can also be wired to a PDM channel input
as an additional permissive or alternative trigger from the ECU side.
```

#### MP4: Brake Lights

```
Trigger: BRAKE_SWITCH (physical brake switch, always active)

NOTE: Brake lights MUST work even if keypad is disconnected.
Wire brake switch directly to PDM Channel Input Ch11.
Do NOT route through keypad.

Properties:
  Mode: Fused
  Max Load: 10A
```

#### LP7: Multi-Warning Red LED

```
Trigger: MULTI_WARNING
  = LOW_OIL_P OR HIGH_COOLANT_T OR HIGH_OIL_T OR LOW_FUEL_P

LOW_OIL_P:     CAN Oil_Pressure < 15 PSI AND RPM > 500
HIGH_COOLANT_T: CAN Coolant_Temp > 105°C
HIGH_OIL_T:    CAN Oil_Temp > 130°C
LOW_FUEL_P:    CAN Fuel_Pressure < 30 PSI AND RPM > 500

RPM > 500 guard prevents false alarms at idle/cranking.

Properties:
  Mode: OVC Protected
  Max Load: 5A (LED draws < 0.5A)
  Can optionally PWM the LED for blinking effect (PWM 2Hz, 50% duty)
```

---

#### Key 07: Pit Limiter — Safety Implementation

```
PITLIMITER_SAFE conditions (PDM side):
  PitLimiter_KYD = ON    (Key 07 latched)
  AND CAN Speed < 60 mph  (speed gate — prevents on-track accidental engage)

If Key 07 pressed while speed > 60 mph:
  → PitLimiter_KYD = ON (latched) but PITLIMITER_ACTIVE = OFF
  → Key 07 LED turns RED (indicates keypad requested, but not safe to engage)
  → When speed drops below 60 mph → automatically activates

PITLIMITER_ACTIVE = PITLIMITER_SAFE AND NOT (TPS > 60%)
  TPS override: any instant with TPS > 60% temporarily releases the limiter
  Useful for: short burst to clear traffic then re-engages if still toggled on

To exit: press Key 07 again (toggle off) — immediate full release

Haltech side (NSP Speed Limiter configuration):
  Target speed: 35 mph (adjust per track pit lane limit)
  Enable signal option A: PDM CAN0 transmit message → Haltech custom CAN receive
    - Configure PDM to broadcast PITLIMITER_ACTIVE state on CAN0
    - Configure Haltech NSP to receive that CAN byte and enable speed limiter
  Enable signal option B: Wire spare PDM LP output → Haltech SPI 2/3/4 pin
    - Configure Haltech SPI pin as digital input in NSP
    - 12V = limiter on, 0V = off
  Recommended: Option A (CAN) — zero extra wire
```

---

#### Keys 09 & 10: PodiumConnect Pit Communication

```
Key 09 — COMMS YES/NO (latching toggle):
  Position 0 (rest/off): No pending message
  Position 1 (on):       Affirmative / "Yes" / "Understood"

  LED behavior:
    COMMS_YN = off → dim (no color)
    COMMS_YN = on  → BRIGHT GREEN

  To say "no": toggle off (treat off state as "no response" or configure
  a second press to cycle to a RED "no" state if Race Studio allows 3-pos)

Key 10 — PIT-IN REQUEST (multi-position, 4 states):
  Position 0 → OFF (no pit request) — LED off
  Position 1 → Pit in 1 lap       — LED dim white
  Position 2 → Pit in 2 laps      — LED medium white
  Position 3 → Pit in 3 laps      — LED bright white
  Each press of Key 10 advances one position; wraps back to 0 after 3.

PodiumConnect CAN integration:
  Both COMMS_YN and PITIN_LAPS values are transmitted to the AIM Podium
  module via the AIM device CAN bus (CAN1). The Podium forwards these to
  PodiumConnect where the team engineer sees the flag/request.

  CAN message configuration: Set up in Race Studio 3 under CAN Outputs
  pointing to the Podium's CAN address. Exact message IDs and byte mapping
  depend on the Podium firmware version — confirm in Race Studio 3 when
  Podium module is connected and recognized.

  Expected display on PodiumConnect:
    COMMS_YN = 1  → "Driver: YES" flag
    PITIN_LAPS = 1/2/3 → "Pit In: X laps" flag
```

---

## CAN Bus Configuration

### CAN0 (PDM Conn A pins 22/11) — Haltech ECU

| Setting | Value |
|---|---|
| Protocol | Haltech Elite 2500 |
| Speed | 500 kbps |
| Termination | External 120Ω |
| Data used | RPM, Coolant Temp, Oil Pressure, Oil Temp, Fuel Pressure, TPS |

### CAN1 — AIM Device Chain

| Setting | Value |
|---|---|
| Devices | AIM Dash → GPS → SmartyCam → Podium |
| Speed | 1 Mbps (AIM standard) or 500 kbps |
| Note | Dash may use LVDS instead of CAN1 |

### CAN2 — AIM CAN Keypad 12

| Setting | Value |
|---|---|
| Device | AIM CAN Keypad 12 |
| Speed | 125 kbps (AIM keypad standard) |
| Buttons | 12 buttons with RGB LED feedback |
| Connection | Dedicated CAN2 bus on PDM |

---

## Keypad LED Color Assignments

Configure in Race Studio 3 → CAN Output 2 (Keypad):

| Key | Function | LED Off | LED Active | Notes |
|---|---|---|---|---|
| 01 | Start | Dim green | Bright green | Momentary press |
| 02 | Horn | Dim yellow | Bright yellow | Momentary (hold to honk) |
| 03 | Lights | Dim blue | Bright blue | Toggle on/off |
| 04 | Coolsuit | Dim cyan | Bright cyan | Toggle on/off |
| 05 | Fan Override | Dim red | Bright red | Toggle — RED = manual override active |
| 06 | Fuel Override | Dim red | Bright red | Toggle — for priming/testing |
| 07 | Pit Limiter | Dim white | Bright white = active; RED if engaged above 60 mph (PITLIMITER_SAFE = false) | Toggle; safety-gated |
| 08 | Wiper | Dim white | Bright white | Toggle |
| 09 | Comms Yes/No | Off | Green = Yes / Red = No | Toggle cycles between states; for PodiumConnect quick ACK |
| 10 | Pit-In Laps | Off | White dim=1 lap / White=2 laps / Bright white=3 laps | Multi-position cycles 0→1→2→3→0 |
| 11-12 | Spare | Off | -- | Available |

The webinar config includes LED color control channels (`ColorsConditionK01` through `ClK08`, plus `BitRedX15`, `BitGreenX15`, `BitBlueX15`). These drive the RGB LEDs based on status variable states.

---

## PDM Channel Input Wiring

With keypad handling most controls, only 3 physical inputs are needed:

| PDM Input | Assignment | Type | Wiring |
|---|---|---|---|
| **Conn B pin 23** | Ignition switch | Built-in IGN input | Latching toggle switch. 12V when ON. |
| **Ch09** | Start backup button | Digital (momentary) | Push button → channel input, active = grounded |
| **Ch11** | Brake light switch | Digital | Brake pedal switch → channel input, closed on press |

Ch10, Ch12, and others are **available** for future physical inputs.

---

## Step-by-Step Race Studio 3 Setup

### 1. Open Starting Config

Open `Tiburon_White_v1_base.zconfig` in Race Studio 3. Output names and basic settings are pre-configured.

### 2. Configure CAN1 Stream (Haltech)

1. Go to Configuration → CAN1 Stream
2. Select **Haltech Elite** as ECU protocol (or import Haltech CAN DBC)
3. Verify these channels appear: RPM, Coolant Temp (ECT), Oil Pressure, Oil Temp, Fuel Pressure, TPS
4. If Haltech is not in the preset list: manually add CAN messages per `opengk/can-bus-messages.md`

### 3. Configure CAN2 Keypad

1. Go to Configuration → CAN2 Keypad
2. Select **AIM CAN Keypad 12**
3. The webinar config already has 8 keypad definitions — remap button numbers:
   - Rename StarterKYD button assignment from Key 04 → **Key 01**
   - Rename SirenKYD (horn) from Key 03 → **Key 02**
   - Rename LightsKYD from Key 02 → **Key 03**
   - Add CoolsuitKYD on **Key 04** (new latching toggle)
   - Rename FanKYD from Key 01 → **Key 05**
   - Add FuelOverride on **Key 06** (new latching toggle)
   - Set Key 07 for Pit Limiter (safety-gated — see Pit Limiter section)
   - Set Key 08 for Wiper (latching toggle)
   - Add COMMS_YN on **Key 09** (latching toggle — PodiumConnect Yes/No)
   - Add PITIN_LAPS on **Key 10** (multi-position 0/1/2/3 — PodiumConnect pit request)

### 4. Configure Channel Inputs

1. **Ch09** → "START_BACKUP" — Digital status, momentary, active = ground
2. **Ch11** → "BRAKE_SWITCH" — Digital status, closed when pedal pressed
3. All other channel inputs → leave at defaults (available for future)

### 5. Create Status Variables

In Configuration → Math Channels:

1. `ENGINE_RUNNING` = CAN RPM > 50 (with 2s off-delay)
2. `FUEL_PRIME` = Timer(SafeIgnition rising edge, 3000ms, one-shot)
3. `FAN_TEMP_25` through `FAN_TEMP_100` = CAN ECT band comparisons
4. `FAN_FAILSAFE` = CAN ECT timeout > 5s
5. `STARTER_SAFE` = (StarterKYD OR Ch09) AND SafeIgnition AND NOT ENGINE_RUNNING
6. `LOW_OIL_P` = CAN Oil_P < 15 AND ENGINE_RUNNING AND CAN RPM > 500
7. `HIGH_COOLANT_T` = CAN ECT > 105
8. `HIGH_OIL_T` = CAN Oil_T > 130
9. `LOW_FUEL_P` = CAN Fuel_P < 30 AND ENGINE_RUNNING AND CAN RPM > 500
10. `MULTI_WARNING` = LOW_OIL_P OR HIGH_COOLANT_T OR HIGH_OIL_T OR LOW_FUEL_P

### 6. Assign Triggers to Power Outputs

Wire each status variable to its power output per the Output Map table above.

### 7. Configure LED Colors

In CAN Output 2 (Keypad), set RGB values for each key state per the LED Color table.

### 8. Configure Warning LED Output

Enable LP7, set trigger to `MULTI_WARNING`, optionally set PWM for blinking.

### 9. Transmit and Test

1. Save configuration
2. Transmit to PDM via USB
3. Force-test each output in Race Studio 3
4. Verify keypad button presses activate correct outputs
5. Verify brake lights work with physical switch only (no keypad required)
6. Verify backup start button on Ch09 cranks the starter

---

## Protection Settings Summary

| Output | Mode | MaxLoad | Inductive | OVC Retries | Latch Off | Soft Start |
|---|---|---|---|---|---|---|
| HP1 Starter | OVC Protected | 20A | Yes | 1 | 5s | No |
| HP2 Fan | Fused | 35A | No | -- | -- | 1.0s |
| HP3 FuelPump | OVC Protected | 15A | Yes | 3 | 5s | No |
| MP1 InjectorPwr | OVC Protected | 15A | Yes | 1 | 5s | No |
| MP2 CoilPwr | OVC Protected | 15A | No | 1 | 5s | No |
| MP3 Horn | OVC Protected | 15A | No | 1 | 5s | No |
| MP4 BrakeLights | Fused | 10A | No | -- | -- | No |
| MP5 TailLights | Fused | 10A | No | -- | -- | No |
| MP7 Coolsuit | OVC Protected | 10A | Yes | 1 | 5s | No |
| LP1-6 Accessories | OVC Protected | 10A | No | 1 | 5s | No |
| LP7 WarningLED | OVC Protected | 5A | No | 1 | 5s | No |

---

## Alarm Thresholds (Tune on Track)

These are starting values — adjust based on engine behavior:

| Alarm | Threshold | Guard | Notes |
|---|---|---|---|
| Low oil pressure | < 15 PSI | RPM > 500 | Normal hot idle may be 20-30 PSI |
| High coolant temp | > 105°C | Always active | Thermostat opens ~82°C |
| High oil temp | > 130°C | Always active | Normal operating ~90-110°C |
| Low fuel pressure | < 30 PSI | RPM > 500 | Stock rail ~45-55 PSI |
| Fan ON | > 80°C | Always active | First band (25%) |
| Fan 100% | > 95°C | Always active | Emergency cooling |
| Fan failsafe | CAN timeout 5s | Always active | Full speed if CAN lost |
| Starter timeout | > 10s continuous | Always active | Motor protection |

---

## Cross-References

| File | Contents |
|---|---|
| `aim-pdm/pdm-pinout.md` | Full 35-pin ×2 connector pinout |
| `aim-pdm/pdm-configuration-guide.md` | Logic stack theory, keypad config, PWM examples |
| `signal-routing.md` | End-to-end signal trace for every wire |
| `opengk/can-bus-messages.md` | CAN message IDs and byte definitions |
| `cars/cop-ignition.md` | COP coil pinout and NSP settings |
| `cars/lowdoller-sensors.md` | Sensor specs and PTC calibration tables |
| `tiburon_haltech_pdm_installation_guide_v1_final.docx` | Physical installation procedure |
| `Tiburon_White_v1_base.zconfig` | Starting-point Race Studio 3 config file |
| `Webinar complete.zconfig` | Original AIM webinar config (reference) |
