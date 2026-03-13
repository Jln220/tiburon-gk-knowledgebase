# Haltech Elite 2500 — 26-Pin Connector (B)
**Source:** `Haltech/main-connector-26-pin-elite2500.pdf` + Haltech Support Center
**URL:** https://support.haltech.com/portal/en/kb/articles/main-connector-26-pin-elite2500

---

## Pinout — Looking Into Connector on ECU

| Pin | Wire Color | Connection | Notes |
|-----|-----------|------------|-------|
| 1 | Y (shd) | Crank (Trigger) (+) | Supports digital and reluctor-based sensors |
| 2 | Y (shd) | Cam (Home) (+) | Supports digital and reluctor-based sensors |
| 3 | GY | AVI 7 (Air Temp) | 0–5V signal input, switchable 1K pull-up |
| 4 | V | AVI 8 (Coolant Temp) | 0–5V signal input, switchable 1K pull-up |
| 5 | G (shd) | Crank (Trigger) (−) | Ground reference for reluctor-based sensors |
| 6 | G (shd) | Cam (Home) (−) | Ground reference for reluctor-based sensors |
| 7 | GY/R (shd) | SPI 4 | 50 kHz max, 25V DC max input |
| 8 | GY (shd) | SPI 1 | 50 kHz max, 25V DC max input |
| 9 | GY/B (shd) | SPI 2 | 50 kHz max, 25V DC max input |
| 10 | GY/BR (shd) | SPI 3 | 50 kHz max, 25V DC max input |
| 11 | R/W | +13.8V ECU Supply (ECU Power) | 12V input to ECU |
| 12 | GY/O (shd) | AVI 6 (O2 Input 1) | 0–5V, compatible with narrow-band O2 sensors |
| 13 | GY/Y (shd) | AVI 1 (O2 Input 2) | 0–5V, compatible with narrow-band O2 sensors |
| 14 | B/W | Signal Ground | Sensor ground reference |
| 15 | B/W | Signal Ground | Sensor ground reference |
| 16 | B/W | Signal Ground | Sensor ground reference |
| 17 | Y/V | IGN 7 | 1A max current |
| 18 | Y/GY | IGN 8 | 1A max current |
| 19 | V/O | DPO 4 | 1A max, output to ground, fixed 12V pull-up |
| 20 | O/G | AVI 5 | 0–5V signal input, switchable 1K pull-up |
| 21 | GY/G | Knock 1 | Supports piezoelectric knock sensors |
| 22 | GY/L | Knock 2 | Supports piezoelectric knock sensors |
| 23 | W | CAN H | CAN Hi (ISO 11898), selectable Haltech or vehicle bus |
| 24 | L | CAN L | CAN Lo (ISO 11898), selectable Haltech or vehicle bus |
| 25 | BR/B | DBW 1 / DPO | 5A peak, 1A avg, 100 kHz max |
| 26 | BR/R | DBW 2 / DPO | 5A peak, 1A avg, 100 kHz max |

## White Tiburon Assignments

| Pin | Wire | Assignment | Notes |
|-----|------|------------|-------|
| 1 | Y (shd) | Crank trigger + | G6BA CKP sensor (39180-37150 / NTK EH0220) |
| 2 | Y (shd) | Cam home + | G6BA CMP sensor (39350-37100 / NTK EC0145) |
| 3 | GY | AVI 7 — IAT | Intake air temp sensor (Haltech default) |
| 4 | V | AVI 8 — Wideband O2 | Innovate LM2 Analog Out 1 (0–5V, 7.35–22.39 AFR) |
| 5 | G (shd) | Crank trigger − | Signal ground ref |
| 6 | G (shd) | Cam home − | Signal ground ref |
| 11 | R/W | ECU power input | From PDM LP1 (A14) |
| 12 | GY/O (shd) | AVI 6 — Coolant temp | Lowdoller LDM899TP100 green wire |
| 13 | GY/Y (shd) | AVI 1 — Fuel pressure | Lowdoller 899404 yellow wire |
| 14–16 | B/W | Signal ground | All Lowdoller black + white wires here |
| 20 | O/G | AVI 5 — Coolant pressure | Lowdoller LDM899TP100 yellow wire |
| 21 | GY/G | Knock 1 | OEM knock sensor |
| 22 | GY/L | Knock 2 | OEM knock sensor |
| 23 | W | CAN H → PDM CAN ECU | PDM Connector A pin 30 (A30) — 500 kbps |
| 24 | L | CAN L → PDM CAN ECU | PDM Connector A pin 31 (A31) — 500 kbps |
