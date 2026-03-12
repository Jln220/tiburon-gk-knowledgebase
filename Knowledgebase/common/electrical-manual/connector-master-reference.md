---
source: HL.pdf, CC.pdf, SD.pdf, CL.pdf, FLA (shop manual)
chapter: ETM Cross-Reference
engine: V6 (2.7L Delta G6BA)
vehicle: 2003 Hyundai Tiburon (GK)
last_updated: 2026-03-12
---

# Connector Master Reference (2.7L V6)

This file maps every V6 engine-management connector to ALL relevant manual sections. Use it as a navigation index and a validation checklist.

**How to use:** Find a connector code (like C113) or component name (like "Crankshaft Position Sensor") → read across to find the HL harness assignment, CC pin count, SD schematic page, CL physical location, FLA shop manual section, and knowledge graph node ID.

**Key principle:** The **connector code** (C113) is the ETM's internal key. The **component name** is the shop manual's key. The **graph node ID** (`comp-ckp-sensor`) is the machine-readable bridge. This table connects all three.

---

## Control Harness (4) — 2.7L V6 (HL-15)

### Engine Management Sensors

| Code | Component | Pins | CC Page | Connector P/N | HL Page | Harness | SD Page | CL Page | FLA Page | DTC Section | Graph Node |
|------|-----------|------|---------|---------------|---------|---------|---------|---------|----------|-------------|------------|
| C111 | Engine coolant temp sensor & sender | 2 | CC-17 | CR02F071 | HL-15 | Control (4) | SD-81 | CL-22 | FLA-35 | FLA-73+ (P0115/P0117/P0118) | `comp-ect-sensor` |
| C112 | Throttle position sensor | 3 | CC-17 | CR03F028 | HL-15 | Control (4) | SD-78 | CL-22 | FLA-46 | FLA-73+ (P0120/P0122/P0123) | `comp-tps` |
| C113 | Crankshaft position sensor | 3 | CC-17 | CR03F038 | HL-15 | Control (4) | SD-78 | CL-22 | FLA-57 | FLA-73+ (P0335/P0336) | `comp-ckp-sensor` |
| C114 | Camshaft position sensor | 3 | CC-17 | CR03F029 | HL-15 | Control (4) | SD-78 | CL-22 | FLA-55 | FLA-73 (P0340/P0341) | `comp-cmp-sensor` |
| C115 | Oil pressure switch | 1 | CC-17 | CR01F020 | HL-15 | Control (4) | SD-82 | — | — | — | — |
| C116 | Front oxygen sensor (non-EOBD) | 4 | CC-18 | CR04F027 | HL-15 | Control (4) | SD-79 | CL-22 | FLA-52 | FLA-73+ (P0130–P0141) | `comp-o2-sensor` |
| C122 | Rear oxygen sensor (non-EOBD) | 4 | CC-18 | CR04M004 | HL-15 | Control (4) | SD-80 | CL-23 | FLA-52 | FLA-73+ (P0136–P0161) | `comp-o2-sensor` |
| C123-1 | Knock sensor #1 | 1–2 | CC-18 | CR02F030 | HL-15 | Control (4) | SD-82 | CL-23 | FLA-65 | FLA-73+ (P0325) | `comp-knock-sensor` |
| C123-2 | Knock sensor #2 | 1–2 | CC-18 | CR03F028 | HL-15 | Control (4) | SD-82 | CL-23 | FLA-65 | FLA-73+ (P0330) | `comp-knock-sensor` |
| C125 | Mass air flow sensor | 3 | CC-18 | CR02F048 | HL-15 | Control (4) | SD-82 | CL-23 | FLA-40 | FLA-73+ (P0100–P0103) | `comp-maf-sensor` |
| C127 | Intake air temperature sensor | 3 | CC-18 | CR02F041 | HL-15 | Control (4) | SD-82 | CL-24 | FLA-43 | FLA-73+ (P0110/P0112/P0113) | `comp-iat-sensor` |
| C109 | Vehicle speed sensor | 3 | CC-17 | CR03F028 | HL-15 | Control (4) | SD-82 | — | — | — | `comp-vss` |
| C144 | Power steering switch | 1 | CC-19 | CR01F008 | HL-15 | Control (4) | SD-82 | CL-25 | — | — | — |

