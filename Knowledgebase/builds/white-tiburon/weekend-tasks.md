# White Tiburon — Weekend Build Tasks
## Haltech + AIM PDM Integration | Physical Switch Panel

**Target:** PDM fully installed and running with stock ECU for next track day. Haltech wired with Lowdoller sensors and MAP vacuum for data logging + CAN communication test. Injector/coil harnesses left ready to plug in the following weekend.

> **Primary reference files:**
> - PDM build guide (3-phase): `guides/pdm-build-guide.md` — Race Studio config, output maps, all phase procedures
> - Harness design: `guides/harness-design.md` — Deutsch connectors, wire routing, bundle sizing
> - Signal routing: `signal-routing.md`
>
> **Supporting files:**
> - `guides/bench-test.md` — bench test procedures, fuse box tap, notes log
> - `guides/keypad-config-future.md` — Phase 3 CAN keypad config (preserved)
>
> **CAN device docs:**
> - `hardware/aim/aim-smartycam/aim-smartycam.md` — SmartyCam pinout, RS3 config
> - `hardware/aim/aim-podium/aim-podium-micro.md` — PodiumConnect Micro, RaceCapture config
> - `hardware/aim/aim-datahub/aim-datahub.md` — Data Hub star topology
> - `hardware/aim/aim-gps08/aim-gps08.md` — GPS-08 auto-broadcast behavior
>
> **Wiper logic:** Relay-less park design finalized — MP9 (G4) / MP10 (G5) / LP9 (G3) on Grey connector with WIPER_PARKING math channel. Config pre-loaded in RS3. Install when wipers are needed.

---

## Current State (March 2026)

| System | Status |
|--------|--------|
| Haltech bench | Cam ✅ Crank ✅ COP fire ✅ — Knock: **next** |
| PDM Race Studio config | ✅ Updated — physical switch panel (no keypad) |
| PDM car connection | Spade connectors → fuse box pin 87 (non-destructive) |
| Physical switch panel | 6 toggles + 1 momentary starter — **not yet wired to PDM** |
| Stock ECU | Connected and running |
| Kill switch | Mounted left of steering wheel, 2 AWG cable run |
| Seat panel | Needs welding (~3 hrs) — **must do before electronics install** |

**Removed from this weekend:** Suspension (coilovers → fab shop Wednesday), front brakes + bearings (fab shop).

---

## FRIDAY AT HOME — Race Studio Config + Fuel Pump Bench (Workday)

PDM at home with laptop + fuel pump. All software work and bench testing — no car needed.

### F.1 Finalize PDM Configuration

> **Full config reference:** `guides/pdm-build-guide.md` → "Race Studio Configuration" section

- [ ] Open Race Studio 3 → `Webinar complete.zconfig` → Save As `Tiburon_White_v1.zconfig`
- [ ] Configure all power outputs per build guide output map (one config for Phase 1 + Phase 2)
  - HP1–HP3 (starter, fan, fuel pump)
  - MP1/MP2 (injector/coil pwr — Phase 1: main relay spade, Phase 2: Deutsch connectors)
  - MP3 Horn, MP4 BrakeLights, MP5 TailLights, MP6 Headlights (MP3/MP6 active in Phase 2+)
  - MP7 Coolsuit, MP8 Defogger
  - LP1–LP8 (ECU, dash, SmartyCam, GPS, wideband, cluster, warning LED, alt exciter)
- [ ] Configure status variables: ENGINE_RUNNING, FUEL_PRIME, FAN_TEMP bands (77/82/87/92°C), FAN_FAILSAFE, STARTER_SAFE, MULTI_WARNING
- [ ] Configure channel inputs: Ch02 (fan low), Ch03 (fan high), Ch10 (coolsuit), Ch11 (defogger), Ch12 (horn), Ch04 (headlights), Ch01 (starter), Ch09 (brake)
- [ ] Verify CAN2 disabled (no keypad — preserved in `guides/keypad-config-future.md`)
- [ ] Configure ECU Stream: Haltech CAN_V2_40 on CAN1 (B30/B31), 500 kbps
  - Enable channels: RPM, ECT, Oil P, Oil T, Fuel P, TPS, Vehicle Speed, Battery V
- [ ] Configure SmartyCam Stream: RPM, Speed (GPS-08), Gear, Coolant Temp, Oil P, TPS, Lat G, Long G
- [ ] Transmit config to PDM via USB

