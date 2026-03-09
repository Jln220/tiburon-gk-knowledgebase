# PDM Bench Test & Car Connection Guide — White Tiburon

**Scope:** Everything from first PDM power-up through Phase 1 car tests (PDM + stock ECU).
**Today's sequence:** Race Studio config → fuel pump bench → PDM to fuse box → alternator exciter / kill switch → starter.

> For Race Studio step-by-step config: `guides/pdm-session-1.md`
> For control scheme overview (status variables, keypad map): `guides/pdm-config.md`

---

## Equipment Needed

| Item | Notes |
|---|---|
| Laptop with Race Studio 3 | USB Binder cable to PDM |
| 12V bench supply or car battery | PDM draws ~0.5A idle; fuel pump ~8A peak |
| PDM + CAN keypad | Already connected on CAN2 |
| Fuel pump (external, bench) | Wago or spade to HP3 (A24+A25) |
| Multimeter | Current clamp preferred for pump draw |
| Fused jumper wires | For fuse box tap connections |

---

## Section 1 — Race Studio Config from Scratch

> **Do this section before powering the PDM for the first time as the Tiburon config.**
> Full procedure: `guides/pdm-session-1.md`

### Quick-start order
1. Open `Webinar complete.zconfig` in Race Studio 3
2. **File → Save As** → `Tiburon_White_v1.zconfig` immediately
3. Work through `pdm-session-1.md` Sections 2–8 in order:
   - Step 2: CAN1 Haltech stream (do this first — all CAN-based status variables need it)
   - Step 3: CAN2 keypad button remap
   - Step 4: Channel inputs (Ch09 = START_BACKUP, Ch11 = BRAKE_SWITCH)
   - Step 5: Add math channels / status variables
   - Step 6: Power output renames and trigger assignments
   - Step 7: Keypad LED colors
   - Step 8: Haltech pit limiter CAN output
4. **Transmit configuration to PDM** (USB)
5. **Save backup** → copy `Tiburon_White_v1.zconfig` to `AIM PDM/` on this machine

### Minimum viable config for today's bench tests
If short on time, only Steps 2–6 are needed to run fuel pump and starter tests. LED colors (Step 7) and pit limiter CAN output (Step 8) can wait.

---

## Section 2 — PDM Bench Power-Up

### Setup
- Connect PDM Surlok (+) → 12V supply or car battery
- Connect PDM ground → chassis/battery ground
- Connect USB → Race Studio 3 laptop
- Connect CAN keypad (CAN2)
- Leave all outputs disconnected

### Power-up
1. Flip IGN toggle → PDM Conn B pin 23 to 12V
2. Race Studio Live Data → confirm `SafeIgnition` = 1
3. Confirm LP1–LP6 show active in Outputs view (no loads connected yet — OK)
4. Confirm keypad LEDs illuminate with correct base colors
5. Walk through all 10 keys per the table in `guides/pdm-config.md` → watch status vars change in Live Data

**Expected at this point:** All keypad buttons trigger correct variables; no fault codes; `SafeIgnition` = 1 when IGN on.

---

## Section 3 — Fuel Pump Bench Test

### Wiring for bench test
```
PDM HP3 outputs:
  A24 ─────┬────── Pump positive (+)
  A25 ─────┘

  Battery GND ─── Pump negative (−)
```
- Both A24 and A25 carry HP3 — connect both to pump positive for full current capacity
- Use 14 AWG minimum for bench test wires

### Test sequence

**3a. Prime cycle**
1. IGN off → IGN on
2. HP3 should activate for exactly **3 seconds** then cut
3. Verify in Race Studio: `FUEL_PRIME` timer fires and `FuelSV` → active → inactive
4. If pump doesn't prime: check `SafeIgnition` = 1 and `FUEL_PRIME` timer rising edge logic in math channels

**3b. Override run**
1. IGN on, engine not running (`ENGINE_RUNNING` = 0)
2. Press Key 06 (Fuel Override) → `FuelOverride` = 1
3. HP3 should activate and stay on
4. Release Key 06 → HP3 should stop (prime delay already expired)
5. Verify HP3 status shows correct duty/active in Outputs view

**3c. Current measurement**
1. With pump running (Key 06 override), measure current draw on HP3 output
2. Expected range: 5–10A continuous (typical EFI pump)
3. If > 15A: check pump for binding or short; HP3 OVC protection will cut at 15A after retry
4. Record peak draw — needed for wiring gauge confirmation

