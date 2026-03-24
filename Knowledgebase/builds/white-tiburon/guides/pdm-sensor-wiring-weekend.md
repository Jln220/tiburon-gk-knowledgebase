# PDM Sensor Wiring — Weekend Config (No Haltech)

**Car:** White 2003 Tiburon GK
**Config:** PDM standalone — Haltech not connected
**Purpose:** Wire all available sensors to PDM analog inputs for logging and monitoring

> **Temporary configuration.** When the Haltech goes in, fuel pressure, coolant temp, and oil pressure move to Haltech AVI channels. This config reclaims switch channels for analog sensors — only 4 switches are active.

---

## Channel Reassignment Summary

Normal PDM config uses Ch01–Ch06 for switches. This weekend, switches move to digital-only channels (Ch09–Ch12) so all 8 analog-capable channels (Ch01–Ch08) are available for sensors.

### Switches This Weekend (Digital-Only Channels)

| Ch | Pin | Name | Close To | Pull-Up | Switch Type | Wiring |
|----|-----|------|----------|---------|-------------|--------|
| IGN | G23 | *(built-in)* | VBatt | No | Latching toggle | 12V → switch → G23 |
| 09 | G21 | `StarterSW` | Ground | ✅ 10kΩ | Momentary button | G21 → switch → GND |
| 10 | G22 | `CoolsuitSW` | Ground | ✅ 10kΩ | Latching toggle | G22 → switch → GND |
| 11 | B26 | `FanLoSW` | Ground | ✅ 10kΩ | Latching toggle | B26 → switch → GND |
| 12 | B27 | `FanHiSW` | Ground | ✅ 10kΩ | Latching toggle | B27 → switch → GND |

> **Ch09 changes from VBatt (brake switch) to Ground (starter).** Reconfigure in Race Studio.
>
> **Ch11–Ch12 move from Grey connector (B-connector) to Black connector (A-connector).** Ch11 = A26, Ch12 = A27. Route switch wires to the Black connector, not Grey.

### Switches NOT Active This Weekend

| Normal Ch | Normal Name | Status |
|-----------|-------------|--------|
| Ch01 (G26) | StarterSW | → Now sensor input |
| Ch02 (G27) | FanLoSW | → Now sensor input |
| Ch03 (G28) | FanHiSW | → Now sensor input |
| Ch04 (G29) | HeadlightSW | → Now sensor input |
| Ch05 (G30) | WiperLoSW | → Now sensor input |
| Ch06 (G31) | WiperHiSW | → Now sensor input |
| Ch09 (G21) | BrakeSW | → Now StarterSW |
| Ch11 (B26) | DefoggerSW | → Now FanLoSW |
| Ch12 (B27) | HornSW | → Now FanHiSW |

---

## Sensor Channel Map (Analog Channels Ch01–Ch08)

All sensors on Grey connector (Connector B). +5V supply from G16 (Vref). GND from G18 or B13/B14 (P GND).

| Ch | Pin | Sensor | Signal | Sensor Wire | Mode | Pull-Up | Calibration |
|----|-----|--------|--------|-------------|------|---------|-------------|
| 01 | G26 | Oil 899404 | **Oil pressure** | Yellow | Analog 0–5V | No | PSI = (V − 0.5) × 37.5 |
| 02 | G27 | Oil 899404 | **Oil temp** | Green | Analog 0–5V | ✅ 10kΩ | PTC table (see below) |
| 03 | G28 | Fuel 899404 | **Fuel pressure** | Yellow | Analog 0–5V | No | PSI = (V − 0.5) × 37.5 |
| 04 | G29 | Fuel 899404 | **Fuel temp** | Green | Analog 0–5V | ✅ 10kΩ | PTC table (see below) |
| 05 | G30 | Coolant LDM899TP100 | **Coolant pressure** | Yellow | Analog 0–5V | No | PSI = (V − 0.5) × 25.0 |
| 06 | G31 | Coolant LDM899TP100 | **Coolant temp** | Green | Analog 0–5V | ✅ 10kΩ | PTC table (see below) |
| 07 | G32 | Crankcase sensor | **Crankcase pressure** | — | Analog 0–5V | No | Per sensor spec (TBD) |
| 08 | G33 | IR pyrometer | **Tire temp** | — | Analog 0–5V | No | Per sensor spec (TBD) |

### Sensor Power & Ground

