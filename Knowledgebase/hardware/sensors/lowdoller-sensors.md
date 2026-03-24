# Lowdoller Motorsports Combo Sensors — White Tiburon
## Pressure + Temperature in One Sensor

All sensors share the same temp element (PTC thermistor) and same wiring scheme.
All are Haltech-compatible with 0.5–4.5V pressure output and resistive temp output.
Compatible with Holley, FuelTech, Haltech, and similar ECUs.

---

## Wiring (Same for All Models)

| Wire | Function | Haltech Connection |
|------|----------|-------------------|
| **Red** | +5V supply | **34-pin connector pin 9** (O, orange) — +5V DC, 100mA max |
| **Black** | Pressure sensor ground | Signal ground: 26-pin pins 14–16 (B/W) |
| **Yellow** | Pressure signal (0.5–4.5V) | Haltech AVI input (0–5V range) |
| **White** | Temp sensor ground | Signal ground: 26-pin pins 14–16 (B/W) |
| **Green** | Temp signal (resistive) | Haltech AVI input (configured as temp) |

**Notes:**
- 8.5 ft flying leads — cut to length and add Deutsch DTM connectors (recommended by Lowdoller)
- Each sensor uses **2 analog input channels** (one for pressure, one for temp)
- Pressure is ratiometric voltage (0.5–4.5V). All Haltech AVI inputs accept 0–5V (20V max tolerant).
- Temp is resistive — use AVI with temp sensor mode and 1K pull-up enabled in NSP
- Already tested and configured in Haltech NSP

**PDM connection (standalone / no Haltech):**
- Red wire → PDM G16 (+5V Vref)
- Black + White wires → PDM G18 (GND)
- Yellow wire → PDM analog channel input (0–5V mode, no pull-up)
- Green wire → PDM analog channel input (0–5V mode, ✅ 10kΩ internal pull-up for PTC)
- See `builds/white-tiburon/guides/pdm-sensor-wiring-weekend.md` for full channel map

**Haltech Elite 2500 Sensor Supply Pins (34-pin connector):**
- **Pin 9 (O, orange): +5V DC** — 100mA max. Use this for all Lowdoller sensors.
- **Pin 12 (O/W, orange/white): +8V DC** — 1A max. For sensors requiring 8V (some OEM sensors, relays, solenoids). NOT for these sensors.

---

## Sensor 1: Fuel Pressure/Temp — 150 PSI (PN 899404)

**Application:** Fuel pressure & temp on return line (also suitable for oil, possibly trans)
**Product:** https://lowdoller-motorsports.com/collections/combo-pressure-and-temp-sensors/products/150-psi-pressure-temperature-combo-150-psi-500-f-pn-899404
**Thread:** 1/8" NPT
**Range:** 0–150 PSI, 0–500°F
**Accuracy:** 0.5% full scale
**Lead length:** 8.5 ft flying leads (cut to length; add Deutsch DTM connector — recommended)
**Construction:** ASIC chip, diffused silicon oil-filled, shock/vibration resistant, corrosion resistant, ultra-compact

### Pressure Calibration (0.5–4.5V Linear)

| Voltage | PSI |
|---------|-----|
| 0.50 | 0 |
| 0.77 | 10 |
| 1.03 | 20 |
| 1.30 | 30 |
| 1.57 | 40 |
| 1.83 | 50 |
| 2.10 | 60 |
| 2.37 | 70 |
| 2.63 | 80 |
| 2.90 | 90 |
| 3.17 | 100 |
| 3.43 | 110 |
| 3.70 | 120 |
| 3.97 | 130 |
| 4.23 | 140 |
| 4.50 | 150 |

**Linear formula:** PSI = (Voltage − 0.5) × 37.5

---

## Sensor 2: Oil Pressure/Temp — 150 PSI (PN 899404)

**Same sensor as fuel.** Second unit of PN 899404.
**Application:** Oil pressure & temp, direct mount to engine
**Thread:** 1/8" NPT
**Range:** 0–150 PSI, 0–500°F
**Accuracy:** 0.5% full scale
**Lead length:** 8.5 ft flying leads (cut to length; add Deutsch DTM connector)
**Construction:** ASIC chip, diffused silicon oil-filled, shock/vibration resistant, corrosion resistant, ultra-compact

*(Same calibration table as Sensor 1 above)*

---

## Sensor 3: Coolant Pressure/Temp — 100 PSI (LDM899TP100)

**Application:** Coolant pressure & temp
**Product:** https://lowdoller-motorsports.com/collections/combo-pressure-and-temp-sensors/products/m12-x-1-5-coolant-pressure-temperature-combo-100-psi-500-f
**Thread:** M12 x 1.5 with sealing ring (metric — confirm fits coolant manifold fitting)
**Range:** 0–100 PSI, 0–500°F
**Accuracy:** 0.5% full scale
**Lead length:** 8.5 ft flying leads (cut to length; add Deutsch DTM connector)
**Construction:** ASIC chip, diffused silicon oil-filled, shock/vibration resistant, corrosion resistant, ultra-compact

