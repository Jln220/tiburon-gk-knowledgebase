# LLM Navigation Guide — Tiburon GK Knowledgebase

This document tells an AI model how to navigate this knowledgebase effectively. Read it at the start of any session where you're unsure where to look.

---

## Directory Map

```
Knowledgebase/
├── LLM-GUIDE.md          ← you are here
├── ARCHITECTURE.md        ← authority tier system, trust ladder, design intent
├── ROADMAP.md             ← future plans (forum scraping, vector store, etc.)
│
├── builds/                ← BUILD-SPECIFIC: one subdirectory per car
│   ├── white-tiburon/     ← Haltech + PDM + Lemons race car — primary active build
│   │   ├── README.md      ← SESSION START for white car work ← load this first
│   │   ├── build-profile.json  ← machine-readable config (AVI pins, PDM map, etc.)
│   │   ├── signal-routing.md   ← end-to-end wire traces, verified vs planned
│   │   ├── weekend-tasks.md    ← phased build procedure with test gates
│   │   ├── guides/        ← PDM Race Studio config guides (white-car-specific)
│   │   └── ...
│   ├── blue-tiburon/      ← OEM ECU + GKFlasher test/race car
│   │   ├── README.md      ← SESSION START for blue car work
│   │   ├── build-profile.json  ← machine-readable config
│   │   └── build-profile.md   ← narrative build profile
│   └── template/          ← blank template for new builds
│
├── common/                ← PLATFORM: applies to all GK Tiburons
│   ├── chassis/           ← G6BA specs, Aisin ratios, dimensions, alignment
│   ├── electrical-manual/ ← ETM chapter indexes + schematics/
│   │   └── schematics/    ← SD.pdf extracted: 47 circuit section files
│   ├── opengk/            ← Community wiki: ECU pinouts, K-Line, SMARTRA, GKFlasher, CAN
│   ├── shop-manual/       ← Factory manual — ALL 18 chapters fully split
│   │   ├── engine-mechanical/              ← EMA (V6): 9 files
│   │   ├── engine-mechanical-i4/           ← EM (I4 1.6/2.0): specs + 2 parts
│   │   ├── fuel-system/                    ← FLA: 6 files
│   │   ├── engine-electrical/              ← EE: specs, ignition, charging, starting, cruise
│   │   ├── transaxle/                      ← TR: specs, automatic, manual (2 parts)
│   │   ├── brake-system/                   ← BR: specs, service, parking, ABS (2 parts)
│   │   ├── body-electrical/                ← BE: specs, ETACS (2 parts), horns, locks, mirrors (3 parts), windows
│   │   ├── body-control-module/            ← BCM: 3 parts (Hi-Scan diagnosis, function flowcharts)
│   │   ├── body-interior-and-exterior/     ← BD: 3 parts (exterior, interior, bumpers/seats)
│   │   ├── heating-ventilation-air-conditioning/ ← HA: specs, heater, A/C (2 parts)
│   │   ├── restraints/                     ← RT: specs, airbag (3 parts)
│   │   ├── general-information/            ← GI: general
│   │   ├── clutch-system/                  ← CH: specs + clutch
│   │   ├── driveshaft-and-axle/            ← DS: specs, driveshaft, rear-axle
│   │   ├── emission-control-system/        ← EC: general, crankcase, evaporative, exhaust
│   │   ├── steering-system/                ← ST: specs + mechanical power steering
│   │   ├── suspension-system/              ← SS: specs, front, rear
│   │   └── _archive/           ← Old monolithic OCR files (superseded)
│   ├── diagrams/          ← Mermaid component diagrams
│   ├── tiburon-knowledge-graph.json  ← platform-level component/signal graph
│   ├── knowledge-graph-schema.md     ← node and edge type definitions
│   └── electrical-manual/connector-master-reference.md ← **connector cross-reference**: code ↔ name ↔ all manual sections
│
├── hardware/              ← DEVICE REFERENCE: generic docs, not car-specific
│   ├── hardware-graph.json  ← Layer 2: device capability graph (reusable across builds)
│   ├── haltech/           ← Elite 2500 pinout sheets, wiring diagram
│   ├── aim/               ← All AIM Sports devices (grouping folder)
│   │   ├── aim-pdm/       ← PDM 32 pinout, configuration theory
│   │   ├── aim-datahub/   ← CAN Data Hub (2-way & 4-way) — passive bus splitter
│   │   ├── aim-gps08/     ← GPS-08 / GPS09c — CAN AiM GPS module
│   │   └── aim-smartycam/ ← SmartyCam 3 series — HD video overlay camera
│   └── sensors/           ← COP coil, Lowdoller sensor, OEM sensors
│
├── fasteners/             ← BOLT DATABASE: JSON index, bin labels, photos
├── forum/                 ← FORUM DATA: thread index, scraping methodology
├── extraction/            ← EXTRACTION GUIDES: start here for any content ingestion
│   ├── README.md          ← Extraction status + which guide to use
│   ├── pdf-extraction-guide.md  ← Shop manual / schematic / hardware datasheet SOP
│   └── forum-extraction-guide.md ← Forum thread + OpenGK ingestion pipeline
├── credibility/           ← SOURCE SCORING: source registry, contributor weights, forum section map
│   ├── sources.json       ← Base credibility per source (OpenGK 9, NewTiburon 3, etc.)
│   ├── contributors.json  ← Known expert weights (Charlie-III, chase206, etc.)
│   ├── forum-sections.json ← Forum section → KB topic mapping
│   └── scoring-algorithm.md ← Composite credibility formula + worked examples
└── validation/            ← KB TESTING: forum questions as test cases
    ├── test-cases.json    ← Questions with expected answer components
    ├── test-results.json  ← Run results and scores
    └── coverage-gaps.md   ← Gap analysis by system
```

