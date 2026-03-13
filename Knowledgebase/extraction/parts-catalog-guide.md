# Parts Catalog Extraction Guide

Procedure for importing OEM part numbers, BOM data, and exploded diagrams from Hyundai EPC (Electronic Parts Catalog) sources into the knowledgebase.

---

## Primary Source: hyundai.catalogs-parts.com

**URL:** `https://hyundai.catalogs-parts.com/#{client:undefined;page:group;lang:en;catalog:hma;family:tiburon;catalog_code:hma2c0pa01;prm:01.c,02.g,03.h,04.6,05.7,dt.l,year.2003}`

**Vehicle config:** 2003 Tiburon, USA market (HMA), 2.7L V6 (G6BA), 6-speed manual

### Site Structure

```
Catalog HYUNDAI [USA]
└── TIBURON 03 (2003-)
    └── Group Parts
        ├── BODY (BO)          — panels, doors, hood, trunk, bumpers
        ├── ENGINE (EN)        — block, head, intake, exhaust, fuel, cooling
        ├── TRANSMISSION (MI)  — clutch, gearbox, driveshaft, axle
        ├── CHASSIS (CH)       — brakes, steering, suspension, wheels
        ├── TRIM (TR)          — seats, interior trim, glass, mirrors
        └── ELECTRICAL (EL)    — wiring, lights, switches, sensors, ECU
```

Each group contains 20-60 subgroups. Each subgroup has:
1. **Exploded diagram** — SVG/image with PNC callout numbers
2. **Parts table** — PNC, Part Number, Qty, Part Name, Model Description, Date Range

### Data Fields

| Field | Description | Example |
|-------|-------------|---------|
| PNC | Part Number Code (diagram callout) | 31305E |
| Part Number | Hyundai OEM part number | 313202C600 |
| Qty | Quantity per vehicle | 1 |
| Part Name | Description | TUBE ASSY - FUEL FEED |
| Model Description | Applicability filters | Engine Capacity: [H] 2700 CC |
| Start Date | Production start | 01.10.2001 |
| End Date | Production end | 31.12.2006 |

### Automated Scraping

**Tool:** `scripts/scrape-parts-catalog.js`

Run in Chrome DevTools console while on the catalog site:

```js
// Scrape entire catalog (~300+ subgroups, ~20 min)
const catalog = await scrapeAllGroups();

// Scrape single group
const engine = await scrapeGroup('EN');

// Scrape single subgroup
const rockerCover = await scrapePart('EN', '2022412');

// Search scraped data
findPart(catalog, 'gasket');
```

Output: `tiburon-2003-v6-parts-catalog.json` auto-downloaded to browser Downloads folder.

### Manual Download / PDF Extraction (Current Method)

PDFs have been printed from the catalog site and are stored in `Sources/OEM Parts Catalogs/`:
- `Engine Parts Catalog/` — 48 PDFs
- `Chassis Parts Catalog/` — 25 PDFs
- `Electrical Parts Catalog/` — 34 PDFs

Extraction script: `scripts/extract-parts-catalog.py`
- Uses pymupdf text extraction (not OCR — text is natively in PDFs)
- Parses column layout from block positions
- Outputs markdown + JSON to `Knowledgebase/common/parts-catalog/`
- Run: `py -3 scripts/extract-parts-catalog.py` from repo root

Re-run this script if new PDFs are added to the source folders.

**Status as of 2026-03-13:** All 107 PDFs extracted. 2,807 parts indexed across EN/CH/EL groups.

---

## Alternative Sources (Easier to Read)

### Tier 1: Free EPC Sites with Diagrams

| Site | URL | Pros | Cons |
|------|-----|------|------|
| **7zap.com** | `hyundai.7zap.com/en/hma/` | Clean UI, USA catalog, good diagrams | Cloudflare bot protection |
| **epc-data.com** | `hyundai.epc-data.com/coupe/` | Simple navigation | Listed as "Coupe" not "Tiburon" |
| **HyundaiPartsDeal** | `hyundaipartsdeal.com/2003-hyundai-tiburon-parts.html` | Organized by system, prices shown | Some diagrams missing |

