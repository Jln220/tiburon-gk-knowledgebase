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
│   │   ├── pdm/           ← PDM Race Studio config guides (white-car-specific)
│   │   └── ...
│   ├── blue-tiburon/      ← OEM ECU + GKFlasher test/race car
│   │   ├── README.md      ← SESSION START for blue car work
│   │   ├── build-profile.json  ← machine-readable config
│   │   └── build-profile.md   ← narrative build profile
│   └── template/          ← blank template for new builds
│
├── common/                ← PLATFORM: applies to all GK Tiburons
│   ├── chassis/           ← G6BA specs, Aisin ratios, dimensions, alignment
│   ├── electrical-manual/ ← ETM chapter indexes (GI, CC, CL, HL, SD) → points to PDFs
│   ├── opengk/            ← Community wiki: ECU pinouts, K-Line, SMARTRA, GKFlasher, CAN
│   ├── shop-manual/       ← Factory manual OCR (searchable; EMA, EE, FLA, TR, etc.)
│   ├── diagrams/          ← Mermaid component diagrams
│   ├── tiburon-knowledge-graph.json  ← platform-level component/signal graph
│   └── knowledge-graph-schema.md     ← node and edge type definitions
│
├── hardware/              ← DEVICE REFERENCE: generic docs, not car-specific
│   ├── haltech/           ← Elite 2500 pinout sheets, wiring diagram
│   ├── aim-pdm/           ← PDM 32 pinout, configuration theory
│   └── sensors/           ← COP coil, Lowdoller sensor, OEM sensors
│
├── fasteners/             ← BOLT DATABASE: JSON index, bin labels, photos
└── forum/                 ← FORUM DATA: (scraper planned; chase206 seeded)
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
- Start in `common/shop-manual/` for mechanical procedures (grep-searchable OCR)
- Start in `common/chassis/gk-chassis-specs.md` for dimensions/ratios

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

---

## Confidence Markers in Files

Used in `signal-routing.md` and other active-build files:
- ✅ — Verified by measurement or bench test
- ⚠️ — Forum/community reported, not personally verified
- 🔲 — Planned but not yet wired/tested

---

## Common Queries and Where to Look

| Question | File(s) |
|---|---|
| What pin is AVI 3 on? | `builds/white-tiburon/build-profile.json` → ecu.avi_assignments.AVI3 |
| How does the fuel pump trigger? | `builds/white-tiburon/pdm/config-guide.md` → HP3 section |
| What's the PDM connector A pin for the fan? | `hardware/aim-pdm/pdm-pinout.md` |
| How do I configure fan PWM in Race Studio? | `builds/white-tiburon/pdm/session-1.md` → Step 6, HP2 |
| What wire color is CAN H on the Haltech? | `hardware/haltech/main-connector-26-pin-elite2500.md` → pin 23 |
| What is the OEM coolant temp sensor resistance? | `common/opengk/sensor-information.md` |
| What torque for cam cap bolts? | `common/shop-manual/engine-mechanical.md` (grep "cam cap" or "camshaft cap") |
| How does SMARTRA immo bypass work? | `common/opengk/smartra.md` + `common/opengk/gkflasher.md` |
| Where is BCM-IM pin 19? | `common/opengk/body-control-module.md` |
| What's the Aisin AY6 final drive ratio? | `common/chassis/gk-chassis-specs.md` |

---

## What's NOT in This Knowledgebase Yet

- Forum thread data (infrastructure ready, scraping not started)
- Bolt photos (database schema ready, `fasteners/bolts/` is empty)
- Vector embeddings (placeholder in `common/vector-store/`)
- Blue car knowledge graph JSON (build-profile.json exists, graph pending)
- Visual diagrams beyond fuel pump + cam sensor

See `ROADMAP.md` for the ingestion pipeline plan.