---

## Session Start Ritual

**For white car (Haltech/PDM work):**
1. Read `builds/white-tiburon/README.md` — loads phase status, AVI assignments, PDM output map, confirmed facts
2. Read `builds/white-tiburon/build-profile.json` — machine-readable config
3. Read the specific file relevant to the question

**For blue car (OEM ECU / GKFlasher work):**
1. Read `builds/blue-tiburon/README.md` — loads ECU type, immo PIN, K-Line facts
2. Read relevant `common/opengk/` file for the specific system

**For platform questions (applies to all GK Tiburons):**
- Start in `common/opengk/` for electrical/ECU topics
- Start in `common/shop-manual/[chapter]/_index.md` for any shop manual topic — each chapter has an index listing section files
- Start in `common/electrical-manual/schematics/_index.md` for circuit diagrams — lists all 47 circuits with links
- Start in `common/electrical-manual/connector-master-reference.md` for **any connector/sensor/pinout question** — maps connector code ↔ component name ↔ all manual sections (HL, CC, SD, CL, FLA) ↔ knowledge graph node
- Start in `common/chassis/gk-chassis-specs.md` for dimensions/ratios

**Shop manual navigation:** All 18 chapters are fully split. Each directory contains:
- `_index.md` — section map with page ranges and links
- `specifications.md` — specs and torque tables (usually first)
- Section files named by topic (e.g., `cooling-system.md`, `timing-system.md`)
- Large sections split into `-part1.md`, `-part2.md`, etc.

---

## How the Knowledge Graphs Work

Two JSON graphs exist and complement each other:

### 1. Platform Graph — `common/tiburon-knowledge-graph.json`
Scope: GK chassis, G6BA engine, OEM components, factory manual chapters
- Nodes: `manual`, `section`, `component`, `part_number`, `torque_spec`, `connector`, `forum_post`
- Covers: shop manual chapter nodes, OEM sensors, standard values, interchangeable parts

### 2. Build Graph — `builds/white-tiburon/build-knowledge-graph.json`
Scope: White car hardware — Haltech, PDM, Lowdoller sensors, wiring
- Nodes: `ecu_pin`, `pdm_output`, `pdm_input`, `sensor_instance`, `device`
- Covers: all 23 Haltech connector pins, 17 PDM outputs, CAN buses, AVI assignments
- Contains `quick_lookup` tables for fast LLM access

**How they link:** Build graph nodes reference platform graph nodes via `platform_ref` fields.
Example: Build node `ckp_sensor_instance` → platform node `ckp_sensor` in `common/tiburon-knowledge-graph.json`.

**Querying:** Read the JSON directly. The `quick_lookup` section in the build graph has pre-computed tables for common queries (AVI by signal, PDM by output name, etc.).

---

## Authority Tiers (Trust Hierarchy)

