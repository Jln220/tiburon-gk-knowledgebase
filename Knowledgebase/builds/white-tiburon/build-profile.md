# White Tiburon — Primary Race Car
## 2003 Hyundai Tiburon GK | 24 Hours of Lemons

**Role:** Primary race car — all best equipment goes here
**Engine:** 2.7L V6 Delta (G6BA)

---

## Engine & Drivetrain

### Engine (Current)
- 2.7L V6 Delta (G6BA)
- Unknown-brand headers (better quality than blue car's ECCPP, same unequal-length layout)
  - **Known issue:** gnarly bend on rear bank — want to correct eventually
- *(Eventually receiving the best built engine — see `/Knowledgebase/cars/engine-builds.md`)*

### Exhaust
- Unknown-brand headers (non-equal-length)
- Rear bank header has problematic bend — future correction needed

### Transmission & Clutch
- **6-speed Aisin** manual transmission (stock, current)
- *(Eventually receiving best built 6-speed Aisin with Quaife LSD — see engine builds doc)*
- Aluminum short shifter
- Torque Solutions shifter bushings (shared mod with blue car)

### Fuel System
- **Radium fuel pressure regulator/damper** (ready to install)
- **6AN PTFE hoses** to replace soft fuel lines (ready to install)

### ECU & Electronics
- **Haltech Elite 2500** ECU — currently being installed
  - 26-pin main connector (see `/Knowledgebase/haltech/main-connector-26-pin-elite2500.md`)
  - 34-pin main connector (see `/Knowledgebase/haltech/main-connector-34-pin-elite2500.md`)
  - Wiring diagram: `/Knowledgebase/haltech/elite-2500-wiring-diagram---rev-6.md`
  - **REM harness** available (no REM unit) — repurposing harness for this build
  - REM harness diagram: `/Knowledgebase/haltech/rem-harness-diagram.md`
- **Coil-on-plug (COP) confirmed** — Toyota 90919-A2005 ×6, sequential, IGN1–6 all active. See `cars/cop-ignition.md`.
- **No wheel speed sensors** — TC and ABS are not possible. Launch control not configured.

### Sensors (Planned/In Progress)
Full specs, wiring, and calibration tables: `Knowledgebase/cars/lowdoller-sensors.md`

- **Lowdoller Motorsports combo pressure/temp sensors:**
  - **Fuel:** PN 899404 (150 PSI / 500°F, 1/8" NPT) — on return line via line tap w/ hose barbs
  - **Oil:** PN 899404 (150 PSI / 500°F, 1/8" NPT) — direct mount to engine
  - **Coolant:** LDM899TP100 (100 PSI / 500°F, M12x1.5 w/ sealing ring) — confirm thread fits manifold
  - **Transmission:** PN 899404 (150 PSI / 500°F, 1/8" NPT) — maybe, depends on AVI channel availability
- **Brake:** PN 899405 (1500 PSI / 500°F, 1/8" NPT) — later, fittings to Jak
- All sensors output 0.5–4.5V pressure + PTC resistive temp (5-wire: red/black/yellow/white/green)
- Each sensor uses 2 Haltech AVI channels (pressure + temp)
- **5V supply:** Haltech 34-pin pin 9 (O, orange) = +5V DC, 100mA — already tested and configured in NSP

---

## Electrical

### AIM PDM 32
- **AIM PDM 32** — currently being installed
- **AIM 10" dash** — being installed alongside PDM
- PDM came with its own harness (currently being labeled)
- Pinout: `/Knowledgebase/aim-pdm/pdm-pinout.md`

### Power & Grounding

**Kill switch:** 4-pole OMP kill switch, left of steering wheel.
- **Large poles:** 2 AWG battery cable → kill switch → 150A breaker → starter B+ / alternator B+ AND 4 AWG → 120A breaker → PDM Surlok (+)
- **Small poles:** Jumpered from battery side large terminal. Output side → IGN toggle switch → PDM Conn B pin 23 (IGN input) + Haltech 34-pin pin 13 (ECU IGN enable)
- Kill switch OFF = all 4 poles open = everything dies instantly (PDM, ECU, alternator field, starter)

**PDM Surlok:** 4 AWG from kill switch large terminal B → 120A breaker → PDM Surlok (+). PDM ground lugs (B13, B14, B18) to chassis.

**Alternator exciter:** OEM D+ field wire cut and routed through PDM LP8 (A21). SafeIgnition trigger — kill switch drops field immediately.

### Mounting
- PDM, Haltech Elite 2500, Podium Micro (SN: 1QTV5KM), Innovate LM2 all mounted on a plate in the **passenger footwell**
- Short wire runs to dash (LVDS), switch panel, CAN buses
- Engine bay harness exits through firewall grommet

### Ignition & Switches
- **Physical switch panel** with 6 latching toggles + 1 momentary starter + warning LED
- **Ignition switch:** Dedicated latching toggle — goes to PDM Conn B pin 23 (Ignition input) AND Haltech 34-pin pin 13 (ECU IGN enable). Turns engine off without cutting PDM/battery power.
- **Start switch:** Momentary push button — PDM Ch09 (B21). Gated by ignition and RPM interlock.
- **Fan override:** Latching toggle — PDM Ch01 (B26). Forces fan to 98% duty.
- **Wiper Low:** Latching toggle — PDM Ch02 (B27). Wiper motor low speed.
- **Wiper High:** Latching toggle — PDM Ch03 (B28). Wiper motor high speed (overrides low).
- **Coolsuit:** Latching toggle — PDM Ch04 (B29). Coolsuit pump on/off.
- **Defogger:** Latching toggle — PDM Ch05 (B30). Rear window defogger.
- **CAN keypad excluded** from this build — all controls are physical switches.
- OEM ignition cylinder **removed** from loop.

---

## Suspension, Steering & Chassis

### Front Suspension
- **Custom tubular control arms** (in development)
  - Build thread: https://www.newtiburon.com/threads/big-strong-arms-front-lower-control-arms-for-the-lemons-tiburons.484870/
  - Use heim joints at knuckle end
  - **KNOWN ISSUE: heim pin fitment** — cannot find heim pins that fit the Tiburon knuckle; had to ream current pins. Tried Pinto pins and several other vehicles, none fit. Finding correct pins is a future project.
  - Will eventually use heim joints for tie rod ends as well
- **ARP studs** (strut-to-knuckle)

### Rear Suspension
- **Ingalls Engineering adjustable rear control arms**
- **SuperPro bushings** in rear trailing arms (shared mod with blue car)

### Strut Bars
- **Front strut bar** installed (blue car does not have)
- **Rear strut bar** installed (blue car does not have)

### Wheels & Tires
- **Enkei RPF01** 17x7 wheels
- **No wheel spacers** (unlike blue car's 25mm spacers)
- *(Tire size/brand TBD)*

### Steering
- **Sparco detachable steering wheel** (quick release)

---

## Interior & Safety

### Seating
- **Sparco Sprint L** seat (currently installed — non-containment)
  - **KNOWN ISSUE:** Floor has NOT been dropped (unlike blue car); seat height relative to cage remains unresolved
  - **Goal:** Replace with full containment seat once floor is modified

### Fire Suppression
- **Lifeline 2020** fire suppression system
- New bottle purchased **September 2025**

### Safety Equipment
- *(Harness details TBD)*
- *(Seat back brace TBD — depends on seat upgrade)*

---

## Maintenance Log

### Service History
| Date | Work Performed | Notes |
|------|---------------|-------|
| In progress | Haltech Elite 2500 install | Bench testing underway — cam/crank confirmed, knock next |
| In progress | AIM PDM 32 + 10" dash install | PDM on spade connectors in fuse box (pin 87) for bench logic testing |
| Planned | Radium FPR + 6AN PTFE fuel lines | Parts ready |
| Planned | Lowdoller combo temp/pressure sensors | Fuel, coolant, oil, possibly trans |
| Confirmed | Coil-on-plug conversion | Toyota 90919-A2005 ×6 — see `cars/cop-ignition.md` |

---

## Known Issues & Ongoing Work
- **Seat height relative to cage** — NOT YET RESOLVED (needs floor drop like blue car, then full containment seat)
- **Heim pin fitment for custom control arms** — no off-the-shelf pin fits Tiburon knuckle; current pins reamed to fit; need to find/make correct size
- **Rear bank header bend** — problematic bend, want to straighten or replace eventually
- **REM-less Haltech build** — repurposing REM harness without the REM unit
- **Haltech/PDM/Dash integration** — bench testing phase: cam/crank signals verified, knock sensor next; PDM connected via fuse box spade connectors for logic testing alongside stock ECU

---

## Notes
This car receives the best equipment. The blue car serves as the test platform before modifications go to the white car. Both cars share: Torque Solutions shifter bushings, SuperPro rear trailing arm bushings.