> **Wiper logic:** Being added separately. Ch05/Ch06 left spare for now.

> **✓ TEST:** Force-test each output in Race Studio Live Measures (no loads — just verify logic triggers)

### F.2 Fuel Pump Bench Test

> **Full procedure:** `guides/pdm-build-guide.md` → "Fuel Pump Bench Test" section

- [ ] Wire fuel pump to HP3 (B24+B25), 14 AWG minimum, battery GND to pump (−)
- [ ] IGN on → verify 3-second prime cycle → off
- [ ] Force HP3 on → measure current (expected 5–10A continuous)
- [ ] Measure voltage at pump (< 0.5V drop from supply)
- [ ] IGN off/on → verify prime timer resets

### F.3 CAN Device Configuration (SmartyCam + Podium)

> **SmartyCam config reference:** `hardware/aim/aim-smartycam/aim-smartycam.md`
> **Podium config reference:** `hardware/aim/aim-podium/aim-podium-micro.md`

**SmartyCam 3 Corsa — RS3 Session B (USB-C to camera):**
- [ ] Connect USB-C to SmartyCam (camera must be powered via 7-pin or internal battery)
- [ ] RS3 → CAN Protocol tab → select **AiM Default** (matches PDM SmartyCam Stream)
- [ ] RS3 → Overlay tab → position: RPM (top center), Speed (bottom), Water Temp, Oil P, TPS, G-force
- [ ] Save → Transmit config to camera
- [ ] On camera: MENU → SETTINGS → AUTO START REC → **Enable**
- [ ] Insert SD card (≥2 GB)

**PodiumConnect Micro — RaceCapture App (USB or phone):**
- [ ] Connect Podium via USB to PC (or Bluetooth to phone)
- [ ] Open RaceCapture app → set CAN baud rate to **1000000** (1 Mbps)
- [ ] Select **AIM** preset for CAN channel mapping (Speed, Lat, Long, RPM, ECT, Oil P, TPS)
- [ ] WiFi → AP mode: Enable (pit wall dashboard on phone)
- [ ] WiFi → STA mode: Enter phone hotspot SSID + password (2.4 GHz only) for cloud streaming
- [ ] Insert SD card (≥2 GB)
- [ ] Optional: create Podium account at podium.live, generate streaming key

> **Podium is NOT an AIM device.** It won't appear in Race Studio. All config is via the RaceCapture app.

**Bench smoke test (all devices on Data Hub):**
- [ ] Connect PDM → expansion cable → Data Hub → GPS-08 (port 1) + SmartyCam EXP (port 2) + Podium (port 3 via Binder-to-M8 adapter)
- [ ] Wire LP3 (B16) → SmartyCam 7-pin power (Red +12V, Black GND) — or use fused bench tap
- [ ] IGN on → verify SmartyCam LED (green/blue = CAN active), GPS-08 LED, Podium CAN LED (⇄)
- [ ] RS3 Live Data → CAN AiM bus shows traffic
- [ ] SmartyCam: press record → 10s → stop → check `.mp4` on SD (overlay labels visible, values = 0 expected)
- [ ] Podium: phone → connect to Podium AP WiFi → RaceCapture dashboard shows channel tiles

> GPS won't lock indoors — all position/speed/G values will be zero. Normal. Verify at shop with sky view.

### F.4 Prep Work

- [ ] Label all PDM harness wires with destination (use build guide output map + harness-design.md)
- [ ] Inventory parts: breakers (150A, 120A), spade connectors, ring terminals, wire (2/4/10/14/18 AWG)
- [ ] Inventory sensors: Lowdoller fuel/oil/coolant, MAP, wideband O2 bung
- [ ] Pack laptop + USB cable for shop

---

## FRIDAY EVENING — Welding + Mechanical Prep (Shop, 5pm+)

**Welding first — sparks and heat cannot coexist with electronics.** Do all hot work before any electronics go near the car.

### FE.1 Weld Seat Panel (~3 hours)

- [ ] Remove seat and loose interior trim from passenger footwell area
- [ ] Weld in floor panel for seat mount
- [ ] Grind and finish welds
- [ ] Clean area thoroughly (metal shavings, sparks, slag)

### FE.2 Mechanical Prep (While Panel Cools / After Welding)