| Tier | Source | Examples |
|---|---|---|
| T1 — Factory | Hyundai shop manual, ETM | Torque specs, wiring diagrams, part numbers |
| T2 — Community | OpenGK wiki | ECU pinouts, K-Line protocol, SMARTRA |
| T3 — Forum | Scraped threads (chase206, etc.) | Aftermarket fits, real-world experiences |
| T4 — Web | Parts sites, datasheets | Cross-vehicle fits, pricing |

When facts conflict, prefer lower tier numbers. Forum claims without corroboration are marked ⚠️.

**Within the same tier**, compare `credibility_score` values on knowledge graph nodes (higher is better). For forum-sourced claims, cross-reference `credibility/contributors.json` to identify priority contributors. See `credibility/scoring-algorithm.md` for the composite formula.

---

## Confidence Markers in Files

Used in `signal-routing.md` and other active-build files:
- ✅ — Verified by measurement or bench test
- ⚠️ — Forum/community reported, not personally verified
- 🔲 — Planned but not yet wired/tested

### Extraction Verification Markers

Used in the `V` column of spec/pinout tables to track OCR extraction accuracy:
- ⬜ — Unverified (raw OCR/AI extraction)
- ✅ — Verified (human confirmed against physical manual)
- ⚠️ — Suspect (known or likely OCR error)
- 🔧 — Corrected (was wrong, now fixed)

See `validation/spot-checks.json` for the verification queue and `validation/spot-check-batch-001.md` for the current checklist.

---

## Quick Spec Reference (Top 20)

The most commonly queried specs, pre-loaded here so an LLM can answer without opening another file.

| Spec | Value | Source File | Page | V |
|------|-------|-------------|------|---|
| Cylinder bore | 86.7 mm | shop-manual/engine-mechanical/specifications.md | EMA-2 | ⬜ |
| Stroke | 75 mm | shop-manual/engine-mechanical/specifications.md | EMA-2 | ⬜ |
| Compression ratio | 10:1 | shop-manual/engine-mechanical/specifications.md | EMA-2 | ⬜ |
| Displacement | 2,656 cc | shop-manual/engine-mechanical/specifications.md | EMA-2 | ⬜ |
| Firing order | 1-2-3-4-5-6 | shop-manual/engine-mechanical/specifications.md | EMA-2 | ⬜ |
| Final drive ratio | 4.050:1 | chassis/gk-chassis-specs.md | — | ✅ |
| Coolant capacity | 7.0 L | shop-manual/engine-mechanical/specifications.md | EMA-4 | ⬜ |
| Oil pressure (min) | 50 kPa at 75-90°C | shop-manual/engine-mechanical/specifications.md | EMA-4 | ⬜ |
| Thermostat opens | 82±2°C | shop-manual/engine-mechanical/specifications.md | EMA-4 | ⬜ |
| Spark plug | NGK BKR5ES-11 | shop-manual/fuel-system/specifications.md | FLA-2 | ⬜ |
| Cylinder head bolt | 25+(58-62°)+(43-47°) Nm | shop-manual/engine-mechanical/specifications.md | EMA-5 | ✅ |
| Cam sprocket bolt | 90-110 Nm | shop-manual/engine-mechanical/specifications.md | EMA-5 | ✅ |
| CKP signal wire | Yellow (Y), 0.5mm | schematics/mfi-control-v6.md | SD-78 | ✅ |
| CMP signal wire | Black (B), 0.5mm | schematics/mfi-control-v6.md | SD-78 | ✅ |
| CKP → ECM pin | C133-3 pin 8 | opengk/ecm-pinouts.md | — | ⬜ |
| CMP → ECM pin | C133-4 pin 6 | opengk/ecm-pinouts.md | — | ⬜ |
| TPS signal wire | Blue (L), 0.5mm | schematics/mfi-control-v6.md | SD-78 | 🔧 |
| MAF → ECM pin | C133-3 pin 1 | opengk/ecm-pinouts.md | — | ⬜ |
| CKP sensor type | Hall effect | shop-manual/fuel-system/specifications.md | FLA-2 | ⬜ |
| Coolant sensor type | NTC thermistor | opengk/sensor-information.md | — | ⬜ |

---

## Common Queries and Where to Look