**3d. Voltage at pump**
1. Measure pump + to − while running
2. Should be within 0.5V of supply voltage (< 0.5V drop across HP3 and wiring)
3. > 1V drop = check connection quality or wire gauge

---

## Section 4 — PDM to Car via Fuse Box (Non-Destructive)

> The stock ECU remains fully connected. PDM outputs shadow or replace specific circuits by inserting spade connectors into relay socket pin 87 positions. No cutting, no splicing into stock wiring.

### Which relays to tap

The OEM fuse/relay box in the engine bay has relay sockets with accessible pin 87 positions. Pin 87 is the NO (normally open) contact — the output side.

| PDM Output | What it powers | Fuse box approach |
|---|---|---|
| **HP3 — Fuel Pump** | Fuel pump | Remove fuel pump relay; insert PDM HP3 wire into pin 87. PDM now solely controls pump power. Stock ECU fuel pump relay **must be removed** to prevent both driving the pump. |
| **MP6 — Alt Exciter** | Alternator D+ exciter | Find the thin alternator exciter wire at fuse box (usually on IG1 relay output or a dedicated fuse). Tap here. |
| **LP1–LP6 — Accessories** | ECU, dash, etc. | Add PDM power alongside stock feeds — PDM supplies in parallel. Low risk since these are just 12V supply. |

> **Critical for fuel pump:** The stock fuel pump relay and the PDM cannot both drive HP3 simultaneously. **Remove the OEM fuel pump relay before connecting PDM HP3 to the fuse box 87 terminal.** This is non-destructive — just pull the relay.

### Procedure

**Step 1: Locate relay positions**
- Fuel pump relay: typically labeled FP or FUEL PUMP in the underhood fuse box
- Alternator relay: labeled ALT, IG1, or MAIN depending on trim
- Refer to `common/electrical-manual/schematic-diagrams.md` → SD-78 (MFI Control System) for fuse box layout

**Step 2: Fuel pump tap**
1. Pull the OEM fuel pump relay
2. Identify pin 87 in the relay socket (power out to pump)
3. Insert male spade connector from PDM HP3 (A24+A25) into pin 87 socket
4. Leave pins 30, 85, 86 untouched (relay coil control — stock ECU still commands it, PDM output just bypasses it)

**Step 3: Verify before starting engine**
1. IGN on → PDM `SafeIgnition` = 1
2. Prime fires → you should hear the fuel pump run 3 seconds
3. Key 06 Fuel Override → pump runs continuously
4. Engine won't start yet with relay pulled (until Phase 1.6 starter test) — OK for now

**Step 4: Alternator exciter tap** (see Section 5 below)

**Step 5: Accessory outputs (LP1–LP6)**
- These can be run in parallel with stock feeds initially — risk is low
- Final state in Phase 3: stock ECU power moved fully to LP1

---

## Section 5 — Alternator Exciter + Kill Switch Test

### Background
The OEM alternator exciter wire provides a small 12V signal to the alternator's D+ (field) terminal to initiate charging. When this wire is cut from the IGN circuit and routed through PDM MP6, the PDM controls when the alternator field is energized — and the kill switch (which kills PDM power) will cut charging immediately.

### Finding the exciter wire
- The alternator D+ terminal is a thin wire (~18 AWG), separate from the main B+ output
- On the GK V6, it typically routes from the CHARGE or ALT fuse → alternator D+ terminal
- At the alternator body: look for the small Yazaki connector (3 or 4 pin) alongside the main battery cable lug
  - One wire in this connector is D+ (exciter) — usually carries ~12V with IGN on, ~0V with IGN off
  - Confirm with multimeter: IGN on = 12V, IGN off = 0V → that's the exciter
- Reference: `common/shop-manual/engine-electrical.md` (grep "alternator" or "charging") for wiring diagram

### Routing through PDM MP6
1. Cut the exciter wire at a convenient point near the fuse box (leave enough length on both ends)
2. Fuse box side → wire to PDM MP6 (A7)
3. Alternator D+ side → leave as the "load" side (already connected to alternator)
4. Configure MP6 in Race Studio: `SafeIgnition`, continuous DC, 5A max, OVC protected

