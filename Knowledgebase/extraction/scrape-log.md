# Forum Scrape Log

Automated run log for the `forum-discovery-and-scrape` scheduled task.

---

## Run: 2026-03-13

**Trigger:** Scheduled task `forum-discovery-and-scrape`
**Operator:** Claude (claude-sonnet-4-6)
**Duration:** Single session (context limit reached; continued in follow-up session)

### Phase 1 — Discovery

Scanned NewTiburon.com `gk-engine-management`, `gk-general-discussion`, and related sections for new high-value threads. Discovered and indexed **15 new threads**, bringing the total thread-index count from 7 → 22.

New threads added to `forum/thread-index.json`:

| Thread ID | Title (truncated) | Section | Post Type |
|-----------|-------------------|---------|-----------|
| 320121 | Hi-Scan Pro / CASCADE Emulator | gk-general-discussion | reference_compilation |
| 102514 | Apexi SAFC/NEO wiring diagrams | gk-engine-management | reference_compilation |
| 122735 | The Definitive Perfect Power SMT-6 Thread | gk-engine-management | stickied_guide |
| 146567 | Valkare's Tuning Compendium | gk-engine-management | stickied_guide |
| 100813 | The Authoritative A/F Info Thread | gk-engine-management | stickied_guide |
| 89570 | ECU pinout | gk-engine-management | question_post |
| 198171 | I want headers but what about the CEL? | gk-general-discussion | stickied_guide |
| 215712 | The NEW V6 Definitive Exhaust Thread | gk-general-discussion | reference_compilation |
| 123286 | Engine Compatibility Info | gk-engine-management | reference_compilation |
| 127614 | Official N/A Cams Information Thread | gk-engine-management | reference_compilation |
| 87013 | How to build a custom TURBO | gk-general-discussion | stickied_guide |
| 100 | Official DYNO graph thread | gk-general-discussion | reference_compilation |
| 217279 | Want to build a custom exhaust? Read this first! | gk-general-discussion | stickied_guide |
| 134166 | Proper PCV Configuration? | gk-engine-management | stickied_guide |
| 187814 | Want to Turbo? Well you need to understand something... | gk-general-discussion | discussion_post |

### Phase 2 — Scraping (10 threads)

All 10 scraped threads: "See more" button clicked on OP before content capture. Full OP text captured in each `posts.json`.

#### 1. Thread 320121 — Hi-Scan Pro / CASCADE Emulator

- **Status:** ✅ Scraped
- **Content:** Download links and setup instructions for Hyundai Hi-Scan Pro diagnostic software and CASCADE emulator. Critical for blue car K-line diagnostics.
- **Notes:** Some download links may be stale. Primary value is the tool identification.

#### 2. Thread 123286 — Engine Compatibility Info

- **Status:** ✅ Scraped
- **Content:** Cross-vehicle engine swap compatibility for G6BA. Documents which donor vehicles share internals.
- **Notes:** Useful for sourcing rebuild parts.

#### 3. Thread 127614 — Official N/A Cams Information Thread

- **Status:** ✅ Scraped
- **Content:** Comprehensive camshaft comparison for GK V6 — lift, duration, LSA specs for OEM and aftermarket cams. Overlaps with `common/opengk/camshaft-specs.md`.
- **Notes:** Corroborates existing knowledge graph cam data.

#### 4. Thread 102514 — Apexi SAFC/NEO Wiring Diagrams (I4 and V6)

- **Status:** ✅ Scraped — **BROKEN IMAGES**
- **Author:** philm00x
- **Content:** OP is image-only — two wiring diagrams (I4 and V6). Both images hosted on defunct image host; broken as of 2026-03-13.
- **General Knowledge Value:** CRITICAL if images recovered; HIGH via cross-reference
- **Notes:** Images may be recoverable from archive.org. Text content of OP: labels only ("I4 diagram:" and "V6 diagram:"). No technical data extractable from text alone.
- **Action:** Flag for image recovery from Wayback Machine.

#### 5. Thread 146567 — Valkare's Tuning Compendium

- **Status:** ✅ Scraped — Full ~2,000 word OP captured
- **Author:** valkare (9,350 posts, senior member)
- **Content:** Closed loop vs open loop theory, LTFT/STFT mechanics, why closed-loop tuning with a piggyback fails, injector size change correction method (290cc → -35% closed loop adjustment), tune preservation after battery reset.
- **Key facts:**
  - Open loop activates at ~40-45% throttle on Neo-equipped cars
  - Tune open loop (WOT) first; closed loop stays at 14.7 AFR
  - 290cc injectors: apply -35% closed loop correction to prevent ECU confusion
  - Piggyback adjusts MAF signal, not actual injector pulse width
  - STFT hovering +10% at given RPM → eventually transfers to LTFT
- **Notes:** No images. Edited by Moderator (content verified at some point).

#### 6. Thread 100813 — The Authoritative A/F Info Thread

- **Status:** ✅ Scraped
- **Author:** tex2678
- **Content:** Narrowband vs wideband sensor theory. **Critical finding:** 2003+ Tiburons use 0–5V wideband titanium O2 sensors in stock ECU — narrowband A/F gauges DO NOT work on these cars (pre-2003 used narrowband). Wideband controller options: Innovate LC-1, AEM UEGO, Zeitronix Zt-2 ($150-600).
- **Key facts:**
  - 2003+ GK: must weld additional O2 bung for wideband controller sensor
  - Standard narrowband gauges will read incorrectly on 2003+ cars
