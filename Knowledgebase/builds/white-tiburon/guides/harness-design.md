# Harness Design — White Tiburon
## Deutsch Connector Architecture for Engine Swap + Serviceability

**Car:** White 2003 Tiburon GK | Haltech Elite 2500 + AIM PDM 32
**Goal:** Every engine-mounted connection unplugs with a Deutsch connector. Pull 5 connectors + 2 ground ring terminals + unbolt starter = engine is free.

> **Connector stock:** 12-pin, 8-pin, 4-pin, 3-pin Deutsch DT series
> **Injector connectors:** New pigtails (pre-terminated, short leads)
> **Coil connectors:** New pigtails (pre-terminated, short leads — Toyota 90919-A2005)
> **Lowdoller sensors:** No factory connector — bare 5-wire leads (red/black/yellow/white/green). All 3 sensors consolidate to a single 8-pin Deutsch.
> **Stock O2 sensors:** Removed / disconnected. Wideband AFR via Innovate LM2 post-collector only.

---

## Harness Overview

```
                                    ┌─────────────────────────────────┐
                                    │      PASSENGER FOOTWELL         │
                                    │  ┌─────────┐  ┌──────────────┐ │
                                    │  │ Haltech  │  │   AIM PDM    │ │
                                    │  │ 34-pin   │  │ Black / Grey │ │
                                    │  │ 26-pin   │  │              │ │
                                    │  └────┬─────┘  └──────┬───────┘ │
                                    │       │               │         │
                                    │  ┌────┴───┐     ┌─────┴──────┐ │
                                    │  │  LM2   │     │  Podium    │ │
                                    │  └────────┘     └────────────┘ │
                                    └───────────┬─────────┬──────────┘
                                                │         │
                                     ═══════════╧═════════╧══════════
                                        CENTER FIREWALL PASS-THROUGH
                                     ════════════════╤═══════════════
                                                     │
                              ┌──────────────────────┼──────────────────────┐
                              │                      │                      │
                         LEFT (Driver)          CENTER              RIGHT (Passenger)
                              │                      │                      │
                    ┌─────────┴────────┐    ┌────────┴────────┐   ┌────────┴────────┐
                    │ [D1] 12-pin      │    │ Fuse box spades │   │ [D4] 8-pin      │
                    │ Engine Sensors   │    │ (Phase 1)       │   │ Lowdoller       │
                    │                  │    │ HP3, MP1/MP2    │   │ Sensors (all 3) │
                    │ [D5] 4-pin      │    │                 │   │                 │
                    │ IACV Stepper    │    │ Horn MP3 (Ph2+) │   │ LP8 Alt Exciter │
                    │                  │    │ Lights MP6(Ph2+)│   │                 │
                    │ [D3] 8-pin      │    │                 │   │ [D2] 8-pin      │
                    │ Bank 2 Rear     │    │                 │   │ Bank 1 Front    │
                    │ (Cyl 2,4,6)     │    │                 │   │ (Cyl 1,3,5)     │
                    │                  │    │                 │   │                 │
                    │ Starter (direct) │    │                 │   │ HB1 Fan         │
                    └──────────────────┘    └─────────────────┘   └─────────────────┘
```

> **Phase structure:** See `guides/pdm-build-guide.md` for the 3-phase build plan. Phase 1 = stock ECU + fuse box spades. Phase 2 = Haltech + Deutsch connectors. Phase 3 = CAN keypad + OE removal.
> **Wiper outputs:** MP9 (G4) low, MP10 (G5) high, LP9 (G3) park sweep — relay-less design using WIPER_PARKING math channel. Install when wipers are needed.

---

## Deutsch Connector Set

| ID | Pins | Location | Purpose | Disconnect For |
|----|------|----------|---------|----------------|
| **D1** | 12-pin | Near engine, driver side upper | Cam, crank, knock, IAT, MAP, TPS | Engine swap |
| **D2** | 8-pin | Front bank (cyl 1,3,5), passenger side | Bank 1: IGN 1/3/5 + INJ 1/3/5 + coil power + injector power | Engine swap |
| **D3** | 8-pin | Rear bank (cyl 2,4,6), driver side near firewall | Bank 2: IGN 2/4/6 + INJ 2/4/6 + coil power + injector power | Engine swap |
| **D4** | 8-pin | Convenient central point in engine bay | All 3 Lowdoller sensors (oil/coolant/fuel) | Sensor service |
| **D5** | 4-pin | Near throttle body / IACV | IACV stepper motor (4 phases) | Engine swap |

