---
source: SD.pdf
chapter: SD
section: SD-52 to SD-55
pages: 52-55
title: Charging System
---

# Charging System

**SD-52 -- Charging System (1) -- 2.0L / 1.6L**
**SD-53 -- Charging System (2) -- 2.7L**
**SD-54 -- Component Location Index**
**SD-55 -- Memo (blank)**

---

## Charging System (1) -- 2.0L / 1.6L (SD-52)

### Component Table

| Component | Connector | Pin | Wire Color | Wire Size |
|-----------|-----------|-----|------------|-----------|
| Battery (+) terminal | E28 | -- | R | 20B |
| Battery ground | -- | -- | B | 20B |
| Battery fusible link (100A) | -- | -- | R | 5.0/R |
| ECU fusible link | -- | -- | R | 3.0B |
| Joint connector | E56 | -- | R | -- |
| Ignition switch (M04) | IG1 | -- | R | 3.0B |
| BCM-LM | pin 4 | -- | R | 3.0B |
| BCM-CE | pin 13 | -- | W | 2.0R/B |
| BCM-IM | -- | -- | -- | -- |
| Fuse 17 | -- | -- | -- | -- |
| Pre-excitation resistor | -- | -- | -- | -- |
| Instrument cluster (M10-1) | pin 12 | -- | L | 0.5L |
| Instrument cluster (M10-2) | pin 3 | CHARGE | -- | 0.5R/O |
| Generator (E20-1) | B+ | BATTERY | R | 5.0B |
| Generator (E20-2) | L | LAMP | W | 0.85S |
| Generator (E20-2) | S | SENSING | W | 0.85S |

### Generator Internal (2.0L)

| Terminal | Function | Internal Connection |
|----------|----------|---------------------|
| B+ (E20-1) | Battery output | Rectifier output |
| S (E20-2) | Sensing | Voltage sensing |
| L (E20-2) | Lamp | Field/regulator via lamp indicator |
| FIELD | Field winding | Regulator controlled |
| R1, R2 | Rectifier diodes | Stator coil to DC |

### Circuit Paths (2.0L / 1.6L)

#### Main Charge Output
```
Generator B+ (E20-1) → [R, 5.0B] → Battery fusible link 100A → [R] → Battery (+) E28
```

#### Charge Lamp / Excitation Circuit
```
IGN SW (IG1) → [R, 3.0B] → BCM-LM → See Power Distribution
  → Fuse 17 → Pre-excitation resistor → [W, 0.85S] → Generator L terminal (E20-2)
```

#### Charge Indicator
```
BCM-CE pin 13 → [W, 2.0R/B] → [0.5W] → [5.5W] → [0.3G] → [0.5R/O] → BCM-IM
  → M10-2 pin 3 (CHARGE indicator) → Instrument cluster
```

#### Sensing
```
Generator S terminal (E20-2) → [W, 0.85S] → [0.9G] → EE01 → BCM-CE
```

---

## Charging System (2) -- 2.7L (SD-53)

### Component Table

| Component | Connector | Pin | Wire Color | Wire Size |
|-----------|-----------|-----|------------|-----------|
| Battery (+) terminal | E28 | -- | R | 20B |
| Battery ground | -- | -- | B | 20B |
| ECU fusible link (80A) | -- | -- | R | 5.0B |
| Generator fusible link (120A) | -- | -- | R | 20B |
| Joint connector | E56 | -- | R | -- |
| Ignition switch (M04) | IG1 | -- | R | 3.0B |
| BCM-LM | pin 4 | -- | R | 3.0B |
| BCM-CE | pin 13 | -- | W | 2.0R/B |
| BCM-IM | -- | -- | -- | -- |
| Fuse 17 | -- | -- | -- | -- |
| Pre-excitation resistor | -- | -- | -- | -- |
| Instrument cluster (M10-1) | pin 12 | -- | L | 0.5L |
| Instrument cluster (M10-2) | pin 3 | CHARGE | -- | 0.5R/O |
| Generator (E61-1) | B+ | BATTERY | R | 5.0B |
| Generator (E61-2) | L | LAMP | W | 0.85S |
| Generator (E61-2) | S | SENSING | W | 0.85S |

