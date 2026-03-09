# Blue Tiburon — Session Start

**2003 Hyundai Tiburon GK | G6BA 2.7L V6 | Stock Siemens SIMK43 ECU | Test/Race Car**

> **LLM: Load this file first, then ask your question.**
> This car uses the stock OEM ECU tuned via GKFlasher. No aftermarket ECU or PDM.

---

## Role & Status

The blue car is the **lower-tech test mule** — simpler wiring, stock ECU, used for:
- Testing mods before implementing on the white car
- 24 Hours of Lemons backup car / primary race car
- GKFlasher tuning experimentation (SIMK43)

---

## Key Facts

| Detail | Value |
|---|---|
| ECU | Siemens SIMK43 (5WY15 or 5WY17/18/1F — verify from ECU label) |
| ECU address (K-Line) | 0x11; diagnostic device 0xF1; 10400 baud; Fast Init |
| Ignition | Wasted spark — 3 OEM coil packs (NOT COP) |
| Injectors | Kefico 9260930004, 194cc @ 45 psi, 14.2 Ω |
| Transmission | 6-speed Aisin AY6, final drive 4.050:1 |
| PDM | None — OEM fuse/relay box |
| Immo default PIN | **2345** (4-digit, NOT the 6-digit DPN) |
| SMARTRA neutralize | GKFlasher routines 0x25 (prereq) then 0x26 (param 0x01) |
| DPN derivation | Last 6 VIN chars → github.com/Dante383/smartra-vin-to-pin |
| LSD | Phantom Grip (block-style) |

---

## Files

| File | What It Covers |
|---|---|
| `README.md` ← *you are here* | Quick reference, key facts, links |
| `build-profile.md` | Full narrative build profile: engine, suspension, electrical, history |
| `build-profile.json` | Machine-readable config (ECU type, ignition, sensors) |

---

## Platform Knowledge (Common to All GK Tiburons)

Most blue car work involves OEM systems — reference these:

| Need | File |
|---|---|
| OEM ECU identification (5WY label reading) | `common/opengk/ecm-identification.md` |
| OEM ECU pinouts (5WY 2 / 5WY 5) | `common/opengk/ecm-pinouts.md` |
| GKFlasher CLI reference | `common/opengk/gkflasher.md` |
| K-Line protocol (diagnostic comms) | `common/opengk/k-line.md` |
| SMARTRA / immobiliser | `common/opengk/smartra.md`, `immobiliser.md` |
| CAN bus messages (DME1–5, ASC1–2) | `common/opengk/can-bus-messages.md` |
| BCM pinouts (BCM-AI, BCM-IM, BCM-JM…) | `common/opengk/body-control-module.md` |
| SIMK43 tuning maps | `common/opengk/map-definitions.md` |
| Fuel injector specs | `common/opengk/fuel-injectors.md` |
| Sensor part numbers (CKP, CMP, MAF, TPS) | `common/opengk/sensor-information.md` |
| Chassis specs, gear ratios | `common/chassis/gk-chassis-specs.md` |
| Shop manual (factory OCR) | `common/shop-manual/` |
| ETM (electrical manual index) | `common/electrical-manual/index.md` |

---

## Deleted Systems (Blue Car Specific)

- AC system deleted
- EVAP/charcoal canister deleted
- OEM ignition switch deleted → **start button** replaces it
- OMP 6-pole kill switch installed
- Battery relocated to rear right

## Suspension & Chassis Notes

- KSport Kontrol Pro coilovers (7.5 kg/mm front, 4 kg/mm rear)
- Moog OE control arms + SuperPro SPF3133K-SPRO bushings (front)
- Strut-to-knuckle bolts: Belmetric BFD14X1.5X70YLW + Nord-Lock WNORD14 washers
- SuperPro rear trailing arm bushings
- 25mm wheel spacers (OEM 17×7, 215/45/17)
