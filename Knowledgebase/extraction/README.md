# Extraction Guide — Entry Point for All Content Ingestion

This directory is the **single entry point** for any Claude session that needs to extract, ingest, or process content into the knowledgebase. Whether you're extracting PDF manual pages, ingesting forum threads, or processing hardware datasheets — start here.

---

## Quick Reference: Which Guide Do I Need?

| Task | Guide | Tool |
|------|-------|------|
| Extract a factory shop manual chapter (EMA, FLA, etc.) | [pdf-extraction-guide.md](pdf-extraction-guide.md) | `scripts/extract-pdf.py` + Claude vision |
| Extract electrical schematics from ETM | [pdf-extraction-guide.md](pdf-extraction-guide.md) | Same tool, see Schematics section |
| Extract a hardware datasheet (AIM, Haltech) | [pdf-extraction-guide.md](pdf-extraction-guide.md) | Same tool, see Hardware section |
| Ingest a NewTiburon forum thread | [forum-extraction-guide.md](forum-extraction-guide.md) | Manual or scraper |
| Ingest OpenGK wiki content | [forum-extraction-guide.md](forum-extraction-guide.md) | Manual web fetch |
| Score an ingested source for credibility | `credibility/scoring-algorithm.md` | Compute formula |
| Add a forum question as a test case | `validation/README.md` | Manual entry |
| Chunk content for vector store | `common/vector-store/README.md` | Future pipeline |

---

## Extraction Status

### Factory Shop Manual Chapters

| Chapter | Code | Pages | Status | File(s) |
|---------|------|-------|--------|---------|
| Engine Mechanical (V6) | EMA | 80 | **Split** (9 files) | `common/shop-manual/engine-mechanical/` |
| Engine Mechanical (I4) | EM | ~60 | **Needs split** | `common/shop-manual/engine-mechanical-i4/` |
| Fuel System | FLA | ~120 | **Split** (6 files) | `common/shop-manual/fuel-system/` |
| Engine Electrical | EE | ~50 | **Needs split** | `common/shop-manual/engine-electrical/` |
| Emission Control | EC | ~40 | **Needs split** | `common/shop-manual/emission-control-system/` |
| Clutch System | CL | ~20 | **Needs split** | `common/shop-manual/clutch-system/` |
| Transaxle | TR | ~60 | **Needs split** | `common/shop-manual/transaxle/` |
| Driveshaft and Axle | DA | ~20 | **Needs split** | `common/shop-manual/driveshaft-and-axle/` |
| Suspension System | SS | ~50 | **Needs split** | `common/shop-manual/suspension-system/` |
| Steering System | ST | ~40 | **Needs split** | `common/shop-manual/steering-system/` |
| Brake System | BR | ~60 | **Needs split** | `common/shop-manual/brake-system/` |
| Body Electrical | BE | ~80 | **Needs split** | `common/shop-manual/body-electrical/` |
| Body Interior/Exterior | BD | ~40 | **Needs split** | `common/shop-manual/body-interior-and-exterior/` |
| Heating/Ventilation/AC | HA | ~60 | **Needs split** | `common/shop-manual/heating-ventilation-air-conditioning/` |
| Restraints | RT | ~30 | **Needs split** | `common/shop-manual/restraints/` |
| General Information | GI | ~20 | **Needs split** | `common/shop-manual/general-information/` |
| Body Control Module | BCM | ~30 | **Needs split** | `common/shop-manual/body-control-module/` |

### Electrical Troubleshooting Manual (ETM)

| Section | Status | Files |
|---------|--------|-------|
| Schematic Diagrams (SD) | **Complete** — 37 circuits extracted | `common/electrical-manual/schematics/` |
| Connector Configurations (CC) | Partial | `common/electrical-manual/connector-configurations.md` |
| Component Locations (CL) | Partial | `common/electrical-manual/component-locations.md` |

### Hardware Datasheets

| Device | Status | Source PDF |
|--------|--------|-----------|
| AIM PDM 32 user guide | Partial (pinout extracted) | `AIM PDM/PDM32_user_guide_eng.pdf` |
| AIM PDM 32 tech sheet | Not started | `AIM PDM/aim_pdm32_tech_sheet.pdf` |
| AIM PDM Dash 10" tech sheet | Not started | `AIM PDM/aim_pdm_dash_10_inches_tech_sheet.pdf` |
| AIM GPS-08 pinout | Not started | `AIM PDM/PinoutGPS08_eng.pdf` |
| AIM Data Hub 101 pinout | Not started | `AIM PDM/Pinout_DataHub_101_eng.pdf` |
| AIM SmartyCam 3 | Not started | `AIM PDM/SmartyCam3_114_eng.pdf` |
| PKP 2600 SI Datasheet | Not started | `AIM PDM/PKP_2600_SI_Datasheet_REV1.pdf` |

### Forum Threads

| Status | Count |
|--------|-------|
| Indexed in thread-index.json | 22 threads |
| Scraped (posts.json populated) | 17 of 22 |
| Multi-page threads (page 1 only) | multiple (see scrape-log.md) |
| Extraction tool | `scripts/forum-scraper.js` |
| Batch pipeline docs | `extraction/forum-extraction-guide.md` § Batch Scraping Pipeline |
| Run log | `extraction/scrape-log.md` |

### OEM Parts Catalog

| Source | Status | Output |
|--------|--------|--------|
| Engine Parts Catalog (48 PDFs) | **Complete** | `common/parts-catalog/engine.md` |
| Chassis Parts Catalog (25 PDFs) | **Complete** | `common/parts-catalog/chassis.md` |
| Electrical Parts Catalog (34 PDFs) | **Complete** | `common/parts-catalog/electrical.md` |
| Raw JSON | **Complete** | `common/parts-catalog/catalog-metadata.json` |
| Knowledge graph enrichment | **Complete** | `common/tiburon-knowledge-graph.json` |

Extraction tool: `scripts/extract-parts-catalog.py` (pymupdf text extraction)
Source PDFs: `Sources/OEM Parts Catalogs/` (107 PDFs, 2003 Tiburon GK USA HMA)
Parts catalog guide: `extraction/parts-catalog-guide.md`

---

## Related Files

| File | Purpose |
|------|---------|
| `extraction/pdf-extraction-guide.md` | Step-by-step PDF extraction SOP |
| `extraction/forum-extraction-guide.md` | Forum thread ingestion SOP |
| `extraction/parts-catalog-guide.md` | Parts catalog ingestion SOP |
| `extraction/scrape-log.md` | Forum scraper run log |
| `scripts/extract-pdf.py` | PDF → PNG extraction tool (pymupdf) |
| `scripts/extract-parts-catalog.py` | Parts catalog PDF → markdown/JSON extractor |
| `common/vector-store/README.md` | Chunking strategy for semantic search |
| `forum/README.md` | Forum scraping methodology and challenges |
| `credibility/README.md` | Source credibility scoring system |
| `credibility/post-classification.md` | Post type classification and metadata flags |
| `validation/README.md` | KB validation test framework |
