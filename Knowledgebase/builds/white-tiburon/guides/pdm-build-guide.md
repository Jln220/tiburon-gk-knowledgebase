# PDM Build Guide — White Tiburon (Consolidated)
## AIM PDM 32 | Haltech Elite 2500 | Physical Switch Panel

**Car:** White 2003 Tiburon GK (2.7L V6 Delta / G6BA)
**Race series:** 24 Hours of Lemons

> **One Race Studio config for all phases.** All outputs are configured for Phase 2 from day one. Outputs with no load connected drive open circuits harmlessly. Phase transitions require rewiring, not reconfiguration. Phase 3 (CAN keypad) is the only config change.

---

## Phase Overview

| Phase | ECU | Relay Box | PDM Role | Reversibility |
|-------|-----|-----------|----------|---------------|
| **1** | Stock SIMK43 | Powered, relays pulled selectively | Smart fuse box + kill switch | Put relays back |
| **2** | Haltech Elite 2500 | Unpowered (leave mounted) | Full power distribution | Plug stock ECU back in, put relays back |
| **3** | Haltech Elite 2500 | Removed | Full power + CAN keypad | N/A — committed |

**Escape clause:** If Phase 1 trips the 120A breaker or shows excessive draw through relay spade connections, skip directly to Phase 2 (Haltech takes over engine, relay box bypassed entirely).

---

## Race Studio Configuration (Friday at Home)

> **Do this ONCE.** This config covers Phase 1 and Phase 2 with no changes. Phase 3 adds CAN2 keypad.

### Starting Point

1. Open `Webinar complete.zconfig` in Race Studio 3
2. **File → Save As** → `Tiburon_White_v1.zconfig`

### Channel Inputs

> **Ch01–Ch08** are analog-capable (0–5V or 0–12V) on PDM Connector B. **Ch09–Ch12** are digital-only on Connector B (Ch09–Ch10 = B21/B22) and Connector A (Ch11–Ch12 = A26/A27). Grouped by physical connector for clean wiring. Speed 1 (B20) and Speed 2 (B19) are dedicated speed inputs — unused since VSS routes to Haltech SPI 1 and PDM reads speed via CAN.
>
> **Naming:** Channel names must not duplicate power output names. All switch inputs use the `*SW` suffix (e.g., `StarterSW` not `Starter`).
>
> **Work As = Momentary for ALL channels.** Physical toggle switches handle their own latching — Race Studio just reads the current pin state. Using "Toggle" mode would cause the PDM to re-toggle on each switch flip, getting out of sync with the physical switch.

#### Quick Reference

| Ch | Pin | Name | Close To | Pull-Up | Physical Switch | Wiring |
|----|-----|------|----------|---------|-----------------|--------|
| IGN | B23 | *(built-in)* | VBatt | No | Latching toggle | 12V → switch → B23 |
| 01 | B26 | `StarterSW` | Ground | ✅ 10kΩ | Momentary button | B26 → switch → GND |
| 02 | B27 | `FanLoSW` | Ground | ✅ 10kΩ | Latching toggle | B27 → switch → GND |
| 03 | B28 | `FanHiSW` | Ground | ✅ 10kΩ | Latching toggle | B28 → switch → GND |
| 04 | B29 | `HeadlightSW` | Ground | ✅ 10kΩ | Latching toggle | B29 → switch → GND |
| 05 | B30 | `WiperLoSW` | Ground | ✅ 10kΩ | Latching toggle | B30 → switch → GND (future) |
| 06 | B31 | `WiperHiSW` | Ground | ✅ 10kΩ | Latching toggle | B31 → switch → GND (future) |
| 07 | B32 | **SPARE** | — | — | — | Available for analog sensor (0–5V) |
| 08 | B33 | **SPARE** | — | — | — | Available for analog sensor (0–5V) |
| 09 | B21 | `BrakeSW` | VBatt | No | OEM brake switch | 12V → OEM switch → B21 |
| 10 | B22 | `CoolsuitSW` | Ground | ✅ 10kΩ | Latching toggle | B22 → switch → GND |
| 11 | A26 | `DefoggerSW` | Ground | ✅ 10kΩ | Latching toggle | A26 → switch → GND |
| 12 | A27 | `HornSW` | Ground | ✅ 10kΩ | Momentary button | A27 → switch → GND |
| Spd1 | B20 | **SPARE** | — | — | — | Speed input — available for wheel speed |
| Spd2 | B19 | **SPARE** | — | — | — | Speed input — available |
| Vref | B16 | *(sensor supply)* | — | — | — | +5V for future ratiometric sensors |

> **Close to Ground** = switch shorts pin to chassis ground when ON. Internal 10kΩ pull-up holds pin high (~5V) when switch is open. All custom panel switches use this — one wire to PDM, one wire to common ground bus. Simple.
>
> **Close to VBatt** = switch provides 12V to pin when ON. No pull-up needed. Used for OEM brake switch (provides 12V on pedal press) and IGN input (toggle feeds 12V).

#### Race Studio Channel Settings

Open **Configuration → Channels → Ch##** for each channel. All channels use Digital mode.

##### Ch01 — `StarterSW`

| Field | Value |
|-------|-------|
| **Name** | `StarterSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

##### Ch02 — `FanLoSW`

| Field | Value |
|-------|-------|
| **Name** | `FanLoSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

##### Ch03 — `FanHiSW`

| Field | Value |
|-------|-------|
| **Name** | `FanHiSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

##### Ch04 — `HeadlightSW`

| Field | Value |
|-------|-------|
| **Name** | `HeadlightSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

##### Ch05 — `WiperLoSW` (future)

| Field | Value |
|-------|-------|
| **Name** | `WiperLoSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

##### Ch06 — `WiperHiSW` (future)

| Field | Value |
|-------|-------|
| **Name** | `WiperHiSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

##### Ch09 — `BrakeSW`

| Field | Value |
|-------|-------|
| **Name** | `BrakeSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to VBatt |
| **Use internal pull up 10kΩ** | ☐ No |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

> OEM brake light switch provides 12V when pedal is pressed — no pull-up needed.

##### Ch10 — `CoolsuitSW`

| Field | Value |
|-------|-------|
| **Name** | `CoolsuitSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

##### Ch11 — `DefoggerSW`