**Engine swap disconnect sequence:** Unplug D1 + D2 + D3 + D4 (if oil sensor goes with engine) + D5, unbolt 2× bank ground ring terminals (front head bolt + rear head bolt), unbolt starter ring terminal, disconnect alternator B+. Engine is free.

**Total Deutsch connectors:** 1× 12-pin, 3× 8-pin, 1× 4-pin. Each bank also has a separate 16 AWG ground wire with ring terminal to its head bolt.

---

## D1 — Engine Sensors (12-Pin Deutsch)

**Location:** Driver side upper engine bay, accessible from top.
**Chassis side:** Haltech harness trunk from firewall.
**Engine side:** Short pigtails to each sensor on the engine.

All sensors on this connector are on or near the engine and go with it during a swap: cam/crank (lower block/front), knock (block, driver side), IAT (back of plenum), MAP (plenum), TPS (throttle body).

| Pin | Signal | Haltech Pin | Wire | Engine-Side Destination |
|-----|--------|-------------|------|------------------------|
| 1 | Crank trigger + | 26-pin pin 1 | Y (shielded) | CKP sensor (lower block, driver side near crank pulley) |
| 2 | Crank trigger − | 26-pin pin 5 | G (shielded) | CKP sensor ground ref |
| 3 | Cam home + | 26-pin pin 2 | Y (shielded) | CMP sensor (front of engine, cam journal area) |
| 4 | Cam home − | 26-pin pin 6 | G (shielded) | CMP sensor ground ref |
| 5 | Knock 1 | 26-pin pin 21 | GY/G | Knock sensor, driver side block |
| 6 | Knock 2 | 26-pin pin 22 | GY/L | Knock sensor, driver side block |
| 7 | IAT signal | 26-pin pin 3 (AVI 7) | GY | IAT sensor, back of plenum |
| 8 | MAP signal | 34-pin pin 15 (AVI 9) | Y | MAP sensor, tapped into plenum |
| 9 | TPS signal | 34-pin pin 14 (AVI 10) | W | Throttle position sensor, throttle body |
| 10 | +8V supply (MAP) | 34-pin pin 12 | O/W | MAP sensor power |
| 11 | Signal GND | 26-pin pin 14/15/16 | B/W | Shared: IAT return, MAP return, shield drains |
| 12 | Shield drain | — | bare | Crank/cam shielded cable shields tied here |

**Notes:**
- Shielded pairs (crank, cam): use twisted shielded cable. Ground shield at Haltech end only. Pin 12 carries the shield drain through the connector so it stays continuous across the disconnect.
- Knock sensors are piezoelectric — body grounds to block. Only signal wire in connector.
- TPS gets +5V supply at the throttle body from the sensor supply bus (branched from +5V trunk, not in this connector — or can run through D4 bus).
- IAT ground shares pin 11 with MAP ground and shield drains.

---

## D2 — Bank 1 Front (Cyl 1, 3, 5) — 8-Pin Deutsch

**Location:** Front bank, passenger side of engine. Accessible from above.
**Chassis side:** Haltech harness trunk from firewall (3× IGN triggers + 3× INJ signals) + MP2 coil power branch + MP1 injector power branch.
**Engine side:** Short pigtails to 3× Toyota 90919-A2005 coil connectors + 3× injector connectors.
**Ground:** Separate 16 AWG wire bundled with pigtails → ring terminal → front cylinder head bolt.