### EOBD Oxygen Sensors (Bank-Specific)

| Code | Component | Pins | CC Page | Connector P/N | HL Page | Harness | SD Page | CL Page | FLA Page | DTC Section | Graph Node |
|------|-----------|------|---------|---------------|---------|---------|---------|---------|----------|-------------|------------|
| C145 | Oxygen sensor (B1/S1) | 4 | CC-17 | — | HL-15 | Control (4) | SD-79 | CL-25 | FLA-52 | FLA-73+ (P0130–P0135) | `comp-o2-sensor` |
| C146 | Oxygen sensor (B2/S1) | 4 | CC-17 | — | HL-15 | Control (4) | SD-80 | CL-26 | FLA-52 | FLA-73+ (P0150–P0155) | `comp-o2-sensor` |
| C147 | Oxygen sensor (B1/S2) | 4 | CC-17 | — | HL-15 | Control (4) | SD-79 | CL-26 | FLA-52 | FLA-73+ (P0136–P0141) | `comp-o2-sensor` |
| C148 | Oxygen sensor (B2/S2) | 4 | CC-17 | — | HL-15 | Control (4) | SD-80 | CL-26 | FLA-52 | FLA-73+ (P0156–P0161) | `comp-o2-sensor` |

### Engine Management Actuators

| Code | Component | Pins | CC Page | Connector P/N | HL Page | Harness | SD Page | CL Page | FLA Page | DTC Section | Graph Node |
|------|-----------|------|---------|---------------|---------|---------|---------|---------|----------|-------------|------------|
| C118 | Ignition coil | — | CC-17 | — | HL-15 | Control (4) | — | CL-23 | EE-14 | — | `comp-ignition-coil` |
| C121 | Canister purge valve | 2 | CC-17 | — | HL-15 | Control (4) | SD-81 | CL-23 | FLA-62 | FLA-73+ (P0443) | — |
| C124-1 | Injector #1 | 2 | CC-17 | — | HL-15 | Injector | SD-81 | CL-23 | FLA-59 | FLA-73+ (P0201) | `comp-injector` |
| C124-2 | Injector #2 | 2 | CC-17 | — | HL-15 | Control (4) | SD-81 | CL-23 | FLA-59 | FLA-73+ (P0202) | `comp-injector` |
| C124-3 | Injector #3 | 2 | CC-17 | — | HL-15 | Injector | SD-81 | CL-23 | FLA-59 | FLA-73+ (P0203) | `comp-injector` |
| C124-4 | Injector #4 | 2 | CC-17 | — | HL-15 | Control (4) | SD-81 | CL-23 | FLA-59 | FLA-73+ (P0204) | `comp-injector` |
| C124-5 | Injector #5 | 2 | CC-17 | — | HL-15 | Injector | SD-81 | CL-23 | FLA-59 | FLA-73+ (P0205) | `comp-injector` |
| C124-6 | Injector #6 | 2 | CC-17 | — | HL-15 | Control (4) | SD-81 | CL-23 | FLA-59 | FLA-73+ (P0206) | `comp-injector` |
| C126 | Idle speed control actuator | 3 | CC-18 | CR02F028 | HL-15 | Control (4) | SD-81 | CL-24 | FLA-49 | FLA-73+ (P0505) | — |
| C128 | A/C compressor | 1 | CC-17 | — | HL-15 | Control (4) | SD-82 | — | — | — | — |

### ECM / TCM Connectors