- **Notes:** No images.

#### 7. Thread 198171 — I Want Headers But What About the CEL?

- **Status:** ✅ Scraped — Full OP (Q&A format)
- **Author:** Will51
- **Content:** Comprehensive header/CEL explainer. 3 catalytic converters (2 pre-cats in manifolds + 1 in Y-pipe). 4 O2 sensors: 2 upstream primary (fuel control — never modify), 2 downstream secondary (catalyst efficiency monitoring). P0420/P0430 codes on header install. Bank 1 = firewall side, Bank 2 = front.
- **Key facts:**
  - 03-06: ECU less sensitive; O2 spacers *may* work; high-flow cat relocation possible
  - 07-08: Headers WILL throw P0420/P0430; no reliable fix; even premium cats not guaranteed
  - ECU reset won't help OBD2 inspection (incomplete cycle check)
  - O2 spacers won't work on anything newer than 03-04
- **Notes:** 1.3M views — highest-traffic thread scraped this session. 188 replies, 7 pages (page 1 only scraped).

#### 8. Thread 87013 — How to Build a Custom TURBO

- **Status:** ✅ Scraped — Full OP (comprehensive build list)
- **Author:** tex2678
- **Content:** Complete custom turbo build guide. Only commercial kit: NGM. All external project build links dead. Full mandatory parts list.
- **Key facts:**
  - Oil feed line: **-4AN** (mandatory spec)
  - Oil return line: **-10AN** (mandatory spec — do NOT size down)
  - Sandwich plate for oil feed — don't use "Home Depot mod" (will fail)
  - **05+ models require returnless fuel system conversion**
  - 290cc+ injectors mandatory; adjustable 1:1 FPR mandatory
  - Solid motor mount(s) mandatory
  - Spark plugs: 1-2 steps colder depending on PSI
- **Notes:** 135K views. 3 pages (page 1 only). All linked projects are dead URLs.

#### 9. Thread 89570 — ECU Pinout

- **Status:** ✅ Scraped — **CORRECTION APPLIED**
- **Author:** Original poster asking about 2003 2.0L I4 ECU
- **Content:** Pinout question for I4 2.0L ECU (NOT V6). Pinout images broken.
- **Key facts (I4 only):**
  - Pin 18 (first instance) = wheel speed sensor (confirmed)
  - Pin 10 = knock signal (NEO-confirmed)
  - Pin 66 = RPM signal (NEO-confirmed)
  - Post #19 (Charlie-III): ECU bypass method
- **Correction:** Initially indexed as `reference_compilation`, `engine: "both"`. Corrected to `question_post`, `engine: "I4"`. Credibility recalculated from 4.1 → 3.8.
- **Notes:** Charlie-III posted at #19 (2024-08-xx) — `has_priority_contributor: true` confirmed. reply_count corrected 18 → 19. **Not useful for V6 pinout.**

#### 10. Thread 215712 — The NEW V6 Definitive Exhaust Thread

- **Status:** ✅ Scraped — Community comparison table
- **Author:** OP solicited crowd-sourced ratings
- **Content:** Exhaust system ratings (scale: 1=loudest/worst, 10=quietest/best build quality).

| Brand | Price | Pipe Dia | Build Q | Sound Q | Loudness |
|-------|-------|----------|---------|---------|----------|
| Borla | $600-700 | 2.25" | 9/10 | 10/10 | 8/10 |
| Aeon | $250 | 2.25-2.5" | 3/10 | 9/10 | 6/10 |
| Greddy Evo 2 | $900 | 2.5" | 8/10 | 4/10 | 3/10 |
| SFR single | $900 | 3" | 10/10 | — | — |
| ARK DT-S V2 | $800-1379 | 2.5" / 4.5" tip | 10/10 | 10/10 | 6/10 |

- **Notes:** Aeon had poor quality issues (broken parts, fitment problems). SFR discontinued. 6 pages (page 1 only).

---

### Phase 3 Summary

**Threads discovered (Phase 1):** 15 new
**Threads scraped (Phase 2):** 10 (all 10 targeted threads)
**Threads remaining unscraped:** 5 (122735, 100, 217279, 134166, 187814)
**Broken image threads:** 102514 (Apexi wiring diagrams — image recovery needed)
**Corrections made post-scrape:** Thread 89570 (engine = I4, not both; post_type = question_post; credibility 4.1 → 3.8)

### Follow-Up Actions

- [ ] Recover broken images from thread 102514 (archive.org)
- [ ] Scrape remaining 5 threads (122735, 100, 217279, 134166, 187814)
- [ ] Scrape additional pages of high-value multi-page threads (198171 p.2-7, 215712 p.2-6, etc.)
- [ ] Begin parts catalog ingestion from `Sources/OEM Parts Catalogs/` (3 catalogs, ~107 PDFs)

---

## Runs Index

| Date | Phase | Threads Indexed | Threads Scraped | Notes |
|------|-------|-----------------|-----------------|-------|
| 2026-03-13 | Phase 1+2 | +15 (total 22) | 10 | First automated run |