| Pin | Signal | Source | Wire | Engine-Side Destination |
|-----|--------|--------|------|------------------------|
| 1 | IGN 1 trigger | Haltech 34-pin pin 3 | Y/B | Coil 1 Pin B |
| 2 | IGN 3 trigger | Haltech 34-pin pin 5 | Y/O | Coil 3 Pin B |
| 3 | IGN 5 trigger | Haltech 34-pin pin 7 | Y/BR | Coil 5 Pin B |
| 4 | INJ 1 signal | Haltech 34-pin pin 19 | L | Injector 1 |
| 5 | INJ 3 signal | Haltech 34-pin pin 21 | L/BR | Injector 3 |
| 6 | INJ 5 signal | Haltech 34-pin pin 27 | L/O | Injector 5 |
| 7 | +12V coil power | PDM MP2 (B3) branch | 14 AWG | Coil Pin D bus → 3 coils |
| 8 | +12V injector power | PDM MP1 (B2) branch | 14 AWG | Injector rail branch → 3 injectors |

**Bank 1 ground wire (not in connector):**
```
Engine side — bundled with D2 pigtails:
  Coil 1 Pin A ──┐
  Coil 3 Pin A ──┼── splice (solder + heat shrink) ── 16 AWG ── ring terminal ── front head bolt
  Coil 5 Pin A ──┘
```

**Notes:**
- Coil Pin C (feedback) left open on all 3.
- Pin 7 carries ~7.5A max (3 of 6 coils). Sequential firing means only 1 coil dwells at a time on this bank — well under 13A DT pin rating.
- Pin 8 carries injector power for 3 cylinders. Haltech INJ outputs are ground-side drivers (low current on signal pins 4–6).
- **Phase 1 (stock ECU):** D2 is built but NOT plugged in. MP2 routes to OE relay spades. Stock ECU drives coils/injectors through OE harness.
- **Phase 2 (Haltech):** Disconnect stock front bank coil/injector connectors. Plug in D2. Bolt ground ring terminal to front head bolt. Reroute MP2 branch → D2 pin 7, MP1 branch → D2 pin 8 (chassis side).

---

## D3 — Bank 2 Rear (Cyl 2, 4, 6) — 8-Pin Deutsch

**Location:** Rear bank, driver side of engine near firewall. Short wire run. Accessible from above.
**Chassis side:** Haltech harness trunk from firewall (3× IGN triggers + 3× INJ signals) + MP2 coil power branch + MP1 injector power branch.
**Engine side:** Short pigtails to 3× Toyota 90919-A2005 coil connectors + 3× injector connectors.
**Ground:** Separate 16 AWG wire bundled with pigtails → ring terminal → rear cylinder head bolt.

| Pin | Signal | Source | Wire | Engine-Side Destination |
|-----|--------|--------|------|------------------------|
| 1 | IGN 2 trigger | Haltech 34-pin pin 4 | Y/R | Coil 2 Pin B |
| 2 | IGN 4 trigger | Haltech 34-pin pin 6 | Y/G | Coil 4 Pin B |
| 3 | IGN 6 trigger | Haltech 34-pin pin 8 | Y/L | Coil 6 Pin B |
| 4 | INJ 2 signal | Haltech 34-pin pin 20 | L/B | Injector 2 |
| 5 | INJ 4 signal | Haltech 34-pin pin 22 | L/R | Injector 4 |
| 6 | INJ 6 signal | Haltech 34-pin pin 28 | L/Y | Injector 6 |
| 7 | +12V coil power | PDM MP2 (B3) branch | 14 AWG | Coil Pin D bus → 3 coils |
| 8 | +12V injector power | PDM MP1 (B2) branch | 14 AWG | Injector rail branch → 3 injectors |

**Bank 2 ground wire (not in connector):**
```
Engine side — bundled with D3 pigtails:
  Coil 2 Pin A ──┐
  Coil 4 Pin A ──┼── splice (solder + heat shrink) ── 16 AWG ── ring terminal ── rear head bolt
  Coil 6 Pin A ──┘
```

**Notes:**
- Identical pin layout to D2 — same connector, same pin functions, different cylinders.
- Rear bank is close to the firewall — shortest wire run of any Deutsch connector.
- Coil Pin C (feedback) left open on all 3.
- **Phase 1 (stock ECU):** D3 is built but NOT plugged in. MP2 routes to OE relay spades. Stock ECU drives coils/injectors through OE harness.
- **Phase 2 (Haltech):** Disconnect stock rear bank coil/injector connectors. Plug in D3. Bolt ground ring terminal to rear head bolt. Reroute MP2 branch → D3 pin 7, MP1 branch → D3 pin 8 (chassis side).

