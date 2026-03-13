# AIM PDM32 Race Studio 3 Configuration Guide — White Tiburon

## Overview

Complete Race Studio 3 configuration for the AIM PDM32 with physical switch panel in the white 2003 Tiburon GK race car. Based on analysis of the AIM "I Have a PDM Now What" webinar config (`Webinar complete.zconfig`), adapted for the Tiburon's Haltech Elite 2500 + COP ignition + physical toggle switch control scheme.

> **CAN keypad excluded from this build.** All driver controls use a physical switch panel with 6 toggle switches and 1 momentary starter button. CAN2 bus is unused and available for future expansion.

> **`.zconfig` files** use proprietary internal UIDs and cross-referenced channel indices managed by Race Studio 3. The starting-point file `Tiburon_White_v1_base.zconfig` has output names and settings pre-configured but trigger logic must be finalized in Race Studio 3.
>
> **Note:** `Tiburon_White_v1_base.zconfig` and `Webinar complete.zconfig` are Race Studio 3 project files — they live on the laptop running Race Studio, not in this repo. Export a backup copy to `AIM PDM/` after each major config change.

---

## Control Scheme

### Physical Switch Panel

All driver controls are physical switches wired directly to PDM channel inputs. No CAN keypad.

```
Switch Panel Layout
====================

Toggle switches (latching):
  [IGN]  [FAN]  [WPR LO]  [WPR HI]  [COOL]  [DEFOG]

Momentary:
  [START]                                       (RED multi-warning LED)
```

### Switch Assignments

| Switch | Type | PDM Connection | Purpose |
|---|---|---|---|
| **Ignition** | Toggle (latching) | PDM Ignition Input (Conn B pin 23) | Master power — keeps PDM powered with engine off (for config, testing, accessories) |
| **Start** | Momentary push | PDM Channel Input Ch09 (B21) | Crank engine — gated by ignition and RPM interlock |
| **Fan** | Toggle (latching) | PDM Channel Input Ch01 (B26) | Manual fan override — forces fan to 98% regardless of coolant temp |
| **Wiper Low** | Toggle (latching) | PDM Channel Input Ch02 (B27) | Wiper motor low speed |
| **Wiper High** | Toggle (latching) | PDM Channel Input Ch03 (B28) | Wiper motor high speed (overrides low) |
| **Coolsuit** | Toggle (latching) | PDM Channel Input Ch04 (B29) | Coolsuit pump on/off |
| **Defogger** | Toggle (latching) | PDM Channel Input Ch05 (B30) | Rear window defogger on/off |

### Warning Light

| Output | Type | Connection | Trigger |
|---|---|---|---|
| **Red LED** | PDM low-power output (LP7) | Wire to switch panel LED | Multi-warning: Low oil P OR High coolant T OR High oil T OR Low fuel P |

---

## PDM Channel Input Wiring

7 physical switches + 1 brake switch use 7 channel inputs plus the dedicated ignition input:

| PDM Input | Pin | Assignment | Type | Wiring |
|---|---|---|---|---|
| **Ignition Input** | B23 | Ignition switch | Built-in IGN input | Latching toggle. 12V when ON. |
| **Ch01** | B26 | Fan override | Digital, latching toggle | 12V when ON |
| **Ch02** | B27 | Wiper Low | Digital, latching toggle | 12V when ON |
| **Ch03** | B28 | Wiper High | Digital, latching toggle | 12V when ON |
| **Ch04** | B29 | Coolsuit | Digital, latching toggle | 12V when ON |
| **Ch05** | B30 | Defogger | Digital, latching toggle | 12V when ON |
| **Ch09** | B21 | Start button | Digital, momentary | Momentary, active = grounded |
| **Ch11** | A26 | Brake light switch | Digital | Brake pedal switch, closed on press |

Ch06, Ch07, Ch08, Ch10, Ch12 are **available** for future inputs.

---

## Status Variables

### Carried Forward from Webinar Config

These webinar status variables are directly reusable:

| Variable | Logic | Used By |
|---|---|---|
| `SafeIgnition` | Ignition input is ON and stable (built-in) | Master permissive for engine outputs |
| `FuelSV` | Composite: SafeIgnition AND RPM conditions | Fuel pump run logic |

### Status Variables — Full List

