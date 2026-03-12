---
source: SD.pdf
chapter: SD
section: SD-78 to SD-85
pages: 78-85
title: MFI Control System (2.7L V6)
---

# MFI Control System (2.7L V6)

**SD-78 -- MFI Control System (2.7L) (3) -- TPS, CMP, CKP, Canister Purge, MAF, ISC**
**SD-79 -- MFI Control System (2.7L) (4) -- Oxygen Sensors Bank 1 (front)**
**SD-80 -- MFI Control System (2.7L) (5) -- Oxygen Sensors Bank 2 (rear)**
**SD-81 -- MFI Control System (2.7L) (6) -- Ignition, MIL, Fuel Pump, Cluster**
**SD-82 -- MFI Control System (2.7L) (7) -- ABS, Multi-Gauge, VSS, ECT, IAT, Knock, P/S**
**SD-83 -- Component Location Index (1)**
**SD-84 -- Component Location Index (2) / Circuit Description**
**SD-85 -- Memo (blank)**

> **Note:** Pages SD-73 through SD-77 (MFI sheets 1-2) cover power distribution, injectors, and additional ECM connections. They are NOT included in this extraction (pages 78-85 only).

---

## SD-78 -- Sheet 3: TPS, CMP, CKP, Canister Purge, MAF, ISC

### Component Table

| Component | Connector | Pin | Wire Color | Wire Size |
|-----------|-----------|-----|------------|-----------|
| Sub fuse box | -- | -- | -- | -- |
| Joint connector | C142 | -- | -- | 0.50 |
| Throttle position sensor | C112 | pin 2 (signal) | -- | 0.5G/W |
| Throttle position sensor | C112 | pin 1 (ground) | -- | 0.5B |
| Canister purge valve | C121 | pin 2 (control) | -- | 0.5B |
| Canister purge valve | C131 | pin 1 (power) | -- | 0.50 |
| Mass air flow sensor | C125 | pin 3 (signal) | -- | 0.50 |
| Mass air flow sensor | C135 | -- | -- | -- |
| Camshaft position sensor | C114 | pin 1 (power) | O | 0.5O |
| Camshaft position sensor | C114 | pin 2 (signal) | -- | 0.5B |
| Camshaft position sensor | C114 | pin 3 (ground) | -- | 0.5G/B |
| Crankshaft position sensor | C113 | pin 1 (power) | O | 0.5O |
| Crankshaft position sensor | C113 | pin 2 (signal) | Y | 0.5Y |
| Crankshaft position sensor | C113 | pin 3 (ground) | -- | 0.5B |
| Idle speed control actuator | C126 | pin 2 (signal) | -- | 0.5B |
| Idle speed control actuator | C126 | pin 1 (power) | -- | -- |
| EC191 | -- | -- | -- | 0.85 |

### ECM Pin Connections (SD-78 Bottom Row)

| ECM Connector | ECM Pin | Signal Name | Wire Color | Wire Size |
|---------------|---------|-------------|------------|-----------|
| C133-3 | 15 | TPS signal | -- | 0.5B |
| C133-3 | -- | TPS supply | -- | 0.5G/W |
| C133-4 | 2 | CMP signal | -- | 0.5B |
| -- | -- | CMP sensor ground | -- | 0.5B |
| -- | -- | CKP signal | Y | 0.5Y |
| -- | -- | CKP signal ground | -- | 0.5B |
| C133-3 | -- | Canister purge control | -- | 0.5B |
| C133-3 | 5 | MAF signal | -- | 0.50 |
| C133-3 | -- | ISC control | -- | 0.5B |
| C133-3 | -- | ISC control | -- | B/W |

### ECM Bottom Pin Row (Left to Right, SD-78)

| Pin Position | ECM Connector | Signal | Wire Color | Wire Size |
|--------------|---------------|--------|------------|-----------|
| leftmost | C133-3 | TPS | 0.5B | 0.5B |
| -- | -- | supply | 0.5G/W | 0.5G/W |
| -- | C133-4 | CMP signal | 0.5B | 0.5B |
| -- | -- | sensor control/ground | 0.5G/B | 0.5G/B |
| -- | -- | CKP signal | 0.5Y | 0.5Y |
| -- | -- | CKP signal ground | 0.5B | 0.5B |
| -- | -- | Canister purge | 0.5L/W | 0.5L/W |
| -- | -- | MAF signal | 0.5B | 0.5B |
| rightmost | C133-3 | ISC | B/W | B/W |