| Field | Value |
|-------|-------|
| **Name** | `DefoggerSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

##### Ch12 — `HornSW`

| Field | Value |
|-------|-------|
| **Name** | `HornSW` |
| **Mode** | ◉ Digital |
| **Function** | Digital Status |
| **Sensor** | Status |
| **Sampling Frequency** | 20 Hz |
| **Log values** | ☐ No |
| **Active when signal is** | ◉ Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Work As** | ◉ Momentary |
| **Use timing** | ☐ No |
| **Not active** | Label: `S0`, Value: `0` |
| **Active** | Label: `S1`, Value: `1` |

> **Switch panel wiring:** All "Close to ground" switches share a common ground bus on the switch panel. One wire from each switch to the PDM channel pin, one wire to ground. The internal 10kΩ pull-up holds the pin high when the switch is open.

> **VSS routing:** Transaxle VSS (Hall IC, 4 pulses/rev, connector C109) → Haltech SPI 1 (26-pin pin 8). PDM reads vehicle speed from CAN ECU Stream (CC45 ECU VehSpeed). No direct PDM speed input needed.
> **Connector grouping:** Ch01–Ch10 + IGN + Speed all on Connector B (single harness run). Ch11–Ch12 on Connector A (short jumper wires to switch panel).

### Status Variables (Math Channels)

Configure all of these now — they work across all phases. Open **Configuration → Status Variables → Add Status Variable** in Race Studio 3.

> **Sampling frequency guide:** 10 Hz is correct for anything gating driver actions (starter, fuel pump). Fan/alarm temperature bands can use **1 Hz** — temps change slowly and this reduces CAN bus + logging load.

---

#### `FuelSV` (webinar — keep as reference)

This is the webinar's existing fuel pump variable. **Do not delete** — it works as-is and demonstrates the condition builder pattern. Our `FUEL_PRIME` and `ENGINE_RUNNING` variables below replace its logic with separate prime + run stages.

| Field | Value |
|-------|-------|
| **Name** | `FuelSV` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ☐ No |
| **Work As** | Momentary |
| **Use timing** | No |
| **Rest Status** | Label: `OFF`, Value: `0` |
| **Active Status** | Label: `ON`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition (compound OR):**

| # | Channel | Operator | Value | TRUE delay | FALSE delay |
|---|---------|----------|-------|------------|-------------|
| 1 | `SafeIgnition` [PDM32] | different from | `1` | 5 sec | 0 sec |
| 2 | OR `ECU RPM` [PDM32-ECU] | greater than | `50` rpm | 0 sec | 0 sec |

> **Webinar logic:** FuelSV activates when SafeIgnition has been OFF for 5 seconds OR RPM > 50. The 5-second delay on SafeIgnition-off provides a brief post-shutdown fuel pump run. We replace this with separate `ENGINE_RUNNING` (RPM-gated with 2s stall protection) and `FUEL_PRIME` (3s one-shot on IGN-on) for cleaner control.

---

#### `ENGINE_RUNNING`

| Field | Value |
|-------|-------|
| **Name** | `ENGINE_RUNNING` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Use timing** | No |
| **Rest Status** | Label: `OFF`, Value: `0` |
| **Active Status** | Label: `RUN`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition:**
| Field | Value |
|-------|-------|
| Channel | `ECU RPM` (Device: Main Device - PDM32, Type: ECU) |
| Operator | greater than |
| Compare to | constant ✅, `50` rpm |
| TRUE after a time of | `0` sec |
| FALSE after a time of | `2` sec |

> The 2s FALSE delay is stall protection — if engine briefly dips below 50 RPM during a stumble, fuel pump and other ENGINE_RUNNING-gated outputs stay on.

---

#### `FUEL_PRIME`

| Field | Value |
|-------|-------|
| **Name** | `FUEL_PRIME` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Use timing** | No |
| **Rest Status** | Label: `OFF`, Value: `0` |
| **Active Status** | Label: `PUMP`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |
| **Generate Square Wave** | ✅ Yes |
| **Duration of status On** | `3.0` sec |
| **Duration of status Off** | `999` sec |

**Activation condition:**
| Field | Value |
|-------|-------|
| Channel | `SafeIgnition` (Device: Main Device - PDM32, Type: Status Variables) |
| Operator | equal to |
| Compare to | constant ✅, `1` |
| TRUE after a time of | `0` sec |
| FALSE after a time of | `0` sec |

> **Why "Generate Square Wave"?** Race Studio requires square wave mode to enable the "Duration of status On" field. Setting ON=3s / OFF=999s (max) creates an effective one-shot: the pump primes for 3 seconds on SafeIgnition rising edge, then the 16-minute off period means it never re-fires during normal operation. When IGN is cycled off→on, the condition resets and a fresh 3s prime fires. ENGINE_RUNNING takes over pump duty within seconds of start.

---

#### `FAN_TEMP_25`

| Field | Value |
|-------|-------|
| **Name** | `FAN_TEMP_25` |
| **Sampling Frequency** | **1 Hz** |
| **Log values** | ☐ No |
| **Work As** | Momentary |
| **Use timing** | No |
| **Rest Status** | Label: `OFF`, Value: `0` |
| **Active Status** | Label: `F25`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition:**
| Field | Value |
|-------|-------|
| Channel | `ECU CoolantTemp` (Device: Main Device - PDM32, Type: ECU) |
| Operator | **hysteresis up to down** |
| Activation Threshold | `160` °F |
| Off Threshold | `170` °F |
| TRUE after a time of | `0` sec |
| FALSE after a time of | `0` sec |

> **Race Studio hysteresis naming is inverted:** "Activation Threshold" is the LOWER bound (OFF below this falling), "Off Threshold" is the UPPER bound (ON above this rising). So Activation=160 / Off=170 means: fan ON rising above 170°F, OFF falling below 160°F. 170°F = thermostat opening point.

---

#### `FAN_TEMP_50`

Same structure as FAN_TEMP_25 except:

| Field | Value |
|-------|-------|
| **Name** | `FAN_TEMP_50` |
| **Sampling Frequency** | **1 Hz** |
| **Rest/Active** | Label: `OFF`/`F50` |
| **Operator** | hysteresis up to down |
| **Activation Threshold** | `170` °F |
| **Off Threshold** | `180` °F |

---

#### `FAN_TEMP_75`

| Field | Value |
|-------|-------|
| **Name** | `FAN_TEMP_75` |
| **Sampling Frequency** | **1 Hz** |
| **Rest/Active** | Label: `OFF`/`F75` |
| **Operator** | hysteresis up to down |
| **Activation Threshold** | `180` °F |
| **Off Threshold** | `190` °F |

---

#### `FAN_TEMP_100`

| Field | Value |
|-------|-------|
| **Name** | `FAN_TEMP_100` |
| **Sampling Frequency** | **1 Hz** |
| **Rest/Active** | Label: `OFF`/`F100` |
| **Operator** | hysteresis up to down |
| **Activation Threshold** | `190` °F |
| **Off Threshold** | `200` °F |

> Thermostat estimated fully open at ~200°F with 170°F unit. Fan at 98% when thermostat is maxed.

---

#### `FAN_FAILSAFE`

| Field | Value |
|-------|-------|
| **Name** | `FAN_FAILSAFE` |
| **Sampling Frequency** | **1 Hz** |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Use timing** | No |
| **Rest Status** | Label: `OK`, Value: `0` |
| **Active Status** | Label: `FAIL`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition:**
| Field | Value |
|-------|-------|
| Channel | `ECU CoolantTemp` (Type: ECU) |
| Operator | equal to |
| Compare to | constant ✅, `0` |
| TRUE after a time of | `5` sec |
| FALSE after a time of | `0` sec |

> When CAN coolant temp is lost, the channel reads 0 for >5s, triggering failsafe fan. If CAN is restored, FAILSAFE clears immediately (0s FALSE delay). If Race Studio provides a dedicated "signal timeout" condition, use that instead of `equal to 0`.

---

#### `STARTER_SAFE`

| Field | Value |
|-------|-------|
| **Name** | `STARTER_SAFE` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Use timing** | No |
| **Rest Status** | Label: `LOCK`, Value: `0` |
| **Active Status** | Label: `CRNK`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition (compound — all must be true):**

Race Studio AND logic: chain conditions using the condition editor's AND gate.

| # | Channel | Operator | Value | TRUE delay | FALSE delay |
|---|---------|----------|-------|------------|-------------|
| 1 | Ch01 (Trigger Commands) | equal to | `1` | 0 sec | 0 sec |
| 2 | AND `SafeIgnition` (Status Variables) | equal to | `1` | 0 sec | 0 sec |
| 3 | AND `ENGINE_RUNNING` (Status Variables) | equal to | `0` | 0 sec | 0 sec |

> Start button (Ch01, B26) must be held, ignition must be on, engine must not be running. All zero-delay for instant response.

---

#### `LOW_OIL_P`

| Field | Value |
|-------|-------|
| **Name** | `LOW_OIL_P` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Rest Status** | Label: `OK`, Value: `0` |
| **Active Status** | Label: `LOW`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition (compound AND):**

| # | Channel | Operator | Value | TRUE delay | FALSE delay |
|---|---------|----------|-------|------------|-------------|
| 1 | `ECU OilPress` (ECU) | less than | `1.03` bar (= 15 PSI) | 0 sec | 0 sec |
| 2 | AND `ENGINE_RUNNING` (Status Variables) | equal to | `1` | 0 sec | 0 sec |
| 3 | AND `ECU RPM` (ECU) | greater than | `500` rpm | 0 sec | 0 sec |

> Factory min 7.3 PSI; normal hot idle ~20–30 PSI. RPM > 500 guard prevents false alarms at cranking. **Unit conversion:** Haltech CAN sends pressure in bar. 15 PSI = 1.03 bar.

---

#### `HIGH_COOLANT_T`

| Field | Value |
|-------|-------|
| **Name** | `HIGH_COOLANT_T` |
| **Sampling Frequency** | **1 Hz** |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Rest Status** | Label: `OK`, Value: `0` |
| **Active Status** | Label: `HOT`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition:**
| Field | Value |
|-------|-------|
| Channel | `ECU CoolantTemp` (ECU) |
| Operator | greater than |
| Compare to | constant ✅, `95` °C |
| TRUE after a time of | `0` sec |
| FALSE after a time of | `0` sec |

> 170°F thermostat: normal 77–87°C, fully open ~92°C. 95°C means fan is maxed and temp is still climbing — problem.

---

#### `HIGH_OIL_T`

| Field | Value |
|-------|-------|
| **Name** | `HIGH_OIL_T` |
| **Sampling Frequency** | **1 Hz** |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Rest Status** | Label: `OK`, Value: `0` |
| **Active Status** | Label: `HOT`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition:**
| Field | Value |
|-------|-------|
| Channel | `ECU OilTemp` (ECU) |
| Operator | greater than |
| Compare to | constant ✅, `130` °C |
| TRUE after a time of | `0` sec |
| FALSE after a time of | `0` sec |

> Normal operating ~90–110°C.

---

#### `LOW_FUEL_P`

| Field | Value |
|-------|-------|
| **Name** | `LOW_FUEL_P` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Rest Status** | Label: `OK`, Value: `0` |
| **Active Status** | Label: `LOW`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition (compound AND):**

| # | Channel | Operator | Value | TRUE delay | FALSE delay |
|---|---------|----------|-------|------------|-------------|
| 1 | `ECU FuelPress` (ECU) | less than | `2.76` bar (= 40 PSI) | 0 sec | 0 sec |
| 2 | AND `ENGINE_RUNNING` (Status Variables) | equal to | `1` | 0 sec | 0 sec |
| 3 | AND `ECU RPM` (ECU) | greater than | `500` rpm | 0 sec | 0 sec |

> Factory idle fuel pressure 46–49 PSI (3.17–3.38 bar). 40 PSI (2.76 bar) catches a failing pump while above injector deadband.

---

#### `MULTI_WARNING`

| Field | Value |
|-------|-------|
| **Name** | `MULTI_WARNING` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Work As** | Momentary |
| **Rest Status** | Label: `OK`, Value: `0` |
| **Active Status** | Label: `WARN`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition (compound OR):**

| # | Channel | Operator | Value | TRUE delay | FALSE delay |
|---|---------|----------|-------|------------|-------------|
| 1 | `LOW_OIL_P` (Status Variables) | equal to | `1` | 0 sec | 0 sec |
| 2 | OR `HIGH_COOLANT_T` (Status Variables) | equal to | `1` | 0 sec | 0 sec |
| 3 | OR `HIGH_OIL_T` (Status Variables) | equal to | `1` | 0 sec | 0 sec |
| 4 | OR `LOW_FUEL_P` (Status Variables) | equal to | `1` | 0 sec | 0 sec |

---

#### `WIPER_ACTIVE` (Future — configure now)

| Field | Value |
|-------|-------|
| **Name** | `WIPER_ACTIVE` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ☐ No |
| **Work As** | Momentary |
| **Rest Status** | Label: `OFF`, Value: `0` |
| **Active Status** | Label: `ON`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition (compound OR):**

| # | Channel | Operator | Value | TRUE delay | FALSE delay |
|---|---------|----------|-------|------------|-------------|
| 1 | Ch05 (Trigger Commands) | equal to | `1` | 0 sec | 0 sec |
| 2 | OR Ch06 (Trigger Commands) | equal to | `1` | 0 sec | 0 sec |

---

#### `WIPER_ACTIVE_DLY` (Future — configure now)

| Field | Value |
|-------|-------|
| **Name** | `WIPER_ACTIVE_DLY` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ☐ No |
| **Work As** | Momentary |
| **Rest Status** | Label: `OFF`, Value: `0` |
| **Active Status** | Label: `DLY`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition:**
| Field | Value |
|-------|-------|
| Channel | `WIPER_ACTIVE` (Status Variables) |
| Operator | equal to |
| Compare to | constant ✅, `1` |
| TRUE after a time of | `0` sec |
| FALSE after a time of | `3` sec |

> The 3s FALSE delay is the park sweep window. When switches turn off, WIPER_ACTIVE_DLY stays TRUE for 3 more seconds.

---

#### `WIPER_PARKING` (Future — configure now)

| Field | Value |
|-------|-------|
| **Name** | `WIPER_PARKING` |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ☐ No |
| **Work As** | Momentary |
| **Rest Status** | Label: `OFF`, Value: `0` |
| **Active Status** | Label: `PARK`, Value: `1` |
| **Condition mode** | Same condition for activation and deactivation |

**Activation condition (compound AND):**

| # | Channel | Operator | Value | TRUE delay | FALSE delay |
|---|---------|----------|-------|------------|-------------|
| 1 | `WIPER_ACTIVE_DLY` (Status Variables) | equal to | `1` | 0 sec | 0 sec |
| 2 | AND `WIPER_ACTIVE` (Status Variables) | equal to | `0` | 0 sec | 0 sec |

> Only TRUE during the 3s window after switches turn off — LP9 powers Brown wire for park sweep. See wiper section below.

---

#### Sampling Frequency Summary

| Variable | Frequency | Reason |
|----------|-----------|--------|
| `ENGINE_RUNNING` | 10 Hz | Gates starter interlock — needs responsive |
| `FUEL_PRIME` | 10 Hz | 3s timer accuracy |
| `FAN_TEMP_25/50/75/100` | **1 Hz** | Temperature changes slowly; reduces CAN load |
| `FAN_FAILSAFE` | **1 Hz** | 5s timeout — 1 Hz is sufficient |
| `STARTER_SAFE` | 10 Hz | Must respond to button press instantly |
| `LOW_OIL_P` | 10 Hz | Oil pressure can spike/dip quickly |
| `HIGH_COOLANT_T` | **1 Hz** | Temperature changes slowly |
| `HIGH_OIL_T` | **1 Hz** | Temperature changes slowly |
| `LOW_FUEL_P` | 10 Hz | Fuel pressure can fluctuate |
| `MULTI_WARNING` | 10 Hz | Inherits urgency from fastest alarm |
| `WIPER_*` | 10 Hz | Park timing accuracy |

> **RPM > 500 guard** on oil/fuel alarms prevents false alarms at cranking and idle.
> **Wiper variables** are pre-configured but inactive until Ch05/Ch06 switches are installed. No relay needed — see wiper section below.
> **Unit note:** Haltech CAN sends pressure in **bar**, not PSI. Conversions: 15 PSI = 1.03 bar, 40 PSI = 2.76 bar.

### ECU Stream (CAN1 — Haltech)

1. Go to **ECU Stream** tab
2. Click **Change ECU** dropdown → select **HALTECH - CAN_V2_40 (ver. 02.00.03) 1 Mbit/sec**
3. Bus: CAN1 (A30/A31), **500 kbps**
4. **Enable the CAN Bus 120 Ohm Resistor** ✅ — bus is PDM ↔ Haltech (two endpoints, both terminated)
5. **Silent on CAN Bus** ☐ — leave unchecked (PDM must transmit to send pit limiter CAN message to Haltech in Phase 3)
6. Enable channels per the list below

> **WARNING — Max 120 channels.** The Haltech CAN_V2_40 protocol has ~267 channels. Race Studio enforces a 120-channel maximum. **Uncheck the header row** to disable ALL channels first, then manually enable only these (~72 total, well under 120).

#### Required — PDM Alarm/Logic Channels

| CC ID | Channel Name | Unit | Purpose |
|---|---|---|---|
| CC01 | ECU RPM | rpm | ENGINE_RUNNING, STARTER_SAFE, alarm guards |
| CC04 | ECU ThrottlePos | % | PITLIMITER_ACTIVE (Phase 3: TPS > 60% bypass) |
| CC05 | ECU OilPress | bar | LOW_OIL_P alarm |
| CC06 | ECU FuelPress | bar | LOW_FUEL_P alarm |
| CC30 | ECU BrakePress | bar | Brake pressure (AVI7 Lowdoller sensor) |
| CC45 | ECU VehSpeed | km/h | PITLIMITER_SAFE — threshold = 97 km/h (= 60 mph) |
| CC52 | ECU BatteryVolt | V | Battery health |
| CC69 | ECU CoolantTemp | °F | Fan bands, HIGH_COOLANT_T alarm |
| CC71 | ECU OilTemp | °C | HIGH_OIL_T alarm |
| CC94 | ECU Oil Press Li | # | ECU oil pressure warning flag |
| CC117 | PitLane SpLimErr | # | Pit lane speed limiter error feedback |
| CC119 | PitLane SpdLimSS | # | Pit lane set speed reference |
| CC249 | ECU PLIGHT STATE | # | Engine protection / fault flag |

#### Logging Channels

| CC ID | Channel Name | Unit | Notes |
|---|---|---|---|
| CC02 | ECU ManifPress | bar | Manifold pressure (MAP) |
| CC03 | ECU CoolantPres | bar | Coolant pressure (AVI5 Lowdoller) |
| CC08 | ECU EngineDeman | % | Engine load / demand |
| CC09 | ECU IgnAngLead | deg | Ignition advance — shows retard events |
| CC10 | ECU InjDT2 | % | Injector duty cycle bank 2 |
| CC11 | ECU InjDT1 | % | Injector duty cycle bank 1 |
| CC15 | ECU Avg Inj 1 | ms | Injection pulse width |
| CC16 | ECU Avg Inj 2 | ms | Injection pulse width |
| CC17 | ECU Avg Inj 3 | ms | Injection pulse width |
| CC23 | ECU TrigSyncLev | # | Trigger sync level — tune health |
| CC24 | ECU TrigErrCount | # | Trigger error count — tune health |
| CC26 | ECU KnockLev2 | # | Knock bank 2 — critical for tune |
| CC27 | ECU KnockLev1 | # | Knock bank 1 — critical for tune |
| CC28 | ECU LateralG | g | Lateral acceleration |
| CC36 | ECU ExhCamAng1 | deg | Exhaust cam angle bank 1 (VVT) |
| CC37 | ECU ExhCamAng2 | deg | Exhaust cam angle bank 2 (VVT) |
| CC38 | ECU LongG | g | Longitudinal acceleration |
| CC46 | ECU IntakeCamA1 | deg | Intake cam angle bank 1 (VVT) |
| CC47 | ECU IntakeCamA2 | deg | Intake cam angle bank 2 (VVT) |
| CC50 | ECU BaromPress | bar | Barometric pressure |
| CC65 | ECU Amb Air T | °C | Ambient air temp |
| CC66 | ECU Rel Humidity | % | Relative humidity |
| CC67 | ECU Abs Humidity | # | Absolute humidity |
| CC68 | ECU Spec Humi | # | Specific humidity |
| CC70 | ECU AirTemp | °C | Air temp (°C) |
| CC72 | ECU FuelTemp | °C | Fuel temperature |
| CC73 | ECU DiffOilTemp | °C | Diff/trans oil temp |
| CC74 | ECU GearOilTemp | °C | Gearbox oil temp |
| CC76 | ECU FuelLevel | l | Fuel level |
| CC77 | ECU FuelTrimSTB1 | % | Short-term fuel trim bank 1 |
| CC78 | ECU FuelTrimSTB2 | % | Short-term fuel trim bank 2 |
| CC79 | ECU FuelTrimLTB1 | % | Long-term fuel trim bank 1 |
| CC80 | ECU FuelTrimLTB2 | % | Long-term fuel trim bank 2 |
| CC91 | ECU CheckEngLtSw | # | Check engine light status |
| CC107 | ECU TPSAct | # | TPS active status |
| CC134 | ECU TargLambda | lambda | Target lambda |
| CC138 | ECU CrankCPress | bar | Crankcase pressure |
| CC141 | ECU InjectionDT4 | % | Injector duty cycle 4 |
| CC142 | ECU IgnitionAng1 | deg | Ignition angle cyl 1 |
| CC143 | ECU IgnitionAng2 | deg | Ignition angle cyl 2 |
| CC144 | ECU RaceTimer | ms | Session timing |
| CC149 | ECU TorqCIgnCorr | deg | Torque/ignition correction |
| CC166 | ECU Temperature | °C | ECU internal temperature |
| CC167 | ECU Gear Sel Pos | gear | Gear display |
| CC168 | ECU WIDEBAND B2 | lambda | AFR bank 2 |
| CC169 | ECU WIDEBAND OVE | lambda | AFR average |
| CC170 | ECU WIDEBAND B1 | lambda | AFR bank 1 |
| CC172 | ECU Inj Pres D | bar | Injector pressure delta |
| CC173 | ECU Acc Ped Pos | % | Accelerator pedal position |
| CC210 | ECU VERTICAL G | g | Vertical acceleration |
| CC211 | ECU PITCH RATE | deg/s | Pitch rate |
| CC212 | ECU ROLL RATE | deg/s | Roll rate |
| CC213 | ECU YAW RATE | deg/s | Yaw rate |
| CC227 | ECU ENG LIM MAX | deg/s | Rev limiter threshold |
| CC254 | ECU FUEL TRIPMT | l | Fuel used — endurance reference |
| CC255 | Trip Meter | m | Distance |
| CC261 | ECU AIR TEMP | °F | IAT |

> ⚠️ **Disable CC260 (ECU H2O INJ DUTY)** — no water injection on this car.

### SmartyCam Stream

1. Go to **SmartyCam Stream** tab
2. Enable SmartyCam on **CAN AiM** bus (CAN0, A22/A11)
3. Assign: RPM, Speed (GPS-08), Gear, Coolant Temp, Oil Pressure, TPS, Lat G, Long G

### CAN2 — Disable

Remove or disable the CAN Keypad 12 config. Delete all `*KYD` variables. CAN2 is unused until Phase 3.

### Output Map (All Phases)

| Output | Name | Pin(s) | Mode | MaxLoad | Inductive | PWM | Trigger |
|--------|------|--------|------|---------|-----------|-----|---------|
| **HP1** | Starter | A1+A13 | OVC | 20A | Yes | DC | STARTER_SAFE |
| **HP2** | Fan | A12+A23 | Fused | 35A | No | 100Hz | Fan PWM curve + Ch02 low / Ch03 high override |
| **HP3** | FuelPump | A24+A25 | OVC | 15A | Yes | DC | FUEL_PRIME OR ENGINE_RUNNING |
| HP4 | Spare | A34+A35 | — | — | — | — | — |
| **MP1** | InjPwr | A2 | OVC | 15A | Yes | DC | SafeIgnition |
| **MP2** | CoilPwr | A3 | OVC | 15A | No | DC | SafeIgnition |
| **MP3** | Horn | A4 | OVC | 10A | Yes | DC | Ch12 |
| **MP4** | BrakeLights | A5 | Fused | 10A | No | DC | Ch09 (always active) |
| **MP5** | TailLights | A6 | Fused | 10A | No | DC | SafeIgnition |
| **MP6** | Headlights | A7 | OVC | 15A | No | DC | Ch04 AND SafeIgnition |
| **MP7** | Coolsuit | A8 | OVC | 10A | Yes | DC | Ch10 AND SafeIgnition |
| **MP8** | Defogger | A9 | OVC | 10A | No | DC | Ch11 AND SafeIgnition |
| **LP1** | ECU_Power | A14 | OVC | 10A | No | DC | SafeIgnition |
| **LP2** | Dash | A15 | OVC | 10A | No | DC | SafeIgnition |
| **LP3** | SmartyCam | A16 | OVC | 10A | No | DC | SafeIgnition |
| **LP4** | Spare (was GPS) | A17 | OVC | 10A | No | DC | SafeIgnition |
| **LP5** | Wideband | A18 | OVC | 10A | No | DC | SafeIgnition |
| **LP6** | Cluster | A19 | OVC | 10A | No | DC | SafeIgnition |
| **LP7** | WarningLED | A20 | OVC | 5A | No | DC | MULTI_WARNING |
| **LP8** | AltExciter | A21 | OVC | 5A | No | DC | SafeIgnition |
| **MP9** | WiperLow | B4 | OVC | 10A | No | DC | Ch05 AND NOT Ch06 AND SafeIgnition |
| **MP10** | WiperHigh | B5 | OVC | 10A | No | DC | Ch06 AND SafeIgnition |
| **LP9** | WiperPark | B3 | OVC | 10A | No | DC | WIPER_PARKING AND SafeIgnition |

> **MP3 and MP6 repurposed** from wipers to horn and headlights. Wipers use MP9 (B4), MP10 (B5), LP9 (B3) on Connector B — relay-less park design using WIPER_PARKING math channel.

### HP2 Fan — Detailed Logic

```
Action 1: ON @ 25% duty  | Priority 1 | Trigger: FAN_TEMP_25 (>170°F)
Action 2: ON @ 50% duty  | Priority 2 | Trigger: FAN_TEMP_50 (>180°F)
Action 3: ON @ 75% duty  | Priority 3 | Trigger: FAN_TEMP_75 (>190°F)
Action 4: ON @ 98% duty  | Priority 4 | Trigger: FAN_TEMP_100 (>200°F) OR FAN_FAILSAFE
Manual Low:  ON @ 50% duty  | Priority 5 | Trigger: Ch02 (fan low toggle)
Manual High: ON @ 98% duty  | Priority 6 | Trigger: Ch03 (fan high toggle — overrides low)