- [ ] Test-fit electronics mounting plate in passenger footwell — mark bolt holes
- [ ] Drill mounting holes in plate and floor (if not using adhesive/rivets)
- [ ] Drain oil for oil sensor install tomorrow (let it drain overnight = cleaner)
- [ ] Prep oil sensor port: verify 1/8" NPT thread, have Teflon tape ready
- [ ] Lay out PDM harness along planned routes (engine bay through firewall, cockpit runs)

---

## SATURDAY — PDM Install + Power System = Phase 1A (Shop, All Day)

> **Detailed procedure:** `guides/pdm-build-guide.md` → "Phase 1A — Core Install"

**Goal by end of Saturday:** PDM installed, powered, all switches working, car starts and runs on stock ECU with PDM controlling engine power, starter, fuel pump, and alternator exciter. Horn/headlights/fan stay on stock BCM relays.

### S.1 Install Electronics Mounting Plate (First Thing)

All electronics on a single plate in passenger footwell: PDM, Haltech Elite 2500, Podium Micro (SN: 1QTV5KM), Innovate LM2.

- [ ] Bolt/rivet mounting plate into passenger footwell
- [ ] Mount PDM on plate (vibration-isolated)
- [ ] Mount Haltech Elite 2500 on plate
- [ ] Mount Podium Micro on plate
- [ ] Mount Innovate LM2 on plate

### S.2 Kill Switch Wiring

Kill switch already mounted. 2 AWG cable already run from battery (+) to large terminal A.

- [ ] Verify jumper from large terminal A to small terminal A
- [ ] Wire large terminal B → 150A breaker → starter B+ / alternator B+ (2 AWG)
- [ ] Wire large terminal B → 120A breaker → PDM Surlok (+) (4 AWG)
- [ ] Wire small terminal B → IGN toggle switch (new)
- [ ] IGN toggle → PDM G23 AND Haltech 34-pin pin 13 (P wire)
- [ ] Connect PDM Surlok power cable
- [ ] Connect PDM grounds (G13, G14, G18 to chassis)

> Kill switch diagram: `guides/pdm-build-guide.md` → "S.2 Kill Switch Wiring"

### S.3 Switch Panel Wiring (Phase 1 Layout)

```
[IGN]  [FAN]  [COOL]  [DEFOG]  [____]  [____]
[START]                                  (LED)
```

- [ ] Start button → Ch01 (G26), momentary, active = GND
- [ ] Fan low toggle → Ch02 (G27), active = 12V
- [ ] Fan high toggle → Ch03 (G28), active = 12V
- [ ] Coolsuit toggle → Ch10 (G22), active = 12V
- [ ] Defogger toggle → Ch11 (B26), active = 12V
- [ ] Brake light switch → Ch09 (G21), closed on press
- [ ] Warning LED → LP7 (B20)

> **2 spare panel positions** reserved for horn (Ch12/B27) and headlights (Ch04/G29) in Phase 2.
> **Wiper switches** not installed — wiper logic being developed separately.

### S.4 First Power-Up in Car

- [ ] Kill switch ON, IGN toggle ON → PDM powers up
- [ ] Connect laptop USB → Race Studio Live Data
- [ ] Verify `SafeIgnition` = 1
- [ ] Flip each toggle → verify correct channel input activates in Live Data
- [ ] Press START button → verify `STARTER_SAFE` logic (should activate with ENGINE_RUNNING = 0)
- [ ] IGN toggle OFF → verify `SafeIgnition` = 0, all outputs drop
- [ ] Kill switch OFF → verify total power loss

> **✓ GATE:** All switches verified before connecting any loads.

### S.5 Dash + LVDS

- [ ] Mount AIM 10" dash (visible from driver position)
- [ ] Connect LVDS cable from PDM to dash
- [ ] Verify dash powers up and shows live data

### S.6 Fuse Box Connections — Core (3 Relay Spades)

**OE Main Relay (MP1/MP2):**
- [ ] Locate OE main relay in underhood fuse box
- [ ] Pull the OE main relay
- [ ] Insert PDM MP1 (B2) wire into relay socket pin 87 (power out)
- [ ] Insert PDM MP2 (B3) wire into same pin 87 socket (parallel)
- [ ] IGN on → verify stock ECU powers up via PDM; IGN off → stock ECU loses power
- [ ] **Test:** Stock dash lights, check engine light, fuel gauge all work