---

## SD-79 -- Sheet 4: Oxygen Sensors (Bank 1 -- Front Sensors)

### Component Table

| Component | Connector | Pin | Wire Color | Wire Size |
|-----------|-----------|-----|------------|-----------|
| Oxygen sensor (B1/S1) | C116 | pin 1 (heater +) | -- | 0.60 |
| Oxygen sensor (B1/S1) | C116 | pin 2 (signal) | -- | 0.5R |
| Oxygen sensor (B1/S1) | C116 | (heater -) | -- | 0.5L |
| Oxygen sensor (Bank 1, Sensor 1) | C145 | pin 1 (heater +) | -- | 0.80 |
| Oxygen sensor (Bank 1, Sensor 1) | C145 | pin 2 (signal) | -- | 0.5R |
| Oxygen sensor (Bank 1, Sensor 1) | C145 | (heater -) | -- | 0.8W |
| Oxygen sensor (Bank 1, Rear/Sensor 1) | C146 | pin 1 (heater +) | -- | 0.60 |
| Oxygen sensor (Bank 1, Rear/Sensor 1) | C146 | pin 2 (signal) | -- | 0.5R |
| Oxygen sensor (Bank 1, Rear/Sensor 1) | C146 | (heater -) | -- | 0.5L/W |
| Joint connector | C142 | -- | -- | -- |

### Fuse/Power Feed

```
fuse/E(160) → [0.60] → EC(60) → [0.80] → Joint connector C142
  → branches to O2 sensor heater circuits
```

### ECM Pin Connections (SD-79 Bottom Row)

| ECM Connector | Signal | Wire Color | Wire Size |
|---------------|--------|------------|-----------|
| C133-2 | O2 sensor signal (B1/S1) | -- | 0.5R |
| C133-2 | O2 sensor ground | -- | 0.5L |
| C133-2 | O2 sensor heating (B1/S1) | -- | 0.8W |
| C133-2 | O2 sensor signal (B1/rear) | -- | 0.5R |
| C133-2 | O2 sensor ground | -- | 0.5L |
| C133-2 | O2 sensor heating | -- | 0.5P |

---

## SD-80 -- Sheet 5: Oxygen Sensors (Bank 2 -- Rear Sensors)

### Component Table

| Component | Connector | Pin | Wire Color | Wire Size |
|-----------|-----------|-----|------------|-----------|
| Oxygen sensor (2) | C112 | pin 2 (signal) | -- | 0.5R |
| Oxygen sensor (2) | C112 | pin 1 (heater) | -- | 0.60 |
| Oxygen sensor (Heater 2) | C147 | pin 2 (signal) | -- | 0.5R |
| Oxygen sensor (Heater 2) | C147 | pin 1 (heater +) | -- | 0.80 |
| Oxygen sensor (Bank 2, Sensor 2) | C148 | pin 2 (signal) | -- | 0.5R |
| Oxygen sensor (Bank 2, Sensor 2) | C148 | pin 1 (heater +) | -- | 0.60 |
| Joint connector | C142 | -- | -- | -- |

### Fuse/Power Feed

```
fuse/E(160) → [0.60] → EC(60) → [0.50] → Joint connector C142
  → branches to O2 sensor heater circuits (Bank 2)
```

### ECM Pin Connections (SD-80 Bottom Row)

| ECM Connector | Signal | Wire Color | Wire Size |
|---------------|--------|------------|-----------|
| C133-2 | O2 sensor signal (B2/S1) | -- | 0.5R |
| C133-2 | O2 sensor ground (B2/S1) | -- | 0.5L/W |
| C133-2 | O2 sensor heating (B2/S1) | -- | 0.5W/B |
| C133-2 | O2 sensor signal (B2/S2) | -- | 0.5P |
| C133-4 | O2 sensor ground (B2/S2) | -- | 0.5R |
| C133-4 | O2 sensor heating (B2/S2) | -- | 0.5L |
| -- | O2 sensor signal | -- | 0.5S |