| Code | Component | Pins | CC Page | Connector P/N | HL Page | Harness | SD Page | CL Page | FLA Page | Graph Node |
|------|-----------|------|---------|---------------|---------|---------|---------|---------|----------|------------|
| C133-1 | ECM connector 1 | — | CC-17 | — | HL-15 | Control (4) | SD-78 | CL-25 | — | — |
| C133-2 | ECM connector 2 | — | CC-17 | — | HL-15 | Control (4) | SD-79/80 | CL-25 | — | — |
| C133-3 | ECM connector 3 | — | CC-17 | — | HL-15 | Control (4) | SD-78/82 | CL-25 | — | — |
| C133-4 | ECM connector 4 | — | CC-17 | — | HL-15 | Control (4) | SD-78/81 | CL-25 | — | — |
| C133-5 | ECM connector 5 | — | CC-17 | — | HL-15 | Control (4) | — | CL-25 | — | — |
| C136-1 | TCM connector 1 | — | CC-17 | — | HL-15 | Control (4) | — | — | — | — |
| C136-2 | TCM connector 2 | — | CC-17 | — | HL-15 | Control (4) | — | — | — | — |
| C136-3 | TCM connector 3 | — | CC-17 | — | HL-15 | Control (4) | — | CL-25 | — | — |

### Joint Connectors & Distribution

| Code | Component | Pins | CC Page | HL Page | Harness | SD Page | CL Page | Notes |
|------|-----------|------|---------|---------|---------|---------|---------|-------|
| C141 | Joint connector | — | CC-17 | HL-15 | Control (4) | — | CL-25 | — |
| C142 | Joint connector | — | CC-17 | HL-15 | Control (4) | SD-78 | CL-25 | SNSR FUSE 10A distribution — powers CKP, CMP, TPS, MAF |

### Switches & Other

| Code | Component | Pins | HL Page | Harness | Notes |
|------|-----------|------|---------|---------|-------|
| C101 | Transaxle range switch | — | HL-15 | Control (4) | A/T only |
| C102-1 | A/T pulse generator #1 | — | HL-15 | Control (4) | A/T only |
| C102-2 | A/T pulse generator #2 | — | HL-15 | Control (4) | A/T only |
| C104 | ATM solenoid valve | — | HL-15 | Control (4) | A/T only |
| C106 | Back-up lamp switch (6MT) | — | HL-15 | Control (4) | M/T only |
| C107 | Front wiper motor | — | HL-15 | Control (4) | — |
| C117 | Starter clutch pedal position switch | — | HL-15 | Control (4) | M/T only |
| C120 | Brake fluid level sensor | — | HL-15 | Control (4) | — |
| C129 | Hood switch | — | HL-15 | Control (4) | — |
| C131 | Stop lamp switch (W/O cruise) | — | HL-15 | Control (4) | — |
| C132 | Stop lamp switch (With cruise) | — | HL-15 | Control (4) | — |
| C135 | Cruise clutch pedal position switch | — | HL-15 | Control (4) | — |
| C137 | A/T control relay | — | HL-15 | Control (4) | — |
| C138 | Cruise control module | — | HL-15 | Control (4) | — |
| C139 | Sport mode switch | — | HL-15 | Control (4) | — |

### Ground Points (V6 Control Harness)

| Code | Function | CL Page |
|------|----------|---------|
| G21 | Ground (TCM) | — |
| G22 | Ground (ECM) | CL-34 |
| G23 | Ground (CONTROL) | — |
| G24 | Ground (ENGINE) | CL-34 |

---

## Engine Harness (HL-7) — Relays & Components

| Code | Component | HL Page | Harness | SD Page | CL Page | Notes |
|------|-----------|---------|---------|---------|---------|-------|
| E11 | Radiator fan motor | HL-7 | Engine | — | — | — |
| E21 | Condenser fan motor | HL-7 | Engine | — | — | — |
| E26 | Triple switch (2.7L) | HL-7 | Engine | — | — | Coolant temp switch (fan/gauge) |
| E37 | ABS control module | HL-7 | Engine | — | CL-12 | — |
| E41 | Start relay | HL-7 | Engine | — | — | — |
| E42 | Engine control relay | HL-7 | Engine | SD-81 | CL-12 | Powers injectors, ISC, purge |
| E43 | Condenser fan relay #2 | HL-7 | Engine | — | — | — |
| E44 | Radiator fan relay | HL-7 | Engine | — | — | — |
| E49 | Fuel pump relay | HL-7 | Engine | SD-81 | CL-12 | — |
| E50 | A/C relay | HL-7 | Engine | SD-82 | — | — |
| E51 | Head lamp relay (High) | HL-7 | Engine | — | — | — |
| E52 | Condenser fan relay #1 | HL-7 | Engine | — | — | — |
| E56 | Joint connector | HL-7 | Engine | — | CL-12 | — |

