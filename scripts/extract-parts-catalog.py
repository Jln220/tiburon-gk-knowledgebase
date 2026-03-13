#!/usr/bin/env python3
"""
Extract parts catalog data from OEM parts catalog PDFs.
Source: Sources/OEM Parts Catalogs/ (Engine, Chassis, Electrical folders)
Output: Knowledgebase/common/parts-catalog/ (JSON + Markdown per section)

Usage:
    python scripts/extract-parts-catalog.py

Output files:
    Knowledgebase/common/parts-catalog/catalog-metadata.json  (full raw data)
    Knowledgebase/common/parts-catalog/engine.md
    Knowledgebase/common/parts-catalog/chassis.md
    Knowledgebase/common/parts-catalog/electrical.md
    Knowledgebase/common/parts-catalog/_index.md
"""

import fitz
import re
import os
import json
from pathlib import Path
from datetime import date

# Paths
REPO_ROOT = Path(__file__).parent.parent
SOURCES = REPO_ROOT / "Sources" / "OEM Parts Catalogs"
OUTPUT = REPO_ROOT / "Knowledgebase" / "common" / "parts-catalog"

CATALOG_FOLDERS = {
    "EN": ("Engine Parts Catalog", "ENGINE"),
    "CH": ("Chassis Parts Catalog", "CHASSIS"),
    "EL": ("Electrical Parts Catalog", "ELECTRICAL"),
}

# Model description keywords that indicate engine applicability
MODEL_DESC_KEYWORDS = [
    "Engine Capacity", "Fuel Type", "Transmission", "Option Codes",
    "Market", "Emission", "Body Type", "[H]", "[G]", "[+]"
]

# V6 indicator
V6_INDICATOR = "2700 CC"
I4_INDICATOR = "2000 CC"


def join_name_fragments(fragments):
    """Join name fragments intelligently, handling mid-word line breaks.

    PDF line breaks can occur mid-word (e.g., "EXHAUST" → "EXHAUS" + "T").
    Heuristics:
    - Next fragment is 1-3 chars: assume mid-word continuation, no space
    - Prev fragment ends with '-' or '/': continuation, no space
    - Otherwise: word boundary, add space
    """
    if not fragments:
        return ""
    result = fragments[0]
    for frag in fragments[1:]:
        if not frag:
            continue
        if result and result[-1] in ("-", "/"):
            # Continuation after hyphen or slash
            result += frag
        elif len(frag) <= 3 and frag.isalpha():
            # Very short fragment = likely mid-word line break (e.g., "UNIT" → "UNI" + "T")
            result += frag
        else:
            result += " " + frag
    return re.sub(r'\s+', ' ', result).strip()


def split_model_desc_from_text(lines):
    """Split part name lines from model description lines."""
    name_lines = []
    model_lines = []
    in_model = False
    for line in lines:
        if any(kw in line for kw in MODEL_DESC_KEYWORDS):
            in_model = True
        if in_model:
            model_lines.append(line)
        else:
            name_lines.append(line)
    return name_lines, model_lines