| Function | Pin | Connector | Notes |
|----------|-----|-----------|-------|
| **+5V sensor supply** | G16 | Grey (B) | Vref — powers all ratiometric sensors. All Red wires here. |
| **Signal GND** | G18 | Grey (B) | All Black (pressure GND) and White (temp GND) wires here. |
| **P GND (alternate)** | G13, G14 | Grey (B) | Power ground — use if G18 is full. Same ground plane. |

---

## Physical Wiring — Combo Sensors (Oil, Fuel, Coolant)

Each Lowdoller combo sensor has 5 wires. Two PDM channels per sensor.

### Oil Combo (899404) — Ch01 + Ch02

| Sensor Wire | Color | Function | PDM Pin | Ch |
|-------------|-------|----------|---------|----|
| Red | Red | +5V supply | G16 (Vref) | — |
| Black | Black | Pressure GND | G18 (GND) | — |
| Yellow | Yellow | Pressure signal (0.5–4.5V) | **G26** | **Ch01** |
| White | White | Temp GND | G18 (GND) | — |
| Green | Green | Temp signal (PTC resistive) | **G27** | **Ch02** |

### Fuel Combo (899404) — Ch03 + Ch04

| Sensor Wire | Color | Function | PDM Pin | Ch |
|-------------|-------|----------|---------|----|
| Red | Red | +5V supply | G16 (Vref) | — |
| Black | Black | Pressure GND | G18 (GND) | — |
| Yellow | Yellow | Pressure signal (0.5–4.5V) | **G28** | **Ch03** |
| White | White | Temp GND | G18 (GND) | — |
| Green | Green | Temp signal (PTC resistive) | **G29** | **Ch04** |

### Coolant Combo (LDM899TP100) — Ch05 + Ch06

| Sensor Wire | Color | Function | PDM Pin | Ch |
|-------------|-------|----------|---------|----|
| Red | Red | +5V supply | G16 (Vref) | — |
| Black | Black | Pressure GND | G18 (GND) | — |
| Yellow | Yellow | Pressure signal (0.5–4.5V) | **G30** | **Ch05** |
| White | White | Temp GND | G18 (GND) | — |
| Green | Green | Temp signal (PTC resistive) | **G31** | **Ch06** |

### Crankcase Pressure — Ch07

| Sensor Wire | Function | PDM Pin | Ch |
|-------------|----------|---------|----|
| +5V (Red or per sensor) | +5V supply | G16 (Vref) | — |
| GND (Black or per sensor) | Signal GND | G18 (GND) | — |
| Signal (per sensor) | 0–5V pressure output | **G32** | **Ch07** |

### Tire Temp IR Pyrometer — Ch08

| Sensor Wire | Function | PDM Pin | Ch |
|-------------|----------|---------|----|
| +5V (per sensor) | +5V supply | G16 (Vref) | — |
| GND (per sensor) | Signal GND | G18 (GND) | — |
| Signal (per sensor) | 0–5V temp output | **G33** | **Ch08** |

---

## G16 (Vref) Load Budget

PDM +5V Vref current capacity is not specified in docs — typical AIM spec is ~150mA.

| Sensor | Est. Current |
|--------|-------------|
| Oil combo (ratiometric) | ~15 mA |
| Fuel combo (ratiometric) | ~15 mA |
| Coolant combo (ratiometric) | ~15 mA |
| Crankcase pressure | ~10 mA |
| IR tire temp | ~20 mA |
| **Total estimate** | **~75 mA** |

Should be well within Vref budget. If Vref sags under load, check with multimeter — should read 5.00V ± 0.05V at the sensor end.

---

## PTC Temp Resolution on PDM (10kΩ Pull-Up)

The Lowdoller PTC thermistor range is 84.27Ω (−40°F) to 197.71Ω (500°F). With the PDM's 10kΩ internal pull-up to ~5V, the voltage divider output is:

| Temp (°F) | Resistance (Ω) | Voltage at Pin (V) |
|-----------|----------------|--------------------|
| −40 | 84.27 | 0.042 |
| 32 | 100.00 | 0.050 |
| 104 | 115.54 | 0.057 |
| 212 | 138.51 | 0.068 |
| 320 | 161.05 | 0.079 |
| 500 | 197.71 | 0.097 |

**Total voltage span: ~55 mV across 540°F.** With 12-bit ADC over 0–5V range, resolution is ~1.22 mV/step → ~45 usable ADC steps → **~12°F per step.**

This is coarse but functional for monitoring. If finer resolution is needed, add an external 1kΩ pull-up resistor (from G16 +5V to the Green wire) and disable the internal 10kΩ pull-up. With 1kΩ pull-up, voltage span improves to ~390–825 mV (~435 mV span → ~1.5°F per step).