---

## Injector Harness (2.7L) (HL-15)

| Code | Component | HL Page | Notes |
|------|-----------|---------|-------|
| C124-1 | Injector #1 | HL-15 | Odd cylinders on injector sub-harness |
| C124-3 | Injector #3 | HL-15 | — |
| C124-5 | Injector #5 | HL-15 | — |
| CC101 | Connection with CONTROL harness | HL-15 | Sub-harness feed connector |

---

## Inter-Harness Connections (V6)

| Code | Connection | HL Page |
|------|------------|---------|
| EC101 | Engine harness ↔ Control harness (2.7L) | HL-7/15 |
| EC102 | Engine harness ↔ Control harness (2.7L) | HL-7/15 |
| MC101 | Main harness ↔ Control harness (2.7L) | HL-3/15 |
| MC102 | Main harness ↔ Control harness (2.7L) | HL-3/15 |
| MC103 | Main harness ↔ Control harness (2.7L) | HL-3/15 |
| CC101 | Control harness ↔ Injector harness (2.7L) | HL-15 |

---

## Pin Count Validation Checklist

Use this table to cross-check extracted sensor pinout tables in `schematics/mfi-control-v6.md` against the CC pin count. If the extracted table has fewer pins, the extraction is incomplete.

**Sources:** CC-17/CC-18 extraction from CC.pdf, user-confirmed values where noted.

| Connector | Component | CC Pins | CC P/N | Extracted Pins | Status | Notes |
|-----------|-----------|---------|--------|----------------|--------|-------|
| C111 | ECT sensor & sender | 2 | CR02F071 | 2 | ✅ OK | Signal + ground |
| C112 | Throttle position sensor | 3 | CR03F028 | 2 | ⚠️ INCOMPLETE | Missing: power supply pin (0.5O via C142). Fix from FLA-46. |
| C113 | Crankshaft position sensor | 3 | CR03F038 | 3 | ✅ OK | User confirmed. Pin 1=Power, Pin 2=Signal, Pin 3=GND |
| C114 | Camshaft position sensor | 3 | CR03F029 | 3 | ✅ OK | User confirmed 3-pin CR03F029. CC extraction misread as 2-pin CR02F028 — extraction error. |
| C115 | Oil pressure switch | 1 | CR01F020 | — | — | Single-wire switch, not in sensor tables |
| C116 | Front oxygen sensor | 4 | CR04F027 | — | — | In O2 summary table (separate section) |
| C122 | Rear oxygen sensor | 4 | CR04M004 | — | — | CC extraction read 2 pins but P/N prefix CR04 = 4 pins. Heated O2 = 4 wire. |
| C123-1 | Knock sensor #1 | 1–2 | CR02F030 | 1 | ⚠️ VERIFY | CC shows 2-pin housing, but piezoelectric may ground through bolt. CR02 = 2 cavities. |
| C123-2 | Knock sensor #2 | 1–2 | CR03F028 | 1 | ⚠️ VERIFY | CC P/N inconsistent with #1 (CR03F028 ≠ CR02F030). May be extraction OCR error. |
| C125 | Mass air flow sensor | 3 | CR02F048 | 1 → 3 | ✅ FIXED | 3-pin confirmed by FLA-40 circuit diagram: power (battery V) / signal / ground. P/N CR02F048 from CC; CR03F008 from original extraction — verify physically. |
| C126 | ISC actuator | 3 | CR02F028 | 2 | ⚠️ VERIFY | CC reads 3 pins but P/N prefix CR02 = 2 cavities. Functional analysis: power + control = 2 wires. Third pin may be unused cavity or feedback. Verify from CC face drawing. |
| C127 | Intake air temp sensor | 3 | CR02F041 | 2 | ⚠️ VERIFY | CC reads 3 pins but P/N prefix CR02 = 2 cavities. IAT is a simple thermistor = 2 wires. Third pin may be shield or unused cavity. Verify from CC face drawing. |
| C128 | A/C compressor clutch | 1 | CR01F028 | — | — | Single-wire |
| C109 | Vehicle speed sensor | 3 | CR03F028 | — | — | Not in MFI sensor tables |