def parse_parts_page(page):
    """Parse a parts table page into a list of part dicts."""
    blocks = page.get_text('blocks')

    # Filter to data blocks only
    data_blocks = []
    for b in blocks:
        x0, y0, x1, y1, text, _, btype = b
        t = text.strip()
        if not t:
            continue
        # Skip icons, footers, headers
        if re.match(r'^[\ue000-\uf8ff\n ]+$', t):
            continue  # Private use area chars (icons)
        if 'hyundai.catalogs-parts.com' in t:
            continue
        if re.match(r'^\d+/\d+/\d+,?\s*\d+:\d+', t):
            continue  # Date/time header
        if t.startswith('Menu'):
            continue
        if t.startswith('Warning'):
            continue
        if t.startswith('PNC') or 'Qty Part Name' in t:
            continue  # Column headers
        data_blocks.append((x0, y0, x1, y1, t))

    # Group blocks into rows by overlapping y ranges (+/- 5px tolerance)
    rows = []
    for block in sorted(data_blocks, key=lambda b: b[1]):
        x0, y0, x1, y1, text = block
        placed = False
        for row in rows:
            for rb in row:
                ry0, ry1 = rb[1], rb[3]
                if y0 < ry1 + 8 and y1 > ry0 - 8:
                    row.append(block)
                    placed = True
                    break
            if placed:
                break
        if not placed:
            rows.append([block])

    parts = []
    for row in rows:
        row.sort(key=lambda b: b[0])  # Sort by x position

        left_block = None
        model_desc_blocks = []
        date_block = None

        for b in row:
            x0, y0, x1, y1, text = b
            if x0 < 160:
                left_block = text
            elif x0 >= 155 and x0 < 400 and any(kw in text for kw in MODEL_DESC_KEYWORDS):
                model_desc_blocks.append(text)
            elif x0 >= 380:
                # Date block (matches date pattern)
                if re.search(r'\d{2}\.\d{2}\.\d{4}', text):
                    date_block = text

        if not left_block:
            continue

        lines = [l.strip() for l in left_block.split('\n') if l.strip()]
        if len(lines) < 2:
            continue

        pnc = lines[0]
        part_number = lines[1] if len(lines) > 1 else ''

        # Skip title rows (part number looks like text, not a number)
        if not re.match(r'^[0-9A-Z]{8,}$', part_number) and not re.match(r'^\d{8,}$', part_number):
            # Skip if part number doesn't look like an OEM part number (8+ alphanumeric)
            continue

        qty = lines[2] if len(lines) > 2 else ''

        # Lines from index 3 onward are name + possibly model desc
        remaining_lines = lines[3:] if len(lines) > 3 else []

        # Check if model desc keywords appear in left block
        name_lines, inline_model_lines = split_model_desc_from_text(remaining_lines)

        # Remove date lines from name
        name_fragments = []
        date_in_left = ''
        for line in name_lines:
            if re.match(r'\d{2}\.\d{2}\.\d{4}', line):
                date_in_left = line
                break
            name_fragments.append(line)

        part_name = join_name_fragments(name_fragments)

        # Combine model description from all sources
        model_desc_parts = inline_model_lines + model_desc_blocks
        model_desc_raw = ' '.join(model_desc_parts)
        model_desc = re.sub(r'\s+', ' ', model_desc_raw).strip()
        # Clean up broken words in model desc
        model_desc = model_desc.replace('MPI- DOHC', 'MPI-DOHC')
        model_desc = model_desc.replace('SPEED ', 'SPEED')

        # Dates
        date_source = date_block or date_in_left
        date_matches = re.findall(r'\d{2}\.\d{2}\.\d{4}', date_source) if date_source else []
        start_date = date_matches[0] if date_matches else ''
        end_date = date_matches[1] if len(date_matches) > 1 else ''

        # Determine V6 applicability
        if V6_INDICATOR in model_desc or I4_INDICATOR in model_desc:
            v6_only = V6_INDICATOR in model_desc and I4_INDICATOR not in model_desc
            v6_applicable = V6_INDICATOR in model_desc
        else:
            v6_only = False
            v6_applicable = True  # No engine filter = fits all engines

        if part_number and pnc and part_name:
            parts.append({
                'pnc': pnc,
                'part_number': part_number,
                'qty': qty,
                'name': part_name,
                'model_desc': model_desc,
                'start_date': start_date,
                'end_date': end_date,
                'v6_applicable': v6_applicable,
                'v6_only': v6_only,
            })

    return parts


def extract_subgroup_from_filename(filename):
    """Extract subgroup name from PDF filename."""
    # e.g. "CAMSHAFT & VALVE (01_03) HYUNDAI TIBURON 03 (2003-).pdf"
    # → "CAMSHAFT & VALVE (01/03)"
    name = filename.replace('.pdf', '')
    name = name.replace(' HYUNDAI TIBURON 03 (2003-)', '').strip()
    # Convert "(01_03)" to "(01/03)"
    name = re.sub(r'\((\d+)_(\d+)\)', r'(\1/\2)', name)
    return name


def process_catalog_folder(folder_path, group_code, group_name):
    """Process all PDFs in a catalog folder."""
    subgroups = {}
    pdf_files = sorted(folder_path.glob('*.pdf'))
    print(f"  Processing {group_name}: {len(pdf_files)} PDFs...")

    for pdf_file in pdf_files:
        subgroup_name = extract_subgroup_from_filename(pdf_file.name)
        print(f"    {subgroup_name}...", end=' ')

        try:
            doc = fitz.open(str(pdf_file))
            all_parts = []
            for page in doc:
                parts = parse_parts_page(page)
                all_parts.extend(parts)
            doc.close()
            print(f"{len(all_parts)} parts")
            subgroups[subgroup_name] = all_parts
        except Exception as e:
            print(f"ERROR: {e}")
            subgroups[subgroup_name] = []

    return subgroups