---

## MP1/MP2 Power Distribution (Chassis Side)

With per-bank connectors, MP1 and MP2 each split into two branches on the chassis side of the firewall:

```
PDM MP2 (B3) ── 14 AWG ── through firewall ──┬── branch → D2 pin 7 (Bank 1 coil power)
                                               └── branch → D3 pin 7 (Bank 2 coil power)

PDM MP1 (B2) ── 14 AWG ── through firewall ──┬── branch → D2 pin 8 (Bank 1 injector power)
                                               ├── branch → D3 pin 8 (Bank 2 injector power)
                                               └── branch → Haltech 34-pin pin 26 (injector power sense, R/L)
```

**Splice location:** Engine bay side of firewall, before the trunks diverge. Use solder + heat shrink or Posi-Tap for serviceability. The MP1 splice is a 3-way (D2 + D3 + Haltech sense). The MP2 splice is a 2-way (D2 + D3).

---

## D4 — Lowdoller Sensors (8-Pin Deutsch)

**Location:** Convenient central spot in engine bay — all 3 sensor wire runs converge here.
**Chassis side:** 8 wires from Haltech through firewall (6 signals + power + ground).
**Engine side:** Bare sensor wires from all 3 Lowdoller sensors run directly to this connector.

| Pin | Signal | Haltech Pin | From Sensor | Notes |
|-----|--------|-------------|-------------|-------|
| 1 | Fuel pressure | 26-pin pin 13 (AVI 1) | Fuel 899404 — Yellow wire | On return line tap, 0–150 PSI |
| 2 | Fuel temp | 34-pin pin 16 (AVI 2) | Fuel 899404 — Green wire | PTC resistive |
| 3 | Oil pressure | 34-pin pin 17 (AVI 3) | Oil 899404 — Yellow wire | By oil filter, passenger side, 0–150 PSI |
| 4 | Oil temp | 34-pin pin 2 (AVI 4) | Oil 899404 — Green wire | PTC resistive |
| 5 | Coolant pressure | 26-pin pin 20 (AVI 5) | Coolant LDM899TP100 — Yellow wire | On manifold tee, 0–100 PSI |
| 6 | Coolant temp | 26-pin pin 12 (AVI 6) | Coolant LDM899TP100 — Green wire | PTC resistive |
| 7 | +5V supply | 34-pin pin 9 (shared) | All 3 sensors — Red wires tied | 100 mA max total |
| 8 | Signal GND | 26-pin pin 14/15/16 (shared) | All 3 sensors — Black + White wires tied | All 6 GND wires (3 black + 3 white) combined |

**Sensor wire routing to D4:**
```
Oil sensor (passenger side, by oil filter)
  └── Yellow, Green, Red, Black, White ──────────┐
                                                  │
Coolant sensor (manifold tee)                     ├──── [D4] 8-pin Deutsch
  └── Yellow, Green, Red, Black, White ──────────┤     (central engine bay)
                                                  │
Fuel sensor (return line tap)                     │
  └── Yellow, Green, Red, Black, White ──────────┘
```

- Red wires from all 3 sensors tied together → D4 pin 7
- Black wires (pressure GND) + White wires (temp GND) from all 3 sensors tied together → D4 pin 8
- Each Yellow (pressure signal) and Green (temp signal) runs individually → D4 pins 1–6

**Notes:**
- Oil sensor on engine block goes with engine on swap. Coolant and fuel sensors stay on chassis (hose/line mounted). During engine swap, either unplug D4 entirely and leave coolant/fuel sensor wires dangling, or split the oil sensor onto its own connector if this becomes annoying.
- Bare sensor wires should be terminated with proper Deutsch DT pins (crimped, not soldered to pin). Solder the tie junctions for the red and black/white buses, then crimp the combined wire into the Deutsch pin.

---

## D5 — IACV Stepper Motor (4-Pin Deutsch)