### Tier 2: Paid/Commercial EPC

| Source | Notes |
|--------|-------|
| **Hyundai Microcat V6** | Official dealer EPC. Most accurate. Requires subscription. |
| **Snap-on EPC** | VIN decoder + cross-references. Commercial license. |
| **Levam.net API** | JSON API access to OEM data. Starts at €300/month. |

### Tier 3: Community References

| Source | Notes |
|--------|-------|
| **NewTiburon.com forums** | Thread: "Parts Diagrams with OEM part numbers" (thread 178385) |
| **newtonnet.co.uk** | Covers Gen1/Gen2 (RD) only — NOT GK |

---

## Output Format

Parts catalog data goes into: `Knowledgebase/common/parts-catalog/`

### Directory Structure

```
common/parts-catalog/
├── _index.md                    ← Master index with all groups
├── catalog-metadata.json        ← Full scraped catalog (raw JSON)
├── engine.md                    ← ENGINE group — all subgroups
├── body.md                      ← BODY group
├── transmission.md              ← TRANSMISSION group
├── chassis.md                   ← CHASSIS group
├── trim.md                      ← TRIM group
└── electrical.md                ← ELECTRICAL group
```

### Markdown Format per Group

```markdown
---
source: hyundai.catalogs-parts.com
catalog_code: hma2c0pa01
group: EN
group_name: ENGINE
vehicle: 2003 Hyundai Tiburon (GK)
engine: V6 (2.7L Delta G6BA)
market: USA (HMA)
extraction_method: web_scrape
extraction_date: YYYY-MM-DD
subgroup_count: 57
total_parts: NNN
---

# ENGINE — Parts Catalog

## [20-224] Rocker Cover (02/02)

| PNC | Part Number | Qty | Part Name | Engine | Dates | V |
|-----|-------------|-----|-----------|--------|-------|---|
| 22420 | 2242037101 | 1 | COVER ASSY - ROCKER, RH | 2700 CC | 10.2001–09.2003 | ⬜ |
| 22420 | 2242037110 | 1 | COVER ASSY - ROCKER, RH | 2700 CC | 09.2003–03.2004 | ⬜ |
| 22441 | 2244137110 | 1 | GASKET - ROCKER COVER | 2700 CC | 09.2003–12.2006 | ⬜ |
```

### Integration with Knowledge Graph

Part numbers can be added to component nodes:

```json
{
  "id": "comp-ckp-sensor",
  "oem_part_numbers": [
    {"pn": "3935037100", "name": "SENSOR ASSY - CRANKSHAFT POSITION", "dates": "10.2001-12.2006"}
  ]
}
```

---

## V6-Only Filtering

Many subgroups contain parts for both 2.0L I4 and 2.7L V6. Filter by:
- **Model Description** contains `[H] 2700 CC` → V6 part
- **Model Description** contains `[G] 2000 CC` → I4 part (exclude for white car)
- **No engine filter** → common part (fits both)

The scraper captures the full Model Description field, so filtering can be done post-extraction.

---

## Supersession / Cross-Reference

Part numbers may be superseded (replaced by newer numbers). The catalog site has an "information" button (ℹ️) per part that shows:
- Supersession chain (old P/N → new P/N)
- Cross-reference to other vehicles
- Weight and dimensions

The scraper does NOT currently extract supersession data. This can be added later via the `/cat_scripts/get_detail.php` endpoint.

---

## Priority Extraction Order

1. **ELECTRICAL (EL)** — sensors, connectors, wiring harnesses → cross-reference with schematics
2. **ENGINE (EN)** — gaskets, seals, bolts → cross-reference with shop manual torque specs
3. **CHASSIS (CH)** — brake pads, suspension → commonly replaced parts
4. **TRANSMISSION (MI)** — clutch, flywheel → build-relevant
5. **BODY (BO)** — panels, weather strips → lower priority for race car
6. **TRIM (TR)** — seats, interior → lowest priority (stripped for Lemons)