def deduplicate_parts(parts):
    """Remove duplicate part entries (same PN + same model desc)."""
    seen = set()
    unique = []
    for p in parts:
        key = (p['part_number'], p['model_desc'], p['start_date'])
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def generate_markdown(group_code, group_name, subgroups, extraction_date):
    """Generate markdown output for a catalog group."""
    total_parts = sum(len(parts) for parts in subgroups.values())
    total_v6 = sum(
        sum(1 for p in parts if p['v6_applicable'])
        for parts in subgroups.values()
    )

    lines = [
        f"---",
        f"source: hyundai.catalogs-parts.com",
        f"catalog_code: hma2c0pa01",
        f"group: {group_code}",
        f"group_name: {group_name}",
        f"vehicle: 2003 Hyundai Tiburon (GK)",
        f"engine: V6 (2.7L Delta G6BA) and I4 (2.0L Beta G4GC) — filter by v6_applicable",
        f"market: USA (HMA)",
        f"extraction_method: pdf_text_extraction (pymupdf)",
        f"extraction_date: {extraction_date}",
        f"subgroup_count: {len(subgroups)}",
        f"total_parts: {total_parts}",
        f"v6_applicable_parts: {total_v6}",
        f"---",
        f"",
        f"# {group_name} — OEM Parts Catalog",
        f"",
        f"Source: `Sources/OEM Parts Catalogs/{group_name.title()} Parts Catalog/`",
        f"Vehicle: 2003 Hyundai Tiburon GK · USA (HMA) · V6 2.7L G6BA · 6-speed manual",
        f"",
        f"**V = V6 applicable** (blank = I4 only, ✓ = fits both/all, V = V6-specific)",
        f"",
    ]

    for subgroup_name, parts in subgroups.items():
        if not parts:
            continue

        v6_parts = [p for p in parts if p['v6_applicable']]
        lines.append(f"## {subgroup_name}")
        lines.append(f"")

        if not v6_parts:
            lines.append(f"*No V6-applicable parts in this subgroup.*")
            lines.append(f"")
            continue

        lines.append(f"| PNC | Part Number | Qty | Part Name | Engine Filter | Dates |")
        lines.append(f"|-----|-------------|-----|-----------|---------------|-------|")

        for p in v6_parts:
            # Abbreviate model desc for table
            if p['v6_only']:
                engine_col = "V6 only"
            elif p['model_desc']:
                engine_col = "V6+I4"
            else:
                engine_col = "all"

            date_range = ""
            if p['start_date'] or p['end_date']:
                date_range = f"{p['start_date']}–{p['end_date']}"

            # Clean name for table (escape pipes)
            name = p['name'].replace('|', '/')

            lines.append(
                f"| {p['pnc']} | `{p['part_number']}` | {p['qty']} | {name} | {engine_col} | {date_range} |"
            )

        lines.append(f"")

    return '\n'.join(lines)


def generate_index(catalog_data, extraction_date):
    """Generate master index markdown."""
    lines = [
        f"# OEM Parts Catalog — Master Index",
        f"",
        f"**Vehicle:** 2003 Hyundai Tiburon GK (USA/HMA) · 2.7L V6 G6BA · 6-speed manual",
        f"**Source:** `hyundai.catalogs-parts.com` (PDF printouts in `Sources/OEM Parts Catalogs/`)",
        f"**Extracted:** {extraction_date}",
        f"**Raw data:** `catalog-metadata.json`",
        f"",
        f"## Groups",
        f"",
        f"| Group | File | Subgroups | Total Parts | V6 Parts |",
        f"|-------|------|-----------|-------------|----------|",
    ]

    for group_code, group_data in catalog_data.items():
        subgroups = group_data['subgroups']
        group_name = group_data['name']
        total = sum(len(p) for p in subgroups.values())
        v6 = sum(sum(1 for p in parts if p['v6_applicable']) for parts in subgroups.values())
        fname = group_name.lower() + ".md"
        lines.append(f"| {group_code} | [{fname}]({fname}) | {len(subgroups)} | {total} | {v6} |")

    lines += [
        f"",
        f"## Integration with Knowledge Graph",
        f"",
        f"Part numbers from this catalog are linked to component nodes in:",
        f"- `common/tiburon-knowledge-graph.json` — OEM platform components",
        f"- See `oem_part_numbers` field on component nodes",
        f"",
        f"## V6 Filtering",
        f"",
        f"- `v6_applicable: true` — part fits V6 (may also fit I4)",
        f"- `v6_only: true` — part is V6-exclusive (`[H] 2700 CC` filter in catalog)",
        f"- `v6_applicable: false` — I4-only part (exclude for white/blue car)",
        f"",
        f"## Diagram Reference",
        f"",
        f"Exploded diagrams are in the source PDFs. The PNC column matches callout",
        f"numbers on the diagrams. Open the corresponding PDF in `Sources/OEM Parts Catalogs/`",
        f"to see where each part fits in the assembly.",
    ]

    return '\n'.join(lines)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    extraction_date = str(date.today())

    catalog_data = {}

    for group_code, (folder_name, group_name) in CATALOG_FOLDERS.items():
        folder_path = SOURCES / folder_name
        if not folder_path.exists():
            print(f"WARNING: {folder_path} not found, skipping.")
            continue

        subgroups = process_catalog_folder(folder_path, group_code, group_name)
        catalog_data[group_code] = {
            'name': group_name,
            'folder': folder_name,
            'subgroups': subgroups,
        }

    # Write raw JSON
    json_output = {}
    for gc, gdata in catalog_data.items():
        json_output[gc] = {
            'name': gdata['name'],
            'subgroups': gdata['subgroups'],
        }

    json_path = OUTPUT / "catalog-metadata.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {json_path}")

    # Write markdown per group
    for group_code, gdata in catalog_data.items():
        md = generate_markdown(group_code, gdata['name'], gdata['subgroups'], extraction_date)
        fname = gdata['name'].lower() + ".md"
        md_path = OUTPUT / fname
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"Wrote: {md_path}")

    # Write index
    index_md = generate_index(catalog_data, extraction_date)
    index_path = OUTPUT / "_index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_md)
    print(f"Wrote: {index_path}")

    print("\nDone.")


if __name__ == '__main__':
    main()