**Location:** Near throttle body / IACV valve, driver side upper — close to D1.
**Chassis side:** 4 wires from Haltech 34-pin pins 31–34 through firewall.
**Engine side:** Short pigtail to IACV connector (OEM connector or direct crimp).
**Part:** Hyundai 35150-33010 / Kefico 9540930002 — 4-phase stepper motor.

| Pin | Signal | Haltech Pin | Wire | Engine-Side Destination |
|-----|--------|-------------|------|------------------------|
| 1 | Stepper 1 P1 — phase A | 34-pin pin 31 | G | IACV stepper coil A+ |
| 2 | Stepper 1 P2 — phase B | 34-pin pin 32 | G/B | IACV stepper coil A− |
| 3 | Stepper 1 P3 — phase C | 34-pin pin 33 | G/BR | IACV stepper coil B+ |
| 4 | Stepper 1 P4 — phase D | 34-pin pin 34 | G/R | IACV stepper coil B− |

**Notes:**
- Haltech Stepper 1 outputs are hi/lo side drivers (1A max per phase) — well within Deutsch DT pin ratings.
- IACV is engine-mounted (bolted to throttle body), so it goes with the engine on swap. D5 provides the disconnect point.
- Phase order (A+/A−/B+/B−) must be confirmed during commissioning. If idle hunts or stepper buzzes, swap phases in Haltech NSP or swap pin pairs at D5.
- Route D5 cable alongside D1 in the LEFT trunk — both terminate in the same area (driver side upper engine bay).

---

## +5V Sensor Supply Bus

All Lowdoller sensor +5V (red wires) and the TPS +5V share a single supply from Haltech 34-pin pin 9 (O wire, 100 mA max).

```
Haltech 34-pin pin 9 (+5V, O wire)
    │
    ├── through firewall ── D4 pin 7 ── branches to all 3 sensor Red wires
    │
    └── through firewall ── D1 pin 9 area ── TPS +5V at throttle body
```

**Signal GND bus** — same topology from Haltech 26-pin pins 14/15/16 (B/W):
```
Haltech 26-pin pins 14/15/16 (Signal GND)
    │
    ├── through firewall ── D4 pin 8 ── branches to all 3 sensor Black+White wires
    │
    └── through firewall ── D1 pin 11 ── IAT, MAP, shield drains
```

---

## High-Current Direct Runs (No Deutsch)

These PDM outputs exceed Deutsch DT pin ratings (13A continuous @ 16 AWG) and run direct with ring terminals or OEM connectors.

| Load | PDM Output | Pins | Wire Gauge | Termination | Routing |
|------|-----------|------|-----------|-------------|---------|
| **Starter** | HP1 | B1 + B13 | 10 AWG | Ring terminal at solenoid S-terminal | Firewall → LEFT → bell housing |
| **Fan** | HB1 | G1 + G2 | 12 AWG | OEM fan connector or ring terminal | Firewall → RIGHT → radiator |
| **Fuel Pump** | HP3 | B24 + B25 | 14 AWG | Spade into fuse box pin 87 (Phase 1) | Firewall → CENTER → fuse box |

**Starter:** unbolt ring terminal from solenoid S-terminal during engine swap.

---

## PDM Medium-Power Runs (Through Firewall, No Deutsch)

These connect to chassis-mounted loads — no engine swap disconnect needed.

| Load | PDM Output | Pin | Wire Gauge | Termination | Routing |
|------|-----------|-----|-----------|-------------|---------|
| **Horn** | MP3 | B4 | 16 AWG | Phase 1: not connected (BCM controls). Phase 2+: direct to horn or relay socket | Firewall → CENTER → horn |
| **Headlights** | MP6 | B7 | 14 AWG | Phase 1: not connected (BCM controls). Phase 2+: direct to headlights or relay socket | Firewall → CENTER → headlight connector |
| **Alt Exciter** | LP8 | B21 | 18 AWG | Splice to cut OEM D+ wire | Firewall → RIGHT → alternator area |
| **MP1** | MP1 | B2 | 14 AWG | Phase 1: spade into OE relay pin 87. Phase 2: splits to D2 pin 8 + D3 pin 8 (injector power, both banks) + Haltech pin 26 sense | Firewall → CENTER → splice → both banks |
| **MP2** | MP2 | B3 | 14 AWG | Phase 1: spade into OE relay pin 87. Phase 2: splits to D2 pin 7 + D3 pin 7 (coil power, both banks) | Firewall → CENTER → splice → both banks |