| Variable | Logic | Used By |
|---|---|---|
| `ENGINE_RUNNING` | CAN RPM > 50 | Starter interlock, fuel pump, oil P alarm |
| `FUEL_PRIME` | 3s one-shot timer on SafeIgnition rising edge | Fuel pump prime |
| `FAN_TEMP_25` | CAN Coolant_T > 77°C (hysteresis -5°C, off at 72°C) | Fan 25% band — 170°F thermostat starts opening at 77°C |
| `FAN_TEMP_50` | CAN Coolant_T > 82°C (hysteresis -5°C) | Fan 50% band |
| `FAN_TEMP_75` | CAN Coolant_T > 87°C (hysteresis -5°C) | Fan 75% band |
| `FAN_TEMP_100` | CAN Coolant_T > 92°C | Fan 98% band — thermostat est. fully open at ~92°C |
| `FAN_FAILSAFE` | CAN coolant_T signal timeout > 5s | Fan 98% failsafe |
| `STARTER_SAFE` | (StarterKYD OR Ch09_START_BACKUP) AND SafeIgnition AND NOT ENGINE_RUNNING | Safe to crank |
| `LOW_OIL_P` | CAN Oil_P < 15 PSI AND ENGINE_RUNNING AND RPM > 500 | Warning light |
| `HIGH_COOLANT_T` | CAN Coolant_T > 95°C | Warning light — thermostat fully open at 92°C; >95°C = problem |
| `HIGH_OIL_T` | CAN Oil_T > 130°C | Warning light |
| `LOW_FUEL_P` | CAN Fuel_P < 40 PSI AND ENGINE_RUNNING AND RPM > 500 | Warning light — factory idle spec 46–49 PSI |
| `MULTI_WARNING` | LOW_OIL_P OR HIGH_COOLANT_T OR HIGH_OIL_T OR LOW_FUEL_P | Red LED trigger |
| `CoolsuitKYD` | Latched toggle from keypad Key 04 | Coolsuit pump |
| `FuelOverrideKYD` | Latched toggle from keypad Key 06 | Manual fuel pump on |
| `PitLimiterKYD` | Latched toggle from keypad Key 07 | Raw keypad state |
| `PITLIMITER_SAFE` | PitLimiterKYD AND CAN Speed < 60 mph | Safe to engage — blocks accidental on-track activation |
| `PITLIMITER_ACTIVE` | PITLIMITER_SAFE AND NOT (TPS > 60%) | Active limiter state sent to Haltech; TPS override always available |
| `CommsKYD` | Latched toggle from keypad Key 08 | PodiumConnect affirmative/negative signal |
| `PitInKYD` | Multi-position from keypad Key 09 (0/1/2/3) | PodiumConnect pit-in request with lap count |

---

## Power Output Configuration

### Output Map

| Output | Name | Mode | MaxLoad | Inductive | PWM | Trigger |
|---|---|---|---|---|---|---|
| **HP1** | Starter | OVC Protected | 20A | **Yes** | DC | STARTER_SAFE |
| **HP2** | Fan | Fused | 35A | No | 100Hz | ECT PWM curve + Ch01 override |
| **HP3** | FuelPump | OVC Protected | 15A | **Yes** | DC | FUEL_PRIME OR ENGINE_RUNNING |
| HP4 | Spare | -- | 20A | -- | -- | -- |
| **MP1** | InjectorPwr | OVC Protected | 15A | **Yes** | DC | SafeIgnition |
| **MP2** | CoilPwr | OVC Protected | 15A | No | DC | SafeIgnition |
| **MP3** | WiperLow | OVC Protected | 10A | **Yes** | DC | Ch02 AND NOT Ch03 |
| **MP4** | BrakeLights | Fused | 10A | No | DC | BRAKE_SWITCH (Ch11, physical, always active) |
| **MP5** | TailLights | Fused | 10A | No | DC | SafeIgnition (always on when car is on) |
| **MP6** | WiperHigh | OVC Protected | 10A | **Yes** | DC | Ch03 |
| **MP7** | Coolsuit | OVC Protected | 10A | **Yes** | DC | Ch04 AND SafeIgnition |
| **MP8** | Defogger | OVC Protected | 10A | No | DC | Ch05 AND SafeIgnition |
| MP9–MP12 | Spare | -- | -- | -- | -- | -- |
| **LP1** | ECU_Power | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP2** | Dash | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP3** | SmartyCam | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP4** | GPS | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP5** | Wideband | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP6** | Cluster | OVC Protected | 10A | No | DC | SafeIgnition |
| **LP7** | WarningLED | OVC Protected | 5A | No | DC | MULTI_WARNING |
| **LP8** | AltExciter | OVC Protected | 5A | No | DC | SafeIgnition |