---

## SD-81 -- Sheet 6: Ignition, MIL, Fuel Pump, Instrument Cluster

### Power Supply

| Source | Fuse | Rating | Feed | Wire Color | Wire Size |
|--------|------|--------|------|------------|-----------|
| HOT IN ON OR START | Fuse 17 | -- | See Passenger Compartment Fuse Details | -- | -- |
| -- | Fuse 18 | 10A | See Passenger Compartment Fuse Details | -- | -- |
| -- | Fuse (50A) | 50A | -- | -- | -- |

### Component Table

| Component | Connector | Pin | Wire Color | Wire Size |
|-----------|-----------|-----|------------|-----------|
| BCM-IM | pin 4 | -- | -- | 0.5R/O |
| BCM-KM | pin 13 | -- | R | 1.25R |
| MC168 | -- | -- | -- | -- |
| Instrument cluster (M10-2) | pin 3 | MIL (CHECK) | -- | 0.5L/B |
| Instrument cluster (M10-1) | pin 14 | -- | -- | 0.3L/B |
| Joint connector | C141 | pin 2 | -- | -- |
| Ignition coil (C118) | -- | To spark plugs | -- | -- |
| MC201 | -- | -- | -- | 0.5L/B |
| Fuel pump relay | -- | -- | -- | -- |

### Ignition Coils (C118 to C116)

| Coil | Connector | Signal | Wire Color | Wire Size |
|------|-----------|--------|------------|-----------|
| Coil 1 | C118 | IGN drive | -- | 0.3R |
| Coil 2 | -- | IGN drive | R/W | 1.25R/W |
| Coil 3 | -- | IGN drive | R | 1.25R |
| Coil 4 | -- | IGN drive | R | 1.25G/B |
| -- | C116 | -- | -- | -- |

### ECM Pin Connections (SD-81 Bottom Row)

| ECM Connector | ECM Pin | Signal Name | Wire Color | Wire Size |
|---------------|---------|-------------|------------|-----------|
| C133-4 | 21 | Check engine (MIL) | -- | 0.5L/B |
| C133-1 | 5 | OCV/ART start | P/R | 0.5P/R |
| -- | -- | Fuel pump relay control | Y/W | 1.25Y/W |
| C133-4 | 15 | Fuel sender signal/ground | R | 0.5R |
| -- | -- | Ignition coil 1 control | R | 1.25R |
| -- | -- | Ignition coil 2 signal | G/B | 1.25G/B |
| G24 | -- | Ground | -- | -- |
| G22 | -- | Ground | -- | 1.0B/B |
| C133-4 | -- | ECM power/ground | -- | -- |

### Ignition Coil Drive Circuit
```
ECM → [1.25R/W] → Ignition coil 2 → To spark plugs
ECM → [0.5R] → Fuel pump relay → [1.25R] → Ignition coil 1 → To spark plugs
ECM → [1.25G/B] → Ignition coil control
```

### MIL (Check Engine Light) Circuit
```
Fuse 17 → BCM-IM pin 4 → [0.5R/O] → MC168 → [0.25R]
  → Instrument cluster M10-2 pin 3 (MIL CHECK lamp)
  → [0.5L/B] → MC201 → [0.5L/B]
  → C141 joint connector → ECM C133-4 pin 21
```

### Fuel Pump Circuit
```
Fuse 18 (10A) → [R] → BCM-KM pin 13 → [1.25R]
  → MC168 → Fuel pump relay coil
  → ECM controls relay ground
Fuel pump relay contact → [R] → Fuel sender & fuel pump motor (M55)
```

### Ignition Coil Power Feed
```
Fuse (50A) → [R] → Joint connector C141 → [R, 0.3R]
  → Ignition coil assembly (C118) → To spark plugs ×6
```

---

## SD-82 -- Sheet 7: ABS, Multi-Gauge, VSS, ECT, IAT, Knock, Power Steering