> **MP3 and MP6 repurposed** from wipers to horn and headlights. Wipers use MP9 (G4) low, MP10 (G5) high, LP9 (G3) park sweep on Grey Connector — relay-less park design, config pre-loaded.

**Phase 2 transition for MP1/MP2:** Pull spades from OE relay socket. Reroute:
- MP1 → 3-way splice: D2 pin 8 (Bank 1 injector power) + D3 pin 8 (Bank 2 injector power) + Haltech 34-pin pin 26 (injector power sense)
- MP2 → 2-way splice: D2 pin 7 (Bank 1 coil power) + D3 pin 7 (Bank 2 coil power)
- See "MP1/MP2 Power Distribution" section above for splice diagram.

---

## Fuse Box Spade Connections (Phase 1 — Temporary)

> Phase 1A (Saturday): Main relay + fuel pump + starter only. Fan added in Phase 1B (Sunday after CAN verified).
> Horn and headlights stay on stock BCM relays through Phase 1.

| PDM Output | Fuse Box Target | Phase 2 (Direct) |
|-----------|----------------|-------------------|
| MP1 InjPwr | OE main relay pin 87 (relay pulled) | → 3-way splice: D2 pin 8 + D3 pin 8 + Haltech pin 26 |
| MP2 CoilPwr | OE main relay pin 87 (relay pulled) | → 2-way splice: D2 pin 7 + D3 pin 7 |
| HP3 FuelPump | Fuel pump relay pin 87 (relay pulled) | Direct to fuel pump + wire |
| HP1 Starter | Direct to solenoid S-terminal (preferred) | Same |
| HB1 Fan | Fan relay pin 87 (Phase 1B, after CAN verified) | Direct to fan motor |
| MP3 Horn | Not connected Phase 1 (BCM controls) | Direct to horn or relay socket |
| MP6 Headlights | Not connected Phase 1 (BCM controls) | Direct to headlight connector or relay socket |

---

## Innovate LM2 Wiring (Cockpit Only)

The LM2 is on the electronics plate in the passenger footwell — all connections are cockpit-side except the O2 sensor cable through the firewall to the exhaust.

### LM2 Connections

| Connection | LM2 Wire | Destination | Notes |
|------------|----------|-------------|-------|
| **Power** | LM2 power cable | PDM LP5 (B18) | 12V switched via SafeIgnition |
| **Analog Out 1 (+)** | Cable 3811 — Lime Green | Haltech 26-pin pin 4 (AVI 8) | 0–5V, default 7.35–22.39 AFR |
| **Analog Out 1 (−)** | Cable 3811 — Yellow | Haltech signal GND (26-pin pin 14/15/16) | Ground reference |
| **O2 sensor cable** | LM2 sensor cable (proprietary) | Wideband O2 bung, post-collector exhaust | Runs through firewall → RIGHT trunk → exhaust |
| **Analog In 1 (+)** | Cable 3811 — Purple | Crankcase pressure sensor signal | 0–5V sensor on vacuum tee between valve covers |
| **Analog In 1 (−)** | Cable 3811 — Black | Crankcase pressure sensor GND | |

### LM2 Analog Cable 3811 — Full Pinout

| Wire Color | Function | Used? |
|------------|----------|-------|
| **Lime Green** | Analog Out 1 (+) | **Yes** → Haltech AVI 8 (wideband AFR) |
| **Yellow** | Analog Out 1 (−) | **Yes** → Haltech signal GND |
| Brown/White | Analog Out 2 (+) | No (simulated narrowband, not needed) |
| Dark Green | Analog Out 2 (−) | No |
| **Purple** | Analog In 1 (+) | **Yes** → crankcase pressure sensor |
| **Black** | Analog In 1 (−) | **Yes** → crankcase pressure GND |
| Grey | Analog In 2 (+) | Spare |
| Brown | Analog In 2 (−) | Spare |
| White | Analog In 3 (+) | Spare |
| Red | Analog In 3 (−) | Spare |
| Peach | Analog In 4 (+) | Spare |
| Orange | Analog In 4 (−) | Spare |
| Black/White | RPM (+) | No |
| Blue | RPM (−) | No |