Soft Start: 1.0s (reduce inrush)
Hysteresis: 10°F per band (ON at threshold, OFF at threshold − 10°F)
Failsafe: CAN coolant_T lost > 5s → 98% duty
```

### HP1 Starter — Detailed Logic

```
Trigger: STARTER_SAFE
  = Ch01 AND SafeIgnition AND NOT ENGINE_RUNNING

OVC Retries: 1, Latch Off: 5s
Add 10s timeout: if HP1 ON > 10s → force off (motor protection)
HP1 has internal series diode (back-EMF protection)
```

### HP3 Fuel Pump — Detailed Logic

```
Trigger: FUEL_PRIME OR ENGINE_RUNNING

FUEL_PRIME:     3s one-shot on SafeIgnition rising edge
ENGINE_RUNNING: CAN RPM > 50 (2s off-delay for stall protection)

OVC Retries: 3 (pump may spike on initial prime)
Latch Off: 5s
No manual fuel override — cycle IGN off/on for 3s prime
```

### Wiper — Relay-Less Park Design (Future — Connector B)

Three PDM outputs replace the OEM park relay. The motor's internal cam disc handles park positioning.

**Motor wires:** Green = low speed, Yellow = high speed, Brown = park common, Black = ground/dynamic brake.

```
MP9  (B4)  → Green wire (low speed)   | Trigger: Ch05 AND NOT Ch06 AND SafeIgnition
MP10 (B5)  → Yellow wire (high speed)  | Trigger: Ch06 AND SafeIgnition
LP9  (B3)  → Brown wire (park sweep)   | Trigger: WIPER_PARKING AND SafeIgnition