### CC Extraction Quality Notes

The CC section was extracted from scanned PDF pages at 300 DPI using visual OCR. Known issues:

- **C114 (CMP):** CC extraction read 2 pins / CR02F028, but user physically confirmed 3-pin / CR03F029. The CMP is a Hall effect sensor requiring power + signal + ground. The extraction likely confused V6 C114 with the I4 C14 row (which IS 2-pin CR02F028 — the I4 uses a magnetic reluctance CMP).
- **C122 (Rear O2):** CC extraction read 2 pins, but part number prefix CR04 indicates 4 cavities. Heated O2 sensors require 4 wires.
- **C123-1/C123-2 (Knock sensors):** Inconsistent part numbers between the two. Physical verification needed.
- **Part numbers marked `[?]`** in the CC extraction have uncertain readings and should be verified against physical connectors.
- **C125 (MAF):** CC extraction reads CR02F048 (2-cavity housing) but MAF has 3 functional pins (power/signal/ground confirmed by FLA-40). Original extraction read CR03F008 (3-cavity). Physical verification needed to confirm P/N.
- **C126 (ISC):** CC reads 3 pins / CR02F028 (2-cavity housing). Pin count vs cavity count inconsistency — CC face drawing may show 3 positions with one unused, or the pin count reading may be an OCR error.
- **C127 (IAT):** CC reads 3 pins / CR02F041 (2-cavity housing). Same cavity/pin inconsistency as C126. IAT thermistor functionally requires only 2 wires.
- **Part number prefix decoding:** `CR##` — the digits after CR indicate physical housing cavity count (e.g., CR03F = 3-cavity female, CR02F = 2-cavity female). Cavities ≥ populated pins; X-marks on face drawings = unpopulated cavities.

> **Action items (resolved):** ~~Fix C112 (TPS) and C125 (MAF) sensor pinout tables in `mfi-control-v6.md`.~~ Done — TPS 3-pin table added from FLA-46, MAF 3-pin table added from FLA-40. C126/C127 pin count discrepancies noted for physical verification.

---

## SD Page Coverage Map

Which schematic diagram page covers which connectors:

| SD Page | Title | Connectors Covered |
|---------|-------|-------------------|
| SD-78 | MFI Control System (2.7L) — ECM Area | C112 (TPS), C113 (CKP), C114 (CMP), C133-1/3/4, C142 (joint — sensor power) |
| SD-79 | MFI Control System — O2 Bank 1 | C116 (front O2), C145 (B1/S1), C147 (B1/S2), C133-2 |
| SD-80 | MFI Control System — O2 Bank 2 | C122 (rear O2), C146 (B2/S1), C148 (B2/S2), C133-2/4 |
| SD-81 | MFI Control System — Fuel/Actuators | C111 (ECT), C121 (purge), C124-1..6 (injectors), C126 (ISC), E42 (ECR), E49 (FPR), C133-3/4 |
| SD-82 | MFI Control System — Air/Misc | C109 (VSS), C115 (oil P/S), C123-1/2 (knock), C125 (MAF), C127 (IAT), C128 (A/C), C144 (P/S sw), C133-3/5 |
| SD-83/84 | Component Location Index | Cross-reference table → CL page numbers |

---

## FLA (Shop Manual) Section Map

Which FLA section covers which sensors/actuators:

| FLA Page | Component | Content |
|----------|-----------|---------|
| FLA-2 | All sensors | General specifications table (type, resistance, voltage) |
| FLA-3 | System | Service standards, fuel pressure, ignition timing |
| FLA-4 | Fasteners | Tightening torques (ECT, O2 sensor, etc.) |
| FLA-20 | MFI system | System overview — how all sensors work together |
| FLA-35 | ECT sensor (C111) | Circuit diagram, inspection, troubleshooting |
| FLA-40 | MAF sensor (C125) | Circuit diagram, inspection, troubleshooting |
| FLA-43 | IAT sensor (C127) | Circuit diagram, inspection, troubleshooting |
| FLA-46 | TPS (C112) | Circuit diagram, 3-pin connector pinout, inspection |
| FLA-49 | ISC actuator (C126) | Circuit diagram, inspection |
| FLA-52 | HO2S (C116/122/145–148) | Circuit diagram, heater circuits, bank identification |
| FLA-55 | CMP sensor (C114) | Circuit diagram, 3-pin connector: Pin 1=Power, Pin 2=Signal, Pin 3=GND |
| FLA-57 | CKP sensor (C113) | Circuit diagram, 3-pin connector: Pin 1=Power, Pin 2=Signal, Pin 3=GND |
| FLA-59 | Fuel injector (C124-1..6) | Circuit diagram, resistance check, waveform |
| FLA-62 | Canister purge valve (C121) | EVAP system circuit diagram |
| FLA-65 | Knock sensor (C123-1/2) | Circuit diagram, signal characteristics |
| FLA-73+ | DTC troubleshooting | All DTCs — P0100 through P0700+ |

---

## Cross-Reference: Connector Code ↔ Component Name ↔ Graph Node

Quick lookup for translating between the ETM key (connector code), shop manual key (component name), and knowledge graph key (node ID).

| Connector Code | Component Name | Graph Node ID | Sensor Type |
|----------------|---------------|---------------|-------------|
| C111 | Engine Coolant Temperature Sensor | `comp-ect-sensor` | Thermistor (NTC) |
| C112 | Throttle Position Sensor | `comp-tps` | Variable resistor |
| C113 | Crankshaft Position Sensor | `comp-ckp-sensor` | Hall effect |
| C114 | Camshaft Position Sensor | `comp-cmp-sensor` | Hall effect |
| C116/C145/C146/C147/C148 | Heated Oxygen Sensor | `comp-o2-sensor` | Titanium |
| C123-1/C123-2 | Knock Sensor | `comp-knock-sensor` | Piezoelectric |
| C125 | Air Flow Sensor (MAF) | `comp-maf-sensor` | Hot film |
| C127 | Intake Air Temperature Sensor | `comp-iat-sensor` | Thermistor |
| C109 | Vehicle Speed Sensor | `comp-vss` | Hall effect |
| C118 | Ignition Coil | `comp-ignition-coil` | COP (white car) / Wasted spark (OEM) |
| C124-1..6 | Fuel Injector | `comp-injector` | Electromagnetic |

---

## Related Files

| File | Contents |
|------|----------|
| [`schematics/mfi-control-v6.md`](schematics/mfi-control-v6.md) | SD-78–85 extraction: ECM pinout tables, sensor pinout tables, O2 summary, component locations |
| [`../shop-manual/fuel-system/`](../shop-manual/fuel-system/) | FLA chapter: specs (part 1), sensor procedures (part 2), DTC troubleshooting |
| [`../opengk/ecm-pinouts.md`](../opengk/ecm-pinouts.md) | Siemens SIMK43 C133-1 through C133-4 pin assignments |
| [`../opengk/sensor-information.md`](../opengk/sensor-information.md) | Replacement part numbers, cross-references |
| [`../tiburon-knowledge-graph.json`](../tiburon-knowledge-graph.json) | Platform knowledge graph with component nodes |
| [`../knowledge-graph-schema.md`](../knowledge-graph-schema.md) | Node and edge type definitions |
| [`hl-harness-layouts.md`](hl-harness-layouts.md) | Full HL extraction — all harness connector tables |
| [`cc-connector-configurations.md`](cc-connector-configurations.md) | Full CC extraction — pin counts, part numbers, face drawings |