> **Phase 2:** Pull MP1/MP2 spades, reroute MP1 → D3 pin 7 (injectors), MP2 → D2 pin 7 (coils). No Race Studio config change.

**Fuel Pump Relay (HP3):**
- [ ] Pull OEM fuel pump relay
- [ ] Insert PDM HP3 (B24+B25) wire into pin 87 socket
- [ ] IGN on → verify 3-second fuel prime (listen for pump), then off
- [ ] Verify in Race Studio: `FUEL_PRIME` timer fires

**Starter (HP1 → direct to solenoid):**
- [ ] Run HP1 (B1+B13) wire directly to starter solenoid S-terminal (10 AWG, ring terminal)
- [ ] Leave OEM starter relay in place as backup
- [ ] Press START (Ch01) → engine cranks; release → stops
- [ ] While engine running: press START → should NOT engage (RPM interlock)

> **Horn, headlights, fan relays left in place.** Stock BCM controls them normally through Phase 1.

### S.7 Alternator Exciter (LP8)

- [ ] Locate OEM alternator D+ exciter wire (thin ~18 AWG at alternator Yazaki connector)
- [ ] Confirm with multimeter: 12V with IGN on, 0V with IGN off
- [ ] Cut exciter wire at convenient point (leave length on both ends)
- [ ] Fuse box side → wire to PDM LP8 (B21, Black Connector)
- [ ] Alternator D+ side → remains connected to alternator (load side)

### S.8 CAN0 Expansion Bus — AIM Devices + Podium

> Data Hub is a passive star splitter — each device plugs into its own port.
> GPS-08 and Podium get power through hub +Vb rail (B33, always on). SmartyCam needs **separate LP3 power** via 7-pin connector.
> All software config should be done Friday (F.3). Saturday is physical install + verification.

**Install:**
- [ ] Verify CAN0 expansion cable: B22 (H) / B11 (L) / B33 (+Vb out) / B10 (GND)
- [ ] Connect Data Hub male port to expansion cable
- [ ] Hub port 1 → GPS-08 (5-pin Binder)
- [ ] Hub port 2 → SmartyCam EXP port (5-pin Binder — CAN data only)
- [ ] Hub port 3 → Podium Micro (Binder-to-M8 adapter)
- [ ] Wire LP3 (B16) → SmartyCam 7-pin main power (Red = +12V, Black = GND)
- [ ] Mount GPS-08 (roof or cowl — clear sky view, antenna face up)
- [ ] Mount SmartyCam (windshield or roll bar bracket)
- [ ] Podium already on electronics plate (S.1)

**Verify:**
- [ ] IGN on → SmartyCam powers up (CAN LED: green/blue solid)
- [ ] GPS-08 LED active (powered via hub B33)
- [ ] Podium power LED on, CAN ⇄ LED active
- [ ] RS3 Live Data → CAN AiM bus shows traffic
- [ ] GPS channels appear in RS3 Channels tab after satellite lock (~30s with sky view)
- [ ] SmartyCam: start recording → overlay shows channel labels (values may be 0 until Haltech CAN connected Sunday)
- [ ] Podium: phone → connect to Podium AP WiFi → RaceCapture dashboard shows channel tiles

> **Podium is NOT visible in Race Studio** — it's Autosport Labs, not AIM. Verify via RaceCapture app only.

### S.9 Full System Test — Phase 1A Gate

- [ ] IGN on → fuel prime (3s) → pump off
- [ ] Press START → engine cranks and starts
- [ ] Verify engine running: `ENGINE_RUNNING` = 1 in Race Studio
- [ ] Verify starter interlock: press START while running → no crank
- [ ] Verify alternator charging: 13.8–14.4V at battery posts
- [ ] Verify fan works via stock BCM relay (should activate on its own at temp)
- [ ] Verify horn works via steering wheel button (stock BCM)
- [ ] Verify headlights work via stalk switch (stock BCM)
- [ ] Verify coolsuit (Ch10) → MP7 on
- [ ] Verify defogger (Ch11) → MP8 on
- [ ] Verify brake lights (Ch09) → MP4 on (test with IGN off too)
- [ ] Verify tail lights → MP5 on with IGN (automatic)
- [ ] **Kill switch test:** engine running → flip kill switch → engine dies, all power drops, alternator stops charging