Motor Black wire → chassis ground (always connected)
Motor Gray wire → leave disconnected (washer or unused)
```

**How park works without a relay:**
1. **Wipers ON:** MP9 or MP10 powers Green/Yellow. Brown (LP9) is OFF (WIPER_PARKING = 0 because WIPER_ACTIVE = 1). Motor runs normally.
2. **Switches OFF:** WIPER_ACTIVE drops to 0. WIPER_ACTIVE_DLY stays 1 for 3s. WIPER_PARKING = 1. LP9 powers Brown → internal cam routes Brown→Yellow → motor sweeps to park.
3. **At park position:** Cam finger flips Brown→Black. Current flows through winding (~6-8A) as dynamic brake. Motor stops instantly.
4. **After 3s:** WIPER_ACTIVE_DLY expires → WIPER_PARKING = 0 → LP9 cuts Brown.

**Safety constraint:** Brown is NEVER powered while Green/Yellow are powered. `NOT WIPER_ACTIVE` in the WIPER_PARKING formula guarantees this — LP9 can only activate when Ch05 and Ch06 are both off.

> **LP9 OVC:** Set to 10A. The Brown→Black current through the motor winding is ~6-8A for the brief park duration. Well within limits.
> **Not installed yet.** Wiper switches (Ch05/Ch06) and motor connections will be added when wipers are needed. Config is pre-loaded.

### Protection Settings

| Output | Mode | MaxLoad | Inductive | OVC Retries | Latch Off | Soft Start |
|--------|------|---------|-----------|-------------|-----------|------------|
| HP1 Starter | OVC | 20A | Yes | 1 | 5s | No |
| HP2 Fan | Fused | 35A | No | — | — | 1.0s |
| HP3 FuelPump | OVC | 15A | Yes | 3 | 5s | No |
| MP1 InjPwr | OVC | 15A | Yes | 1 | 5s | No |
| MP2 CoilPwr | OVC | 15A | No | 1 | 5s | No |
| MP3 Horn | OVC | 10A | Yes | 1 | 5s | No |
| MP4 BrakeLights | Fused | 10A | No | — | — | No |
| MP5 TailLights | Fused | 10A | No | — | — | No |
| MP6 Headlights | OVC | 15A | No | 1 | 5s | No |
| MP7 Coolsuit | OVC | 10A | Yes | 1 | 5s | No |
| MP8 Defogger | OVC | 10A | No | 1 | 5s | No |
| LP1–LP6 | OVC | 10A | No | 1 | 5s | No |
| LP7 WarningLED | OVC | 5A | No | 1 | 5s | No |
| LP8 AltExciter | OVC | 5A | No | 1 | 5s | No |

### Alarm Thresholds (Tune on Track)

| Alarm | Threshold | Guard | Notes |
|-------|-----------|-------|-------|
| Low oil pressure | < 15 PSI | RPM > 500 | Factory min 7.3 PSI; normal hot idle ~20–30 PSI |
| High coolant temp | > 203°F | Always | 170°F thermostat; normal 170–190°F; fully open ~200°F |
| High oil temp | > 266°F | Always | Normal operating ~194–230°F |
| Low fuel pressure | < 40 PSI | RPM > 500 | Factory idle spec 46–49 PSI |
| Fan ON (25%) | > 170°F | Always | 170°F thermostat opens here |
| Fan 100% | > 200°F | Always | Thermostat est. fully open |
| Fan failsafe | CAN timeout 5s | Always | Full speed if CAN data lost |
| Starter timeout | > 10s continuous | Always | Motor protection |

> **Note:** Fan temp bands (`FAN_TEMP_25` etc.) depend on Haltech CAN coolant temp, which isn't available until Sunday SU.6 when Haltech CAN1 is connected. On Saturday (Phase 1A), these variables will read 0/inactive — this is expected. Fan runs on stock BCM relay Saturday.

### SmartyCam Config (Session B — USB-C to Camera)

After PDM config is transmitted, connect USB-C directly to SmartyCam 3 Corsa:

1. RS3 detects SmartyCam as separate device
2. **CAN Protocol** tab → select **AiM Default** (matches PDM Session A setting)
3. **Overlay** tab → position RPM (top center), Speed (bottom center), Water Temp, Oil Pressure, TPS, G-force meter
4. **Save → Transmit** config to camera
5. On camera menu: **MENU → SETTINGS → AUTO START REC → Enable**
6. Insert SD card (≥2 GB)

> SmartyCam config reference: `hardware/aim/aim-smartycam/aim-smartycam.md`

### Podium Micro Config (USB or Phone — RaceCapture App)

1. Connect Podium Micro via USB to PC (or phone via Bluetooth)
2. Open **RaceCapture** app
3. Set CAN baud rate to **1000000** (1 Mbps — matches AIM CAN0)
4. Select **AIM** preset for CAN channel mapping
5. Map minimum channels: Speed, Latitude, Longitude (+ RPM, ECT, Oil P, TPS if in preset)
6. **WiFi → AP mode:** Enable (creates hotspot for pit wall dashboard on phone/tablet)
7. **WiFi → STA mode:** Enter phone hotspot SSID + password (2.4 GHz only) for cloud streaming
8. Insert SD card (≥2 GB) for local logging

> Podium config reference: `hardware/aim/aim-podium/aim-podium-micro.md`

### Transmit PDM Config

1. Save `Tiburon_White_v1.zconfig`
2. Connect PDM via USB
3. Transmit configuration
4. Force-test each output in Race Studio Live Measures (no loads — verify logic triggers only)
5. Backup: copy `.zconfig` to `AIM PDM/` folder

---

## Fuel Pump Bench Test (Friday at Home)

### Wiring

```
PDM HP3 outputs:
  A24 ─────┬────── Pump positive (+)
  A25 ─────┘

  Battery GND ─── Pump negative (−)