### Pressure Calibration (0.5–4.5V Linear)

| Voltage | PSI |
|---------|-----|
| 0.50 | 0 |
| 0.77 | 7 |
| 1.03 | 13 |
| 1.30 | 20 |
| 1.57 | 27 |
| 1.83 | 33 |
| 2.10 | 40 |
| 2.37 | 47 |
| 2.63 | 53 |
| 2.90 | 60 |
| 3.17 | 67 |
| 3.43 | 73 |
| 3.70 | 80 |
| 3.97 | 87 |
| 4.23 | 93 |
| 4.50 | 100 |

**Linear formula:** PSI = (Voltage − 0.5) × 25.0

---

## Sensor 4: Brake Pressure/Temp — 1500 PSI (PN 899405)

**Application:** Brake pressure & temp (install later — fittings to Jak)
**Model:** LDM899TP | **PN:** 899405
**Product:** https://lowdoller-motorsports.com/collections/combo-pressure-and-temp-sensors/products/brake-pressure-temperature-combo-1500-psi-500-f-pn-899405
**Thread:** 1/8" NPT
**Range:** 0–1500 PSI, 0–500°F
**Accuracy:** 0.5% full scale
**Lead length:** 8.5 ft flying leads (cut to length; add Deutsch DTM connector)
**Construction:** ASIC chip, diffused silicon oil-filled, shock/vibration resistant, corrosion resistant, ultra-compact

### Pressure Calibration (0.5–4.5V Linear)

| Voltage | PSI |
|---------|-----|
| 0.50 | 0 |
| 0.77 | 100 |
| 1.03 | 200 |
| 1.30 | 300 |
| 1.57 | 400 |
| 1.83 | 500 |
| 2.10 | 600 |
| 2.37 | 700 |
| 2.63 | 800 |
| 2.90 | 900 |
| 3.17 | 1000 |
| 3.43 | 1100 |
| 3.70 | 1200 |
| 3.97 | 1300 |
| 4.23 | 1400 |
| 4.50 | 1500 |

**Linear formula:** PSI = (Voltage − 0.5) × 375.0

---

## Temperature Calibration (Same for ALL Models)

**PTC thermistor — resistance INCREASES as temperature increases.**
(Opposite of typical automotive NTC sensors — requires custom calibration table in Haltech NSP.)

| Temp (°F) | Resistance (Ω) |
|-----------|----------------|
| -40 | 84.27 |
| -4 | 89.54 |
| 32 | 100 |
| 68 | 107.79 |
| 104 | 115.54 |
| 140 | 123.24 |
| 176 | 130.9 |
| 212 | 138.51 |
| 248 | 146.07 |
| 284 | 153.585 |
| 320 | 161.05 |
| 356 | 168.48 |
| 392 | 175.86 |
| 428 | 183.19 |
| 464 | 190.47 |
| 500 | 197.71 |

**Note:** PTC (positive temperature coefficient) — resistance increases with temperature. This is the opposite of OEM automotive NTC sensors. Haltech NSP supports custom resistance-vs-temperature tables; the PTC curve above has been configured as a custom cal table in NSP. Do NOT wire this to the OEM gauge cluster — the gauge expects NTC behavior and will read backwards.

**Haltech setup:** Enter this table as a custom calibration in Haltech NSP. Map resistance → temperature using the values above.

---

## Haltech AVI Channel Assignment Plan (White Tiburon)

Each combo sensor uses 2 AVI channels. 3 combo sensors = 6 AVI channels. Remaining 4 channels: IAT, wideband O2, crankcase pressure, TPS. Built-in MAP does NOT use an AVI channel.

| AVI Channel | Assignment | Signal Type | Calibration |
|-------------|-----------|-------------|-------------|
| AVI 1 | Fuel pressure | 0.5–4.5V | 150 PSI linear |
| AVI 2 | Fuel temp | Resistive | PTC custom table |
| AVI 3 | Oil pressure | 0.5–4.5V | 150 PSI linear |
| AVI 4 | Oil temp | Resistive | PTC custom table |
| AVI 5 | Coolant pressure | 0.5–4.5V | 100 PSI linear |
| AVI 6 | Coolant temp | Resistive | PTC custom table |
| AVI 7 | IAT | Resistive | NTC, 1K pull-up (Haltech default) |
| AVI 8 | Wideband O2 (Innovate LM2) | 0–5V | 7.35–22.39 AFR linear |
| AVI 9 | Crankcase pressure | 0–5V | Per sensor spec |
| AVI 10 | TPS | 0–5V | Haltech default |

**All 10 AVI channels used.** Brake combo (899405) and trans combo (899404) require expansion — see `builds/white-tiburon/signal-routing.md` for future expansion strategy. Options: Haltech TPS module (CAN-based, frees AVI 10), REM harness AVI inputs, CAN-based EGT module.