> **MP1/MP2 temporary usage (Phase 1 — stock ECU):** While running on the stock ECU, MP1 and MP2 are wired to the OE main relay socket pin 87 (pull the relay). This provides switched 12V to the stock ECU and its loads whenever SafeIgnition is active. The trigger (`SafeIgnition`) and protection settings are identical to the final Haltech configuration. When switching to Haltech, simply reroute MP1 to the injector rail and MP2 to the COP coil power bus — no Race Studio config change needed.
>
> **LP8 — Alternator Exciter:** The OEM alternator D+ field wire is cut and routed through LP8 (A21, Connector A). When SafeIgnition drops (kill switch or IGN off), LP8 de-energizes and the alternator stops charging immediately. LP8 draws < 1A (field excitation only).

### Detailed Output Logic

#### HP1: Starter

```
Trigger: STARTER_SAFE
  = Ch09 [physical start button press]
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
```

#### HP2: Fan (4-Level Priority PWM + Manual Override)

```
Fan speed is driven by CAN coolant temp from Haltech, with manual toggle override.

Action 1: ON @ 25% duty  | Priority 1 | Trigger: FAN_TEMP_25 (>77°C — 170°F thermostat opens here)
Action 2: ON @ 50% duty  | Priority 2 | Trigger: FAN_TEMP_50 (>82°C)
Action 3: ON @ 75% duty  | Priority 3 | Trigger: FAN_TEMP_75 (>87°C)
Action 4: ON @ 98% duty  | Priority 4 | Trigger: FAN_TEMP_100 (>92°C est. fully open) OR FAN_FAILSAFE

Manual override: Ch01 (Fan toggle switch) → 98% duty, Priority 5 (highest)

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
Trigger: FUEL_PRIME OR ENGINE_RUNNING

  FUEL_PRIME:    3s one-shot timer on SafeIgnition rising edge
  ENGINE_RUNNING: CAN RPM > 50 (with 2s off-delay for stall protection)

Properties:
  Mode: OVC Protected
  Max Load: 15A
  Inductive: YES (pump motor)
  OVC Retries: 3 (pump may spike on initial prime)
  Latch Off: 5s

Note: No manual fuel override switch in this build. If manual priming is
needed, cycle the ignition switch off/on to trigger the 3s FUEL_PRIME timer.

Haltech DPO 5 (34-pin pin 24, B/Y) can also be wired to a PDM channel input
as an additional permissive or alternative trigger from the ECU side.
```

#### MP3: Wiper Low Speed

```
Trigger: Ch02 AND NOT Ch03
  = Wiper Low toggle ON AND Wiper High toggle OFF

If both Wiper Low and Wiper High switches are on, the high speed
output takes priority and low speed is disabled (prevents driving
both motor windings simultaneously).

Properties:
  Mode: OVC Protected
  Max Load: 10A
  Inductive: YES (wiper motor)
```

#### MP4: Brake Lights

```
Trigger: BRAKE_SWITCH (physical brake switch, always active)

NOTE: Brake lights MUST work regardless of ignition state.
Wire brake switch directly to PDM Channel Input Ch11.

Properties:
  Mode: Fused
  Max Load: 10A
```

#### MP5: Tail Lights

```
Trigger: SafeIgnition

Tail lights are always on when the car is running. No dedicated switch —
they activate automatically with the ignition switch.

Properties:
  Mode: Fused
  Max Load: 10A
```

#### MP6: Wiper High Speed

```
Trigger: Ch03
  = Wiper High toggle ON

When Wiper High is on, MP3 (Wiper Low) is forced off via the
AND NOT Ch03 condition in its trigger. High speed always wins.

Properties:
  Mode: OVC Protected
  Max Load: 10A
  Inductive: YES (wiper motor)
```

#### MP7: Coolsuit