### Component Table

| Component | Connector | Pin | Wire Color | Wire Size |
|-----------|-----------|-----|------------|-----------|
| ABS control module (E37) | -- | -- | -- | 0.5S/B |
| ABS control module | -- | -- | -- | 0.85/B |
| Multi-gauge unit (M42) | -- | -- | -- | 0.5W/B |
| Multi-gauge unit | -- | -- | -- | 0.50 |
| Instrument cluster (M10-1) | -- | -- | -- | 0.5W |
| MC109 | -- | -- | -- | 0.30 |
| MC191 | -- | -- | -- | 0.50 |
| MC168 | -- | -- | -- | 0.50 |
| Right front wheel sensor (E39) | -- | (EOBD, without ABS) | -- | 0.5L |
| EC/ECS connector | EC105 | -- | -- | -- |
| Engine coolant temp sensor & sender | C111 | pin 1 (signal) | -- | 0.5B |
| Engine coolant temp sensor & sender | C111 | pin 2 (ground) | -- | -- |
| Intake air temperature sensor | C127 | pin 1 (signal) | -- | 0.5B |
| Intake air temperature sensor | C127 | pin 2 (ground) | -- | -- |
| Knock sensor #1 | C123-1 | -- | -- | 0.5B |
| Knock sensor #2 | C123-2 | -- | -- | 0.5B |
| Power steering switch | C144 | -- | -- | -- |

### ECM Pin Connections (SD-82)

The bottom row shows the ECM connector pins with the shaded junction area representing the ECM internal connections.

| ECM Connector | ECM Pin | Signal Name | Wire Color | Wire Size |
|---------------|---------|-------------|------------|-----------|
| C133-4 | 20 | Vehicle speed (from ABS/VSS) | -- | 0.5S/B |
| -- | -- | HFM signal (from multi-gauge) | -- | 0.3G |
| -- | -- | RPM/speed signal | -- | 0.5W |
| -- | -- | A/C relay | -- | -- |
| C136-2 | -- | EOBD | -- | 0.5B |
| C133-2 | 17 | A/C signal | -- | 0.5B |
| -- | -- | Exhaust control | -- | -- |
| -- | -- | Knock sensor 1 signal | -- | 0.5B |
| C133-4 | -- | Vehicle speed signal | -- | 0.5B/B |
| -- | -- | ECT signal | -- | 0.5B |
| -- | -- | ECT ground | -- | 0.5S/W |
| -- | -- | IAT signal | -- | 0.5B |
| -- | -- | IAT ground | -- | 0.5B |
| -- | -- | Knock sensor 2 signal | -- | 0.5B |
| C133-4 | -- | Knock sensor ground | -- | 0.5B |
| C123-1 | -- | Knock sensor #1 | -- | 0.5B |
| C123-2 | -- | Knock sensor #2 | -- | 0.5B |

### ABS / Vehicle Speed Circuit
```
ABS control module (E37) → [0.5S/B] → EC/KCS → [0.30] → MC109
  → [0.50] → MC191 → [0.50] → MC168 → [0.50]
  → ECM C133-4 pin 20 (vehicle speed)
```

### Right Front Wheel Speed Sensor (EOBD, without ABS)
```
Right front wheel sensor (E39) → [0.5L] → EC105
  → [0.5L] → ECM C133-4
```

### ECT Sensor Circuit (Separate from Cooling System ECT)
```
Engine coolant temp sensor (C111 pin 1) → [0.5B] → ECM (ECT signal)
Engine coolant temp sensor (C111 pin 2) → [0.5S/W] → ECM (sensor ground)
```

### Intake Air Temperature Sensor Circuit
```
IAT sensor (C127 pin 1) → [0.5B] → ECM (IAT signal)
IAT sensor (C127 pin 2) → [0.5B] → ECM (sensor ground)
```

### Knock Sensor Circuits
```
Knock sensor #1 (C123-1) → [0.5B] → ECM knock signal 1
Knock sensor #2 (C123-2) → [0.5B] → ECM knock signal 2
```