### Generator Internal (2.7L)

| Terminal | Function | Internal Connection |
|----------|----------|---------------------|
| B+ (E61-1) | Battery output | Rectifier output |
| S (E61-2) | Sensing | Voltage sensing |
| L (E61-2) | Lamp | Field/regulator via lamp indicator |
| FIELD | Field winding | Regulator controlled |
| R1, R2 | Rectifier diodes | Stator coil to DC |

### Circuit Paths (2.7L)

#### Main Charge Output
```
Generator B+ (E61-1) → [R, 5.0B] → Generator fusible link 120A → [R, 20B] → Battery (+) E28
```

#### Charge Lamp / Excitation Circuit
```
IGN SW (IG1) → [R, 3.0B] → BCM-LM → See Power Distribution
  → Fuse 17 → Pre-excitation resistor → [W, 0.85S] → Generator L terminal (E61-2)
```

#### Charge Indicator to Cluster
```
BCM-CE pin 13 → [0.85U] → [0.9G] → [0.5G] → [0.5R/O] → BCM-IM
  → M10-2 pin 3 (CHARGE indicator) → Instrument cluster
```

#### Sensing
```
Generator S terminal (E61-2) → [W, 0.85S] → [0.5L] → EE01 → BCM-CE
```

---

## Ground Points

| Ground ID | Location | Components |
|-----------|----------|------------|
| (Battery ground) | Engine block | Battery negative cable, 20B |

---

## Component Location Index (SD-54)

| Component | Description | Location Page |
|-----------|-------------|---------------|
| E20-1 | Generator (B+) (2.0L) | -- |
| E20-2 | Generator (L, S) (2.0L) | -- |
| E28 | Battery (+) terminal | -- |
| E56 | Joint connector | -- |
| E61-1 | Generator (B+) (2.7L) | -- |
| E61-2 | Generator (L, S) (2.7L) | -- |
| M04 | Ignition switch | -- |
| M10-1 | Instrument cluster | -- |
| M10-2 | Instrument cluster | -- |

### Connectors

| Connector | Location Page |
|-----------|---------------|
| BCM-CE | -- |
| BCM-IM | -- |
| BCM-LM | -- |
| EE01 | -- |

---

## Notes

- The generator produces AC voltage in its windings as it is belt-driven by the engine. The rectifier converts AC to DC voltage.
- The voltage regulator, included in the generator frame, controls the generator output to meet electrical system requirements. The regulator also controls the charge warning lamp.
- Fuse 17 supplies battery voltage to the charge warning indicator. With the engine not running and the ignition switch in ON, terminal L of the regulator is grounded internally and the indicator lights up.
- A small amount of current provided by both the charge warning lamp and the pre-excitation resistor is used to "excite" the magnetic field windings to start the charging process.
- With the engine running and the generator charging, terminal L voltage rises and the indicator goes out. If the generator fails to charge, terminal L remains below battery voltage and the indicator remains lit.
- **V6 build note:** The 2.7L uses generator connectors E61-1 (B+) and E61-2 (L, S) with a 120A fusible link.

### Exciter Wire Identification

The **exciter wire** is the **L (LAMP)** terminal — not the S (SENSING) terminal.

- **L / LAMP** = Exciter wire. Carries initial field current from the ignition switch through Fuse 17 and the pre-excitation resistor to energize the alternator's field coil and initiate charging. This wire also drives the dash charge warning light. On the 2.0L/1.6L it is at connector E20-2; on the 2.7L it is at connector E61-2.
- **S / SENSING** = Voltage feedback wire. Provides a battery voltage reference to the internal regulator so it can compensate for wiring voltage drop and accurately regulate output. It does not excite the field.