### AVI 8 Reassignment

AVI 8 (26-pin pin 4) was previously assigned to OEM CTS — **redundant** since Lowdoller coolant temp is already on AVI 6 (26-pin pin 12). Reassigned to LM2 wideband AFR.

| AVI | Previous | Now |
|-----|----------|-----|
| AVI 7 | Brake pressure (later) / IAT | **IAT** (keep — sensor on back of plenum) |
| AVI 8 | OEM CTS (redundant) / Brake temp (later) | **LM2 Wideband AFR** (0–5V, Analog Out 1) |

> **Haltech NSP config:** Set AVI 8 input type to "Wideband Lambda". Calibration: 0V = 7.35 AFR (0.50λ), 5V = 22.39 AFR (1.523λ). Or use Innovate default linear scale with custom cal table.

> **Brake sensors (later):** When brake sensors go in, move LM2 to Haltech serial wideband input (MTS protocol) to free AVI 8. Move IAT to an LM2 analog input or AIM expansion channel to free AVI 7.

### Stock O2 Sensors

**Removed / disconnected.** The stock narrowband sensors (one per bank, pre-cat) provide no useful tuning data — they only switch rich/lean at stoich. The LM2 wideband post-collector gives actual lambda across the full range. Leave the bungs plugged or sensors in place but disconnected. No Haltech heater wiring needed.

---

## Physical Bundle Routing

### Through Center Firewall Hole

All harnesses pass through a single center firewall grommet, then split into 3 trunks.

**LEFT TRUNK (Driver Side):**
- D1 engine sensor cable (12 wires, includes shielded pairs for crank/cam)
- D3 Bank 2 rear cable (8 wires + 16 AWG ground) — short run, rear bank is near firewall on driver side
- D5 IACV stepper cable (4 wires) — routes to throttle body area near D1
- HP1 starter cable (10 AWG heavy, to bell housing)

**RIGHT TRUNK (Passenger Side):**
- D2 Bank 1 front cable (8 wires + 16 AWG ground) — routes forward to front bank, passenger side
- D4 sensor bus branch to oil sensor (oil filter area, passenger side)
- HB1 fan cable (12 AWG heavy, to radiator fan)
- LP8 alt exciter (18 AWG, to alternator D+ splice)
- LM2 O2 sensor cable (proprietary, to exhaust bung)

**CENTER TRUNK (Underhood):**
- D4 sensor connector (8 wires — positioned centrally, sensor wires fan out from here)
- D4 sensor bus branch to coolant sensor (manifold tee)
- D4 sensor bus branch to fuel sensor (return line tap)
- HP3 fuel pump (14 AWG, to fuse box)
- MP1/MP2 trunk (14 AWG each, to OE relay Phase 1 / splice point Phase 2)
- MP3 horn (16 AWG, Phase 2+ only)
- MP6 headlights (14 AWG, Phase 2+ only)
- +5V sensor supply trunk
- Signal GND trunk

> **MP1/MP2 splice point:** Located in the center trunk near the firewall. MP1 and MP2 each split here — branches route left to D3 (rear bank) and right to D2 (front bank). See "MP1/MP2 Power Distribution" section.

### Bundle Sizing

| Trunk | Approx Wire Count | Suggested Loom |
|-------|--------------------|----------------|
| LEFT | ~26 wires + HP1 heavy + D3 ground | 1" split loom or braided sleeve |
| RIGHT | ~18 wires + HB1 heavy + D2 ground + O2 cable | 1" split loom or braided sleeve |
| CENTER | ~14 wires + HP3 heavy | 3/4" split loom |

---

## Build Order (Sunday SU.9)

