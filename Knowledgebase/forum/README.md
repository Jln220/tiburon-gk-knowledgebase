# NewTiburon Forum Data
**Source:** https://www.newtiburon.com/
**Purpose:** Preserve community knowledge from key contributors for LLM lookup during builds.

---

## Status

| Phase | Status |
|-------|--------|
| Priority contributor list | In progress |
| Scraping methodology defined | In progress |
| Initial scrape | ☐ Not started |
| Data structured for LLM | ☐ Not started |

---

## Priority Contributors

Posts from these contributors are scraped and indexed first. They have the highest signal-to-noise ratio for technical content. Full credibility weights and metadata are tracked in `credibility/contributors.json`.

| Username | Role | Known expertise | Weight | Priority |
|----------|------|----------------|--------|----------|
| Charlie-III | Administrator | Engine mechanical, ignition, diagnostics, general maintenance | 5/10 | **High** |
| chase206 | Super Moderator | Engine builds, suspension, race prep, fabrication, Lemons | 5/10 | **High** |
| eagleprime | Member | *(to be filled after profile review)* | 5/10 | **High** |
| The_Evenger | Member | *(to be filled after profile review)* | 5/10 | **High** |

**How to add:** Add the contributor to `credibility/contributors.json` with their profile metadata and calculated weight (see `credibility/scoring-algorithm.md` Section 2). Then add a row here for quick reference.

---

## Scraping Methodology

### What to Scrape

Target thread sections (V6 / GK-specific content only — see `credibility/forum-sections.json` for full mapping):

**GK Performance (03+):**
- V6 - Naturally Aspirated (Intakes, Exhaust, Headers, Pulleys)
- V6 - Forced Induction (Turbo / Supercharger)
- Engine Management (ECU, Wiring Harnesses, Custom Wiring)
- Transmissions (Clutch, Flywheel, 5/6-spd, Driveshafts)
- Wheel, Tire, & Suspension (Springs, Coilovers, Shocks, Brakes)

**Also relevant (selective):**
- Audio & Security — only immobilizer/SMARTRA threads
- I4 sections — only when discussing shared-platform components

Exclude:
- For Sale / Wanted
- I4 / GK2-specific threads (unless also V6-relevant)
- Off-topic / General Chat

### Thread Selection Criteria

1. **Priority contributor started or replied** — always include
2. **High reply count** (>15 replies) — likely contains useful debate/refinement
3. **Pinned/sticky** threads — official community wisdom
4. **Keywords:** G6BA, 2.7L, V6, Delta, Haltech, AIM, Lemons, endurance, COP, knock sensor, etc.

### Data Format

Each scraped thread is saved as:
```
forum/threads/{thread-id}/
├── metadata.json       ← thread title, URL, date, reply count
└── posts.json          ← array of {author, date, post_number, content}
```

`forum/thread-index.json` — searchable index of all threads (title, URL, contributor list, tags).

---

## Extraction Challenges

NewTiburon (XenForo/Fora platform) has several quirks that make automated extraction difficult. Any scraper or agent must handle these:

### "See More" Collapsed Content

Long OPs are truncated behind a "See more" button. **The collapsed content is often the most valuable part** — detailed specs, part numbers, comparison tables, and procedures are below the fold. A scraper that only reads the visible content will miss the critical data.

**Mitigation:** Scraper must click/expand the "See more" element before extracting, or use the XenForo API/full-page HTML source where the content is not truncated. Flag threads with `"has_collapsed_content": true` in thread-index.json.

### Multi-Page Threads

Reference threads often span dozens of pages (e.g., header thread: 583 replies). Key information accumulates across many pages — corrections, updates, new product additions, and discontinuation notices.

**Mitigation:** Extract all pages. Flag with `"multi_page": true` and `"page_count"`. For reference compilations, the OP is usually the primary data source; replies add corrections and additions over time.

### Discontinued Parts / Dead Links

Most Tiburon aftermarket parts are no longer manufactured. Threads reference products, manufacturers, and websites that no longer exist. External links are frequently dead.

**Mitigation:** Flag with `"has_discontinued_parts": true` and list specific items in `"discontinued_parts"`. Capture the `"general_knowledge_value"` — the engineering principles, design parameters, and performance baselines that survive beyond specific product availability.