### Power Steering Switch
```
Power steering switch (C144) → [0.5B] → GND (G22)
```

---

## Ground Points (All MFI V6 Sheets)

| Ground ID | Location | Components | Reference |
|-----------|----------|------------|-----------|
| G22 | Engine block | ECM grounds, power steering switch, ignition coil ground | SD-81, SD-82 |
| G24 | Engine block | ECM ground | SD-81 |

---

## Master ECM Pinout Table (2.7L V6, from SD-78 through SD-82)

### Connector C133-1

| Pin | Signal Name | Wire Color | Wire Size | Connected To |
|-----|-------------|------------|-----------|-------------|
| 5 | OCV/ART start signal | P/R | 0.5P/R | Fuel pump relay circuit |

### Connector C133-2

| Pin | Signal Name | Wire Color | Wire Size | Connected To |
|-----|-------------|------------|-----------|-------------|
| 17 | A/C signal | -- | 0.5B | A/C relay |
| -- | O2 sensor signal (B1/S1) | -- | 0.5R | Oxygen sensor C116/C145 |
| -- | O2 sensor ground (B1) | -- | 0.5L | Oxygen sensor C116/C145 |
| -- | O2 sensor heating (B1) | -- | 0.8W | Oxygen sensor C145 heater |
| -- | O2 sensor signal (B1/rear) | -- | 0.5R | Oxygen sensor C146 |
| -- | O2 sensor ground (B1/rear) | -- | 0.5L | Oxygen sensor C146 |
| -- | O2 sensor heating (B1/rear) | -- | 0.5P | Oxygen sensor C146 heater |
| -- | O2 sensor signal (B2/S1) | -- | 0.5R | Oxygen sensor C112/C147 |
| -- | O2 sensor ground (B2/S1) | -- | 0.5L/W | Oxygen sensor C112/C147 |

### Connector C133-3

| Pin | Signal Name | Wire Color | Wire Size | Connected To |
|-----|-------------|------------|-----------|-------------|
| 5 | MAF signal | -- | 0.50 | Mass air flow sensor C125 |
| 15 | TPS signal | -- | 0.5B | Throttle position sensor C112 |
| -- | TPS sensor supply | -- | 0.5G/W | Throttle position sensor C112 |
| -- | CKP signal | Y | 0.5Y | Crankshaft position sensor C113 |
| -- | CKP ground | -- | 0.5B | Crankshaft position sensor C113 |
| -- | Canister purge control | -- | 0.5B | Canister purge valve C121/C131 |
| -- | ISC control | -- | 0.5B | Idle speed control actuator C126 |
| -- | ISC control | B/W | B/W | Idle speed control actuator C126 |

### Connector C133-4

| Pin | Signal Name | Wire Color | Wire Size | Connected To |
|-----|-------------|------------|-----------|-------------|
| 2 | CMP signal | -- | 0.5B | Camshaft position sensor C114 |
| 15 | Fuel sender signal | R | 0.5R | Fuel pump circuit |
| 20 | Vehicle speed | -- | 0.5S/B | ABS control module / VSS |
| 21 | MIL (check engine) | -- | 0.5L/B | Instrument cluster M10-2 pin 3 |
| -- | ECT sensor signal | -- | 0.5B | Coolant temp sensor C111 |
| -- | ECT sensor ground | -- | 0.5S/W | Coolant temp sensor C111 |
| -- | IAT signal | -- | 0.5B | Intake air temp sensor C127 |
| -- | IAT ground | -- | 0.5B | Intake air temp sensor C127 |
| -- | O2 sensor ground (B2/S2) | -- | 0.5R | Oxygen sensor C148 |
| -- | O2 sensor heating (B2/S2) | -- | 0.5L | Oxygen sensor C148 heater |
| -- | Knock sensor #1 | -- | 0.5B | Knock sensor C123-1 |
| -- | Knock sensor #2 | -- | 0.5B | Knock sensor C123-2 |

### Connector C136-2

| Pin | Signal Name | Wire Color | Wire Size | Connected To |
|-----|-------------|------------|-----------|-------------|
| -- | EOBD | -- | 0.5B | Right front wheel sensor E39 |

