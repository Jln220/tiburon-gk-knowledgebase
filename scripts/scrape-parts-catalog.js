/**
 * Hyundai Parts Catalog Scraper
 *
 * Extracts OEM part numbers, diagrams, and BOM data from hyundai.catalogs-parts.com
 * for the 2003 Hyundai Tiburon GK (USA market, 2.7L V6).
 *
 * Usage:
 *   1. Open Chrome to: https://hyundai.catalogs-parts.com/#{client:undefined;page:group;lang:en;catalog:hma;family:tiburon;catalog_code:hma2c0pa01;prm:01.c,02.g,03.h,04.6,05.7,dt.l,year.2003}
 *   2. Open DevTools Console (F12 → Console)
 *   3. Paste this entire script and press Enter
 *   4. Call: await scrapeAllGroups()    — full catalog
 *      or:  await scrapeGroup('EN')    — just ENGINE
 *      or:  await scrapePart('EN', '2022412')  — single subgroup
 *
 * Output: JSON object with all parts data, downloadable as .json file.
 *
 * Vehicle parameters (encoded in URL):
 *   catalog: hma (Hyundai Motor America)
 *   family: tiburon
 *   catalog_code: hma2c0pa01
 *   prm: 01.c,02.g,03.h,04.6,05.7,dt.l,year.2003
 *   → 2003 Tiburon, 2.7L V6 (G6BA), 6-speed manual
 *
 * Site API (discovered from catalog.js):
 *   /cat_scripts/get_group.php     → top-level groups (BODY, ENGINE, etc.)
 *   /cat_scripts/get_subgroup.php  → subgroups within a group
 *   /cat_scripts/get_part.php      → parts table + diagram for a subgroup
 *   /cat_scripts/get_detail.php    → supersession/cross-reference for a part
 *
 * Group codes: BO (Body), EN (Engine), MI (Transmission), CH (Chassis), TR (Trim), EL (Electrical)
 */

const CATALOG_CONFIG = {
  client: 'undefined',
  lang: 'en',
  catalog: 'hma',
  family: 'tiburon',
  catalog_code: 'hma2c0pa01',
  prm: '01.c,02.g,03.h,04.6,05.7,dt.l,year.2003',
  groups: ['BO', 'EN', 'MI', 'CH', 'TR', 'EL'],
  groupNames: {
    BO: 'BODY', EN: 'ENGINE', MI: 'TRANSMISSION',
    CH: 'CHASSIS', TR: 'TRIM', EL: 'ELECTRICAL'
  }
};

// Rate limiting — be respectful to the server
const DELAY_BETWEEN_PAGES_MS = 1500;
const DELAY_BETWEEN_GROUPS_MS = 3000;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Navigate to a subgroup listing page and extract all subgroup IDs
 */
async function getSubgroups(groupCode) {
  // Navigate to subgroup page via the site's own function
  subgroup_get(
    CATALOG_CONFIG.client, CATALOG_CONFIG.lang, CATALOG_CONFIG.catalog,
    CATALOG_CONFIG.family, CATALOG_CONFIG.catalog_code, CATALOG_CONFIG.prm,
    groupCode, ''
  );

  await sleep(DELAY_BETWEEN_PAGES_MS);

  // Wait for content to load (poll for onclick elements)
  let attempts = 0;
  while (attempts < 10) {
    const els = document.querySelectorAll('[onclick*="part_get"]');
    if (els.length > 0) break;
    await sleep(500);
    attempts++;
  }

  const clickables = document.querySelectorAll('[onclick]');
  const subgroups = [];

  for (const el of clickables) {
    const onclick = el.getAttribute('onclick') || '';
    const match = onclick.match(/part_get\([^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,'(\w+)','(\d+)'/);
    if (match) {
      // Extract the section code from the text, e.g. "[20-224]"
      const text = el.textContent.trim();
      const codeMatch = text.match(/\[([^\]]+)\]/);
      subgroups.push({
        group: match[1],
        id: match[2],
        sectionCode: codeMatch ? codeMatch[1] : null,
        name: text.replace(/^\[[^\]]+\]\s*-\s*/, '')
      });
    }
  }

  console.log(`  Found ${subgroups.length} subgroups in ${CATALOG_CONFIG.groupNames[groupCode]}`);
  return subgroups;
}

/**
 * Navigate to a part page and extract the parts table
 */
async function getPartTable(groupCode, subgroupId) {
  // Navigate via the site's own function
  part_get(
    CATALOG_CONFIG.client, CATALOG_CONFIG.lang, CATALOG_CONFIG.catalog,
    CATALOG_CONFIG.family, CATALOG_CONFIG.catalog_code, CATALOG_CONFIG.prm,
    groupCode, subgroupId, ''
  );

  await sleep(DELAY_BETWEEN_PAGES_MS);

  // Wait for table to load
  let attempts = 0;
  while (attempts < 10) {
    const rows = document.querySelectorAll('table tr');
    if (rows.length > 1) break;
    await sleep(500);
    attempts++;
  }

  const rows = document.querySelectorAll('table tr');
  const parts = [];

  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].querySelectorAll('td');
    if (cells.length >= 6) {
      const part = {
        pnc: (cells[0]?.textContent || '').trim(),
        partNumber: (cells[1]?.textContent || '').trim(),
        qty: parseInt((cells[2]?.textContent || '0').trim()) || 0,
        partName: (cells[3]?.textContent || '').trim(),
        modelDescription: (cells[4]?.textContent || '').trim(),
        startDate: (cells[5]?.textContent || '').trim(),
        endDate: (cells[6]?.textContent || '').trim()
      };
      // Skip empty rows
      if (part.pnc && part.partNumber) {
        parts.push(part);
      }
    }
  }

  // Get the diagram image URL if present
  const diagImg = document.querySelector('img[src*="img"]');
  const diagramUrl = diagImg ? diagImg.src : null;

  // Get the page title
  const title = document.querySelector('h1, h2');
  const pageTitle = title ? title.textContent.trim() : '';

  return { parts, diagramUrl, pageTitle };
}

