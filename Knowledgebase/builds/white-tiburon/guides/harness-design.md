# Harness Design — White Tiburon
## Deutsch Connector Architecture for Engine Swap + Serviceability

**Car:** White 2003 Tiburon GK | Haltech Elite 2500 + AIM PDM 32
**Goal:** Every engine-mounted connection unplugs with a Deutsch connector. Pull 4 connectors + unbolt starter = engine is free.

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
                                    │  │ 34-pin   │  │  Conn A / B  │ │
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
                    │ [D2] 8-pin      │    │                 │   │                 │
                    │ Coil Harness    │    │ Fan (HP2 direct)│   │ LP8 Alt Exciter │
                    │                  │    │ Wiper MP3/MP6   │   │                 │
                    │ Starter (direct) │    │                 │   │ HP2 Fan         │
                    └──────────────────┘    │ [D3] 8-pin     │   │ (direct)        │
                                           │ Injector Harness│   └─────────────────┘
                                           └─────────────────┘
```

---

## Deutsch Connector Set

| ID | Pins | Location | Purpose | Disconnect For |
|----|------|----------|---------|----------------|
| **D1** | 12-pin | Near engine, driver side upper | Cam, crank, knock, IAT, MAP, TPS | Engine swap |
| **D2** | 8-pin | Near engine, top/rear between banks | Coil triggers (IGN 1–6) + power + ground | Engine swap |
| **D3** | 8-pin | Near fuel rail, top of engine | Injector signals (INJ 1–6) + power | Engine swap |
| **D4** | 8-pin | Convenient central point in engine bay | All 3 Lowdoller sensors (oil/coolant/fuel) | Sensor service |

**Engine swap disconnect sequence:** Unplug D1 + D2 + D3 + D4 (if oil sensor goes with engine), unbolt starter ring terminal, disconnect alternator B+. Engine is free.

**Total Deutsch connectors:** 1× 12-pin, 3× 8-pin.

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

## D2 — Coil Harness (8-Pin Deutsch)

**Location:** Top/rear of engine, between banks. Accessible from above.
**Chassis side:** Haltech harness trunk from firewall (trigger wires) + PDM MP2 power wire.
**Engine side:** Short pigtails to 6× Toyota 90919-A2005 coil connectors (new pre-terminated pigtails).

| Pin | Signal | Source | Wire | Engine-Side Destination |
|-----|--------|--------|------|------------------------|
| 1 | IGN 1 trigger | Haltech 34-pin pin 3 | Y/B | Coil 1, Pin B (Cyl 1) |
| 2 | IGN 2 trigger | Haltech 34-pin pin 4 | Y/R | Coil 2, Pin B (Cyl 2) |
| 3 | IGN 3 trigger | Haltech 34-pin pin 5 | Y/O | Coil 3, Pin B (Cyl 3) |
| 4 | IGN 4 trigger | Haltech 34-pin pin 6 | Y/G | Coil 4, Pin B (Cyl 4) |
| 5 | IGN 5 trigger | Haltech 34-pin pin 7 | Y/BR | Coil 5, Pin B (Cyl 5) |
| 6 | IGN 6 trigger | Haltech 34-pin pin 8 | Y/L | Coil 6, Pin B (Cyl 6) |
| 7 | +12V coil power | PDM MP2 (A3) | 14 AWG | Pin D common bus → all 6 coils |
| 8 | Ground | Engine block | 14 AWG | Pin A common bus → all 6 coils |

**Notes:**
- Pin 7 carries up to 15A total for all 6 coils. At ~2.1 ms dwell × 6 coils sequential, average current is well under the 13A DT pin rating.
- Coil Pin C (feedback) left open on all 6.
- **Phase 1 (stock ECU):** D2 is built but NOT plugged in. MP2 routes to OE relay spades. Stock ECU drives coils through OE harness.
- **Phase 2 (Haltech):** Disconnect stock coil connectors. Plug in D2. Reroute MP2 from OE relay spade → D2 pin 7 (chassis side).

---

## D3 — Injector Harness (8-Pin Deutsch)

**Location:** Near fuel rail, top of engine. Accessible from above.
**Chassis side:** Haltech harness trunk (INJ signal wires) + PDM MP1 power wire.
**Engine side:** Short pigtails to 6× injector connectors (new pre-terminated pigtails).

| Pin | Signal | Source | Wire | Engine-Side Destination |
|-----|--------|--------|------|------------------------|
| 1 | INJ 1 | Haltech 34-pin pin 19 | L | Injector 1 |
| 2 | INJ 2 | Haltech 34-pin pin 20 | L/B | Injector 2 |
| 3 | INJ 3 | Haltech 34-pin pin 21 | L/BR | Injector 3 |
| 4 | INJ 4 | Haltech 34-pin pin 22 | L/R | Injector 4 |
| 5 | INJ 5 | Haltech 34-pin pin 27 | L/O | Injector 5 |
| 6 | INJ 6 | Haltech 34-pin pin 28 | L/Y | Injector 6 |
| 7 | +12V injector power | PDM MP1 (A2) | 14 AWG | Injector rail 12V + Haltech 34-pin pin 26 (R/L) |
| 8 | Spare | — | — | Future use |

**Notes:**
- Pin 7 feeds both the injector rail (physical 12V) AND Haltech 34-pin pin 26 (ECU injector power sense). Splice these on the chassis side of D3.
- Haltech INJ outputs are ground-side drivers (0–8A peak / 0–2A hold per injector). Low current on signal pins.
- **Phase 1 (stock ECU):** D3 is built but NOT plugged in. MP1 routes to OE relay spades. Stock ECU drives injectors through OE harness.
- **Phase 2 (Haltech):** Disconnect stock injector connectors. Plug in D3. Reroute MP1 from OE relay spade → D3 pin 7 (chassis side).

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
| **Starter** | HP1 | A1 + A13 | 10 AWG | Ring terminal at solenoid S-terminal | Firewall → LEFT → bell housing |
| **Fan** | HP2 | A12 + A23 | 12 AWG | OEM fan connector or ring terminal | Firewall → RIGHT → radiator |
| **Fuel Pump** | HP3 | A24 + A25 | 14 AWG | Spade into fuse box pin 87 (Phase 1) | Firewall → CENTER → fuse box |

**Starter:** unbolt ring terminal from solenoid S-terminal during engine swap.

---

## PDM Medium-Power Runs (Through Firewall, No Deutsch)

These connect to chassis-mounted loads — no engine swap disconnect needed.

| Load | PDM Output | Pin | Wire Gauge | Termination | Routing |
|------|-----------|-----|-----------|-------------|---------|
| **Wiper Low** | MP3 | A4 | 16 AWG | Spade (Phase 1), direct splice (Phase 2) | Firewall → CENTER → wiper motor |
| **Wiper High** | MP6 | A7 | 16 AWG | Spade (Phase 1), direct splice (Phase 2) | Firewall → CENTER → wiper motor |
| **Alt Exciter** | LP8 | A21 | 18 AWG | Splice to cut OEM D+ wire | Firewall → RIGHT → alternator area |
| **MP1 (Phase 1)** | MP1 | A2 | 14 AWG | Spade into OE relay pin 87 | Firewall → CENTER → fuse box |
| **MP2 (Phase 1)** | MP2 | A3 | 14 AWG | Spade into OE relay pin 87 | Firewall → CENTER → fuse box |

**Phase 2 transition for MP1/MP2:** Pull spades from OE relay socket. Reroute:
- MP1 → D3 pin 7 (injector power, chassis side of Deutsch)
- MP2 → D2 pin 7 (coil power, chassis side of Deutsch)

---

## Fuse Box Spade Connections (Phase 1 — Temporary)

| PDM Output | Fuse Box Target | Phase 2 (Direct) |
|-----------|----------------|-------------------|
| HP3 Fuel Pump | Fuel pump relay pin 87 (relay pulled) | Direct to fuel pump + wire |
| MP1 InjectorPwr | OE main relay pin 87 (relay pulled) | → D3 pin 7 (injector Deutsch) |
| MP2 CoilPwr | OE main relay pin 87 (relay pulled) | → D2 pin 7 (coil Deutsch) |
| MP3 WiperLow | Wiper relay socket | Direct splice to wiper motor low |
| MP6 WiperHigh | Wiper relay socket | Direct splice to wiper motor high |
| HP1 Starter | Starter relay pin 87 or direct to solenoid | Direct to solenoid S-terminal |

---

## Innovate LM2 Wiring (Cockpit Only)

The LM2 is on the electronics plate in the passenger footwell — all connections are cockpit-side except the O2 sensor cable through the firewall to the exhaust.

### LM2 Connections

| Connection | LM2 Wire | Destination | Notes |
|------------|----------|-------------|-------|
| **Power** | LM2 power cable | PDM LP5 (A18) | 12V switched via SafeIgnition |
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
- D2 coil harness cable (8 wires) — routes over/around engine to both banks
- HP1 starter cable (10 AWG heavy, to bell housing)

**RIGHT TRUNK (Passenger Side):**
- D4 sensor bus branch to oil sensor (oil filter area, passenger side)
- HP2 fan cable (12 AWG heavy, to radiator fan)
- LP8 alt exciter (18 AWG, to alternator D+ splice)
- LM2 O2 sensor cable (proprietary, to exhaust bung)

**CENTER TRUNK (Underhood):**
- D3 injector harness cable (8 wires, to fuel rail top of engine)
- D4 sensor connector (8 wires — positioned centrally, sensor wires fan out from here)
- D4 sensor bus branch to coolant sensor (manifold tee)
- D4 sensor bus branch to fuel sensor (return line tap)
- HP3 fuel pump (14 AWG, to fuse box)
- MP1/MP2 (14 AWG, to OE relay, Phase 1)
- MP3/MP6 wiper (16 AWG, to fuse box / wiper motor)
- +5V sensor supply trunk
- Signal GND trunk

### Bundle Sizing

| Trunk | Approx Wire Count | Suggested Loom |
|-------|--------------------|----------------|
| LEFT | ~22 wires + HP1 heavy | 1" split loom or braided sleeve |
| RIGHT | ~8 wires + HP2 heavy + O2 cable | 3/4" split loom |
| CENTER | ~20 wires + HP3 heavy | 1" split loom |

---

## Build Order (Sunday SU.9)

1. **Lowdoller sensor pigtails** — crimp Deutsch DT pins onto each sensor's bare wires. Tie red wires together → pin 7, tie black+white wires together → pin 8. Do on bench before installing sensors.
2. **D4 chassis side** — run 8 wires from Haltech AVI pins through firewall to D4 location. Terminate with 8-pin Deutsch.
3. **D1 engine sensor harness** — build chassis-side cable (12 wires from Haltech 26-pin/34-pin through firewall). Build engine-side pigtails to cam, crank, knock, IAT, MAP, TPS. Terminate both sides with 12-pin Deutsch.
4. **D2 coil harness** — build chassis-side cable (6× IGN triggers from Haltech + MP2 power wire + ground). Build engine-side branches to 6× coil pigtail connectors. Terminate with 8-pin Deutsch.
5. **D3 injector harness** — build chassis-side cable (6× INJ wires from Haltech + MP1 power wire). Build engine-side branches to 6× injector pigtail connectors. Terminate with 8-pin Deutsch.
6. **LM2 analog cable** — short cockpit run: Lime Green → AVI 8, Yellow → signal GND.

**Phase 1 note:** D2 and D3 are built but NOT plugged in. MP1/MP2 go to OE relay spades. Stock ECU drives coils/injectors. When switching to Haltech, disconnect stock coil/injector connectors, plug in D2 + D3, reroute MP1 → D3 pin 7 and MP2 → D2 pin 7.

---

## Cross-References

| File | Contents |
|------|----------|
| `guides/pdm-config.md` | PDM output map, trigger logic, protection settings |
| `signal-routing.md` | Complete pin-to-pin signal trace |
| `guides/bench-test.md` | Test procedures for each output |
| `hardware/haltech/main-connector-26-pin-elite2500.md` | Haltech 26-pin pinout |
| `hardware/haltech/main-connector-34-pin-elite2500.md` | Haltech 34-pin pinout |
| `hardware/aim/aim-pdm/pdm-pinout.md` | PDM connector pinout |
| `hardware/sensors/lowdoller-sensors.md` | Lowdoller sensor specs, wire colors, calibration |
| `hardware/sensors/cop-ignition.md` | Toyota COP coil pinout (A/B/C/D) |