> **For this weekend:** Start with the 10kΩ internal pull-up. If temp readings are too coarse, add external 1kΩ pull-ups later. The Haltech AVI inputs use 1kΩ pull-ups for these sensors.

---

## Race Studio 3 Configuration Changes

### Channels to Reconfigure (Switches → Digital-Only Pins)

For each switch channel that moves, update Race Studio:

#### Ch09 — `StarterSW` (was `BrakeSW`)

| Field | Old Value | New Value |
|-------|-----------|-----------|
| **Name** | `BrakeSW` | `StarterSW` |
| **Active when signal is** | Close to VBatt | **Close to ground** |
| **Use internal pull up 10kΩ** | No | **✅ Yes** |
| **Work As** | Momentary | Momentary |

#### Ch11 — `FanLoSW` (was `DefoggerSW`)

| Field | Old Value | New Value |
|-------|-----------|-----------|
| **Name** | `DefoggerSW` | `FanLoSW` |
| **Active when signal is** | Close to ground | Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes | ✅ Yes |
| **Work As** | Momentary | Momentary |

#### Ch12 — `FanHiSW` (was `HornSW`)

| Field | Old Value | New Value |
|-------|-----------|-----------|
| **Name** | `HornSW` | `FanHiSW` |
| **Active when signal is** | Close to ground | Close to ground |
| **Use internal pull up 10kΩ** | ✅ Yes | ✅ Yes |
| **Work As** | Momentary | Momentary |

### Channels to Reconfigure (Switches → Analog Sensors)

For each analog sensor channel, switch from Digital to Analog mode:

#### Ch01 — `OilPressure` (was `StarterSW`)

| Field | Value |
|-------|-------|
| **Name** | `OilPressure` |
| **Mode** | ◉ Analog |
| **Sensor** | Custom (0–5V) |
| **Sampling Frequency** | 50 Hz |
| **Log values** | ✅ Yes |
| **Use internal pull up 10kΩ** | ❌ No |
| **Custom calibration** | 0.5V = 0 PSI, 4.5V = 150 PSI (linear) |

#### Ch02 — `OilTemp` (was `FanLoSW`)

| Field | Value |
|-------|-------|
| **Name** | `OilTemp` |
| **Mode** | ◉ Analog |
| **Sensor** | Custom (resistive / 0–5V) |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Custom calibration** | PTC table: 0.042V = −40°F … 0.097V = 500°F (see PTC table above) |

#### Ch03 — `FuelPressure` (was `FanHiSW`)

| Field | Value |
|-------|-------|
| **Name** | `FuelPressure` |
| **Mode** | ◉ Analog |
| **Sensor** | Custom (0–5V) |
| **Sampling Frequency** | 50 Hz |
| **Log values** | ✅ Yes |
| **Use internal pull up 10kΩ** | ❌ No |
| **Custom calibration** | 0.5V = 0 PSI, 4.5V = 150 PSI (linear) |

#### Ch04 — `FuelTemp` (was `HeadlightSW`)

| Field | Value |
|-------|-------|
| **Name** | `FuelTemp` |
| **Mode** | ◉ Analog |
| **Sensor** | Custom (resistive / 0–5V) |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Custom calibration** | PTC table (same as OilTemp) |

#### Ch05 — `CoolantPressure` (was `WiperLoSW`)

| Field | Value |
|-------|-------|
| **Name** | `CoolantPressure` |
| **Mode** | ◉ Analog |
| **Sensor** | Custom (0–5V) |
| **Sampling Frequency** | 50 Hz |
| **Log values** | ✅ Yes |
| **Use internal pull up 10kΩ** | ❌ No |
| **Custom calibration** | 0.5V = 0 PSI, 4.5V = 100 PSI (linear) |

#### Ch06 — `CoolantTemp` (was `WiperHiSW`)

| Field | Value |
|-------|-------|
| **Name** | `CoolantTemp` |
| **Mode** | ◉ Analog |
| **Sensor** | Custom (resistive / 0–5V) |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Use internal pull up 10kΩ** | ✅ Yes |
| **Custom calibration** | PTC table (same as OilTemp) |

#### Ch07 — `CrankcasePressure` (was SPARE)

| Field | Value |
|-------|-------|
| **Name** | `CrankcasePressure` |
| **Mode** | ◉ Analog |
| **Sensor** | Custom (0–5V) |
| **Sampling Frequency** | 50 Hz |
| **Log values** | ✅ Yes |
| **Use internal pull up 10kΩ** | ❌ No |
| **Custom calibration** | Per sensor spec (TBD) |