```
Trigger: Ch04 AND SafeIgnition
  = Coolsuit toggle ON AND ignition ON

Coolsuit pump only runs with ignition on to prevent accidental
battery drain if the switch is left on.

Properties:
  Mode: OVC Protected
  Max Load: 10A
  Inductive: YES (pump motor)
```

#### MP8: Defogger

```
Trigger: Ch05 AND SafeIgnition
  = Defogger toggle ON AND ignition ON

Rear window defogger element. Consider adding a 15-minute auto-off
timer in Race Studio 3 to prevent excessive battery draw during
long sessions.

Properties:
  Mode: OVC Protected
  Max Load: 10A
  Inductive: No (resistive heating element)
```

#### LP7: Multi-Warning Red LED

```
Trigger: MULTI_WARNING
  = LOW_OIL_P OR HIGH_COOLANT_T OR HIGH_OIL_T OR LOW_FUEL_P

LOW_OIL_P:      CAN Oil_Pressure < 15 PSI AND RPM > 500
HIGH_COOLANT_T:  CAN Coolant_Temp > 95°C
HIGH_OIL_T:     CAN Oil_Temp > 130°C
LOW_FUEL_P:     CAN Fuel_Pressure < 40 PSI AND RPM > 500

RPM > 500 guard prevents false alarms at idle/cranking.

Properties:
  Mode: OVC Protected
  Max Load: 5A (LED draws < 0.5A)
  Can optionally PWM the LED for blinking effect (PWM 2Hz, 50% duty)
```

#### LP8: Alternator Exciter

```
Trigger: SafeIgnition

OEM alternator D+ field wire cut and routed through LP8 (A21).
When kill switch or IGN toggle cuts SafeIgnition, LP8 drops and
the alternator immediately stops charging — no residual field.

Properties:
  Mode: OVC Protected
  Max Load: 5A (field excitation draws < 1A)
  Inductive: No
```

#### MP1/MP2: OE Main Relay Power (Phase 1 — Stock ECU)

```
Phase 1 (stock ECU running):
  MP1 (A2) and MP2 (A3) → OE relay box main relay pin 87
  Pull the OE main relay. Insert PDM wires into pin 87 socket.
  This provides switched 12V to the stock ECU and associated
  circuits whenever SafeIgnition is active.

  Fan, headlights, horn, fuel pump, and starter have their own
  dedicated PDM outputs and are NOT powered through the OE relay.
  Only the stock ECU power/control circuits run through pin 87.

Phase 2 (Haltech switchover):
  MP1 rerouted → injector rail 12V + Haltech 34-pin pin 26 (R/L)
  MP2 rerouted → COP coil Pin D common bus (all 6 Toyota coils)
  No Race Studio config change needed — trigger is SafeIgnition
  in both phases.
```

---

## Power Distribution & Kill Switch

### Kill Switch Wiring (4-Pole, Left of Steering Wheel)

```
Battery (+) ─── 2 AWG ─── Kill Switch [Large Terminal A]
                                │
                          [Jumper] to [Small Terminal A]
                                │
                     Kill Switch [Large Terminal B] ───┬─── 2 AWG ─── 150A Breaker ─── Starter B+ / Alternator B+
                                │                      │
                                │                      └─── 4 AWG ─── 120A Breaker ─── PDM Surlok (+)
                                │
                     Kill Switch [Small Terminal B] ─── IGN toggle switch ─── PDM Conn B pin 23 (IGN input)
                                                                         └─── Haltech 34-pin pin 13 (ECU IGN)
```

**Kill switch ON:** All 4 poles connected. Battery power flows to starter/alt B+ (150A breaker), PDM Surlok (120A breaker), and through IGN toggle to PDM B23 + Haltech IGN enable.

**Kill switch OFF:** All 4 poles disconnected instantly:
- PDM loses Surlok power → all outputs drop
- `SafeIgnition` drops → LP8 (alt exciter) off → alternator stops charging
- Starter/alt B+ cut at 150A breaker feed
- Haltech IGN enable drops → ECU shuts down

**IGN toggle ON, kill switch ON:** `SafeIgnition` = 1, all ignition-gated outputs active.
**IGN toggle OFF, kill switch ON:** `SafeIgnition` = 0, engine outputs off, but PDM still has Surlok power for Race Studio config/testing.

### Mounting