```

Both A24 and A25 carry HP3 — connect both for full current capacity. Use 14 AWG minimum.

### Test Sequence

**1. Prime cycle**
- IGN off → IGN on
- HP3 activates for **3 seconds** then cuts
- Verify in Race Studio: `FUEL_PRIME` timer fires, pump runs, then stops
- If no prime: check `SafeIgnition` = 1, verify timer rising edge logic

**2. Current measurement**
- Force HP3 ON in Race Studio Live Measures
- Measure current: expected 5–10A continuous
- If > 15A: check pump for binding; HP3 OVC will cut at 15A
- Record peak draw for wire gauge confirmation

**3. Voltage at pump**
- Measure pump + to − while running
- Should be within 0.5V of supply voltage
- > 1V drop: check connections or wire gauge

**4. Prime repeat test**
- IGN off, wait 5s, IGN on → should prime again
- Confirm one-shot timer resets properly

---

## Phase 1 — PDM + Stock ECU

### Concept

PDM acts as a smart fuse box with kill switch integration. Stock ECU and BCM remain connected and running. PDM replaces specific relays via spade connectors into pin 87 sockets. BCM continues to control horn, headlights, and (initially) fans through stock relays.

**What PDM controls in Phase 1:**
- Engine power via main relay pin 87 (coils, injectors, O2 sensors)
- Fuel pump via fuel pump relay pin 87
- Starter via solenoid S-terminal
- Alternator exciter via cut D+ wire
- Brake lights, tail lights
- Accessories (Haltech, dash, cameras, LM2, cluster)
- Fan (after CAN verified — see Phase 1B below)
- Warning LED

**What stays on stock relays (BCM controls):**
- Horn (steering wheel button → BCM → horn relay)
- Headlights (stalk switch → BCM → headlight relay)
- Fan (initially, until CAN data verified)

### Phase 1 Load Estimate

| Load Group | Est. Draw | Notes |
|------------|-----------|-------|
| MP1/MP2 (main relay → stock ECU circuits) | 15–25A | ECU + injectors + coils + O2 heaters |
| HP3 (fuel pump) | 5–10A | Continuous while running |
| HP1 (starter) | 15–20A | Momentary only |
| HP2 (fan, when added) | 10–35A | PWM dependent on temp |
| LP1–LP8 + MP4/MP5 | 10–15A | Accessories + lights |
| **Total (no fan, no starter)** | **~40–50A** | Well under 120A breaker |
| **Total (with fan peak)** | **~75–85A** | Comfortable margin |
| **Total (worst case all)** | **~105A** | Still under 120A; starter is momentary |

### Phase 1A — Core Install (Saturday Morning)

#### S.1 Mount Electronics Plate

All electronics on a single plate in passenger footwell: PDM, Haltech, Podium Micro (SN: 1QTV5KM), Innovate LM2.

- [ ] Bolt/rivet plate into passenger footwell
- [ ] Mount PDM (vibration-isolated)
- [ ] Mount Haltech Elite 2500
- [ ] Mount Podium Micro
- [ ] Mount Innovate LM2

#### S.2 Kill Switch Wiring

Kill switch already mounted left of steering wheel. 2 AWG cable already run to large terminal A.

```
Battery (+) ─── 2 AWG ─── Kill Switch [Large Terminal A]
                                │
                          [Jumper] to [Small Terminal A]
                                │
                     Kill Switch [Large Terminal B] ───┬─── 2 AWG ─── 150A Breaker ─── Starter B+ / Alt B+
                                │                      │
                                │                      └─── 4 AWG ─── 120A Breaker ─── PDM Surlok (+)
                                │
                     Kill Switch [Small Terminal B] ─── IGN toggle ───┬─── PDM B23 (IGN input)
                                                                      └─── Haltech 34-pin pin 13 (ECU IGN)
```

- [ ] Verify jumper: large terminal A → small terminal A
- [ ] Large terminal B → 150A breaker → starter B+ / alternator B+ (2 AWG)
- [ ] Large terminal B → 120A breaker → PDM Surlok (+) (4 AWG)
- [ ] Small terminal B → IGN toggle switch
- [ ] IGN toggle → PDM B23 AND Haltech 34-pin pin 13 (P wire)
- [ ] Connect PDM Surlok power cable
- [ ] Connect PDM grounds: B13, B14, B18 to chassis

#### S.3 Switch Panel Wiring

```
Switch Panel Layout (Phase 1)
==============================

Latching toggles:
  [IGN]  [FAN LO]  [FAN HI]  [COOL]  [DEFOG]  (1 spare position)

Momentary:
  [START]                                       (RED warning LED)
