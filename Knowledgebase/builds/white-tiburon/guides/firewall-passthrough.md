# Firewall Pass-Through Wiring Guide

All wires route from the cabin (where the PDM 32 and Haltech Elite 2500 are mounted) through a **single center firewall grommet**, then split into three trunks on the engine-bay side.

---

## Phase 1 — PDM + Stock ECU, Haltech Sensors Only

Stock ECU still runs the engine. Haltech is powered but only reads the 6 Lowdoller sensor channels. PDM handles power distribution.

**All PDM power wires for Phase 2 are pulled through the firewall now** so Phase 2 only adds Haltech signal wires. Coil/injector power runs are coiled and capped on the engine-bay side until needed.

### PDM Power Outputs → Engine Bay

| Wire | PDM Output | Pin | Gauge | Destination | Phase 1 State |
|------|-----------|-----|-------|-------------|---------------|
| Starter | HP1 | B1+B13 | 10 AWG | Starter solenoid S-terminal | **Active** |
| Fan | HB1 | G1+G2 | 12 AWG | Radiator fan | **Active** |
| Fuel Pump | HP3 | B24+B25 | 14 AWG | OEM fuse box pin 87 (piggyback) | **Active** |
| Alt Exciter | LP8 | B21 | 18 AWG | Alternator D+ wire splice | **Active** |
| Injector Power | MP1 | B2 | 14 AWG | 3-way splice → D2-8 + D3-8 + Haltech 34-pin-26 sense | Coiled & capped |
| Coil Power | MP2 | B3 | 14 AWG | 2-way splice → D2-7 + D3-7 | Coiled & capped |
| Headlights | MP6 | B7 | 14 AWG | Headlight connector | Coiled & capped |
| Horn | MP3 | B4 | 16 AWG | Horn | Coiled & capped |

### Haltech Sensor Wiring → Engine Bay (D4 Deutsch 8-pin)

| Wire | Haltech Pin | AVI | Sensor |
|------|------------|-----|--------|
| Fuel pressure signal | 26-pin-13 | AVI1 | Lowdoller 899404 yellow |
| Fuel temp signal | 34-pin-16 | AVI2 | Lowdoller 899404 green |
| Oil pressure signal | 34-pin-17 | AVI3 | Lowdoller 899404 yellow |
| Oil temp signal | 34-pin-2 | AVI4 | Lowdoller 899404 green |
| Coolant pressure signal | 26-pin-20 | AVI5 | Lowdoller LDM899TP100 yellow |
| Coolant temp signal | 26-pin-12 | AVI6 | Lowdoller LDM899TP100 green |
| +5V supply | 34-pin-9 | — | All 3 sensor red wires |
| Signal GND | 26-pin-14/15/16 | — | All 6 sensor black+white wires |

### Stays Cabin-Side (No Firewall)

- **CAN bus:** Haltech 26-pin-23/24 → PDM A30/A31 (both devices in cabin)
- **Haltech power:** PDM LP1 (B14) → Haltech 26-pin-11
- **IGN sense:** PDM G23 splice → Haltech 34-pin-13
- **Battery GND:** Chassis → Haltech 34-pin-10, 34-pin-11

### Phase 1 Firewall Wire Count

| Item | Wires |
|------|-------|
| PDM power runs — active (starter, fan, fuel pump, alt exciter) | 4 heavy-gauge direct runs |
| PDM power runs — coiled & capped (inj power, coil power, headlights, horn) | 4 direct runs |
| D4 Deutsch (Lowdoller sensors) | 8 |
| LM2 O2 sensor cable (if installed) | 1 proprietary cable |
| **Total** | **~16 wires + O2 cable** |

---

## Phase 2 — Full Haltech Running the Engine

All PDM power wires are already through the firewall from Phase 1. This phase adds only the Haltech signal wires: engine sensors, ignition triggers, injector drives, and wideband O2. Uncap the coil/injector power runs and splice them into D2/D3.

### Engine Sensors (D1 Deutsch 12-pin)

| Wire | Haltech Pin | Destination |
|------|------------|-------------|
| Crank trigger + | 26-pin-1 | CKP sensor (shielded) |
| Crank trigger − | 26-pin-5 | CKP sensor (shielded) |
| Cam home + | 26-pin-2 | CMP sensor (shielded) |
| Cam home − | 26-pin-6 | CMP sensor (shielded) |
| Knock 1 | 26-pin-21 | Knock sensor, driver block |
| Knock 2 | 26-pin-22 | Knock sensor, driver block |
| IAT signal | 26-pin-3 (AVI7) | IAT, back of plenum |
| MAP signal | 34-pin-15 (AVI9) | MAP sensor, plenum tap |
| TPS signal | 34-pin-14 (AVI10) | Throttle body |
| +8V supply | 34-pin-12 | MAP sensor power |
| Signal GND | 26-pin-14/15/16 | IAT/MAP return + shield drains |
| Shield drain | — | Crank/cam shield ties |