PDM, Haltech Elite 2500, Podium Micro (SN: 1QTV5KM), and Innovate LM2 are mounted on a plate in the **passenger footwell**. Short wire runs to dash (LVDS), switch panel, and CAN buses. Engine bay harness exits through firewall.

---

## CAN Bus Configuration

### CAN0 (PDM Conn A pins A22 H / A11 L) — AIM Expansion Bus

| Setting | Value |
|---|---|
| Devices | CAN Data Hub → GPS-08, SmartyCAM, Podium module |
| Speed | 1 Mbps (AIM internal protocol) |
| Physical cable | Pre-wired "CAN expansion" harness (5-pin Binder, 22 AWG). **Do not reuse pins A10, A11, A22, A32, A33.** |
| Power to devices | A33 (+Vb out CAN via expansion cable) |
| Note | Dash connects via LVDS (4-pin Rosenberger), not CAN0 |

### CAN1 (PDM Conn A pins A30 H / A31 L) — Haltech Elite 2500

| Setting | Value |
|---|---|
| Protocol | Haltech Elite 2500 |
| Speed | 500 kbps |
| Termination | 120Ω at PDM end (A30/A31) if Haltech does not self-terminate |
| Silent on CAN Bus | Try OFF first; enable if Haltech errors on extra ACK signals from PDM |
| Data used | RPM, Coolant Temp, Oil Pressure, Oil Temp, Fuel Pressure, TPS |
| Haltech wiring | Haltech 26-pin pin 23 (W wire) → A30; pin 24 (L wire) → A31 |
| Note | A30/A31 shared with RS232 TX/RX — RS232 unavailable when CAN1 active |

> **"Silent on CAN Bus"** (RS3 ECU config option): By default PDM sends an ACK to every ECU message. Some ECUs misbehave when another device sends ACK on their bus. If Haltech logs CAN errors after PDM is connected, enable this flag. *(Source: PDM32 User Guide §12)*

### CAN2 (PDM Conn A pins A28 H / A29 L) — Unused

| Setting | Value |
|---|---|
| Status | **Not connected** — CAN keypad excluded from this build |
| Pins A28/A29 | Available for future CAN device (keypad, additional ECU, data logger, etc.) |

---

## Step-by-Step Race Studio 3 Setup

### 1. Open Starting Config

Open `Tiburon_White_v1_base.zconfig` in Race Studio 3. Output names and basic settings are pre-configured.

### 2. Configure ECU Stream (Haltech)

1. Go to **ECU Stream** tab *(RS3 tab name — this connects to the CAN ECU bus, PDM pins A30/A31)*
2. Select **Haltech Elite** as ECU protocol (or import Haltech CAN DBC)
3. Enable **120Ω termination** if Haltech does not self-terminate on its end
4. Leave **"Silent on CAN Bus"** OFF initially; enable only if Haltech logs CAN errors after PDM connects
5. Verify these channels appear: RPM, Coolant Temp (ECT), Oil Pressure, Oil Temp, Fuel Pressure, TPS
6. If Haltech is not in the preset list: manually add CAN messages per `opengk/can-bus-messages.md`

### 3. Disable CAN2 Keypad

1. Go to Configuration → CAN2
2. **Remove** or **disable** the AIM CAN Keypad 12 configuration
3. Remove all keypad-related status variables (StarterKYD, SirenKYD, LightsKYD, FanKYD, CoolsuitKYD, FuelOverride, PitLimiter_KYD, COMMS_YN, PITIN_LAPS)
4. Remove all keypad LED color assignments

### 4. Configure Channel Inputs

1. **Ch01** → "FAN_OVERRIDE" — Digital status, latching toggle, active = 12V
2. **Ch02** → "WIPER_LOW" — Digital status, latching toggle, active = 12V
3. **Ch03** → "WIPER_HIGH" — Digital status, latching toggle, active = 12V
4. **Ch04** → "COOLSUIT" — Digital status, latching toggle, active = 12V
5. **Ch05** → "DEFOGGER" — Digital status, latching toggle, active = 12V
6. **Ch09** → "START" — Digital status, momentary, active = grounded
7. **Ch11** → "BRAKE_SWITCH" — Digital status, closed when pedal pressed

### 5. Create Status Variables

In Configuration → Math Channels:

1. `ENGINE_RUNNING` = CAN RPM > 50 (with 2s off-delay)
2. `FUEL_PRIME` = Timer(SafeIgnition rising edge, 3000ms, one-shot)
3. `FAN_TEMP_25` through `FAN_TEMP_100` = CAN ECT band comparisons
4. `FAN_FAILSAFE` = CAN ECT timeout > 5s
5. `STARTER_SAFE` = Ch09 AND SafeIgnition AND NOT ENGINE_RUNNING
6. `LOW_OIL_P` = CAN Oil_P < 15 AND ENGINE_RUNNING AND CAN RPM > 500
7. `HIGH_COOLANT_T` = CAN ECT > 95
8. `HIGH_OIL_T` = CAN Oil_T > 130
9. `LOW_FUEL_P` = CAN Fuel_P < 40 AND ENGINE_RUNNING AND CAN RPM > 500
10. `MULTI_WARNING` = LOW_OIL_P OR HIGH_COOLANT_T OR HIGH_OIL_T OR LOW_FUEL_P

### 6. Assign Triggers to Power Outputs

Wire each status variable / channel input to its power output per the Output Map table above.

### 7. Configure Warning LED Output

Enable LP7, set trigger to `MULTI_WARNING`, optionally set PWM for blinking.

### 8. Configure SmartyCam Stream

1. Go to **SmartyCam Stream** tab *(rightmost tab in PDM RS3 config)*
2. Enable SmartyCam, select **CAN AiM** bus (expansion bus, A22/A11)
3. Assign channels to SmartyCam overlay slots — click each slot, select channel from panel
   - If a channel is missing from the list, check **"Enable all channels for functions"** to see all
   - Key channels: RPM, Speed (GPS-08), Gear, Coolant Temp, Oil Pressure, TPS, Lat G, Long G
4. Choose **AiM Default** protocol (or create Advanced protocol for custom channel set)
5. See `hardware/aim/aim-smartycam/aim-smartycam.md` for full channel map and SmartyCam-side RS3 config

### 9. Transmit and Test

1. Save configuration
2. Transmit to PDM via USB
3. Force-test each output in Race Studio 3 (Device window → Live Measures → force channel values)
4. Verify each toggle switch activates its assigned output:
   - Fan toggle → HP2 runs at 98%
   - Wiper Low toggle → MP3 on (verify MP6 off)
   - Wiper High toggle → MP6 on (verify MP3 off)
   - Coolsuit toggle → MP7 on
   - Defogger toggle → MP8 on
5. Verify brake lights work with physical switch only (Ch11)
6. Verify start button on Ch09 cranks the starter (with ignition on, engine not running)
7. Verify tail lights come on automatically with ignition switch

---

## Protection Settings Summary

| Output | Mode | MaxLoad | Inductive | OVC Retries | Latch Off | Soft Start |
|---|---|---|---|---|---|---|
| HP1 Starter | OVC Protected | 20A | Yes | 1 | 5s | No |
| HP2 Fan | Fused | 35A | No | -- | -- | 1.0s |
| HP3 FuelPump | OVC Protected | 15A | Yes | 3 | 5s | No |
| MP1 InjectorPwr | OVC Protected | 15A | Yes | 1 | 5s | No |
| MP2 CoilPwr | OVC Protected | 15A | No | 1 | 5s | No |
| MP3 WiperLow | OVC Protected | 10A | Yes | 1 | 5s | No |
| MP4 BrakeLights | Fused | 10A | No | -- | -- | No |
| MP5 TailLights | Fused | 10A | No | -- | -- | No |
| MP6 WiperHigh | OVC Protected | 10A | Yes | 1 | 5s | No |
| MP7 Coolsuit | OVC Protected | 10A | Yes | 1 | 5s | No |
| MP8 Defogger | OVC Protected | 10A | No | 1 | 5s | No |
| LP1-6 Accessories | OVC Protected | 10A | No | 1 | 5s | No |
| LP7 WarningLED | OVC Protected | 5A | No | 1 | 5s | No |
| LP8 AltExciter | OVC Protected | 5A | No | 1 | 5s | No |

---

## Alarm Thresholds (Tune on Track)

These are starting values — adjust based on engine behavior:

| Alarm | Threshold | Guard | Notes |
|---|---|---|---|
| Low oil pressure | < 15 PSI | RPM > 500 | Factory min 7.3 PSI; normal hot idle ~20-30 PSI |
| High coolant temp | > 95°C | Always active | 170°F thermostat — normal 77–87°C; est. fully open at ~92°C |
| High oil temp | > 130°C | Always active | Normal operating ~90-110°C |
| Low fuel pressure | < 40 PSI | RPM > 500 | Factory idle spec 46–49 PSI |
| Fan ON | > 77°C | Always active | First band (25%) — 170°F thermostat opens here |
| Fan 100% | > 92°C | Always active | Thermostat est. fully open |
| Fan failsafe | CAN timeout 5s | Always active | Full speed if CAN lost |
| Starter timeout | > 10s continuous | Always active | Motor protection |

---

## What Changed — CAN Keypad → Physical Switch Panel

This section documents what was removed or changed when the CAN keypad was excluded from the build.

### Removed

| Item | Was | Notes |
|---|---|---|
| CAN Keypad 12 | CAN2 device, 12 buttons | Hardware excluded from build |
| LP8 Keypad Power | OVC Protected, 5A, SafeIgnition trigger | Output freed — now spare |
| CAN2 bus config | 125 kbps, keypad protocol | Bus unused — available for future |
| Horn (MP3) | Key 02 momentary → MP3 | No horn switch in panel; MP3 reassigned to Wiper Low |
| Fuel Override | Key 06 toggle | No switch; cycle ignition off/on for fuel prime instead |
| Pit Limiter | Key 07 toggle + speed/TPS safety gating | No switch; feature removed |
| PodiumConnect Comms | Key 09 toggle (Yes/No) | No switch; feature removed |
| PodiumConnect Pit-In | Key 10 multi-position (0-3 laps) | No switch; feature removed |
| Keypad LED colors | 12 RGB LED assignments | No keypad |
| All `*KYD` status vars | StarterKYD, SirenKYD, LightsKYD, FanKYD, CoolsuitKYD | Replaced by direct channel input reads |
| PitLimiter vars | PitLimiter_KYD, PITLIMITER_SAFE, PITLIMITER_ACTIVE | Feature removed |
| FuelOverride var | Latched toggle from Key 06 | Feature removed |
| COMMS_YN, PITIN_LAPS | PodiumConnect integration vars | Feature removed |

### Changed

| Item | Was | Now |
|---|---|---|
| Starter trigger | StarterKYD (Key 01) OR Ch09 backup | Ch09 only (physical momentary button) |
| Fan override | FanKYD (Key 05) toggle | Ch01 physical toggle switch |
| Coolsuit trigger | CoolsuitKYD (Key 04) toggle | Ch04 AND SafeIgnition |
| Tail lights trigger | LightsKYD (Key 03) toggle | SafeIgnition (always on when car is on) |
| Wiper | Key 08 single toggle | Two switches: Wiper Low (Ch02) + Wiper High (Ch03) with priority logic |
| Fuel pump trigger | FUEL_PRIME OR ENGINE_RUNNING OR FuelOverride | FUEL_PRIME OR ENGINE_RUNNING (no manual override) |

### Added

| Item | Details |
|---|---|
| Defogger (MP8) | New output — Ch05 toggle AND SafeIgnition |
| Wiper High (MP6) | Separate high-speed wiper output — Ch03 toggle |
| 5 new channel inputs | Ch01–Ch05 for physical toggle switches |

---

## Cross-References

| File | Contents |
|---|---|
| `aim-pdm/pdm-pinout.md` | Full 35-pin ×2 connector pinout |
| `aim-pdm/pdm-configuration-guide.md` | Logic stack theory, input config, PWM examples |
| `guides/keypad-config-future.md` | Archived keypad button assignments, LED colors, variable names for future re-addition |
| `signal-routing.md` | End-to-end signal trace for every wire |
| `opengk/can-bus-messages.md` | CAN message IDs and byte definitions |
| `cars/cop-ignition.md` | COP coil pinout and NSP settings |
| `cars/lowdoller-sensors.md` | Sensor specs and PTC calibration tables |
| `tiburon_haltech_pdm_installation_guide_v1_final.docx` | Physical installation procedure |
| `Tiburon_White_v1_base.zconfig` | Starting-point Race Studio 3 config file |
| `Webinar complete.zconfig` | Original AIM webinar config (reference) |
