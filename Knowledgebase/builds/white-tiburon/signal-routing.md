# Signal Routing — White Tiburon (Haltech + AIM PDM)
## End-to-End Signal Trace Reference

**Car:** White 2003 Hyundai Tiburon GK — Haltech Elite 2500 + AIM PDM 32
**Confidence key:** ✅ Verified from factory/Haltech PDF | ⚠️ Forum/wiki sourced, needs NSP confirmation | 🔲 Planned, not yet wired

---

## Cluster Gauges (OEM Cluster → Haltech Integration)

| Signal | Physical Source | Source Connector | OEM Wire | Cluster Connector/Pin | Haltech Connection | Haltech Wire | Notes |
|--------|----------------|-----------------|---------|----------------------|-------------------|--------------|-------|
| **Tachometer** | Haltech ECU (generated) | — | — | M10-1 TACHO SIGNAL | **34-pin pin 18** (DPO 1) | V/B | ✅ 3 pulses/rev, 12V pull-up, active low; configure in NSP as Tacho Output. OLD source: ECM C133-4 pin 17 — disconnect ECM side |
| **Speedometer** | VSS on transaxle (C109) | C109 Hall IC | OEM VSS wire | M10-1 SPEED SIGNAL | **26-pin pin 8** (SPI 1) | GY (shielded) | ✅ Keep OEM VSS→cluster wire; add splice/T to SPI 1. 4 pulses/rev, 637 rpm = 60 km/h |
| **Fuel Level** | OEM fuel sender (M55) | M55 | FUEL UNIT wire | M10-1 FUEL UNIT + FUEL GND | NOT involved | — | ✅ Direct resistive circuit: Fuse17→gauge→sender→GND. 6Ω(full)–97Ω(empty). No ECU in loop |
| **Coolant Temp (gauge)** | OEM CTS sender (C111 gauge pin) | C111 | TEMP UNIT wire | M10-1 TEMP UNIT | NOT involved | — | ✅ Direct resistive circuit: Fuse17→gauge→CTS sender→GND. NTC 143.4Ω@60°C → 17.5Ω@125°C |
| **Check Engine Light** | Haltech DPO (optional) | — | — | — | Available DPO | — | 🔲 Stock: ECM C133-4 ground-side drive. Haltech can replicate via DPO if desired |
| **VSS → BCM** | VSS on transaxle (C109) | C109 | OEM BCM wire | — | BCM-JM pin 4 | — | ⚠️ BCM uses VSS for over-speed warning/wiper speed. Keep if BCM retained |

**Cluster power:** Fuse 17 (10A, IG1 switched) → cluster indicator power and gauge coil power.

---

## Lowdoller Combo Sensors (+5V Supply, Ratiometric Pressure + PTC Temp)

All sensors: Red=+5V, Black=pressure GND, Yellow=pressure signal, White=temp GND, Green=temp signal.
**+5V Supply:** All red wires → **Haltech 34-pin pin 9** (O, orange) — 100mA max total.
**Signal GND:** All black + white wires → **Haltech 26-pin pins 14/15/16** (B/W) signal ground.