| Question | File(s) |
|---|---|
| What pin is AVI 3 on? | `builds/white-tiburon/build-profile.json` → ecu.avi_assignments.AVI3 |
| How does the fuel pump trigger? | `builds/white-tiburon/guides/pdm-config.md` → HP3 section |
| What's the PDM connector A pin for the fan? | `hardware/aim/aim-pdm/pdm-pinout.md` |
| How do I configure fan PWM in Race Studio? | `builds/white-tiburon/guides/pdm-session-1.md` → Step 6, HP2 |
| What wire color is CAN H on the Haltech? | `hardware/haltech/main-connector-26-pin-elite2500.md` → pin 23 |
| What is the OEM coolant temp sensor resistance? | `common/opengk/sensor-information.md` |
| What torque for cam cap bolts? | `common/shop-manual/engine-mechanical/specifications.md` or `main-moving-system.md` |
| How does SMARTRA immo bypass work? | `common/opengk/smartra.md` + `common/opengk/gkflasher.md` |
| Where is BCM-IM pin 19? | `common/opengk/body-control-module.md` |
| What's the Aisin AY6 final drive ratio? | `common/chassis/gk-chassis-specs.md` |
| How does the GPS-08 connect to the PDM? | `hardware/aim/aim-gps08/aim-gps08.md` + `hardware/aim/aim-datahub/aim-datahub.md` |
| What CAN bus are the GPS / SmartyCam on? | CAN AiM (PDM A22/A11, 1 Mbps) via 4-way Data Hub — `hardware/aim/aim-datahub/aim-datahub.md` |
| How do I set up SmartyCam in Race Studio? | `hardware/aim/aim-smartycam/aim-smartycam.md` — two sessions: PDM SmartyCam Stream tab + SmartyCam USB-C/SD config |
| Does GPS-08 need RS3 configuration? | No — auto-broadcasts when powered; channels appear in Channels tab automatically |
| What wire goes to ECM pin C133-4-6? | `common/electrical-manual/schematics/mfi-control-v6.md` (ECM pin table) |
| What are the pinouts on the crank sensor? | `common/electrical-manual/connector-master-reference.md` → C113 row → links to FLA-57, SD-78, CC-17 |
| How many pins does connector C114 have? | `common/electrical-manual/connector-master-reference.md` → Pin Count Validation table |
| What connector code is the TPS? | `common/electrical-manual/connector-master-reference.md` → C112 (Cross-Reference table at bottom) |
| What harness is the MAF sensor on? | `common/electrical-manual/connector-master-reference.md` → C125 → Control Harness (4), HL-15 |
| Where is the CKP sensor physically? | `common/electrical-manual/connector-master-reference.md` → C113 → CL-22 |
| Where are the ground points? | `common/electrical-manual/schematics/ground-distribution.md` |
| How credible is this forum post? | `credibility/scoring-algorithm.md` + check node's `credibility_score` |
| Who are the trusted forum contributors? | `credibility/contributors.json` → priority_contributor = true |
| What KB coverage gaps exist? | `validation/coverage-gaps.md` |
| What fuse feeds the headlamps? | `common/electrical-manual/schematics/fuse-relay-info.md` or `power-distribution.md` |
| Starter circuit wiring? | `common/electrical-manual/schematics/starting-system.md` |
| OBD2 / K-Line / CAN data link? | `common/electrical-manual/schematics/data-link.md` |

---

## What's NOT in This Knowledgebase Yet

- Forum thread data (7 threads indexed, 0 scraped — see `extraction/forum-extraction-guide.md`)
- Bolt photos (database schema ready, `fasteners/bolts/` is empty)
- Blue car knowledge graph JSON (build-profile.json exists, graph pending)
- Visual diagrams beyond fuel pump + cam sensor
- Hardware PDFs (AIM PDM32 user guide, GPS-08 pinout, SmartyCam, Data Hub — see `extraction/README.md`)

**For extraction work:** Start at `extraction/README.md` — it has status tables and links to the correct SOP for each source type.

## Extraction Statistics (Phase 1 Complete)

- **Shop manual:** 18 chapter directories, ~90 section files, ~40,000+ lines
- **SD schematics:** 47 circuit section files, ~11,700 lines
- **Source PDFs:** Scanned (image-only) versions in `Tiburon-Shop-Manual/` and `Electrical Troubleshooting Manual/`
- **Extraction tool:** `scripts/extract-pdf.py` (pymupdf, 150 DPI, Claude vision agents)
- **Old monolithic files:** Archived in `common/shop-manual/_archive/`