/**
 * Scrape a single part page by group + subgroup ID
 */
async function scrapePart(groupCode, subgroupId) {
  console.log(`Scraping ${groupCode}/${subgroupId}...`);
  const result = await getPartTable(groupCode, subgroupId);
  console.log(`  → ${result.parts.length} parts found: ${result.pageTitle}`);
  return result;
}

/**
 * Scrape all subgroups within a single group
 */
async function scrapeGroup(groupCode) {
  console.log(`\n=== Scraping ${CATALOG_CONFIG.groupNames[groupCode]} (${groupCode}) ===`);

  const subgroups = await getSubgroups(groupCode);
  const results = [];

  for (let i = 0; i < subgroups.length; i++) {
    const sg = subgroups[i];
    console.log(`  [${i + 1}/${subgroups.length}] ${sg.sectionCode} - ${sg.name}`);

    const data = await getPartTable(groupCode, sg.id);

    results.push({
      group: groupCode,
      groupName: CATALOG_CONFIG.groupNames[groupCode],
      subgroupId: sg.id,
      sectionCode: sg.sectionCode,
      subgroupName: sg.name,
      diagramUrl: data.diagramUrl,
      parts: data.parts
    });

    // Rate limit
    if (i < subgroups.length - 1) {
      await sleep(DELAY_BETWEEN_PAGES_MS);
    }
  }

  console.log(`\n  Total: ${results.reduce((sum, r) => sum + r.parts.length, 0)} parts across ${results.length} subgroups`);
  return results;
}

/**
 * Scrape the entire catalog — all 6 groups
 */
async function scrapeAllGroups() {
  console.log('Starting full catalog scrape...');
  console.log(`Vehicle: 2003 Hyundai Tiburon (USA) 2.7L V6`);
  console.log(`Source: hyundai.catalogs-parts.com\n`);

  const catalog = {
    _meta: {
      vehicle: '2003 Hyundai Tiburon GK',
      engine: '2.7L V6 (G6BA)',
      market: 'USA (HMA)',
      source: 'hyundai.catalogs-parts.com',
      catalogCode: CATALOG_CONFIG.catalog_code,
      scrapedAt: new Date().toISOString(),
      scriptVersion: '1.0'
    },
    groups: {}
  };

  for (const groupCode of CATALOG_CONFIG.groups) {
    catalog.groups[groupCode] = await scrapeGroup(groupCode);
    await sleep(DELAY_BETWEEN_GROUPS_MS);
  }

  // Summary
  let totalParts = 0;
  let totalSubgroups = 0;
  for (const [code, subgroups] of Object.entries(catalog.groups)) {
    totalSubgroups += subgroups.length;
    totalParts += subgroups.reduce((sum, sg) => sum + sg.parts.length, 0);
  }

  catalog._meta.totalSubgroups = totalSubgroups;
  catalog._meta.totalParts = totalParts;

  console.log(`\n========================================`);
  console.log(`Scrape complete!`);
  console.log(`  Groups: ${Object.keys(catalog.groups).length}`);
  console.log(`  Subgroups: ${totalSubgroups}`);
  console.log(`  Total parts: ${totalParts}`);
  console.log(`========================================\n`);

  // Auto-download as JSON
  downloadJSON(catalog, 'tiburon-2003-v6-parts-catalog.json');

  return catalog;
}

/**
 * Download a JSON object as a file
 */
function downloadJSON(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  console.log(`Downloaded: ${filename}`);
}

/**
 * Quick search: find a part number across already-scraped data
 */
function findPart(catalog, query) {
  const results = [];
  const q = query.toLowerCase();
  for (const [groupCode, subgroups] of Object.entries(catalog.groups)) {
    for (const sg of subgroups) {
      for (const part of sg.parts) {
        if (part.partNumber.toLowerCase().includes(q) ||
            part.partName.toLowerCase().includes(q) ||
            part.pnc.toLowerCase().includes(q)) {
          results.push({
            group: sg.groupName,
            section: `${sg.sectionCode} - ${sg.subgroupName}`,
            ...part
          });
        }
      }
    }
  }
  return results;
}

console.log('Parts Catalog Scraper loaded!');
console.log('Commands:');
console.log('  await scrapeAllGroups()       — scrape entire catalog (~300+ pages, ~20 min)');
console.log('  await scrapeGroup("EN")       — scrape just ENGINE');
console.log('  await scrapePart("EN","2022412") — scrape single subgroup');
console.log('  findPart(catalog, "gasket")   — search scraped data');