---

## Sensor Connector Pinouts

> **Note:** TPS (C112) and MAF (C125/C135) connector tables below are incomplete — they only show ECM-connected pins. Both sensors have additional pins (power supply via C142 joint connector from SNSR FUSE 10A) that were not captured in the original extraction. CMP (C114) and CKP (C113) have been corrected to show all 3 pins. See SD-78 schematic for full wiring.

### Throttle Position Sensor (C112)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 1 | Sensor ground | -- | 0.5B | C133-3 |
| 2 | TPS signal output | -- | 0.5G/W | C133-3 pin 15 |

### Camshaft Position Sensor (C114)

| Pin | Function | Wire Color | Wire Size | Connects To |
|-----|----------|------------|-----------|-------------|
| 1 | Power supply (battery voltage) | O | 0.5O | C142 joint connector (SNSR FUSE 10A) |
| 2 | CMP signal | -- | 0.5B | ECM C133-4 pin 2 |
| 3 | Sensor ground | -- | 0.5G/B | ECM C133-4 |

### Crankshaft Position Sensor (C113)

| Pin | Function | Wire Color | Wire Size | Connects To |
|-----|----------|------------|-----------|-------------|
| 1 | Power supply (battery voltage) | O | 0.5O | C142 joint connector (SNSR FUSE 10A) |
| 2 | CKP signal | Y | 0.5Y | ECM C133-3 pin 8 |
| 3 | Sensor ground | -- | 0.5B | ECM C133-3 |

### Mass Air Flow Sensor (C125/C135)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 3 | MAF signal | -- | 0.50 | C133-3 pin 5 |

### Idle Speed Control Actuator (C126)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 1 | Power supply | -- | -- | via fuse |
| 2 | ISC control signal | -- | 0.5B | C133-3 |

### Canister Purge Valve (C121/C131)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 1 | Power supply | -- | 0.50 | via fuse |
| 2 | Purge control | -- | 0.5B | C133-3 |

### Engine Coolant Temperature Sensor (C111)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 1 | ECT signal | -- | 0.5B | C133-4 |
| 2 | Sensor ground | -- | 0.5S/W | C133-4 |

### Intake Air Temperature Sensor (C127)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 1 | IAT signal | -- | 0.5B | C133-4 |
| 2 | Sensor ground | -- | 0.5B | C133-4 |

### Knock Sensor #1 (C123-1)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 1 | Knock signal | -- | 0.5B | C133-4 |

### Knock Sensor #2 (C123-2)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 1 | Knock signal | -- | 0.5B | C133-4 |

### Power Steering Switch (C144)

| Pin | Function | Wire Color | Wire Size | ECM Pin |
|-----|----------|------------|-----------|---------|
| 1 | P/S signal | -- | -- | ECM |
| 2 | Ground | -- | -- | G22 |

---

## Oxygen Sensor Summary (All 6 Sensors)

### Bank 1 (Front -- SD-79)

| Sensor | Connector | Signal Wire | Signal Size | Heater Wire | Heater Size | ECM Connector |
|--------|-----------|-------------|-------------|-------------|-------------|---------------|
| O2 Sensor (B1/S1) | C116 | 0.5R | 0.5R | 0.5L | 0.5L | C133-2 |
| O2 Sensor (B1/S1) pre-cat | C145 | 0.5R | 0.5R | 0.8W | 0.8W | C133-2 |
| O2 Sensor (B1/Rear) post-cat | C146 | 0.5R | 0.5R | 0.5L/W | 0.5P | C133-2 |

### Bank 2 (Rear -- SD-80)

| Sensor | Connector | Signal Wire | Signal Size | Heater Wire | Heater Size | ECM Connector |
|--------|-----------|-------------|-------------|-------------|-------------|---------------|
| O2 Sensor (B2/S1) | C112 | 0.5R | 0.5R | 0.60 | 0.60 | C133-2 |
| O2 Sensor (B2/S1) pre-cat | C147 | 0.5R | 0.5R | 0.80 | 0.5L/W | C133-2 |
| O2 Sensor (B2/S2) post-cat | C148 | 0.5R | 0.5R | 0.60 | 0.5L | C133-4 |