> **Bench test first:** Before cutting in car, bench-test by connecting a 12V indicator lamp or resistor to MP6 and verifying it activates/deactivates with IGN toggle.

### Test sequence in car

**5a. Charging test**
1. IGN on → engine running (on stock ECU)
2. MP6 active → alternator should charge
3. Measure battery voltage: expect **13.8–14.4V** at battery posts while running
4. If < 13.5V: check D+ connection and that field terminal is correct

**5b. Kill switch cuts charging**
1. Engine running, charging confirmed (14V)
2. Flip OMP kill switch → this cuts power to PDM (kills PDM B+ or IGN supply)
3. `SafeIgnition` drops → MP6 off → alternator D+ de-energized
4. Battery voltage should drop back toward resting (~12.6V) immediately
5. Engine should also stop (stock ECU loses power through kill switch circuit)

> ⚠️ **If kill switch doesn't cut the stock ECU:** Check kill switch wiring. The OMP kill switch must be in the main battery/chassis circuit, not just the PDM circuit. The goal is that kill switch kills everything — PDM, ECU, ignition, fuel.

---

## Section 6 — Starter Test

> **Prerequisite:** `STARTER_SAFE` logic in Race Studio must be configured before this test.
> `STARTER_SAFE` = (StarterKYD OR START_BACKUP) AND SafeIgnition AND NOT ENGINE_RUNNING

### Method A — Through Fuse Box (Try First)

The OEM starter relay in the fuse box has a pin 87 output that goes to the starter solenoid S-terminal. Tapping here lets the PDM energize the solenoid through the existing relay wiring without cutting anything.

1. Locate the starter relay in the underhood fuse box (labeled START or ST)
2. The OEM ignition switch feeds pin 86 (relay coil) via the IGN switch circuit
3. **Option A1 — Parallel:** Insert PDM HP1 wire (A1+A13) into pin 87 alongside the existing OEM wire
   - PDM and stock ignition switch can both trigger the solenoid independently
   - Safe for Phase 1 since stock ECU still runs
4. **Option A2 — Replace:** Remove stock starter relay; wire HP1 directly to pin 87 socket
   - PDM is sole starter trigger; stock IGN switch no longer cranks
   - Use this approach if Option A1 causes feed-through issues

**Test:**
1. IGN on, engine not running (RPM = 0 → `ENGINE_RUNNING` = 0)
2. Press Key 01 (Start) on keypad → should hear starter engage
3. Or press physical backup button (Ch09)
4. While engine running: press Key 01 → should NOT engage (RPM interlock)
5. Measure HP1 current during crank: expect 15–25A inrush spike then drop

### Method B — Direct to Solenoid (If Fuse Box Doesn't Work)

If the fuse box tap has too much resistance or the solenoid doesn't respond:

1. Run a new wire from PDM HP1 (A1+A13) directly to the starter solenoid S-terminal (small stud, not the main battery cable)
2. This wire carries 12V when HP1 is active — solenoid sees direct PDM output
3. Leave the original OEM starter relay circuit intact as backup
4. **Important:** HP1 has an internal series diode to prevent back-EMF — no additional protection needed

**Wiring at solenoid:**
```
PDM HP1 (A1+A13) ────────── Solenoid S terminal (small lug)
                             (OEM start wire also connects here — OK in parallel)
```

---

## Section 7 — Phase 1 Test Gate Summary

After completing Sections 3–6, verify:

| Test | Expected | Pass? |
|---|---|---|
| Fuel prime (3s) | HP3 on 3s after IGN on | |
| Fuel override | Key 06 runs pump | |
| Pump current | 5–10A continuous | |
| Alternator charging | 13.8–14.4V while running | |
| Kill switch cuts charging | Voltage drops on kill | |
| Kill switch kills engine | Engine stops on kill | |
| Starter via Key 01 | Cranks when `ENGINE_RUNNING` = 0 | |
| Starter interlock | Does NOT crank while running | |
| Backup starter (Ch09) | Same behavior as Key 01 | |

---

## Notes & Issues Log

*(Update this section as tests are completed)*

| Date | Test | Result | Notes |
|---|---|---|---|
| | Race Studio config | | |
| | Fuel pump bench | | |
| | Fuse box tap — fuel | | |
| | Alt exciter wire found | | |
| | Kill switch cuts alt | | |
| | Starter — fuse box | | |
