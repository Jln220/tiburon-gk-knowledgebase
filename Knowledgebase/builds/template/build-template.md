# Build Template — [CAR NAME]
## [Year] Hyundai Tiburon GK | [Series / Class]

> **How to use:** Copy this folder to `builds/{your-build-name}/`, rename this file to `build-profile.md`, and fill in every section. Delete fields that don't apply. Blank fields are fine — fill progressively as you learn. Reference files in `common/` and `hardware/` rather than duplicating content.

---

## Car Identity

| Field | Value |
|-------|-------|
| **Year** | |
| **Color / Nickname** | |
| **Role** | (primary race car / test car / both) |
| **VIN** | |
| **Chassis code** | GK (Tiburon) |
| **Engine family** | G6BA (2.7L V6 Delta) |
| **Series** | (24 Hours of Lemons / ChumpCar / track day / etc.) |

---

## Engine

### Current Engine
| Field | Value |
|-------|-------|
| **Displacement** | 2.7L V6 |
| **State** | (stock / built — see `common/engine-builds.md`) |
| **Headers** | |
| **Exhaust** | |
| **Intake** | |
| **Known issues** | |

### Fuel System
| Component | Part / Status |
|-----------|--------------|
| Fuel pressure regulator | |
| Fuel lines | |
| Fuel injectors | |
| Fuel pump | |

---

## ECU / Engine Management

| Field | Value |
|-------|-------|
| **ECU type** | (Stock Siemens SIMK43 / Haltech Elite 2500 / other) |
| **Tune method** | (GKFlasher / NSP / other) |
| **Map file location** | |
| **Cam/crank confirmed** | ☐ |
| **Knock sensors confirmed** | ☐ |
| **COP or wasted spark** | (COP — Toyota 90919-A2005 / OEM wasted spark) |

### AVI Channel Assignments (Haltech — fill if applicable)

| AVI | Signal | Haltech Pin | Wire Color |
|-----|--------|-------------|------------|
| AVI 1 | | | |
| AVI 2 | | | |
| AVI 3 | | | |
| AVI 4 | | | |
| AVI 5 | | | |
| AVI 6 | | | |
| AVI 7 | | | |
| AVI 8 | | | |
| AVI 9 | | | |
| AVI 10 | | | |

### Digital/Pulse Inputs (Haltech)

| Input | Signal | Haltech Pin | Notes |
|-------|--------|-------------|-------|
| SPI 1 | | | |
| SPI 2 | | | |
| DPO 1 | | | |

### CAN Bus (ECU)

| Bus | Device | Speed | Pins |
|-----|--------|-------|------|
| CAN | | | |

---

## Power Distribution

| Field | Value |
|-------|-------|
| **PDM type** | (AIM PDM 32 / stock fuse box / other) |
| **Battery location** | |
| **Main fuse** | |

### Physical Switch Inputs (PDM or relay — fill if applicable)

| Switch | Connection | Type | Function |
|--------|-----------|------|----------|
| Ignition | | Latching toggle | Master power |
| Start (backup) | | Momentary | Physical start backup |
| | | | |

### CAN Keypad (fill if applicable)

| Key | Function | Mode | LED: Rest / Active |
|-----|----------|------|-------------------|
| 01 | | | |
| 02 | | | |
| 03 | | | |
| 04 | | | |
| 05 | | | |
| 06 | | | |
| 07 | | | |
| 08 | | | |
| 09 | | | |
| 10 | | | |
| 11 | | | |
| 12 | | | |

### Power Output Map

| Output | Name | PDM Pins | Load | Trigger |
|--------|------|----------|------|---------|
| HP1 | | | | |
| HP2 | | | | |
| HP3 | | | | |
| HP4 | | | | |
| MP1 | | | | |
| MP2 | | | | |
| MP3 | | | | |
| MP4 | | | | |
| MP5 | | | | |
| MP6 | | | | |
| MP7 | | | | |
| MP8 | | | | |
| LP1 | | | | |
| LP2 | | | | |
| LP3 | | | | |
| LP4 | | | | |
| LP5 | | | | |
| LP6 | | | | |
| LP7 | | | | |

### CAN Bus (PDM)

| Bus | PDM Pins | Device | Speed | Notes |
|-----|----------|--------|-------|-------|
| CAN0 | | | | |
| CAN1 | | | | |
| CAN2 | | | | |

---

## Sensors

### Pressure / Temperature (fill for each sensor installed)

| Location | Part # | Type | Interface | Notes |
|----------|--------|------|-----------|-------|
| Fuel | | | | |
| Oil | | | | |
| Coolant | | | | |
| Brake | | | | |
| Transmission | | | | |

### OEM Sensors Retained

| Sensor | Status | Notes |
|--------|--------|-------|
| Cam position | | |
| Crank position | | |
| Knock (×2) | | |
| TPS | | |
| MAF | | |
| MAP | | |
| Coolant temp | | |
| Intake air temp | | |
| O2 (front/rear) | | |
| VSS | | |

---

## Data & Telemetry

| Component | Status | Notes |
|-----------|--------|-------|
| AIM dash | | |
| SmartyCam | | |
| GPS module | | |
| AIM Podium (WiFi/4G) | | |
| PodiumConnect | | |
| Pit limiter | | |

---

## Transmission & Drivetrain

| Field | Value |
|-------|-------|
| **Transmission** | (6-speed Aisin AY6 / 5-speed / other) |
| **LSD** | (None / Quaife ATB / other) |
| **Shifter** | (Stock / aluminum short shifter) |
| **Shifter bushings** | |
| **Final drive ratio** | 4.050:1 (stock 6-speed) |

---

## Suspension & Steering

| Component | Spec / Part |
|-----------|------------|
| Front control arms | |
| Rear control arms | |
| Rear trailing arm bushings | |
| Strut bars (front / rear) | |
| Wheels | |
| Wheel spacers | |
| Tires | |
| Steering wheel | |

---

## Interior & Safety

| Component | Spec / Status |
|-----------|--------------|
| Seat | |
| Harness | |
| Cage | |
| Floor drop | ☐ Yes / ☐ No |
| Fire suppression | |
| Warning LED | |

---

## Maintenance Log

| Date | Work Performed | Notes |
|------|---------------|-------|
| | | |

---

## Known Issues

-

---

## Build Status

| System | Status |
|--------|--------|
| Engine installed | ☐ |
| ECU wiring complete | ☐ |
| ECU bench test (cam/crank) | ☐ |
| ECU bench test (knock) | ☐ |
| ECU bench test (CAN broadcast) | ☐ |
| PDM logic test | ☐ |
| Car started with new ECU | ☐ |
| All sensors installed | ☐ |
| Fuel system complete | ☐ |
| Data/telemetry verified | ☐ |
| Race-ready | ☐ |

---

## Notes

*Add any build-specific notes, workarounds, or future plans here.*

---

## Related Files

| File | Contents |
|------|----------|
| `builds/{car}/signal-routing.md` | End-to-end signal routing |
| `builds/{car}/weekend-tasks.md` | Phased build procedure |
| `hardware/aim-pdm/pdm-configuration-guide.md` | PDM logic setup |
| `builds/{car}/pdm/config-guide.md` | Race Studio 3 config guide (car-specific) |
| `hardware/haltech/main-connector-26-pin-elite2500.md` | Haltech 26-pin pinout |
| `hardware/haltech/main-connector-34-pin-elite2500.md` | Haltech 34-pin pinout |
| `hardware/sensors/lowdoller-sensors.md` | Lowdoller sensor specs |
| `common/chassis/gk-chassis-specs.md` | GK platform specs |
