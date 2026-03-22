# Firewall Pass-Through Wiring Guide

All wires route from the cabin (where the PDM 32 and Haltech Elite 2500 are mounted) through a **single center firewall grommet** to the engine bay. Connector strategy (Deutsch breakouts, splice points, trunk routing) will be determined after sensor placement is finalized in the engine bay.

---

## Phase 1 — PDM + Stock ECU, Haltech Sensors Only

Stock ECU still runs the engine. Haltech is powered but only reads the Lowdoller sensor channels. PDM handles power distribution.

**All PDM power wires for Phase 2 are pulled through the firewall now** so Phase 2 only adds Haltech signal wires. Unused power runs are coiled and capped on the engine-bay side until needed.

### PDM Power Outputs → Engine Bay

| Wire | PDM Output | Pin | Gauge | Destination | Phase 1 State |
|------|-----------|-----|-------|-------------|---------------|
| Starter | HP1 | B1+B13 | 10 AWG | Starter solenoid S-terminal | **Active** |
| Fan | HB1 | G1+G2 | 12 AWG | Radiator fan | **Active** |
| Fuel Pump | HP3 | B24+B25 | 14 AWG | OEM fuse box pin 87 (piggyback) | **Active** |
| Alt Exciter | LP8 | B21 | 18 AWG | Alternator D+ wire splice | **Active** |
| Injector Power | MP1 | B2 | 14 AWG | Injector rail (both banks) + Haltech 34-pin-26 sense | Coiled & capped |
| Coil Power | MP2 | B3 | 14 AWG | Coil Pin D bus (both banks) | Coiled & capped |
| Headlights | MP6 | B7 | 14 AWG | Headlight connector | Coiled & capped |
| Horn | MP3 | B4 | 16 AWG | Horn | Coiled & capped |

### Haltech Sensor Wiring → Engine Bay (ECU-Critical)

These stay on Haltech AVI inputs — the ECU uses them for engine protection and closed-loop strategies. No CAN latency acceptable.

| Wire | Haltech Pin | AVI | Sensor | ECU Use |
|------|------------|-----|--------|---------|
| Fuel pressure signal | 26-pin-13 | AVI1 | Lowdoller 899404 yellow | Closed-loop fuel pressure |
| Oil pressure signal | 34-pin-17 | AVI3 | Lowdoller 899404 yellow | Engine protection (RPM limit/cut) |
| Oil temp signal | 34-pin-2 | AVI4 | Lowdoller 899404 green | Engine protection (temp limit) |
| Coolant temp signal | 26-pin-12 | AVI6 | Lowdoller LDM899TP100 green | Engine protection, fan control, cold-start enrichment |
| +5V supply | 34-pin-9 | — | Haltech sensor red wires | Shared 100mA supply |
| Signal GND | 26-pin-14/15/16 | — | Haltech sensor black+white wires | Shared signal return |

### PDM Analog Sensor Wiring → Engine Bay (Monitoring Only)

Logging/dash display only — routed to PDM analog inputs. Data reaches the Haltech via CAN if needed.

| Wire | PDM Analog Input | Sensor | Notes |
|------|-----------------|--------|-------|
| Fuel temp signal | TBD | Lowdoller 899404 green | Fuel combo sensor, monitoring only |
| Coolant pressure signal | TBD | Lowdoller LDM899TP100 yellow | Coolant combo sensor, monitoring only |
| +5V supply | TBD | Sensor red wires | PDM analog supply or shared from Haltech |
| Signal GND | TBD | Sensor black+white wires | PDM analog ground |

### Stays Cabin-Side (No Firewall)

- **CAN bus:** Haltech 26-pin-23/24 → PDM A30/A31 (both devices in cabin)
- **Haltech power:** PDM LP1 (B14) → Haltech 26-pin-11
- **IGN sense:** PDM G23 splice → Haltech 34-pin-13
- **Battery GND:** Chassis → Haltech 34-pin-10, 34-pin-11

### Phase 1 Firewall Wire Count

| Item | Wires |
|------|-------|
| PDM power runs — active (starter, fan, fuel pump, alt exciter) | 4 heavy-gauge |
| PDM power runs — coiled & capped (inj power, coil power, headlights, horn) | 4 |
| Haltech ECU-critical sensors (fuel press, oil press, oil temp, coolant temp + supply + gnd) | 6 |
| PDM analog sensors (fuel temp, coolant press + supply + gnd) | 4 |
| LM2 O2 sensor cable (if installed) | 1 proprietary cable |
| **Total** | **~18 wires + O2 cable** |

---

## Phase 2 — Full Haltech Running the Engine

All PDM power wires are already through the firewall from Phase 1. This phase adds only the Haltech signal wires: engine sensors, ignition triggers, injector drives, and wideband O2. Uncap the coil/injector power runs and connect them.