### Engine and Build Applicability

Threads often discuss modifications for one engine variant (I4 vs V6) or assume a specific ECU setup (stock vs standalone). This is rarely explicit in the title.

**Mitigation:** Every thread record in thread-index.json carries `"engine"`, `"ecu_requirement"`, and `"build_applicability"` flags. These are set during classification — see `credibility/post-classification.md` for the full flag definitions. Critical for routing content to the correct build (white car = standalone ECU, blue car = stock ECU).

### Embedded Images

Install photos, dyno charts, wiring diagrams, and comparison tables are often in images, not text. These carry significant information that cannot be extracted by text scraping alone.

**Mitigation:** Flag with `"has_embedded_images": true`. For manual extraction, describe key image content in the `posts.json` record. For automated extraction, consider OCR or image captioning in a future pipeline.

---

## Scraping Tools

### Option A: Manual (no cost, no risk)
1. Open thread in browser
2. Copy post content into `posts.json` template
3. Fill `metadata.json`
4. Tag with relevant keywords

### Option B: Python script (semi-automated)
Uses `requests` + `BeautifulSoup4` with a politeness delay (3–5 seconds between requests).
Does NOT bypass login walls or rate limiting.

```bash
pip install requests beautifulsoup4
python forum/scraper.py --thread-url "https://www.newtiburon.com/threads/..." --output forum/threads/
```

Script respects `robots.txt` and adds a `User-Agent` identifying itself.

### Option C: HTTrack / wget (mirror)
Full section mirror — useful for bulk download but creates large files. Not recommended as primary method since unstructured HTML is harder for LLMs.

---

## Legal / Ethical Notes

- NewTiburon.com is a public forum — posts are publicly accessible without login for most content
- The scrape is for personal/community use in a private/semi-private knowledgebase, not re-publication
- Individual post attribution is preserved (author field in `posts.json`)
- If a contributor asks to have their posts removed, delete the relevant `posts.json` entries
- Do not scrape at a rate that would stress the server — 3+ second delays between requests
- Check `robots.txt` at `https://www.newtiburon.com/robots.txt` before running automated scraping

---

## Index Structure

`forum/thread-index.json` — each thread record now includes credibility fields:
```json
{
  "_meta": {
    "source": "https://www.newtiburon.com/",
    "last_scraped": "",
    "priority_contributors": ["Charlie-III", "chase206", "eagleprime", "The_Evenger"],
    "credibility_system": "credibility/README.md"
  },
  "threads": {
    "484870": {
      "title": "Big Strong Arms — Front Lower Control Arms for the Lemons Tiburons",
      "url": "https://www.newtiburon.com/threads/...",
      "section": "gk-wheel-tire-suspension",
      "reply_count": null,
      "has_priority_contributor": true,
      "tags": ["control-arms", "fabrication", "lemons", "heim-joint", "suspension", "g6ba"],
      "post_type": "build_log",
      "credibility_score": null,
      "contributor_weights": { "chase206": 5 },
      "scraped": false
    }
  }
}
```

**Credibility fields:** `post_type`, `credibility_score`, `contributor_weights` — see `credibility/scoring-algorithm.md`.

**Extraction metadata:** `engine` (V6/I4/both), `ecu_requirement` (stock/standalone/piggyback/reflash), `build_applicability` (which builds can use this), `has_collapsed_content`, `has_discontinued_parts`, `discontinued_parts[]`, `general_knowledge_value` — see `credibility/post-classification.md` for full definitions.

---

## Related Files

| File | Contents |
|------|----------|
| `forum/thread-index.json` | Searchable index of all threads (with credibility fields) |
| `forum/threads/{id}/metadata.json` | Thread metadata |
| `forum/threads/{id}/posts.json` | Post content |
| `forum/scraper.py` | Semi-automated scraping script (planned) |
| `credibility/sources.json` | Source registry — NewTiburon base credibility = 3/10 |
| `credibility/contributors.json` | Contributor weights for priority contributors |
| `credibility/forum-sections.json` | Forum section → KB topic mapping with modifiers |
| `credibility/scoring-algorithm.md` | Composite credibility formula |
| `credibility/post-classification.md` | Post type definitions (stickied_guide, question_post, etc.) |
| `validation/test-cases.json` | Forum questions used as KB test cases |