1. **Lowdoller sensor pigtails** — crimp Deutsch DT pins onto each sensor's bare wires. Tie red wires together → pin 7, tie black+white wires together → pin 8. Do on bench before installing sensors.
2. **D4 chassis side** — run 8 wires from Haltech AVI pins through firewall to D4 location. Terminate with 8-pin Deutsch.
3. **D1 engine sensor harness** — build chassis-side cable (12 wires from Haltech 26-pin/34-pin through firewall). Build engine-side pigtails to cam, crank, knock, IAT, MAP, TPS. Terminate both sides with 12-pin Deutsch.
3a. **D5 IACV stepper harness** — build chassis-side cable (4 wires from Haltech 34-pin pins 31–34 through firewall). Build engine-side pigtail to IACV connector (35150-33010). Terminate with 4-pin Deutsch. Route alongside D1 in LEFT trunk.
4. **D2 Bank 1 front harness** — build chassis-side cable (3× IGN + 3× INJ from Haltech + MP2 coil power branch + MP1 injector power branch). Build engine-side pigtails to 3× coil connectors (cyl 1,3,5) + 3× injector connectors (cyl 1,3,5). Build ground splice (3× coil Pin A → 16 AWG → ring terminal). Terminate signal/power with 8-pin Deutsch. Bundle ground wire alongside but terminate separately at front head bolt.
5. **D3 Bank 2 rear harness** — identical to D2 but for cylinders 2,4,6. Shorter wire run (rear bank near firewall). Ground ring terminal → rear head bolt.
6. **MP1/MP2 splice** — on engine bay side of firewall, splice MP1 into 3-way (D2 pin 8 + D3 pin 8 + Haltech pin 26 sense) and MP2 into 2-way (D2 pin 7 + D3 pin 7). Solder + heat shrink or Posi-Tap.
7. **LM2 analog cable** — short cockpit run: Lime Green → AVI 8, Yellow → signal GND.

**Phase 1 note:** D2 and D3 are built but NOT plugged in. Ground ring terminals NOT bolted (stock coils ground through OE harness). MP1/MP2 go to OE relay spades. Stock ECU drives coils/injectors through OE harness. Horn (MP3) and headlights (MP6) are not connected — BCM controls them.

**Phase 2 switchover:** Disconnect stock coil/injector connectors on both banks. Disconnect stock IACV connector. Plug in D2 (front bank) + D3 (rear bank) + D5 (IACV). Bolt both ground ring terminals to respective head bolts. Pull MP1/MP2 spades from OE relay socket — splices route power to both Deutsch connectors automatically. Add horn button (Ch12) and headlight toggle (Ch04). Wire MP3 → horn, MP6 → headlights. No Race Studio config change. See `guides/pdm-build-guide.md` → "Phase 2 — Transition Procedure".

**Wiper wiring (when needed):** MP9 (G4) → motor Green wire (low), MP10 (G5) → motor Yellow wire (high), LP9 (G3) → motor Brown wire (park sweep). Motor Black → chassis ground. No external relay — PDM WIPER_PARKING math channel handles park positioning. See `guides/pdm-build-guide.md` → "Wiper — Relay-Less Park Design".

---

## Cross-References

| File | Contents |
|------|----------|
| `guides/pdm-build-guide.md` | **Primary:** 3-phase PDM build guide, output maps, Race Studio config, test gates |
| `weekend-tasks.md` | Weekend build schedule — sensor install, harness fab, test procedures |
| `signal-routing.md` | Complete pin-to-pin signal trace |
| `guides/bench-test.md` | Additional bench test procedures and notes log |
| `guides/keypad-config-future.md` | Phase 3 CAN keypad button/LED/variable config |
| `hardware/haltech/main-connector-26-pin-elite2500.md` | Haltech 26-pin pinout |
| `hardware/haltech/main-connector-34-pin-elite2500.md` | Haltech 34-pin pinout |
| `hardware/aim/aim-pdm/pdm-pinout.md` | PDM connector pinout |
| `hardware/aim/aim-podium/aim-podium-micro.md` | PodiumConnect Micro pinout, CAN mapping |
| `hardware/sensors/lowdoller-sensors.md` | Lowdoller sensor specs, wire colors, calibration |
| `hardware/sensors/cop-ignition.md` | Toyota COP coil pinout (A/B/C/D) |