| Signal | Sensor | Sensor PN | Thread | Haltech AVI | Physical Pin | Wire Color | Calibration |
|--------|--------|-----------|--------|-------------|-------------|------------|-------------|
| **Fuel pressure** | Fuel return line | 899404 | 1/8" NPT | AVI 1 | 26-pin pin 13 | GY/Y (shld) | PSI = (V−0.5)×37.5, range 0–150 PSI ✅ |
| **Fuel temp** | Fuel return line | 899404 | — (same body) | AVI 2 | 34-pin pin 16 | O/B | PTC custom table (84.27Ω@-40°F → 197.71Ω@500°F) ✅ |
| **Oil pressure** | Engine (1/8" NPT port) | 899404 | 1/8" NPT | AVI 3 | 34-pin pin 17 | O/R | PSI = (V−0.5)×37.5, range 0–150 PSI ✅ |
| **Oil temp** | Engine (same body) | 899404 | — | AVI 4 | 34-pin pin 2 | O/Y | PTC custom table ✅ |
| **Coolant pressure** | Coolant manifold | LDM899TP100 | M12×1.5 | AVI 5 | 26-pin pin 20 | O/G | PSI = (V−0.5)×25.0, range 0–100 PSI ✅ |
| **Coolant temp** | Coolant manifold | LDM899TP100 | — (same body) | AVI 6 | 26-pin pin 12 | GY/O (shld) | PTC custom table ✅ |
**Brake combo (899405) moved to future expansion** — requires 2 additional AVI channels. See harness planning notes below.

---

## Engine Sensors (OEM / MAP)

| Signal | Sensor | Connector | Haltech Pin | Wire Color | Signal Type | Notes |
|--------|--------|-----------|-------------|------------|-------------|-------|
| **MAP sensor** | Elite 2500 built-in MAP | — | Internal | — | — | ✅ Built-in to ECU — does NOT use an AVI channel. Connect vacuum line to ECU barb |
| **Throttle position (TPS)** | OEM TPS on throttle body | — | **34-pin pin 14** (AVI 10) | W | 0–5V | ✅ |
| **Intake air temp (IAT)** | IAT sensor | — | **26-pin pin 3** (AVI 7) | GY | Resistive, 1K pull-up | ✅ Default Haltech label for this pin |
| **Wideband O2 (AFR)** | Innovate LM2 Analog Out 1 (Lime Green +, Yellow −) | Cable 3811 | **26-pin pin 4** (AVI 8) | V | 0–5V (7.35–22.39 AFR) | 🔲 LM2 in footwell — cockpit run only. Haltech default label "Coolant Temp" — reassign in NSP |
| **Crankcase pressure** | 0–5V sensor on vacuum tee between valve covers | — | **34-pin pin 15** (AVI 9) | Y | 0–5V ratiometric | 🔲 Built-in MAP frees AVI 9 for crankcase pressure |
| **Crank position (+)** | CKP sensor (39180-37150 / NTK EH0220) | — | **26-pin pin 1** (Trig+) | Y (shielded) | Hall effect | ✅ |
| **Crank position (−)** | CKP sensor | — | **26-pin pin 5** | G (shielded) | Signal ground ref | ✅ |
| **Cam position (+)** | CMP sensor (39350-37100 / NTK EC0145) | — | **26-pin pin 2** (Home+) | Y (shielded) | Hall effect | ✅ |
| **Cam position (−)** | CMP sensor | — | **26-pin pin 6** | G (shielded) | Signal ground ref | ✅ |
| **Knock sensor 1** | OEM knock sensor | — | **26-pin pin 21** | GY/G | Piezoelectric | ✅ |
| **Knock sensor 2** | OEM knock sensor | — | **26-pin pin 22** | GY/L | Piezoelectric | ✅ |

---

## Ignition (Coils — COP Sequential)

**Coil:** Toyota 90919-A2005 smart coil ×6. Sequential COP — IGN1–6 all used.
**Power:** PDM MP2 → 12V common bus → Pin D on all 6 coils.
**Ground:** Engine block → GND bus → Pin A on all 6 coils.
**Dwell:** ~2.1 ms in Haltech NSP. Smart coil — internal igniter. Do NOT exceed dwell.
**NSP setting:** Ignition mode = Sequential COP, Coil type = Smart coil.
See `cars/cop-ignition.md` for full coil pinout (A/B/C/D), wiring diagram, and part numbers.

| Signal | Haltech Pin | Wire Color | Coil Pin | Notes |
|--------|-------------|------------|----------|-------|
| Ignition 1 | 34-pin pin 3 | Y/B | B (trigger) | 🔲 COP Cyl 1 — Toyota 90919-A2005 |
| Ignition 2 | 34-pin pin 4 | Y/R | B (trigger) | 🔲 COP Cyl 2 |
| Ignition 3 | 34-pin pin 5 | Y/O | B (trigger) | 🔲 COP Cyl 3 |
| Ignition 4 | 34-pin pin 6 | Y/G | B (trigger) | 🔲 COP Cyl 4 |
| Ignition 5 | 34-pin pin 7 | Y/BR | B (trigger) | 🔲 COP Cyl 5 |
| Ignition 6 | 34-pin pin 8 | Y/L | B (trigger) | 🔲 COP Cyl 6 |

---

## Fuel Injectors

**Power:** PDM output → 12V to injector rail → also to **34-pin pin 26** (R/L) ECU injector power input.

| Signal | Haltech Pin | Wire Color | Notes |
|--------|-------------|------------|-------|
| ECU injector power in | **34-pin pin 26** | R/L | **REQUIRED** — 12V from injection relay |
| Injector 1 | 34-pin pin 19 | L | Ground-side, 0–8A peak / 0–2A hold |
| Injector 2 | 34-pin pin 20 | L/B | |
| Injector 3 | 34-pin pin 21 | L/BR | |
| Injector 4 | 34-pin pin 22 | L/R | |
| Injector 5 | 34-pin pin 27 | L/O | |
| Injector 6 | 34-pin pin 28 | L/Y | |

---

## Fuel Pump

| Signal | From | To | Notes |
|--------|------|----|-------|
| 12V power | PDM output | Fuel pump + | PDM provides switched 12V |
| Trigger (control) | **Haltech 34-pin pin 24** (DPO 5) | PDM channel input | B/Y wire. Ground-side trigger to PDM. PDM logic: 3s prime + RPM>50 |

---

## Power & ECU Supply

| Signal | Source | Haltech Pin | Notes |
|--------|--------|-------------|-------|
| ECU 13.8V supply | PDM output / fuse block | **26-pin pin 11** | R/W wire |
| ECU ignition input | Ignition switch / PDM | **34-pin pin 13** | P (purple). 12V when IGN on + cranking |
| Battery ground | Battery negative | **34-pin pins 10, 11** | B (black) — two pins to chassis/batt GND |
| +5V sensor supply | Internal (output) | **34-pin pin 9** | O (orange) — 100mA max. For Lowdoller sensors |
| +8V sensor supply | Internal (output) | **34-pin pin 12** | O/W (orange/white) — 1A max. For MAP sensor, OEM-type sensors |

---

## CAN Bus & Data Chain

| Signal | From Pin | To Device | To Pin | Wire | Protocol | Notes |
|--------|----------|-----------|--------|------|----------|-------|
| CAN H | Haltech 26-pin pin 23 | AIM PDM (CAN0) | PDM Connector A pin 22 | W (white) | ISO 11898, 500 kbps | ✅ Haltech broadcasts RPM, coolant temp, throttle, etc. |
| CAN L | Haltech 26-pin pin 24 | AIM PDM (CAN0) | PDM Connector A pin 11 | L (blue) | | ✅ PDM uses CAN data for: fuel pump RPM trigger, fan temp trigger |
| CAN H (PDM → dash) | PDM Connector A pin 22 | AIM 10" Dash | — | — | | ⚠️ AIM dash may daisy-chain from PDM or use its own CAN port |
| CAN H (PDM → GPS) | PDM CAN | AIM GPS | — | — | | 🔲 GPS adds lap timing |
| CAN H (PDM → Smartycam) | PDM CAN | AIM Smartycam | — | — | | 🔲 Smartycam overlays data on video |
| CAN H (PDM → Podium) | PDM CAN | AIM Podium | — | — | | 🔲 Podium = telemetry uplink |

**Haltech CAN data available to PDM:** Engine RPM, MAP (built-in), coolant temp, throttle position, vehicle speed, fuel pressure, oil pressure, all AVI values — eliminates need for duplicate analog wiring to PDM.

---

## Sensor Supply Bus (+5V)

All Lowdoller sensors share the **+5V rail** from Haltech 34-pin pin 9:

```
Haltech 34-pin pin 9 (+5V, O wire)
    ├── Fuel sensor (899404) — Red wire
    ├── Oil sensor (899404) — Red wire
    ├── Coolant sensor (LDM899TP100) — Red wire
    └── Crankcase pressure sensor — Red wire (if 5V supply type)
```

**All pressure grounds** (Black wires) and **temp grounds** (White wires) → Haltech 26-pin pins 14/15/16 (B/W signal GND).

---

## Sensors on PDM (Lower Priority / Logging Only)

| Sensor | PDM Input | Signal Type | Notes |
|--------|-----------|-------------|-------|
| **Narrowband O2** (×2) | PDM analog inputs | 0–1V | OEM-style for A/F logging — not used for closed-loop fuel control |
| **Track/tire temp** | PDM analog input | Resistive / infrared | IR pyrometer or contact sensor for tire temps |

**PDM analog inputs are 0–5V, 12-bit.** Lower sample rate than Haltech AVI but sufficient for logging-only sensors.

---

## Future Expansion — Leave Harness Room

All sensors below require additional AVI channels. Plan harness connector capacity and wire runs now, but do not assign AVI pins until ready to install.

| Sensor | Type | AVI Needed | Connector | Harness Notes |
|--------|------|-----------|-----------|---------------|
| **Brake pressure/temp** | Lowdoller 899405 (1500 PSI combo) | 2 | Deutsch DTM-4 | Run to brake line — fittings to Jak. 5-wire → DTM-4 (combine GNDs) |
| **Transmission temp/pressure** | Lowdoller 899404 (150 PSI combo) | 2 | Deutsch DTM-4 | Run to trans — depends on AVI availability |
| **Haltech TPS module** | Haltech dual TPS (CAN-based) | 0 (CAN) | Haltech connector | Replaces AVI 10 TPS — frees 1 AVI channel |
| **EGT** (×1 or ×6) | K-type thermocouple | 1 per (or CAN EGT module) | Miniature K-type | CAN-based EGT module preferred to avoid consuming AVI channels |

**Expansion strategy:** Haltech TPS module frees AVI 10. CAN-based EGT module avoids AVI consumption. Brake + trans combos need 4 AVI — possible with TPS module freeing 1 + REM harness AVI inputs (REM harness has AVI 1–10 wired back to ECU even without REM unit).

---

## Vehicle Speed Sensor (VSS) Distribution

```
Transaxle VSS (C109) — Hall IC, 4 pulses/rev
    ├── Cluster M10-1 SPEED SIGNAL (OEM wire, keep as-is)
    ├── Haltech 26-pin pin 8 (SPI 1, GY shielded) — add splice/T
    └── BCM-JM pin 4 (OEM wire, keep if BCM retained)
```

---

## Quick Lookup — Haltech AVI Assignments

| AVI | Function | Physical Connector/Pin | Wire | Calibration |
|-----|----------|----------------------|------|-------------|
| AVI 1 | Fuel pressure | 26-pin pin 13 | GY/Y (shld) | 0–150 PSI linear |
| AVI 2 | Fuel temp | 34-pin pin 16 | O/B | PTC table |
| AVI 3 | Oil pressure | 34-pin pin 17 | O/R | 0–150 PSI linear |
| AVI 4 | Oil temp | 34-pin pin 2 | O/Y | PTC table |
| AVI 5 | Coolant pressure | 26-pin pin 20 | O/G | 0–100 PSI linear |
| AVI 6 | Coolant temp | 26-pin pin 12 | GY/O (shld) | PTC table |
| AVI 7 | IAT | 26-pin pin 3 | GY | Resistive, 1K pull-up |
| AVI 8 | Wideband O2 (LM2) | 26-pin pin 4 | V | 0–5V (7.35–22.39 AFR) |
| AVI 9 | Crankcase pressure | 34-pin pin 15 | Y | 0–5V ratiometric |
| AVI 10 | TPS | 34-pin pin 14 | W | 0–5V |

---

## Quick Lookup — Haltech DPO Assignments

| DPO | Function | Physical Pin | Wire | Notes |
|-----|----------|-------------|------|-------|
| DPO 1 | Tacho output → cluster | 34-pin pin 18 | V/B | User-definable pull-up → 12V, 3 ppr, active low |
| DPO 2 | Speed output (optional) | 34-pin pin 1 | V/BR | Fixed 5V pull-up — only needed if cluster VSS rerouted |
| DPO 3 | Available | 34-pin pin 23 | V/R | Fixed 12V pull-up |
| DPO 4 | Available | 26-pin pin 19 | V/O | Fixed 12V pull-up |
| DPO 5 | Fuel pump trigger | 34-pin pin 24 | B/Y | Fixed 12V pull-up → to PDM input |
| DPO 6 | ECR out | 34-pin pin 25 | B/R | Fixed 12V pull-up |

---

---

## PDM Physical Inputs

All driver controls use a physical switch panel — no CAN keypad in this build.

| PDM Pin | Function | Type | Notes |
|---------|----------|------|-------|
| **Conn B pin 23** (Ignition) | Ignition toggle switch | Latching, 12V when ON | Master PDM power state; source for `SafeIgnition`. Also spliced to Haltech 34-pin pin 13 (P, purple) — ECU IGN enable. Engine off without cutting battery. ✅ |
| **Ch01 — B26** | Fan override toggle | Latching, 12V when ON | Manual fan 98% override 🔲 |
| **Ch02 — B27** | Wiper Low toggle | Latching, 12V when ON | Wiper motor low speed 🔲 |
| **Ch03 — B28** | Wiper High toggle | Latching, 12V when ON | Wiper motor high speed (overrides low) 🔲 |
| **Ch04 — B29** | Coolsuit toggle | Latching, 12V when ON | Coolsuit pump on/off 🔲 |
| **Ch05 — B30** | Defogger toggle | Latching, 12V when ON | Rear window defogger 🔲 |
| **Ch09 — B21** | Start button | Momentary, active = GND | Crank engine — gated by ignition and RPM interlock 🔲 |
| **Ch11 — A26** | Brake light switch | Momentary, closed on press | Always active, independent of ignition 🔲 |

**CAN2 bus unused** — available for future CAN keypad or other device. Ch06–Ch08, Ch10, Ch12 available for future inputs.

---

## PDM Power Outputs

| Output | PDM Pins | Name | Trigger | Load Notes |
|--------|----------|------|---------|------------|
| HP1 | A1 + A13 | Starter | `STARTER_SAFE` = Ch09 AND IGN AND NOT RPM | Inductive; HP1 has internal series diode |
| HP2 | A12 + A23 | Fan | ECT 4-band PWM 77–92°C + Ch01 override | 100Hz; freewheeling diode |
| HP3 | A24 + A25 | Fuel Pump | 3s prime OR RPM > 50 | Inductive; freewheeling diode |
| MP1 | A2 | Injector Power | `SafeIgnition` | → Injector rail + Haltech 34-pin pin 26 (R/L) |
| MP2 | A3 | Coil Power | `SafeIgnition` | → Pin D, all 6 Toyota 90919-A2005 COPs |
| MP3 | A4 | Wiper Low | Ch02 AND NOT Ch03 | Inductive (wiper motor) |
| MP4 | A5 | Brake Lights | Ch11 direct (brake switch) | — |
| MP5 | A6 | Tail Lights | `SafeIgnition` (always on when car is on) | — |
| MP6 | A7 | Wiper High | Ch03 (overrides low speed) | Inductive (wiper motor) |
| MP7 | A8 | Coolsuit | Ch04 AND SafeIgnition | Inductive |
| MP8 | A9 | Defogger | Ch05 AND SafeIgnition | Resistive heating element |
| LP1 | A14 | ECU Power | `SafeIgnition` | → Haltech 26-pin pin 11 (R/W, 13.8V) |
| LP2 | A15 | Dash | `SafeIgnition` | AIM 10" dash |
| LP3 | A16 | SmartyCam | `SafeIgnition` | — |
| LP4 | A17 | GPS | `SafeIgnition` | — |
| LP5 | A18 | Wideband | `SafeIgnition` | Innovate LM2 power |
| LP6 | A19 | Cluster | `SafeIgnition` | OEM instrument cluster |
| LP7 | A20 | Warning LED | `MULTI_WARNING` | Low oil P / high ECT / high oil T / low fuel P |
| LP8 | A21 | AltExciter | `SafeIgnition` | OEM alternator D+ field wire routed through LP8; kill switch drops field immediately; < 1A draw |

> **MP1/MP2 temporary usage (Phase 1 — stock ECU):** While running on the stock ECU, MP1 and MP2 are wired to the OE main relay socket pin 87 (pull the relay). This provides switched 12V to the stock ECU and its loads whenever SafeIgnition is active. When switching to Haltech, reroute MP1 → injector rail and MP2 → COP coil power bus. No Race Studio config change needed — trigger is `SafeIgnition` in both phases.
>
> Full configuration details: `builds/white-tiburon/guides/pdm-config.md`

---

*Last updated: 2026-03-13*
*Sources: Haltech Elite 2500 pinout PDFs (verified), factory electrical manual BE section, OpenGK ECM pinouts, Lowdoller product specs, AIM PDM 32 pinout*