```

- [ ] IGN toggle → B23 (already wired in S.2)
- [ ] Start button → Ch01 (B26), close to GND, pull-up 10kΩ
- [ ] Fan low → Ch02 (B27), close to GND, pull-up 10kΩ
- [ ] Fan high → Ch03 (B28), close to GND, pull-up 10kΩ
- [ ] Coolsuit → Ch10 (B22), close to GND, pull-up 10kΩ
- [ ] Defogger → Ch11 (A26), close to GND, pull-up 10kΩ
- [ ] Brake light switch → Ch09 (B21), close to VBatt, no pull-up (OEM switch provides 12V)
- [ ] Warning LED → LP7 (A20)

> **Phase 2 additions:** Add horn button → Ch12 (A27, close to GND, pull-up 10kΩ) and headlight toggle → Ch04 (B29, close to GND, pull-up 10kΩ) when BCM is unplugged.

#### S.4 First Power-Up

- [ ] Kill switch ON, IGN toggle ON → PDM powers up
- [ ] Connect laptop USB → Race Studio Live Data
- [ ] Verify `SafeIgnition` = 1
- [ ] Flip each toggle → verify correct channel input in Live Data
- [ ] Press START (Ch01) → verify `STARTER_SAFE` activates (ENGINE_RUNNING = 0)
- [ ] IGN toggle OFF → verify `SafeIgnition` = 0, all outputs drop
- [ ] Kill switch OFF → verify total power loss

> **GATE: All switches verified before connecting any loads.**

#### S.5 Dash + LVDS

- [ ] Mount AIM 10" dash
- [ ] Connect LVDS cable (PDM Rosenberger → dash)
- [ ] Verify dash powers up and shows live data

#### S.6 Fuse Box Connections — Core

**Main Relay (MP1 + MP2 → OE main relay pin 87):**
- [ ] Locate OE main relay in underhood fuse box
- [ ] Pull the relay
- [ ] Insert MP1 (A2) wire into pin 87 socket
- [ ] Insert MP2 (A3) wire into same pin 87 socket (parallel)
- [ ] IGN on → verify stock ECU powers up; IGN off → ECU loses power
- [ ] **Test:** Stock dash lights, check engine light, fuel gauge all work

**Fuel Pump Relay (HP3 → fuel pump relay pin 87):**
- [ ] Pull OEM fuel pump relay
- [ ] Insert HP3 (A24+A25) wire into pin 87 socket
- [ ] IGN on → listen for 3-second fuel prime → off
- [ ] Verify in Race Studio: `FUEL_PRIME` fires, `FuelSV` active → inactive

**Starter (HP1 → solenoid S-terminal):**
- [ ] Run HP1 (A1+A13) wire directly to starter solenoid S-terminal (10 AWG, ring terminal)
- [ ] Press START (Ch01) → engine cranks; release → stops
- [ ] Start engine → press START again → should NOT engage (RPM interlock)

> **Direct to solenoid is more reliable than fuse box spade for starter.** HP1 has internal series diode — no additional protection needed. Leave OEM starter relay in place as backup (can be used if PDM fails).

#### S.7 Alternator Exciter (LP8)

- [ ] Locate OEM alternator D+ exciter wire (~18 AWG at alternator Yazaki connector)
- [ ] Confirm with multimeter: 12V with IGN on, 0V with IGN off
- [ ] Cut exciter wire; leave length on both ends
- [ ] Fuse box side → wire to PDM LP8 (A21)
- [ ] Alternator D+ side → remains connected to alternator

#### S.8 CAN0 Expansion Bus — AIM Devices + Podium

> The Data Hub is a passive star splitter — each device plugs into its own hub port. GPS-08 and Podium get power through the hub's +Vb rail (PDM A33, always on). SmartyCam Corsa needs **separate 12V** from LP3 (A16) via its 7-pin main power connector — the 5-pin EXP port carries CAN data only.

**Physical connections:**
- [ ] Verify CAN0 expansion cable: A22 (H) / A11 (L) / A33 (+Vb) / A10 (GND)
- [ ] Connect AIM CAN Data Hub (4-way) male port to expansion cable
- [ ] Hub port 1 → GPS-08 (5-pin Binder male cable)
- [ ] Hub port 2 → SmartyCam 3 Corsa EXP port (5-pin Binder — CAN data only)
- [ ] Hub port 3 → Podium Micro (Binder-to-M8 adapter cable)
- [ ] Wire LP3 (A16) → SmartyCam 7-pin main power connector (Red = +12V, Black = GND)

**Mounting:**
- [ ] Mount GPS-08 (roof/cowl — clear sky view, antenna face up)
- [ ] Mount SmartyCam (windshield or roll bar bracket)
- [ ] Podium Micro already on electronics plate (S.1)

**Verification:**
- [ ] IGN on → LP3 active → SmartyCam powers up (LED shows CAN activity: green/blue solid)
- [ ] GPS-08 powers up automatically via hub +Vb (LED on)
- [ ] Podium powers up via hub +Vb (power LED on, CAN ⇄ LED active)
- [ ] RS3 Live Data → CAN AiM bus shows traffic
- [ ] GPS channels appear in RS3 Channels tab after satellite lock (~30s outdoors)
- [ ] Connect phone to Podium AP WiFi → RaceCapture app shows channel tiles

> **Podium is NOT visible in Race Studio.** It's an Autosport Labs device, not AIM. Verify via the RaceCapture app (phone/tablet), not RS3. See `hardware/aim/aim-podium/aim-podium-micro.md` for config.

> **LP4 (A17):** Listed as "GPS" in output map but GPS-08 gets power through the hub's +Vb rail (A33, always on). LP4 is currently a spare — repurpose if needed for another accessory.

### Test Gate — Phase 1A (Saturday)

| Test | Expected | Pass? |
|------|----------|-------|
| SafeIgnition toggles with IGN switch | ON/OFF clean | |
| Fuel prime (3s) on IGN on | HP3 on 3s then off | |
| Engine cranks via Ch01 START | Starter engages | |
| Engine starts and runs | ENGINE_RUNNING = 1 | |
| Starter interlock while running | No crank | |
| Alternator charging | 13.8–14.4V at battery | |
| Kill switch kills everything | Engine dies, power drops, alt stops | |
| Fan works via stock relay | BCM controls fan normally | |
| Horn works via steering wheel | BCM controls horn normally | |
| Headlights work via stalk | BCM controls headlights normally | |
| Brake lights via pedal | MP4 on (test with IGN off too) | |
| Tail lights automatic | MP5 on with SafeIgnition | |
| Warning LED | LP7 triggers on forced alarm | |
| Dash shows live data | LVDS working | |

> **GATE: Car starts, runs, and stops reliably. Kill switch kills everything. Fan/horn/lights work through stock BCM.**

### Phase 1B — CAN + Sensors + Fan Migration (Sunday)

After sensors are installed and Haltech CAN data is confirmed flowing to PDM.

#### SU.1–SU.5 Sensor Installation

> Full sensor installation procedure in `weekend-tasks.md` (SU.1–SU.5). Combination sensors (oil/coolant/fuel pressure+temp) wire to Haltech AVIs.

#### SU.6 Verify CAN1 (Haltech → PDM)

- [ ] Connect Haltech 26-pin pins 23/24 (CAN H/L) → PDM A30/A31 (CAN1)
- [ ] Power Haltech from PDM LP1 (A14)
- [ ] Verify in Race Studio Live Data: RPM, Coolant Temp, Oil Pressure visible
- [ ] Confirm `FAN_TEMP_25` through `FAN_TEMP_100` react to live coolant temp
- [ ] Confirm `MULTI_WARNING` triggers when alarm thresholds crossed (force values in NSP)

> **GATE: CAN data flowing before moving fan to PDM control.**

#### SU.7 Move Fan to PDM Control

Now that CAN temp data is confirmed, move fan from stock relay to PDM.

**Option A — Through relay socket (reversible, try first):**
- [ ] Pull OEM fan relay
- [ ] Insert HP2 (A12+A23) wire into fan relay pin 87 socket (12 AWG)
- [ ] Test: warm up engine → verify fan bands activate at correct temps

**Option B — Direct to fan motor (if relay socket has too much resistance):**
- [ ] Run HP2 (A12+A23) directly to fan motor connector
- [ ] Leave OEM fan relay in place as backup (can be reinstalled)
- [ ] Test: same as Option A

- [ ] Verify fan low toggle (Ch02) → 50% duty
- [ ] Verify fan high toggle (Ch03) → 98% duty
- [ ] Verify fan failsafe: disconnect Haltech CAN temporarily → fan goes to 98% after 5s
- [ ] Reconnect CAN

#### SU.8 Full System Test

- [ ] Start car → all CAN data flowing
- [ ] Drive around → fan cycles with temp, all gauges work
- [ ] Kill switch test → everything dies
- [ ] All switches function correctly
- [ ] Record: peak fan current, total PDM current (POTotCurrent)

### Phase 1 — What Stays on Stock Relays

| Load | Why It Stays | Phase 2 Migration |
|------|-------------|-------------------|
| Horn | BCM + steering wheel button works perfectly | MP3 (A4) + Ch12 button |
| Headlights | BCM + stalk switch works, has features (delay, hi/lo) | MP6 (A7) + Ch04 toggle |

These loads move to PDM in Phase 2 when BCM is unplugged. The outputs (MP3, MP6) are already configured in Race Studio — just need physical wiring and switch panel additions.

---

## Phase 2 — PDM + Haltech ECU

### Concept

Haltech takes over engine control. Stock ECU and BCM are unplugged but left mounted for easy reversal. The OE relay box is unpowered — PDM outputs go directly to loads. Deutsch connectors D2 (coils) and D3 (injectors) plug in. Horn and headlights move to PDM since BCM is disconnected.

### What Changes from Phase 1

| Item | Phase 1 | Phase 2 |
|------|---------|---------|
| Engine ECU | Stock SIMK43 (connected) | Haltech Elite 2500 (active) |
| Stock ECU | Powered via MP1/MP2 → main relay pin 87 | Unplugged, mounted |
| BCM | Connected and active | Unplugged, mounted |
| MP1 wire | OE main relay pin 87 | 3-way splice → D2 pin 8 + D3 pin 8 (both banks injector power) + Haltech pin 26 |
| MP2 wire | OE main relay pin 87 | 2-way splice → D2 pin 7 + D3 pin 7 (both banks coil power) |
| HP3 wire | Fuel pump relay pin 87 | Direct to fuel pump (or leave on relay socket) |
| Coils | Stock harness (OE ECU drives) | D2 (Bank 1) + D3 (Bank 2) → 6× Toyota 90919-A2005 via Haltech IGN 1–6 |
| Injectors | Stock harness (OE ECU drives) | D2 (Bank 1) + D3 (Bank 2) → 6× injectors via Haltech INJ 1–6 |
| Horn | BCM + steering wheel | MP3 (A4) → horn relay pin 87 or direct; Ch12 button |
| Headlights | BCM + stalk switch | MP6 (A7) → headlight relay pin 87 or direct; Ch04 toggle |
| Relay box | Powered, relays pulled selectively | Unpowered — all relays can go back in (no current) |
| Race Studio config | **No change** | **No change** |

### Transition Procedure

> **Reversibility:** To go back to Phase 1, plug stock ECU + BCM back in, reconnect MP1/MP2 to main relay pin 87, pull D2 + D3 Deutsch connectors, remove Ch12/Ch04 switches. Relay box powers back up normally.

**Step 1 — Disconnect stock ECU**
- [ ] Unplug stock ECU connectors (C133-1 through C133-4)
- [ ] Leave ECU mounted in place
- [ ] Label all connectors for reversal

**Step 2 — Disconnect BCM**
- [ ] Unplug BCM connector
- [ ] Leave BCM mounted
- [ ] Note: horn (steering wheel button) and headlights (stalk) will no longer function through stock path

**Step 3 — Reroute MP1 (injector power)**
- [ ] Pull MP1 spade from OE main relay pin 87 socket
- [ ] Connect MP1 (A2) to 3-way splice: D2 pin 8 (Bank 1) + D3 pin 8 (Bank 2) + Haltech 34-pin pin 26 (R/L, injector power sense)
- [ ] See `guides/harness-design.md` → "MP1/MP2 Power Distribution" for splice diagram

**Step 4 — Reroute MP2 (coil power)**
- [ ] Pull MP2 spade from OE main relay pin 87 socket
- [ ] Connect MP2 (A3) to 2-way splice: D2 pin 7 (Bank 1) + D3 pin 7 (Bank 2)
- [ ] D2/D3 pin 7 → Coil Pin D bus on each bank (3 coils per bank)

**Step 5 — Put main relay back**
- [ ] Re-insert the OE main relay (slot is now empty, relay box unpowered — relay does nothing)
- [ ] This keeps the relay socket tidy and available if reverting

**Step 6 — Connect Deutsch harnesses + ground ring terminals**
- [ ] Plug in D2 (Bank 1 front — cyl 1,3,5) — engine side already connected to coils + injectors
- [ ] Bolt D2 ground ring terminal to front head bolt
- [ ] Plug in D3 (Bank 2 rear — cyl 2,4,6) — engine side already connected to coils + injectors
- [ ] Bolt D3 ground ring terminal to rear head bolt
- [ ] Verify D1 (engine sensors) connected — cam, crank, knock, IAT, MAP, TPS to Haltech
- [ ] Verify D4 (Lowdoller sensors) connected — oil/coolant/fuel to Haltech AVIs

**Step 7 — Add horn + headlight controls**
- [ ] Add momentary horn button → Ch12 (A27), close to GND, pull-up 10kΩ
- [ ] Add latching headlight toggle → Ch04 (B29), close to GND, pull-up 10kΩ
- [ ] Wire MP3 (A4) → horn (direct to horn or through relay socket)
- [ ] Wire MP6 (A7) → headlights (direct or through relay socket)

**Step 8 — First fire on Haltech**
- [ ] Haltech powered via LP1 (A14)
- [ ] Verify base tune loaded in Haltech NSP
- [ ] IGN on → fuel prime → press START → engine fires
- [ ] Confirm idle, check for fault codes
- [ ] Verify all CAN data flowing (RPM, temps, pressures)

### Test Gate — Phase 2

| Test | Expected | Pass? |
|------|----------|-------|
| Engine starts on Haltech | Clean idle, no faults | |
| All CAN data flowing | RPM, temps, pressures in Race Studio | |
| Fan PWM tracks coolant temp | Correct bands at correct temps | |
| Fuel pump runs while engine running | HP3 active, correct current | |
| Starter interlock | No crank while running | |
| Kill switch kills everything | Engine dies, all power drops | |
| Horn via Ch12 button | MP3 sounds horn | |
| Headlights via Ch04 toggle | MP6 lights on/off | |
| Brake lights | MP4 on pedal press (works with IGN off) | |
| Tail lights | MP5 on with SafeIgnition | |
| Warning LED on alarm | LP7 triggers correctly | |
| OE cluster still works | Tach from Haltech DPO 1, speedo from OEM VSS | |
| Wideband AFR reading | LM2 → AVI 8 shows lambda | |
| **Reversal test:** plug stock ECU back in | Car runs on stock ECU | |

### Deutsch Connector Reference (Phase 2 Harnesses)

> Full harness design with pin maps: `guides/harness-design.md`

**D1 — Engine Sensors (12-pin):** Cam, crank, knock, IAT, MAP, TPS
**D2 — Bank 1 Front (8-pin):** Cyl 1/3/5 — IGN 1/3/5 + INJ 1/3/5 + coil power + injector power (+ separate 16 AWG ground to front head bolt)
**D3 — Bank 2 Rear (8-pin):** Cyl 2/4/6 — IGN 2/4/6 + INJ 2/4/6 + coil power + injector power (+ separate 16 AWG ground to rear head bolt)
**D4 — Lowdoller Sensors (8-pin):** Oil/coolant/fuel pressure+temp, +5V, GND

**Phase 1 note:** D2 and D3 are built during Phase 1 but NOT plugged in. Ground ring terminals NOT bolted. Stock ECU drives coils/injectors through OE harness. When switching to Phase 2, disconnect stock coil/injector connectors per bank, plug in D2 + D3, bolt ground ring terminals to head bolts, reroute MP1/MP2 splices.

---

## Phase 3 — CAN Keypad + OE Removal

### Concept

Full commitment to PDM + Haltech. OE ECU, BCM, and relay box physically removed. CAN keypad adds redundant driver controls alongside physical switches. Direct wiring to all loads — no relay sockets.

### What Changes from Phase 2

| Item | Phase 2 | Phase 3 |
|------|---------|---------|
| Stock ECU | Mounted, unplugged | Removed |
| BCM | Mounted, unplugged | Removed |
| Relay box | Unpowered, relays in place | Removed |
| CAN2 | Unused | CAN Keypad 12 (125 kbps) |
| Fan wiring | Through relay socket or direct | Direct only |
| Horn wiring | Through relay socket or direct | Direct only |
| Headlights | Through relay socket or direct | Direct only |
| Wipers | Not installed | MP9 (B4) / MP10 (B5) via keypad or toggle |
| Race Studio config | **UPDATE REQUIRED** | Add CAN2 keypad + OR triggers |

### Race Studio Config Changes

1. **Enable CAN2** → 125 kbps, AIM CAN Keypad 12 protocol
2. **Add keypad buttons** K33–K42 (see `guides/keypad-config-future.md` for full assignments)
3. **Add keypad power output** — use a spare LP (LP9 B3 or repurpose)
4. **Update Math Channel triggers** to OR keypad + physical switch:

| Trigger | Phase 2 | Phase 3 |
|---------|---------|---------|
| STARTER_SAFE | Ch01 AND SafeIgnition AND NOT ENGINE_RUNNING | **(StarterKYD OR Ch01)** AND SafeIgnition AND NOT ENGINE_RUNNING |
| Fan low override | Ch02 | **(FanLoKYD OR Ch02)** |
| Fan high override | Ch03 | **(FanHiKYD OR Ch03)** |
| Coolsuit | Ch10 AND SafeIgnition | **(CoolsuitKYD OR Ch10)** AND SafeIgnition |
| Horn | Ch12 | **(HornKYD OR Ch12)** |
| Headlights | Ch04 AND SafeIgnition | **(LightsKYD OR Ch04)** AND SafeIgnition |

5. **Add new features** (keypad-only):
   - Fuel override (K38 → FuelOverride toggle → HP3 additional trigger)
   - Pit limiter (K39 → PITLIMITER_SAFE + TPS gating → Haltech CAN output)
   - PodiumConnect comms (K40), pit-in laps (K41)

6. **Add wipers** if needed (relay-less park design):
   - MP9 (B4) → Green (low), MP10 (B5) → Yellow (high), LP9 (B3) → Brown (park)
   - Math channels: WIPER_ACTIVE, WIPER_ACTIVE_DLY (3s delay off), WIPER_PARKING — already configured
   - Trigger: WiperKYD positions OR physical toggles on Ch05/Ch06
   - Motor Black wire → chassis ground. No external relay needed.

### CAN2 Keypad Wiring

| PDM Pin | Connector | Signal | Keypad Side |
|---------|-----------|--------|-------------|
| A28 (CAN2 H) | Black | CAN H | Deutsch pin 2 (White) |
| A29 (CAN2 L) | Black | CAN L | Deutsch pin 1 (Blue) |
| LP power output | Black | +12V | Deutsch pin 4 (Red) |
| B18 (GND) | Grey | GND | Deutsch pin 3 (Black) |

> Full keypad config preserved in `guides/keypad-config-future.md` — button assignments, LED colors, variable names, cable pinout.

### Direct Wiring (Relay Box Removed)

With the relay box removed, all loads wire directly to PDM outputs:

| Load | PDM Output | Wiring |
|------|-----------|--------|
| Fan motor | HP2 (A12+A23) | Direct to fan motor connector, 12 AWG |
| Fuel pump | HP3 (A24+A25) | Direct to pump, 14 AWG |
| Starter | HP1 (A1+A13) | Direct to solenoid S, 10 AWG (already done) |
| Horn | MP3 (A4) | Direct to horn, 16 AWG |
| Headlights | MP6 (A7) | Direct to headlight connector, 14 AWG |
| Wiper low | MP9 (B4) | Direct to motor Green wire, 16 AWG |
| Wiper high | MP10 (B5) | Direct to motor Yellow wire, 16 AWG |
| Wiper park | LP9 (B3) | Direct to motor Brown wire, 16 AWG |

---

## Reference — Kill Switch States

| Kill Switch | IGN Toggle | State |
|-------------|-----------|-------|
| OFF | Any | Dead — all power cut, engine stops, alternator stops |
| ON | OFF | PDM has Surlok power (Race Studio config/testing), SafeIgnition = 0 |
| ON | ON | SafeIgnition = 1, all ignition-gated outputs active |

---

## Reference — CAN Bus Configuration

### CAN0 — AIM Expansion (A22 H / A11 L)

| Setting | Value |
|---------|-------|
| Speed | 1 Mbps |
| Devices | CAN Data Hub (star topology) → GPS-08 (port 1), SmartyCam (port 2), Podium (port 3) |
| Cable | Pre-wired CAN expansion harness (5-pin Binder, 22 AWG) |
| Power | A33 (+Vb out CAN, always on) powers GPS-08 + Podium via hub. SmartyCam powered separately via LP3 (A16, SafeIgnition). |
| Note | Dash connects via LVDS, not CAN0 |

### CAN1 — Haltech ECU (A30 H / A31 L)

| Setting | Value |
|---------|-------|
| Speed | 500 kbps |
| Protocol | Haltech CAN_V2_40 |
| Termination | 120Ω at PDM end if Haltech doesn't self-terminate |
| Silent on CAN | OFF initially; enable if Haltech logs CAN errors |
| Haltech wiring | 26-pin pin 23 (W) → A30; pin 24 (L) → A31 |
| Note | A30/A31 shared with RS232 — RS232 unavailable when CAN1 active |

### CAN2 — Unused (Phase 1/2) / Keypad (Phase 3)

| Setting | Value |
|---------|-------|
| Pins | A28 (H) / A29 (L) |
| Speed | 125 kbps (when keypad connected) |
| Phase 1/2 | Disabled |
| Phase 3 | AIM CAN Keypad 12 |

> **CRITICAL:** Never wire CAN2 devices to CAN0 (A11/A22). CAN0 = 1 Mbps. Mixing speeds = both buses fail.

---

## Reference — PDM Physical Connections by Phase

### Connector A (Black) — All Phases

| Pin | Output | Load | Ph1 | Ph2 | Ph3 |
|-----|--------|------|-----|-----|-----|
| A1+A13 | HP1 | Starter solenoid S | Direct | Direct | Direct |
| A2 | MP1 | Power | Main relay pin 87 | D3 pin 7 (inj) | Direct to inj rail |
| A3 | MP2 | Power | Main relay pin 87 | D2 pin 7 (coils) | Direct to coil bus |
| A4 | MP3 | Horn | Not connected | Horn relay/direct | Direct |
| A5 | MP4 | Brake lights | Connected | Same | Same |
| A6 | MP5 | Tail lights | Connected | Same | Same |
| A7 | MP6 | Headlights | Not connected | Relay/direct | Direct |
| A8 | MP7 | Coolsuit | Connected | Same | Same |
| A9 | MP8 | Defogger | Connected | Same | Same |
| A12+A23 | HP2 | Fan | Ph1B: relay/direct | Direct | Direct |
| A14 | LP1 | Haltech ECU | Connected | Same | Same |
| A15 | LP2 | Dash | Connected | Same | Same |
| A16 | LP3 | SmartyCam | Connected | Same | Same |
| A17 | LP4 | GPS | Connected | Same | Same |
| A18 | LP5 | LM2 Wideband | Connected | Same | Same |
| A19 | LP6 | Cluster | Connected | Same | Same |
| A20 | LP7 | Warning LED | Connected | Same | Same |
| A21 | LP8 | Alt exciter | Connected | Same | Same |
| A24+A25 | HP3 | Fuel pump | Relay pin 87 | Direct | Direct |

### Connector B (Grey) — Wiper + Phase 3 Additions

| Pin | Output | Load | Ph3 |
|-----|--------|------|-----|
| B3 | LP9 | Wiper Park (Brown) | Direct to motor Brown wire |
| B4 | MP9 | Wiper Low (Green) | Direct to motor Green wire |
| B5 | MP10 | Wiper High (Yellow) | Direct to motor Yellow wire |

---

## Reference — Switch Panel by Phase

### Phase 1 Panel (6 positions + 1 momentary + 1 LED)

```
[IGN]  [FAN]  [COOL]  [DEFOG]  [____]  [____]
[START]                                  (LED)
```

### Phase 2 Panel (8 positions + 1 momentary + 1 LED)

```
[IGN]  [FAN]  [COOL]  [DEFOG]  [HORN]  [LIGHTS]
[START]                                  (LED)
```

> Horn = momentary (not latching). Headlights = latching toggle.

### Phase 3 Panel — Same + CAN Keypad

Physical panel remains as backup. CAN keypad provides redundant controls with LED feedback.

---

## Reference — Webinar Config → Tiburon Mapping

Starting point: `Webinar complete.zconfig`. This table maps what was renamed/repurposed.

| Webinar Output | Webinar HW | Tiburon Output | Notes |
|---|---|---|---|
| `Starter` | HP (series diode) | **HP1 Starter** | Keep — OVC 20A, inductive |
| `FanSpeed` | HP | **HP2 Fan** | Keep — add 4-level PWM bands |
| `Fuel1A` + `Fuel1B` | 2× MP | **HP3 FuelPump** | Consolidate to single HP3 |
| `Siren` | MP | **MP3 Horn** | Rename |
| `Ignition` | LP/MP | **MP1 InjectorPwr** | Repurpose |
| `High Beams` | MP | **MP2 CoilPwr** | Repurpose |
| `Low Beams` | MP | **MP4 BrakeLights** | Repurpose |
| `MidPO3` spare | MP | **MP5 TailLights** | Enable |
| `MidPO4` spare | MP | **MP6 Headlights** | Enable |
| `MidPO5` spare | MP | **MP7 Coolsuit** | Enable |
| `LowPO2–7` spares | LP | **LP1–LP6** Accessories | Enable |
| `LowPO8` spare | LP | **LP7 WarningLED** | Enable |

**Webinar variables to delete:** `StarterKYD`, `SirenKYD`, `LightsKYD`, `FanKYD`, `IgnitionKYD`, `ColorsConditionK01–K12`, `BitRed/Green/BlueX15–X1C`. Keep `SafeIgnition`, `FuelSV` (keep as-is, reference example), `momentary_SW` (repurpose → Ch01 START).

---

## Reference — Pit Limiter CAN Output (Phase 3)

To send `PITLIMITER_ACTIVE` to the Haltech when CAN keypad is added:

**Option A (CAN — recommended):**
1. CAN Output 1 → create new CAN message
2. Destination: Haltech CAN address (check Haltech NSP CAN Receive page for message ID and byte)
3. Map `PITLIMITER_ACTIVE` to the correct byte/bit
4. In Haltech NSP: Configure → Speed Limiter → Enable via CAN → set target speed (35 mph for pit lane)

**Option B (Wire):**
1. Assign `PITLIMITER_ACTIVE` → spare LP output
2. Wire that LP output → Haltech SPI pin configured as digital input
3. In Haltech NSP: Configure → Speed Limiter → Enable via digital input pin

---

## Cross-References

| File | Contents |
|------|----------|
| `guides/harness-design.md` | Deutsch connector pin maps, wire routing, bundle sizing |
| `guides/bench-test.md` | Bench test procedures, fuse box tap procedure, notes log |
| `guides/keypad-config-future.md` | Full CAN keypad button/LED/variable config for Phase 3 |
| `signal-routing.md` | End-to-end signal trace for every wire |
| `weekend-tasks.md` | Current weekend build tasks (sensor install, harness fab) |
| `hardware/aim/aim-pdm/pdm-pinout.md` | Full 35-pin ×2 connector pinout |
| `hardware/aim/aim-pdm/pdm-configuration-guide.md` | Logic stack theory, PWM examples |
| `hardware/aim/aim-smartycam/aim-smartycam.md` | SmartyCam 3 pinout, RS3 config, overlay setup |
| `hardware/aim/aim-podium/aim-podium-micro.md` | PodiumConnect Micro pinout, RaceCapture config, CAN mapping |
| `hardware/aim/aim-datahub/aim-datahub.md` | CAN Data Hub star topology, pin mapping |
| `hardware/aim/aim-gps08/aim-gps08.md` | GPS-08 pinout, CAN behavior, mounting |
| `hardware/sensors/lowdoller-sensors.md` | Sensor specs, PTC calibration |
| `hardware/sensors/cop-ignition.md` | Toyota COP coil pinout |
