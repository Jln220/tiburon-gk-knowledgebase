# Tiburon GK Knowledgebase — Architecture Reference

This document describes the full design of the knowledgebase: how information is structured, how authority is assigned, how community input flows in, and how users customize queries for their specific build.

---

## Contents

1. [Authority Tiers](#1-authority-tiers)
2. [Trust Ladder](#2-trust-ladder)
3. [Knowledge Sources by Tier](#3-knowledge-sources-by-tier)
4. [Interchangeable Parts](#4-interchangeable-parts)
5. [Build Profile — Query Customization](#5-build-profile--query-customization)
6. [Community Input Areas](#6-community-input-areas)
7. [GitHub Issues Workflow](#7-github-issues-workflow)
8. [Bolt Database Integration](#8-bolt-database-integration)
9. [Mermaid Diagrams](#9-mermaid-diagrams)
10. [MCP Access for Community Models](#10-mcp-access-for-community-models)
11. [File Structure Summary](#11-file-structure-summary)
12. [Source Credibility and Weighting](#12-source-credibility-and-weighting)

---

## 1. Authority Tiers

Every piece of information in this knowledgebase carries an `authority_tier` that tells AI models and humans how much to trust it.

| Tier | Label | Source | Color coding |
|------|-------|---------|--------------|
| 1 | **Factory** | Hyundai shop manual, electrical troubleshooting manual | Solid edge in diagrams |
| 2 | **Community wiki** | OpenGK.org — peer-reviewed community technical data | Solid edge, italic label |
| 3 | **Forum** | NewTiburon.com threads, attributed posts | Dashed edge in diagrams |
| 4 | **Web / parts data** | RockAuto, OEM parts sites, manufacturer datasheets | Dashed edge, `[web]` tag |

**Rule:** When tiers conflict, the lower-numbered tier wins unless the higher tier has `trust_level: "verified_fit"` or `"measured"` (see Section 2).

All nodes in the knowledge graph carry an `authority_tier` field (integer 1–4). AI models using the MCP should cite the tier in their answers.

---

## 2. Trust Ladder

Forum and community data climbs a trust ladder as it accumulates evidence. Each rung is a value of the `trust_level` field on community nodes.

```
rumor
  └─ community_report          ← one person says so, no corroboration
       └─ multiple_reports     ← ≥3 independent sources confirm
            └─ verified_fit    ← someone installed it and it works (with photos/thread link)
                 └─ measured   ← dimensional or electrical measurement provided
                      └─ factory_spec  ← confirmed in factory manual (upgrades to Tier 1)
```

### How a claim moves up the ladder

1. A new forum post is ingested as `trust_level: "community_report"`.
2. A GitHub Issue is opened (label: `community-review`) to vet it.
3. Commenters add corroboration. When ≥3 independent sources confirm, a maintainer updates to `"multiple_reports"`.
4. When someone reports an actual install with photos/video: `"verified_fit"`.
5. When someone provides a measurement (resistance, dimension, torque): `"measured"`.
6. When a factory manual citation is found: node migrates to Tier 1, `authority_tier: 1`.

### In the knowledge graph

Forum-derived nodes carry:
```json
{
  "authority_tier": 3,
  "trust_level": "community_report",
  "community_review_issue": 12,
  "corroboration_count": 1,
  "verified_by": []
}
```

Interchangeable part claims carry the same fields plus a `fit_notes` string (e.g., "direct plug-and-play", "requires adapter", "dimensional match confirmed").

---

## 3. Knowledge Sources by Tier

### Tier 1 — Factory Manuals

| File | Chapter codes | Content |
|------|--------------|---------|
| `common/shop-manual/engine-mechanical.md` | EMA (V6), EM (I4) | Specs, torques, procedures |
| `common/shop-manual/fuel-system.md` | FLA (V6), FL (I4) | Injectors, ECM, sensors, DTCs |
| `common/shop-manual/engine-electrical.md` | EE | Alternator, starter, battery |
| `common/shop-manual/emission-control-system.md` | EC | O2 sensors, EGR, EVAP |
| `common/electrical-manual/connector-configurations.md` | CC | Connector codes and pin counts |
| `common/electrical-manual/component-locations.md` | CL | Physical locations on car |
| `common/electrical-manual/schematics.md` | Various | Circuit schematics by system |

**MCP access:** All Tier 1 content is served via `@modelcontextprotocol/server-filesystem` from `common/`. This is the only tier guaranteed available to community model users (see Section 10).

### Tier 2 — OpenGK (Community Wiki)

| File | Content |
|------|---------|
| `common/opengk/sensor-information.md` | Replacement part numbers, compatible sensors |
| `common/opengk/ecm-pinouts.md` | Siemens SIMK43 connector pinouts |
| `common/opengk/gkflasher.md` | GKFlasher tuning CLI reference |
| `common/opengk/k-line.md` | KWP2000 protocol, security, I/O |
| `common/opengk/smartra.md` | SMARTRA2 immobilizer architecture |
| `common/opengk/can-bus-messages.md` | CAN bus message IDs |
| `common/opengk/body-control-module.md` | BCM connector pinouts |

**Ingestion policy:** OpenGK content is manually reviewed before inclusion. Each file carries `"authority_tier": 2` in the knowledge graph.

### Tier 3 — Forum (NewTiburon.com)

Stored in `forum/threads/{thread_id}/`. Each post is a separate chunk with `community_verified: false` until reviewed via GitHub Issues.

**Priority contributors:** Posts from `chase206` are ingested first and tagged `priority_contributor: true`.

### Tier 4 — Web / Parts Data

Web-sourced data is stored as part_number nodes in the knowledge graph with:
- `source: "RockAuto"` | `"OEMPartsFast"` | `"manufacturer"`
- `url`: direct link to product page
- `authority_tier: 4`
- Interchangeable-part claims include `source_vehicle` and `trust_level`

**What gets scraped:** Part numbers, fitment notes, dimensional data from product listings, OEM-style schematic diagrams from manufacturer sites. No scraping of paywalled data.

---

## 4. Interchangeable Parts

The knowledge graph supports cross-vehicle part compatibility via `interchangeable_with` edges and extended `part_number` node fields.

### Extended `part_number` node schema

```json
{
  "id": "pn-toyota-90919-A2005",
  "type": "part_number",
  "label": "Toyota 90919-A2005 Ignition Coil",
  "number": "90919-A2005",
  "source": "Toyota",
  "authority_tier": 4,
  "trust_level": "verified_fit",
  "source_vehicle": "Toyota Camry 3.0L 1MZ-FE",
  "fit_notes": "Direct plug-and-play on G6BA. Pins A=GND, B=trigger, C=feedback (leave open), D=12V. Smart coil (internal igniter).",
  "corroboration_count": 5,
  "verified_by": ["chase206", "OpenGK"],
  "community_review_issue": 7,
  "url": "https://www.rockauto.com/en/parts/toyota,...,90919-A2005",
  "notes": "COP coil used on white Tiburon build"
}
```

### `interchangeable_with` edge

```json
{
  "from": "pn-toyota-90919-A2005",
  "to": "comp-ignition-coil",
  "type": "interchangeable_with",
  "fit_confidence": "verified_fit",
  "source_vehicle": "Toyota Camry 1MZ-FE / 2JZ-GE",
  "notes": "Direct plug-and-play. Same smart-coil interface.",
  "authority_tier": 3,
  "community_review_issue": 7
}
```

### Query behavior

When an AI queries for "Tiburon ignition coil", the graph traversal should:
1. Find `comp-ignition-coil`
2. Follow `has_part` edges → OEM part numbers
3. Follow `interchangeable_with` edges → Toyota 90919-A2005
4. Return all results, clearly labeled by tier and trust level

**Display convention:** Factory OEM parts listed first, then interchangeable parts in descending trust_level order, with source vehicle and fit notes.

### Interchangeable part categories already known

| Component | Interchangeable PN | Source Vehicle | Trust |
|-----------|-------------------|----------------|-------|
| Ignition coil (COP) | Toyota 90919-A2005 | Camry 1MZ-FE / Lexus 1UZ | verified_fit |
| Spark plug | NGK BKR5ES-11 | Many applications | factory_spec |
| Oxygen sensor | Check `opengk/sensor-information.md` | Various | community_report |
| Camshaft position sensor | Check `opengk/sensor-information.md` | Various | community_report |

---

## 5. Build Profile — Query Customization

Each user can provide a **build profile** that AI models load as context to customize queries for their specific car. This eliminates the need to re-specify "I have a Haltech, my AVI1 is fuel pressure" in every query.

### Build profile file

Location: `builds/{your-car}/build-profile.json`

This is a **machine-readable** companion to the human-readable `build-profile.md`. AI models load this JSON at session start to understand your car's configuration.

```json
{
  "build_id": "white-tiburon",
  "description": "2003 Hyundai Tiburon GT V6 — Lemons race car",
  "engine": "G6BA",
  "transmission": "Aisin AY6",
  "ecu": {
    "make": "Haltech",
    "model": "Elite 2500",
    "avi_assignments": {
      "AVI1": { "signal": "fuel_pressure",    "sensor": "Lowdoller 899404", "pin_26": 13 },
      "AVI2": { "signal": "fuel_temp",        "sensor": "Lowdoller 899405", "pin_34": 16 },
      "AVI3": { "signal": "oil_pressure",     "sensor": "Lowdoller 899402", "pin_34": 17 },
      "AVI4": { "signal": "oil_temp",         "sensor": "Lowdoller 899403", "pin_34": 2  },
      "AVI5": { "signal": "coolant_pressure", "sensor": "Lowdoller 899406", "pin_26": 20 },
      "AVI6": { "signal": "coolant_temp",     "sensor": "Lowdoller 899407", "pin_26": 12 },
      "AVI7": { "signal": "brake_pressure",   "sensor": "Lowdoller 899408", "pin_26": 3  },
      "AVI8": { "signal": "brake_temp",       "sensor": "Lowdoller 899409", "pin_26": 4  },
      "AVI9": { "signal": "MAP",              "sensor": "factory_oem",      "pin_34": 15 },
      "AVI10":{ "signal": "TPS",              "sensor": "factory_oem",      "pin_34": 14 }
    },
    "ignition": {
      "type": "COP",
      "coils": "Toyota 90919-A2005",
      "count": 6,
      "dwell_ms": 2.1,
      "mode": "sequential"
    }
  },
  "pdm": {
    "make": "AIM",
    "model": "PDM 32",
    "outputs": {
      "HP1": { "load": "starter_motor",     "trigger": "STARTER_SAFE" },
      "HP2": { "load": "alternator_field",  "trigger": "IGN_ON" },
      "HP3": { "load": "fuel_pump",         "trigger": "FP_PRIME + RUN" },
      "HP4": { "load": "COP_coils_12V",     "trigger": "IGN_ON" },
      "HP5": { "load": "injectors_12V",     "trigger": "IGN_ON" },
      "HP6": { "load": "cooling_fan_HI",    "trigger": "FAN_HI" },
      "HP7": { "load": "cooling_fan_LO",    "trigger": "FAN_LO" },
      "MP1": { "load": "Haltech_ECU",       "trigger": "IGN_ON" },
      "MP2": { "load": "COP_coils_12V_B",   "trigger": "IGN_ON" },
      "LP7": { "load": "warning_LED",       "trigger": "CAN_WARN" }
    }
  },
  "oem_car": false,
  "note": "Load this file at session start. Use AVI assignments and PDM map to answer wiring questions without re-asking."
}
```

### How models use the build profile

When using the MCP filesystem server, models should:
1. At session start, read `builds/{your-car}/build-profile.json`
2. Cache AVI assignments, PDM map, ignition type, etc.
3. Use this context to resolve ambiguous queries:
   - "Which pin is fuel pressure?" → AVI1 → 26-pin pin 13
   - "What coils does this car use?" → Toyota 90919-A2005, COP, sequential

### For community members (non-Haltech builds)

Duplicate `builds/template/build-profile-template.json` → `builds/{your-car}/build-profile.json` and fill in your ECU, sensors, and wiring. The template covers:
- OEM ECU (Siemens SIMK43 / GKFlasher) configuration
- Haltech Elite 750 / 1500 / 2500 configs
- Other aftermarket ECU configs (custom fields)
- Stock and modified cars

---

## 6. Community Input Areas

The following areas are specifically where community contributions would most improve the knowledgebase. Each is tracked as an open GitHub Issue with label `help-wanted`.

### Priority 1 — Part Numbers (Tier 4 → Tier 2)

| Component | What we need | Issue label |
|-----------|-------------|-------------|
| CMP sensor replacement | OEM-compatible part numbers with source vehicle | `part-number` |
| CKP sensor replacement | Same | `part-number` |
| O2 sensors (front + rear) | Compatible aftermarket PNs, verified fit | `part-number` |
| IAT sensor | Compatible replacements | `part-number` |
| Throttle body | Compatible replacements, bore size if different | `part-number` |
| Wheel bearing (front/rear) | Hub dimensions, compatible PNs from other vehicles | `part-number` |
| Brake caliper (front/rear) | Rebuilt vs new, compatible from other Hyundai/Kia | `part-number` |

### Priority 2 — Procedure Verification (Tier 3 → Tier 2)

| Procedure | What we need | Issue label |
|-----------|-------------|-------------|
| Timing belt interval | Factory says 60k mi, community reports vary | `procedure-verify` |
| Valve clearance adjustment | Feeler gauge specs from hands-on experience | `procedure-verify` |
| Immobilizer bypass | K-Line procedure confirmed working on specific VIN ranges | `procedure-verify` |
| Wheel alignment specs | Track alignment vs street for Lemons racing | `procedure-verify` |

### Priority 3 — Measurements (Tier 3 → measured)

| What | Why | Issue label |
|------|-----|-------------|
| CMP sensor air gap | Factory spec missing from manual; community measurement needed | `measurement` |
| Injector flow rate (stock) | Needed for Haltech base map fuel math | `measurement` |
| Intercooler sizing (I4 turbo) | No factory spec; community builds vary | `measurement` |
| Driveshaft length per gear | Race transmission swap reference | `measurement` |

### Priority 4 — Forum Thread Ingestion

Threads we know are valuable but not yet scraped:
- Chase206's race prep series (NewTiburon.com)
- GKFlasher tune comparison thread
- Control arm bushing replacement thread (thread 484870 — seeded)
- Lemons GK build threads

To nominate a thread: open an Issue with label `forum-ingest` and paste the URL.

---

## 7. GitHub Issues Workflow

### Label schema

| Label | Color | Use |
|-------|-------|-----|
| `community-review` | Yellow | New forum claim needing vetting |
| `spec-error` | Red | Reported incorrect spec in KB |
| `part-number` | Blue | New or corrected part number |
| `procedure-verify` | Purple | Procedure step needs confirmation |
| `measurement` | Teal | Dimensional/electrical measurement needed |
| `forum-ingest` | Gray | Request to ingest a forum thread |
| `interchangeable-part` | Orange | Cross-vehicle part compatibility claim |
| `help-wanted` | Green | Open request for community contribution |
| `verified` | Dark green | Claim confirmed, ready to merge |

### Review flow

```
New forum post ingested
        │
        ▼
GitHub Issue opened (community-review)
  │  Include: thread URL, post author, claim quoted, chunk_id
  │
  ▼
Community comments with corroboration
  │  Maintainer tracks corroboration_count
  │
  ├── ≥3 confirmations → trust_level: "multiple_reports"
  ├── Install report + photos → trust_level: "verified_fit"
  ├── Measurement data → trust_level: "measured"
  └── Manual citation found → authority_tier: 1, close issue
  │
  ▼
Maintainer updates knowledge graph node + adds PR
  │
  ▼
Issue closed with label: verified
```

### Spec error flow

```
User finds wrong spec
        │
        ▼
Open Issue: spec-error
  Include: file:line, wrong value, correct value + source
        │
        ▼
Maintainer verifies against factory manual
        │
        ▼
PR updates the .md file and knowledge graph node
  Issue closed
```

### How to contribute a measurement

1. Open Issue with label `measurement`
2. Include: component name, value (with units), test method, tool used, car (VIN range or year)
3. Attach photo if physical measurement
4. Maintainer adds to knowledge graph as `trust_level: "measured"`, cites the Issue number

---

## 8. Bolt Database Integration

The `fasteners/` database stores physical bolt records with photos and measurements. These link into the knowledge graph via `bolt_record` nodes.

### How bolt records connect to the graph

Every bolt in `fasteners/bolt-index.json` has a `related_graph_nodes` field linking it to:
- The `torque_spec` node for that fastener (from shop manual)
- The `component` node it fastens
- The `section` node covering its installation procedure

```json
{
  "bolt_id": "M6x1.0-20-flange-hex-valve-cover",
  "location": { "system": "engine", "subsystem": "valve-cover" },
  "torque": { "nm": 10, "method": "standard" },
  "related_graph_nodes": {
    "torque_spec": "ts-valve-cover-bolt",
    "component": "comp-valve-cover",
    "procedure_section": "EMA-45"
  }
}
```

### `bolt_record` node type (in knowledge graph)

```json
{
  "id": "bolt-M6x1.0-20-flange-hex-valve-cover",
  "type": "bolt_record",
  "label": "Valve Cover Bolt M6×1.0×20",
  "bolt_id": "M6x1.0-20-flange-hex-valve-cover",
  "record_path": "fasteners/bolts/M6x1.0-20-flange-hex-valve-cover/",
  "photos": ["spec.jpg", "head.jpg", "side.jpg", "location.jpg"],
  "has_dimensions": true,
  "has_location_photo": true
}
```

### Edges from bolt records

| Edge | From | To | Meaning |
|------|------|----|---------|
| `fastens` | bolt_record → component | This bolt secures this component |
| `torque_defined_by` | bolt_record → torque_spec | Factory torque for this bolt |
| `procedure_in` | bolt_record → section | Installation procedure |
| `stored_in_bin` | bolt_record → string | Bin label (e.g., "ENGINE-01") |

### Query integration

When looking up a component, include its bolts:
- "What bolts hold the valve cover?" → follow `fastens^-1` from `comp-valve-cover` → find all bolt records → show torque, part number, bin label, photos

When sorting parts bins, cross-reference:
- Bolt in hand → scan `bolt_id` → find `related_graph_nodes` → know exactly where it goes

### Building the database progressively

Add bolts from your parts bin as you disassemble/reassemble. Each entry needs:
1. Measure: thread diameter, pitch, under-head length (UHL)
2. Identify head type + drive
3. Photograph: spec card (with ruler), head, side, installed location
4. Add entry to `bolt-index.json`
5. Link `related_graph_nodes` to the knowledge graph

See `fasteners/README.md` for bolt_id naming format and photo standards.

---

## 9. Mermaid Diagrams

Each component has a Mermaid diagram (`.md` file) with clickable nodes pointing to relevant knowledge base sections.

### Visual authority coding

| Edge style | Meaning |
|-----------|---------|
| `-->` solid arrow | Tier 1 (factory) or Tier 2 (OpenGK) — authoritative |
| `-.->` dashed arrow | Tier 3 (forum) or Tier 4 (web) — lower confidence |

### Existing diagrams

| File | Component |
|------|-----------|
| `builds/white-tiburon/diagrams/fuel-pump.md` | Fuel pump — power path + sensor path (white car) |
| `common/diagrams/cam-sensor.md` | CMP sensor — signal path, connector, DTCs |

### Planned diagrams (open `help-wanted` Issue to claim one)

| Component | Priority |
|-----------|----------|
| Ignition coil (COP — white car) | High |
| Alternator + exciter circuit | High |
| Starter motor circuit | High |
| OEM instrument cluster signals | Medium |
| Knock sensor | Medium |
| O2 sensor (front + rear) | Medium |
| Throttle body + IAC | Medium |
| EGR system | Low |
| EVAP system | Low |

### How to add a diagram

1. Copy `common/diagrams/_template.md` (planned)
2. Add component nodes (ECU pin → wire → component → load)
3. Add `click` events pointing to relevant KB files
4. Use solid edges for factory-confirmed paths, dashed for community data
5. Open PR — diagrams are auto-rendered on GitHub

---

## 10. MCP Access for Community Models

The MCP filesystem server gives any AI model (Claude, GPT-4, Gemini, etc.) read access to the full knowledgebase — no API keys, no cost.

### For community members

```bash
# Clone the repo
git clone https://github.com/USERNAME/tiburon-gk-knowledgebase.git
cd tiburon-gk-knowledgebase

# Start the MCP server (needs Node.js)
npx @modelcontextprotocol/server-filesystem ./Knowledgebase
```

Then add to your AI client config (see `mcp/README.md` for Claude Desktop and other client configs).

### Authority-aware prompting

Tell your AI model to respect authority tiers:

> "You have access to the Tiburon knowledgebase via MCP. When answering questions:
> 1. Prefer factory manual content (Tier 1) over OpenGK (Tier 2) over forum (Tier 3) over web data (Tier 4).
> 2. Always cite the source tier and file:page_ref when giving specs.
> 3. Load my build profile from `builds/white-tiburon/build-profile.json` for context.
> 4. If a claim has `trust_level` below `verified_fit`, flag it clearly."

### Build profile loading

Add to your session prompt:
```
Before answering, read builds/{your-car}/build-profile.json and use it to
resolve AVI pin, PDM output, and wiring questions without re-asking.
```

---

## 11. File Structure Summary

```
Knowledgebase/
├── ARCHITECTURE.md              ← This file
├── common/
│   ├── tiburon-knowledge-graph.json   ← Common graph (Tier 1+2 data)
│   ├── knowledge-graph-schema.md      ← Schema reference
│   ├── shop-manual/                   ← Tier 1: factory manual content
│   ├── electrical-manual/             ← Tier 1: ETM content
│   ├── opengk/                        ← Tier 2: OpenGK wiki
│   ├── chassis/                       ← Tier 1/2: G6BA specs, Aisin ratios
│   ├── diagrams/                      ← Mermaid component diagrams (common)
│   └── vector-store/                  ← Semantic search implementation
├── builds/
│   ├── template/
│   │   ├── build-template.md          ← Human intake form
│   │   └── build-profile-template.json ← Machine-readable build profile
│   ├── white-tiburon/
│   │   ├── build-profile.md           ← Human-readable build
│   │   ├── build-profile.json         ← Machine-readable (MCP context)
│   │   ├── build-knowledge-graph.json ← Build-specific graph overlay
│   │   ├── signal-routing.md          ← End-to-end signal routing
│   │   ├── weekend-tasks.md           ← Phased build procedure
│   │   └── diagrams/                  ← Build-specific Mermaid diagrams
│   └── blue-tiburon/
│       └── build-profile.md
├── hardware/
│   ├── haltech/                       ← Elite 2500 connector pinouts
│   ├── aim-pdm/                       ← PDM 32 pinout + config guide
│   └── sensors/                       ← Lowdoller specs, COP wiring
├── fasteners/
│   ├── README.md                      ← Bolt_id naming, photo standards
│   ├── bolt-index.json                ← All bolt records (indexed)
│   └── bolts/{bolt_id}/               ← Per-bolt directory with 4 photos
├── forum/
│   ├── README.md                      ← Scraping methodology, ethics
│   ├── thread-index.json              ← Index of scraped threads
│   └── threads/{id}/                  ← Per-thread data
├── credibility/
│   ├── README.md                      ← Credibility system overview
│   ├── sources.json                   ← Source registry (sites, wikis, manuals)
│   ├── contributors.json              ← Known contributor weights
│   ├── forum-sections.json            ← Forum section → KB topic mapping
│   ├── scoring-algorithm.md           ← Composite credibility formula
│   └── post-classification.md         ← Post type definitions + modifiers
├── validation/
│   ├── README.md                      ← Test framework methodology
│   ├── test-cases.json                ← Forum questions as test cases
│   ├── test-results.json              ← Run results (model, scores, gaps)
│   └── coverage-gaps.md               ← Gap analysis organized by system
├── extraction/
│   ├── README.md                      ← Extraction status + entry point
│   ├── pdf-extraction-guide.md        ← Shop manual / schematic / hardware SOP
│   └── forum-extraction-guide.md      ← Forum + OpenGK ingestion pipeline
└── mcp/
    ├── README.md                      ← MCP setup for community
    └── claude_desktop_config.example.json
```

---

## 12. Source Credibility and Weighting

The `credibility/` directory extends the T1-T4 authority tiers (Section 1) with a numeric composite scoring system. It provides granularity *within* each tier — two T3 claims can now be compared by their credibility score.

**Key principle:** The credibility score does NOT replace tier promotion. Tier changes still follow the GitHub Issues workflow (Section 7). The score helps maintainers prioritize which claims to review first and helps LLMs weight conflicting same-tier sources.

### Components

| File | What it tracks |
|------|---------------|
| `credibility/sources.json` | External sources (OpenGK 9/10, NewTiburon 3/10 base, RockAuto 4/10, etc.) |
| `credibility/contributors.json` | Known forum experts with credibility weights (Charlie-III, chase206, eagleprime, The_Evenger at 5/10; unknown users default 2/10) |
| `credibility/forum-sections.json` | NewTiburon sections mapped to KB systems with per-section modifiers (Engine Management +1, Exterior -1) |
| `credibility/scoring-algorithm.md` | The composite formula: 30% source + 40% contributor + 30% post context, plus engagement, corroboration, and trust ladder bonuses |
| `credibility/post-classification.md` | Post types: stickied_guide (+2), build_log (+1), technical_reply (+1), question_post (-1), etc. |

### Knowledge Graph Integration

Forum-derived nodes gain two optional fields alongside the existing `authority_tier`, `trust_level`, and `corroboration_count`:

```json
{
  "credibility_score": 5.6,
  "credibility_breakdown": {
    "source": "newtiburon",
    "contributor": "Charlie-III",
    "post_type": "stickied_guide",
    "computed": "2026-03-12"
  }
}
```

### Validation Framework

The `validation/` directory uses real forum questions as test cases to measure KB coverage:

1. Questions from NewTiburon are extracted as test cases
2. Expert responses (from priority contributors) define expected answer components
3. The KB is queried and scored against those components
4. Gaps are tracked in `validation/coverage-gaps.md` and drive content development

### Scheduled Agent Entry Points

Three agent workflows use this system:

| Agent | Entry Point | Schedule |
|-------|-------------|----------|
| Forum Ingestion | `credibility/scoring-algorithm.md` Section 6 | On new thread ingestion |
| KB Validation | `validation/README.md` | Weekly or after KB additions |
| Data Quality Audit | `credibility/scoring-algorithm.md` Section 6 | Monthly |

See `credibility/README.md` for full documentation.