> **✓ GATE:** Car starts, runs, and stops reliably on stock ECU with PDM. Kill switch kills everything. Horn/headlights/fan work through stock BCM.

---

## SUNDAY — Sensors + CAN + Fan Migration = Phase 1B (Shop, All Day)

> **Fan migration procedure:** `guides/pdm-build-guide.md` → "Phase 1B — CAN + Sensors + Fan Migration"

**Goal by end of Sunday:** All Lowdoller sensors installed and reading, Haltech CAN data flowing to PDM, fan moved to PDM control (verified via CAN temp), coil/injector harnesses built and ready to plug in.

### SU.1 Oil Sensor Install (Oil Already Drained Friday)

- [ ] Install Lowdoller 150 PSI oil pressure/temp sensor (PN 899404, 1/8" NPT)
- [ ] Refill oil, check for leaks
- [ ] Wire: Yellow → AVI 3 (34-pin pin 17, O/R), Green → AVI 4 (34-pin pin 2, O/Y)

### SU.2 Coolant Sensor Install

- [ ] Full coolant flush (water out, fresh coolant in)
- [ ] Install Lowdoller coolant sensor (LDM899TP100, M12×1.5) on tee with OE coolant temp sender
- [ ] Wire: Yellow → AVI 5 (26-pin pin 20, O/G), Green → AVI 6 (26-pin pin 12, GY/O shielded)

### SU.3 Fuel System + Fuel Sensor

- [ ] Install Radium FPR/damper on fuel rail
- [ ] Route 6AN PTFE lines (collect all fittings first)
- [ ] Cut return line and install line tap + Lowdoller fuel sensor (PN 899404, 1/8" NPT)
- [ ] Wire: Yellow → AVI 1 (26-pin pin 13, GY/Y shielded), Green → AVI 2 (34-pin pin 16, O/B)

### SU.4 MAP Sensor

- [ ] Drill and tap threaded hole in intake plenum (standard boss)
- [ ] Install MAP sensor
- [ ] Connect vacuum tube to plenum
- [ ] Wire MAP → Haltech AVI 9 (34-pin pin 15, Y); power from +8V (pin 12, O/W)

### SU.5 Sensor Common Wiring

- [ ] All red wires → Haltech +5V (34-pin pin 9, O wire)
- [ ] All black + white wires → Haltech signal GND (26-pin pins 14/15/16, B/W)

> **✓ TEST:** All AVIs show 0.5–0.6V resting (zero pressure); temp channels read room temp

### SU.6 Haltech CAN1 → PDM

- [ ] Connect Haltech 26-pin pins 23/24 (CAN H/L) → PDM B30/B31 (CAN1)
- [ ] Power Haltech from PDM LP1 (B14)
- [ ] Verify Haltech CAN_V2_40 protocol active — all enabled channels visible in Race Studio Live Data
- [ ] Confirm fan temp bands react to live coolant temp on CAN
- [ ] Confirm warning LED (LP7) triggers when sensor thresholds crossed (force values in NSP)
- [ ] Verify MAP reading in NSP at idle vacuum

> **✓ GATE:** CAN data flowing confirmed before moving fan to PDM control.

> **✓ TEST:** Start car → RPM > 50 → `ENGINE_RUNNING` activates → fuel pump stays on → all CAN sensor data flowing

### SU.6B Move Fan to PDM Control

> CAN temp data confirmed flowing → safe to migrate fan from stock BCM relay to PDM PWM control.

**Try Option A first (reversible):**
- [ ] Pull OEM fan relay
- [ ] Insert HB1 (G1+G2) wire into fan relay pin 87 socket (12 AWG)
- [ ] Warm up engine → verify fan bands activate at correct temps (25%@77°C, 50%@82°C, 75%@87°C, 98%@92°C)

**If relay socket has too much resistance → Option B (direct):**
- [ ] Run HB1 directly to fan motor connector
- [ ] Leave OEM fan relay as backup

- [ ] Verify fan override toggle (Ch02/Ch03) → 98% duty
- [ ] Verify fan failsafe: disconnect Haltech CAN temporarily → fan goes to 98% after 5s → reconnect

### SU.7 Wideband AFR (Innovate LM2)

- [ ] Wire LM2 power → PDM LP5 (B18) — already mounted on plate Saturday
- [ ] Wire LM2 Analog Out 1: Lime Green (+) → Haltech AVI 8 (26-pin pin 4); Yellow (−) → signal GND (26-pin pin 14/15/16)
- [ ] Install wideband O2 sensor bung in exhaust post-collector (weld if not already in place)
- [ ] Install O2 sensor, route proprietary cable through firewall → RIGHT trunk → footwell → LM2
- [ ] Configure Haltech NSP: AVI 8 = "Wideband Lambda", cal 0V = 7.35 AFR / 5V = 22.39 AFR
- [ ] Verify AFR reading in Haltech NSP and on AIM dash
- [ ] Disconnect / remove stock narrowband O2 sensors (no value with wideband installed)
- [ ] Optional: wire crankcase pressure sensor to LM2 Analog In 1 (Purple +, Black −)

> See `guides/harness-design.md` for LM2 cable 3811 full pinout

### SU.8 OE Cluster Verification

- [ ] Confirm tach signal: Haltech DPO 1 (34-pin pin 18, V/B) → cluster TACHO
- [ ] Confirm speedo: OEM VSS (C109) → cluster + Haltech SPI 1 (26-pin pin 8)
- [ ] Fuel gauge: direct OEM circuit (no ECU involvement) — verify still works
- [ ] Coolant gauge: direct OEM circuit — verify still works

### SU.9 Harness Fabrication (Prep for Haltech Switchover)

> **Full harness design with Deutsch connector pin maps:** `guides/harness-design.md`

Build all harnesses with Deutsch connectors now. Switching from stock ECU → Haltech = plug in D2 + D3, reroute MP1/MP2.

**Deutsch connectors to build:**

| Connector | Pins | What It Carries |
|-----------|------|-----------------|
| **D1** | 12-pin | Engine sensors: cam, crank, knock, IAT, MAP, TPS |
| **D2** | 8-pin | Coil harness: IGN 1–6 triggers + MP2 power + ground |
| **D3** | 8-pin | Injector harness: INJ 1–6 signals + MP1 power |
| **D4** | 8-pin | Lowdoller sensors: all 3 sensors (6 signals + +5V + GND) |

**Build order:**
- [ ] **D4 sensor connector** — crimp Deutsch DT pins onto all 3 Lowdoller sensor bare wires. Tie reds → pin 7, tie blacks+whites → pin 8. Build chassis-side cable (8 wires from Haltech through firewall).
- [ ] **D1 engine sensor harness** — 12 wires from Haltech 26-pin/34-pin through firewall. Engine-side pigtails to cam, crank, knock, IAT, MAP, TPS.
- [ ] **D2 coil harness** — 6× IGN trigger wires + MP2 power + ground through firewall. Engine-side branches to 6× Toyota 90919-A2005 coil pigtails.
- [ ] **D3 injector harness** — 6× INJ signal wires + MP1 power through firewall. Engine-side branches to 6× new injector pigtails. Splice MP1 to both injector rail and Haltech pin 26 on chassis side.
- [ ] **LM2 cockpit cable** — Lime Green → AVI 8, Yellow → signal GND (short run, no firewall)

---

## PDM Wiring Summary — Physical Connections

### Engine Bay

| Load | PDM Output | Pin(s) | Notes |
|------|-----------|--------|-------|
| Starter | HP1 | B1 + B13 | Via solenoid; inductive; series diode |
| Fan | HB1 | G1 + G2 | PWM 100Hz; Half Bridge 35A; freewheeling diode |
| Fuel Pump | HP3 | B24 + B25 | Via fuse box pin 87; freewheeling diode |
| Injector Power / OE Relay | MP1 | B2 | **Phase 1:** OE relay box pin 87 (pull relay). **Phase 2:** → D3 pin 7 (injector rail + Haltech 34-pin pin 26) |
| Coil Power / OE Relay | MP2 | B3 | **Phase 1:** OE relay box pin 87 (same socket). **Phase 2:** → D2 pin 7 (Pin D all 6 COPs) |
| Horn | MP3 | B4 | **Phase 1:** Not connected (BCM controls). **Phase 2:** → horn direct or relay socket; Ch12 button |
| Headlights | MP6 | B7 | **Phase 1:** Not connected (BCM controls). **Phase 2:** → headlight direct or relay socket; Ch04 toggle |
| Alternator exciter | LP8 | B21 | D+ field wire cut and routed through LP8; SafeIgnition trigger; < 1A draw |

### Cockpit

| Load | PDM Output | Pin(s) | Notes |
|------|-----------|--------|-------|
| Brake Lights | MP4 | B5 | Always active (Ch09 trigger) |
| Tail Lights | MP5 | B6 | SafeIgnition (always on) |
| Coolsuit | MP7 | B8 | Ch10 AND SafeIgnition |
| Defogger | MP8 | B9 | Ch11 AND SafeIgnition |
| Fuel sender | — | — | OEM direct circuit, no PDM involvement |

### Accessories (SafeIgnition trigger)

| Load | PDM Output | Pin |
|------|-----------|-----|
| ECU Power | LP1 | B14 |
| Dash | LP2 | B15 |
| SmartyCam | LP3 | B16 |
| Spare (was GPS) | LP4 | B17 |
| Wideband | LP5 | B18 |
| Cluster | LP6 | B19 |
| Warning LED | LP7 | B20 |
| AltExciter | LP8 | B21 |

### CAN Buses

| Bus | PDM Pins | Device | Speed |
|-----|----------|--------|-------|
| CAN0 (AIM expansion) | B22 (H) / B11 (L) | Data Hub → GPS, SmartyCam, Podium | 1 Mbps |
| CAN1 (ECU) | B30 (H) / B31 (L) | Haltech Elite 2500 | 500 kbps |
| CAN2 | B28 (H) / B29 (L) | **Unused** — available for future CAN device | 125 kbps |

### Switch Panel Inputs

| Switch | PDM Input | Pin | Type |
|--------|----------|-----|------|
| Ignition | IGN input | G23 | Latching toggle, 12V |
| Start | Ch01 | G26 | Momentary, active = GND |
| Fan low | Ch02 | G27 | Latching toggle, 12V |
| Fan high | Ch03 | G28 | Latching toggle, 12V |
| Headlights | Ch04 | G29 | Latching toggle, 12V (Phase 2+) |
| Brake switch | Ch09 | G21 | Closed on press |
| Coolsuit | Ch10 | G22 | Latching toggle, 12V |
| Defogger | Ch11 | B26 | Latching toggle, 12V |
| Horn | Ch12 | B27 | Momentary, active = GND (Phase 2+) |

> **Wipers:** Ch05 (G30) / Ch06 (G31) reserved — wiper logic being developed separately.
> **Spare:** Ch07 (G32), Ch08 (G33)

---

## Haltech Wiring Summary — Sensor + Harness Connections

### Lowdoller Combo Sensors (5-wire each)

| AVI | Signal | Sensor PN | Wire → Pin | Calibration |
|-----|--------|-----------|-----------|-------------|
| AVI 1 | Fuel pressure | 899404 | Yellow → 26-pin pin 13 (GY/Y shld) | PSI = (V−0.5) × 37.5 |
| AVI 2 | Fuel temp | 899404 | Green → 34-pin pin 16 (O/B) | PTC custom table |
| AVI 3 | Oil pressure | 899404 | Yellow → 34-pin pin 17 (O/R) | PSI = (V−0.5) × 37.5 |
| AVI 4 | Oil temp | 899404 | Green → 34-pin pin 2 (O/Y) | PTC custom table |
| AVI 5 | Coolant pressure | LDM899TP100 | Yellow → 26-pin pin 20 (O/G) | PSI = (V−0.5) × 25.0 |
| AVI 6 | Coolant temp | LDM899TP100 | Green → 26-pin pin 12 (GY/O shld) | PTC custom table |
| AVI 7 | Brake pressure | 899405 | *Leave ready* | PSI = (V−0.5) × 375.0 |
| AVI 8 | Brake temp | 899405 | *Leave ready* | PTC custom table |
| AVI 9 | MAP | — | Yellow → 34-pin pin 15 (Y) | Per MAP spec |
| AVI 10 | TPS | OEM | → 34-pin pin 14 (W) | 0–5V |

**+5V supply:** All red wires → 34-pin pin 9 (O, 100mA)
**Signal GND:** All black + white wires → 26-pin pins 14/15/16 (B/W)

### Coil Harness (Toyota 90919-A2005 ×6)

| Coil | Haltech IGN | Pin | Wire Color |
|------|------------|-----|------------|
| Cyl 1 | IGN 1 | 34-pin pin 3 | Y/B |
| Cyl 2 | IGN 2 | 34-pin pin 4 | Y/R |
| Cyl 3 | IGN 3 | 34-pin pin 5 | Y/O |
| Cyl 4 | IGN 4 | 34-pin pin 6 | Y/G |
| Cyl 5 | IGN 5 | 34-pin pin 7 | Y/BR |
| Cyl 6 | IGN 6 | 34-pin pin 8 | Y/L |

Power: PDM MP2 (B3) → Pin D common bus
Ground: Pin A → engine block

### Injector Harness

| Injector | Haltech INJ | Pin | Wire Color |
|----------|------------|-----|------------|
| Cyl 1 | INJ 1 | 34-pin pin 19 | L |
| Cyl 2 | INJ 2 | 34-pin pin 20 | L/B |
| Cyl 3 | INJ 3 | 34-pin pin 21 | L/BR |
| Cyl 4 | INJ 4 | 34-pin pin 22 | L/R |
| Cyl 5 | INJ 5 | 34-pin pin 27 | L/O |
| Cyl 6 | INJ 6 | 34-pin pin 28 | L/Y |

Power: PDM MP1 (B2) → injector rail + Haltech 34-pin pin 26 (R/L)

### ECU Sensitive Bundle (Shielded)

| Signal | Haltech Pin | Wire |
|--------|------------|------|
| Crank trigger + | 26-pin pin 1 | Y (shielded) |
| Crank trigger − | 26-pin pin 5 | G (shielded) |
| Cam home + | 26-pin pin 2 | Y (shielded) |
| Cam home − | 26-pin pin 6 | G (shielded) |
| Knock 1 | 26-pin pin 21 | GY/G |
| Knock 2 | 26-pin pin 22 | GY/L |

---

## NEXT WEEKEND — Phase 2: Haltech Takes Over Engine

> **Full Phase 2 procedure:** `guides/pdm-build-guide.md` → "Phase 2 — PDM + Haltech ECU"

After track day with stock ECU + PDM, switch to Haltech running the engine. **No Race Studio config change needed.** Physical wiring only.

- [ ] Unplug stock ECU connectors (C133-1 through C133-4) — leave mounted, label for reversal
- [ ] Unplug BCM connector — leave mounted
- [ ] Pull MP1/MP2 spades from OE main relay pin 87 socket
- [ ] Reroute MP1 (B2) → D3 pin 7 (injector rail + Haltech 34-pin pin 26)
- [ ] Reroute MP2 (B3) → D2 pin 7 (COP coil Pin D common bus)
- [ ] Plug in D2 (coil Deutsch) — engine side already on coils
- [ ] Plug in D3 (injector Deutsch) — engine side already on injectors
- [ ] Add horn button → Ch12 (B27), wire MP3 (B4) → horn
- [ ] Add headlight toggle → Ch04 (G29), wire MP6 (B7) → headlights
- [ ] First fire on Haltech — base tune, confirm idle
- [ ] Verify all PDM tests still pass with Haltech running
- [ ] **Reversal test:** plug stock ECU + BCM back in, MP1/MP2 back to relay → car runs on stock

---

## LATER / ONGOING

> **Phase 3 (CAN keypad + OE removal):** `guides/pdm-build-guide.md` → "Phase 3"

- [ ] Rubber-mount ECU and PDM plate (vibration isolation)
- [ ] Clean and label all harnesses
- [ ] Harness routing: confirm no chafing on steering/suspension movement
- [ ] Configure PodiumConnect telemetry channels for race engineer
- [ ] Mount Lowdoller 1500 PSI brake sensor bracket (leave wires terminated, AVI 7+8 reserved)
- [ ] Crankcase pressure sensor (valve cover or PCV port → available PDM/Haltech input)
- [ ] IR tire temp sensor bracket + PDM channel input wiring
- [ ] Wiper integration — relay-less park design: MP9 (G4) low, MP10 (G5) high, LP9 (G3) park sweep. Ch05/Ch06 switches. Math channels pre-configured in RS3.
- [ ] CAN Keypad 12 installation (Phase 3 — see `guides/keypad-config-future.md`)
- [ ] Remove OE ECU, BCM, and relay box (Phase 3 — after proven reliability)