#### Ch08 — `TireTemp` (was SPARE)

| Field | Value |
|-------|-------|
| **Name** | `TireTemp` |
| **Mode** | ◉ Analog |
| **Sensor** | Custom (0–5V) |
| **Sampling Frequency** | 10 Hz |
| **Log values** | ✅ Yes |
| **Use internal pull up 10kΩ** | ❌ No |
| **Custom calibration** | Per IR pyrometer spec (TBD) |

---

## Power Output Trigger Updates

Moving switch inputs to new channels requires updating power output triggers.

| Output | Trigger Change |
|--------|---------------|
| HP1 (Starter) | Change trigger from `Ch01` (StarterSW) → **`Ch09`** (StarterSW) |
| HP2 (Fan) | Change trigger from `Ch02`/`Ch03` (FanLoSW/FanHiSW) → **`Ch11`/`Ch12`** (FanLoSW/FanHiSW). Without Haltech CAN providing ECT, fan runs on manual switches only. |
| MP3 (WiperLow) | **Disable** — no wiper switch this weekend |
| MP6 (WiperHigh) | **Disable** — no wiper switch this weekend |
| MP7 (Coolsuit) | Change trigger from `Ch04` → **`Ch10`** (CoolsuitSW). Ch10 was already CoolsuitSW — verify trigger matches. |
| MP8 (Defogger) | **Disable** — no defogger switch this weekend |

> **Fan without ECT data:** With no Haltech on CAN, the PDM has no ECT value for automatic PWM. Fan control is manual only via FanLoSW (Ch11) and FanHiSW (Ch12). Consider setting FanLo trigger = Ch11 at 60% duty, FanHi trigger = Ch12 at 100% duty. Or just run 100% on either switch.

---

## Connector Pin Summary — Grey Connector (B) This Weekend

| Pin | Normal Config | Weekend Config |
|-----|---------------|----------------|
| G16 | Vref (unused) | **Vref → all sensor +5V** |
| G18 | GND | **GND → all sensor grounds** |
| G21 (Ch09) | BrakeSW (VBatt) | **StarterSW (GND, 10kΩ)** |
| G22 (Ch10) | CoolsuitSW | CoolsuitSW *(no change)* |
| G26 (Ch01) | StarterSW | **OilPressure (analog 0–5V)** |
| G27 (Ch02) | FanLoSW | **OilTemp (analog, 10kΩ PTC)** |
| G28 (Ch03) | FanHiSW | **FuelPressure (analog 0–5V)** |
| G29 (Ch04) | HeadlightSW | **FuelTemp (analog, 10kΩ PTC)** |
| G30 (Ch05) | WiperLoSW | **CoolantPressure (analog 0–5V)** |
| G31 (Ch06) | WiperHiSW | **CoolantTemp (analog, 10kΩ PTC)** |
| G32 (Ch07) | SPARE | **CrankcasePressure (analog 0–5V)** |
| G33 (Ch08) | SPARE | **TireTemp (analog 0–5V)** |

## Connector Pin Summary — Black Connector (A) This Weekend

| Pin | Normal Config | Weekend Config |
|-----|---------------|----------------|
| A26 (Ch11) | DefoggerSW | **FanLoSW (GND, 10kΩ)** |
| A27 (Ch12) | HornSW | **FanHiSW (GND, 10kΩ)** |

---

## Reverting to Normal Config

When the Haltech goes in and sensors move to AVI inputs:

1. **Race Studio:** Reload `Tiburon_White_v1.zconfig` (original config)
2. **Rewire switches** back to Grey connector Ch01–Ch06 pins
3. **Move sensor wires** from PDM Grey connector to Haltech 26-pin / 34-pin
4. **Sensors staying on PDM permanently:** Crankcase pressure (Ch07), Tire temp (Ch08)
5. **Sensors moving to Haltech AVI:** Oil P/T, Fuel P/T, Coolant P/T (6 signals → AVI 1–6)

---

## Related Files

| File | Contents |
|------|----------|
| `pdm-build-guide.md` | Normal PDM config — all switch assignments, power output map |
| `lowdoller-sensors.md` | Sensor specs, calibration tables, wiring colors |
| `signal-routing.md` | Full signal routing plan (Haltech + PDM) |
| `pdm-pinout.md` | Complete PDM 32 connector pinout |