### Bank 1 Front — Cyl 1, 3, 5 (D2 Deutsch 8-pin + ground ring)

| Wire | Source | Destination |
|------|--------|-------------|
| IGN 1 trigger | 34-pin-3 | Coil 1 Pin B |
| IGN 3 trigger | 34-pin-5 | Coil 3 Pin B |
| IGN 5 trigger | 34-pin-7 | Coil 5 Pin B |
| INJ 1 signal | 34-pin-19 | Injector 1 |
| INJ 3 signal | 34-pin-21 | Injector 3 |
| INJ 5 signal | 34-pin-27 | Injector 5 |
| +12V coil power | PDM MP2 (B3) branch | Coil Pin D bus |
| +12V injector power | PDM MP1 (B2) branch | Injector rail |
| **GND ring** (outside connector) | 16 AWG | Front head bolt |

### Bank 2 Rear — Cyl 2, 4, 6 (D3 Deutsch 8-pin + ground ring)

| Wire | Source | Destination |
|------|--------|-------------|
| IGN 2 trigger | 34-pin-4 | Coil 2 Pin B |
| IGN 4 trigger | 34-pin-6 | Coil 4 Pin B |
| IGN 6 trigger | 34-pin-8 | Coil 6 Pin B |
| INJ 2 signal | 34-pin-20 | Injector 2 |
| INJ 4 signal | 34-pin-22 | Injector 4 |
| INJ 6 signal | 34-pin-28 | Injector 6 |
| +12V coil power | PDM MP2 (B3) branch | Coil Pin D bus |
| +12V injector power | PDM MP1 (B2) branch | Injector rail |
| **GND ring** (outside connector) | 16 AWG | Rear head bolt |

### Uncap Phase 1 PDM Runs — Splice into D2/D3

| Wire | Action |
|------|--------|
| MP1 (injector power) | Uncap → 3-way splice: D2 pin 8 + D3 pin 8 + Haltech 34-pin-26 sense |
| MP2 (coil power) | Uncap → 2-way splice: D2 pin 7 + D3 pin 7 |
| MP6 (headlights) | Uncap → connect to headlight harness |
| MP3 (horn) | Uncap → connect to horn |

### Wideband O2

| Wire | Notes |
|------|-------|
| LM2 O2 sensor cable | Proprietary cable, firewall → exhaust bung |

### Phase 2 New Firewall Wires (Added to Phase 1 Bundle)

| Bundle | Wires | Connector |
|--------|-------|-----------|
| D1 engine sensors | 12 | 12-pin Deutsch |
| D2 Bank 1 | 8 + GND ring | 8-pin Deutsch |
| D3 Bank 2 | 8 + GND ring | 8-pin Deutsch |
| LM2 O2 cable | 1 | Proprietary |
| **Phase 2 additions** | **~28 wires + 2 GND rings + O2 cable** | |

### Combined Firewall Total (Phase 1 + Phase 2)

| Item | Wires |
|------|-------|
| PDM power runs (from Phase 1) | 8 direct runs |
| D4 Lowdoller sensors (from Phase 1) | 8 |
| D1 engine sensors | 12 |
| D2 Bank 1 | 8 + GND ring |
| D3 Bank 2 | 8 + GND ring |
| LM2 O2 cable | 1 |
| **Total** | **~44 wires + 2 GND rings + O2 cable** |

---

## Physical Routing — Engine Bay Side

All wires converge at the center firewall grommet, then split into three trunks:

### Left Trunk (Driver Side)
- D1 engine sensor cable (12 wires, includes shielded pairs for crank/cam)
- D3 Bank 2 rear cable (8 wires + 16 AWG ground ring)
- HP1 starter cable (10 AWG)

### Right Trunk (Passenger Side)
- D2 Bank 1 front cable (8 wires + 16 AWG ground ring)
- D4 branch to oil sensor (oil filter area, passenger side)
- HB1 fan cable (12 AWG)
- LP8 alt exciter (18 AWG)
- LM2 O2 sensor cable

### Center Trunk
- D4 sensor connector (positioned centrally, branches to coolant and fuel sensors)
- HP3 fuel pump (14 AWG)
- MP1/MP2 power buses (14 AWG each — coiled & capped in Phase 1, spliced to D2/D3 in Phase 2)
- MP3 horn + MP6 headlights (coiled & capped in Phase 1, connected in Phase 2)
- +5V sensor supply trunk
- Signal GND trunk

### Splice Points (Engine-Bay Side, Before Trunks Diverge)
- **MP1** → 3-way splice: D2 pin 8 + D3 pin 8 + Haltech 34-pin-26 sense wire
- **MP2** → 2-way splice: D2 pin 7 + D3 pin 7
