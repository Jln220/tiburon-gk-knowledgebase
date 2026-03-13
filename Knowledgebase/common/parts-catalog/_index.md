# OEM Parts Catalog — Master Index

**Vehicle:** 2003 Hyundai Tiburon GK (USA/HMA) · 2.7L V6 G6BA · 6-speed manual
**Source:** `hyundai.catalogs-parts.com` (PDF printouts in `Sources/OEM Parts Catalogs/`)
**Extracted:** 2026-03-13
**Raw data:** `catalog-metadata.json`

## Groups

| Group | File | Subgroups | Total Parts | V6 Parts |
|-------|------|-----------|-------------|----------|
| EN | [engine.md](engine.md) | 48 | 1444 | 1444 |
| CH | [chassis.md](chassis.md) | 25 | 867 | 867 |
| EL | [electrical.md](electrical.md) | 34 | 496 | 496 |

## Integration with Knowledge Graph

Part numbers from this catalog are linked to component nodes in:
- `common/tiburon-knowledge-graph.json` — OEM platform components
- See `oem_part_numbers` field on component nodes

## V6 Filtering

- `v6_applicable: true` — part fits V6 (may also fit I4)
- `v6_only: true` — part is V6-exclusive (`[H] 2700 CC` filter in catalog)
- `v6_applicable: false` — I4-only part (exclude for white/blue car)

## Diagram Reference

Exploded diagrams are in the source PDFs. The PNC column matches callout
numbers on the diagrams. Open the corresponding PDF in `Sources/OEM Parts Catalogs/`
to see where each part fits in the assembly.