### Engine Sensors

| Wire | Haltech Pin | Destination |
|------|------------|-------------|
| Crank trigger + | 26-pin-1 | CKP sensor (shielded pair) |
| Crank trigger − | 26-pin-5 | CKP sensor (shielded pair) |
| Cam home + | 26-pin-2 | CMP sensor (shielded pair) |
| Cam home − | 26-pin-6 | CMP sensor (shielded pair) |
| Knock 1 | 26-pin-21 | Knock sensor, driver block |
| Knock 2 | 26-pin-22 | Knock sensor, driver block |
| IAT signal | 26-pin-3 (AVI7) | IAT, back of plenum |
| MAP signal | 34-pin-15 (AVI9) | MAP sensor, plenum tap |
| TPS signal | 34-pin-14 (AVI10) | Throttle body |
| +8V supply | 34-pin-12 | MAP sensor power |
| Signal GND | 26-pin-14/15/16 | IAT/MAP return + shield drains |
| Shield drain | — | Crank/cam shield ties |

### Ignition Triggers (6× COP — Toyota 90919-A2005)

| Wire | Haltech Pin | Destination |
|------|------------|-------------|
| IGN 1 | 34-pin-3 | Coil 1 Pin B (Cyl 1, Bank 1 front) |
| IGN 2 | 34-pin-4 | Coil 2 Pin B (Cyl 2, Bank 2 rear) |
| IGN 3 | 34-pin-5 | Coil 3 Pin B (Cyl 3, Bank 1 front) |
| IGN 4 | 34-pin-6 | Coil 4 Pin B (Cyl 4, Bank 2 rear) |
| IGN 5 | 34-pin-7 | Coil 5 Pin B (Cyl 5, Bank 1 front) |
| IGN 6 | 34-pin-8 | Coil 6 Pin B (Cyl 6, Bank 2 rear) |

### Injector Drives (6× sequential)

| Wire | Haltech Pin | Destination |
|------|------------|-------------|
| INJ 1 | 34-pin-19 | Injector 1 (Cyl 1, Bank 1 front) |
| INJ 2 | 34-pin-20 | Injector 2 (Cyl 2, Bank 2 rear) |
| INJ 3 | 34-pin-21 | Injector 3 (Cyl 3, Bank 1 front) |
| INJ 4 | 34-pin-22 | Injector 4 (Cyl 4, Bank 2 rear) |
| INJ 5 | 34-pin-27 | Injector 5 (Cyl 5, Bank 1 front) |
| INJ 6 | 34-pin-28 | Injector 6 (Cyl 6, Bank 2 rear) |

### Coil & Injector Power (Uncap Phase 1 Runs)

| Wire | Action |
|------|--------|
| MP1 (injector power, 14 AWG) | Uncap → splice to both injector rails + Haltech 34-pin-26 sense |
| MP2 (coil power, 14 AWG) | Uncap → splice to coil Pin D bus (both banks) |

### Coil & Injector Grounds (Engine-Bay Side Only)

| Wire | Gauge | Destination |
|------|-------|-------------|
| Bank 1 coil GND bus | 16 AWG | Ring terminal → front head bolt (Coil 1/3/5 Pin A) |
| Bank 2 coil GND bus | 16 AWG | Ring terminal → rear head bolt (Coil 2/4/6 Pin A) |

### Wideband O2

| Wire | Notes |
|------|-------|
| LM2 O2 sensor cable | Proprietary cable, firewall → exhaust bung |

### Uncap Remaining Phase 1 Runs

| Wire | Action |
|------|--------|
| MP6 (headlights) | Uncap → connect to headlight harness |
| MP3 (horn) | Uncap → connect to horn |

### Phase 2 New Firewall Wires

| Item | Wires |
|------|-------|
| Engine sensors (crank, cam, knock, IAT, MAP, TPS + supply + gnd + shield) | 12 |
| Ignition triggers (IGN 1–6) | 6 |
| Injector drives (INJ 1–6) | 6 |
| LM2 O2 cable | 1 |
| **Phase 2 additions** | **~24 wires + O2 cable** |

### Combined Firewall Total (Phase 1 + Phase 2)

| Item | Wires |
|------|-------|
| PDM power runs (from Phase 1) | 8 |
| Haltech ECU-critical sensors (from Phase 1) | 6 |
| PDM analog sensors (from Phase 1) | 4 |
| Engine sensors | 12 |
| Ignition triggers (IGN 1–6) | 6 |
| Injector drives (INJ 1–6) | 6 |
| LM2 O2 cable | 1 |
| **Total** | **~42 wires + O2 cable** |

Note: Coil/injector grounds are engine-bay local (ring terminals to head bolts) — they do not pass through the firewall.