---

## Component Location Index (SD-83 / SD-84)

### Components

| Component | Description | Location Page |
|-----------|-------------|---------------|
| C111 | Engine coolant temperature sensor & sender | CL-22 |
| C112 | Throttle position sensor | CL-22 |
| C113 | Crankshaft position sensor | CL-22 |
| C114 | Camshaft position sensor | CL-22 |
| C116 | Oxygen sensor (Except EOBD) | CL-22 |
| C118 | Ignition coil | CL-23 |
| C121 | Canister purge valve | CL-23 |
| C122 | Rear Oxygen sensor (Except EOBD) | CL-23 |
| C123-1 | Knock sensor #1 | CL-23 |
| C123-2 | Knock sensor #2 | CL-23 |
| C124-1 | Injector #1 | CL-23 |
| C124-2 | Injector #2 | CL-23 |
| C124-3 | Injector #3 | CL-23 |
| C124-4 | Injector #4 | CL-23 |
| C124-5 | Injector #5 | CL-23 |
| C124-6 | Injector #6 | CL-23 |
| C125 | Mass air flow sensor | CL-23 |
| C126 | Idle speed control actuator | CL-24 |
| C127 | Intake air temperature sensor | CL-24 |
| C133-1 | ECM | CL-25 |
| C133-2 | ECM | CL-25 |
| C133-3 | ECM | CL-25 |
| C133-4 | ECM | CL-25 |
| C136-3 | TCM | CL-25 |
| C141 | Joint connector | CL-25 |
| C142 | Joint connector | CL-25 |
| C144 | Power steering switch | CL-25 |
| C145 | Oxygen sensor (B1/S1) | CL-25 |
| C146 | Oxygen sensor (B2/S1) | CL-26 |
| C147 | Oxygen sensor (B1/S2) | CL-26 |
| C148 | Oxygen sensor (B2/S2) | CL-26 |
| E37 | ABS control module | CL-12 |
| E39 | Right front wheel sensor | CL-12 |
| E42 | Engine control relay | CL-12 |
| E49 | Fuel pump relay | CL-12 |
| E56 | Joint connector | CL-12 |
| M06 | Multipurpose check connector | CL-2 |
| M07 | Data link connector | CL-2 |
| M10-1 | Instrument cluster | CL-2 |
| M10-2 | Instrument cluster | CL-2 |
| M34 | Joint connector | CL-2 |
| M42 | Multi gauge unit | CL-4 |
| M55 | Fuel sender & fuel pump motor | CL-5 |

### Connectors

| Connector | Location Page |
|-----------|---------------|
| BCM-IM | CL-8 |
| BCM-KM | CL-8 |
| EC101 | CL-14 |
| EC102 | CL-14 |
| EM01 | CL-14 |
| MC101 | CL-8 |
| MC102 | CL-8 |
| MC103 | CL-8 |
| MM01 | CL-9 |
| MM02 | CL-9 |

### Grounds

| Ground ID | Location Page |
|-----------|---------------|
| G22 | CL-34 |
| G24 | CL-34 |

---

## Notes

- The Multiport Fuel Injection (MFI) control system is an electronic fuel metering system with fuel injectors near the inlet port of each cylinder. The amount of fuel injection is determined by the ECM according to engine speed and intake air-flow quantity measured.
- The emission control system includes the oxygen sensors and catalytic converters.
- The MFI's three major functions are air-fuel mixture, idle speed, and ignition timing control. Refer to the shop manual, section FL for details.
- **V6 build note:** The 2.7L V6 uses FOUR ECM connectors (C133-1, C133-2, C133-3, C133-4) plus C136-3 (TCM). Six injectors (C124-1 through C124-6) are on pages not included in this extraction (SD-73 to SD-77).
- **O2 sensor count:** Six total -- 3 per bank (B1 on SD-79, B2 on SD-80). Pre-cat and post-cat sensors on each bank.
- **Ignition coils** (C118) are shown on SD-81 receiving power from a 50A fuse through C141 joint connector, with ECM controlling individual coil firing.
