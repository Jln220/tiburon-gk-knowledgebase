# Race Studio 3 — Session 1: Tiburon Config from Webinar Starting Point

**Goal:** Configure PDM32 for white Tiburon starting from `Webinar complete.zconfig`
**Time estimate:** 60–90 minutes
**Source file analysis:** Webinar config has SafeIgnition, StarterKYD, SirenKYD, LightsKYD, FanKYD, FuelSV, FanSpeed, Starter, Siren, Fuel1A/B, plus all keypad color channels — ~80% reusable.

**Before you start:** Export a backup of the webinar config to `AIM PDM/` before making any changes.

---

## What the Webinar Config Already Has

| Webinar Variable | What It Does | Tiburon Action |
|---|---|---|
| `SafeIgnition` | ON when PDM IGN input (B23) active | **Keep as-is** — this is our master permissive |
| `StarterKYD` | Latched toggle from keypad press | **Keep, remap to Key 01** |
| `SirenKYD` | Momentary from keypad press | **Keep, rename HornKYD, remap to Key 02** |
| `LightsKYD` | Latched toggle from keypad press | **Keep, remap to Key 03** |
| `FanKYD` | Latched toggle from keypad press | **Keep, remap to Key 05** |
| `IgnitionKYD` | Was Key 05 — keypad-controlled ignition | **Delete — we use physical IGN switch (B23)** |
| `FuelSV` | Composite fuel pump run condition | **Keep, update logic** |
| `FANOFFSV` | Fan manual off state | **Keep** |
| `FlashSV` | Momentary flash state | **Keep** |
| `momentary_SW` | Physical momentary switch template | **Repurpose → START_BACKUP on Ch09** |
| `ColorsConditionK01–K12` | Keypad LED color logic | **Keep, update per new key assignments** |
| `BitRed/Green/BlueX15–X1C` | RGB color bits for keypad LEDs | **Keep** |

| Webinar Output | HW Channel | Webinar Setting | Tiburon Action |
|---|---|---|---|
| `Starter` | HP (series diode) | OVC, 20A, inductive, DC | **Keep → HP1, rename Starter** |
| `FanSpeed` | HP | Fused, 35A, not inductive, DC | **Keep → HP2, add 4-level PWM bands** |
| `Fuel1A` + `Fuel1B` | 2× MP | OVC, 15A, inductive, DC | **Consolidate → HP3 FuelPump** |
| `Siren` | MP | OVC, 15A, not inductive, DC | **Keep → MP3, rename Horn** |
| `Ignition` | LP/MP | OVC, 10A, DC | **Repurpose → MP1 InjectorPwr** |
| `High Beams` | MP | Fused, 15A, DC | **Repurpose → MP2 CoilPwr** |
| `Low Beams` | MP | Fused, 15A, DC | **Repurpose → MP4 BrakeLights** |
| `MidPO3` | MP spare | Disabled | **→ MP5 TailLights** |
| `MidPO4` | MP spare | Disabled | **→ MP6 AltExciter** |
| `MidPO5` | MP spare | Disabled | **→ MP7 Coolsuit** |
| `LowPO2–7` | LP spares | Disabled | **→ LP1 ECUPwr, LP2 Dash, LP3 SmartyCam, LP4 GPS, LP5 Wideband, LP6 Cluster** |
| `LowPO8` | LP spare | Disabled | **→ LP7 WarningLED** |

---

## Step 1: Open Webinar Config

1. Open Race Studio 3
2. File → Open → select `Webinar complete.zconfig`
3. Immediately: File → Save As → `Tiburon_White_v1.zconfig` (work in the copy)
4. Device tree → expand PDM32 node

---

## Step 2: CAN1 — Haltech ECU Stream

This is the most important step and must be done first — all sensor channels (RPM, ECT, Oil P, etc.) depend on it.

1. In device tree → **CAN1 Stream**
2. Click the ECU dropdown — the webinar may have a different ECU loaded
3. Search for **"Haltech"** in the ECU list
   - If found: select **Haltech Elite 2500**
   - If not found: click **"Import from file"** and load the Haltech `.dbc` or `.xc1` file (download from Haltech support portal → Resources → CAN Bus Protocols)
4. Set baud rate: **1 Mbps** (Haltech Elite 2500 default)
5. Verify these channels appear in the channel list:
   - `RPM` (Engine Speed)
   - `ECT` (Engine Coolant Temperature)
   - `Oil_Pressure`
   - `Oil_Temp`
   - `Fuel_Pressure`
   - `TPS` (Throttle Position)
   - `Vehicle_Speed`
6. Click **Apply**

> **Note:** CAN0 on the PDM connects to Haltech (A22=CANH, A11=CANL). If Race Studio labels them CAN0/CAN1/CAN2, confirm which physical connector pin pair corresponds to which CAN index in your firmware version.

---

## Step 3: CAN2 Keypad — Remap Button Assignments

1. Device tree → **CAN2 Keypad** → AIM CAN Keypad 12
2. The webinar has buttons K01–K08 defined. Make the following remaps:

| Old Key | Old Function | New Key | New Function | Type |
|---|---|---|---|---|
| K04 | StarterKYD | **K01** | Starter | Latching toggle |
| K03 | SirenKYD | **K02** | Horn | Momentary |
| K02 | LightsKYD | **K03** | Lights | Latching toggle |
| K05 | IgnitionKYD | **DELETE** | — | (remove — use physical IGN) |
| K01 | FanKYD | **K05** | Fan Override | Latching toggle |
| K06 | (spare) | **K04** | CoolsuitKYD | Latching toggle |
| — | (new) | **K06** | FuelOverride | Latching toggle |
| — | (new) | **K07** | PitLimiter_KYD | Latching toggle |
| — | (new) | **K08** | WiperKYD | Latching toggle |
| — | (new) | **K09** | COMMS_YN | Latching toggle |
| — | (new) | **K10** | PITIN_LAPS | Multi-position (4 pos) |

For each key, set the generated status variable name to match the table above.

---

## Step 4: Channel Inputs — Physical Switches

1. Device tree → **Channels** (or Inputs section)
2. **Ch09** (Connector B):
   - Name: `START_BACKUP`
   - Type: Digital
   - Mode: Momentary (push button)
   - Active: Ground (closed = active)
3. **Ch11** (Connector B, pin B28):
   - Name: `BRAKE_SWITCH`
   - Type: Digital
   - Mode: Bistable (closed when brake pressed)
   - Active: Ground
4. All other channel inputs: leave at defaults (available for future)

---

## Step 5: Math Channels — Status Variables

Go to **Math Channels** (or Calculated Channels). Add/modify in this order:

### 5a. Keep and Update Existing

**`FuelSV` — update trigger logic:**
```
FuelSV = FUEL_PRIME OR ENGINE_RUNNING OR FuelOverride
```
(Previously it used SafeIgnition + RPM; update to use the new variables below)

**`momentary_SW` — rename to `START_BACKUP`:**
- Change input source from whatever it was → Channel Input Ch09

### 5b. Add New Variables

Add each as a new Math Channel (use New → Status Variable or Condition):

---

**`ENGINE_RUNNING`**
```
Condition: RPM > 50
Off-delay: 2000 ms
```
*Used by: Starter interlock, fuel pump logic, oil pressure alarm guard*

---

**`FUEL_PRIME`**
```
Type: One-shot timer
Trigger: SafeIgnition rising edge (0→1 transition)
Duration: 3000 ms
```
*Energizes fuel pump for 3 seconds on IGN on, before engine starts*

---

**`STARTER_SAFE`**
```
Condition: (StarterKYD OR START_BACKUP) AND SafeIgnition AND NOT ENGINE_RUNNING
```
*Prevents cranking into a running engine; requires IGN on*

---

Fan temperature bands (use ECT channel from CAN1 Haltech):

**`FAN_TEMP_25`**
```
Condition: ECT > 80
Hysteresis: 5°C (turns off at 75°C)
```

**`FAN_TEMP_50`**
```
Condition: ECT > 85
Hysteresis: 5°C
```

**`FAN_TEMP_75`**
```
Condition: ECT > 90
Hysteresis: 5°C
```

**`FAN_TEMP_100`**
```
Condition: ECT > 95
Hysteresis: 5°C
```

**`FAN_FAILSAFE`**
```
Condition: CAN timeout on ECT > 5 seconds
```
*If Haltech CAN lost, run fan at 100%*

---

Warning conditions:

**`LOW_OIL_P`**
```
Condition: Oil_Pressure < 15 AND ENGINE_RUNNING AND RPM > 500
```

**`HIGH_COOLANT_T`**
```
Condition: ECT > 105
```

**`HIGH_OIL_T`**
```
Condition: Oil_Temp > 130
```

**`LOW_FUEL_P`**
```
Condition: Fuel_Pressure < 30 AND ENGINE_RUNNING AND RPM > 500
```

**`MULTI_WARNING`**
```
Condition: LOW_OIL_P OR HIGH_COOLANT_T OR HIGH_OIL_T OR LOW_FUEL_P
```

---

Pit limiter:

**`PITLIMITER_SAFE`**
```
Condition: PitLimiter_KYD AND Vehicle_Speed < 60
```
*Speed gate: keypad can latch on even at speed, but won't activate until <60 mph*

**`PITLIMITER_ACTIVE`**
```
Condition: PITLIMITER_SAFE AND NOT (TPS > 60)
```
*TPS override: flooring it temporarily bypasses limiter*

---

PodiumConnect:

**`COMMS_YN`** — comes from K09 keypad output (latching toggle), no additional math needed

**`PITIN_LAPS`** — comes from K10 keypad output (multi-position 0/1/2/3), no additional math needed

---

## Step 6: Power Outputs — Rename and Reconfigure

Go to **Triggered Power Outputs**. Map each physical output:

### HP1 — Starter
- Rename: `Starter` → already named correctly ✅
- Mode: OVC Protected
- Max Load: 20A
- Inductive: YES
- OVC Retries: 1, Latch Off: 5s
- **Trigger (Action 1):** `STARTER_SAFE` → DC (100% duty)
- Add timeout: if output ON for > 10s → force off

### HP2 — Fan
- Rename: `FanSpeed` → `Fan`
- Mode: Fused (auto-disable on overcurrent)
- Max Load: 35A
- Inductive: NO
- PWM Freq: 100 Hz
- Soft Start: 1.0 s
- **Add 5 trigger actions (priority order):**

| Priority | Trigger | Duty |
|---|---|---|
| 1 (lowest) | `FAN_TEMP_25` | 25% |
| 2 | `FAN_TEMP_50` | 50% |
| 3 | `FAN_TEMP_75` | 75% |
| 4 | `FAN_TEMP_100` | 100% |
| 5 (highest) | `FanKYD OR FAN_FAILSAFE` | 100% |

Higher priority actions override lower ones when multiple triggers are active.

### HP3 — Fuel Pump
- Repurpose `Fuel1A` OR add HP3 if available (Fuel1A+Fuel1B may have been split across two MPs in the webinar — consolidate to HP3)
- Rename to `FuelPump`
- Mode: OVC Protected
- Max Load: 15A
- Inductive: YES
- OVC Retries: 3
- **Trigger (Action 1):** `FUEL_PRIME OR ENGINE_RUNNING OR FuelOverride` → DC

### MP1 — Injector Power
- Repurpose `Ignition` output → rename `InjectorPwr`
- Mode: OVC Protected
- Max Load: 15A
- Inductive: YES
- **Trigger:** `SafeIgnition` → DC

### MP2 — Coil Power
- Repurpose `High Beams` → rename `CoilPwr`
- Mode: OVC Protected
- Max Load: 15A
- Inductive: NO
- **Trigger:** `SafeIgnition` → DC

### MP3 — Horn
- `Siren` → rename `Horn`
- Mode: OVC Protected, 15A, not inductive
- **Trigger:** `HornKYD` (momentary, hold to honk) → DC
- Already configured correctly in webinar ✅

### MP4 — Brake Lights
- Repurpose `Low Beams` → rename `BrakeLights`
- Mode: Fused, 10A
- **Trigger:** `BRAKE_SWITCH` (Ch11) → DC
- **Must work independently of keypad — wire brake switch to Ch11 only**

### MP5 — Tail Lights
- Repurpose `MidPO3` → rename `TailLights`
- Mode: Fused, 10A
- **Trigger:** `LightsKYD` (Key 03 toggle) → DC

### MP6 — Alternator Exciter
- Repurpose `MidPO4` → rename `AltExciter`
- Mode: OVC Protected, 5A
- **Trigger:** `SafeIgnition` → DC

### MP7 — Coolsuit
- Repurpose `MidPO5` → rename `Coolsuit`
- Mode: OVC Protected, 10A, Inductive: YES (pump motor)
- **Trigger:** `CoolsuitKYD` (Key 04 toggle) → DC

### LP1–LP6 — Accessories (all trigger on SafeIgnition)
| Output | Rename From | New Name |
|---|---|---|
| LP1 | LowPO2 | ECUPwr |
| LP2 | LowPO3 | Dash |
| LP3 | LowPO4 | SmartyCam |
| LP4 | LowPO5 | GPS |
| LP5 | LowPO6 | Wideband |
| LP6 | LowPO7 | Cluster |

All: OVC Protected, 10A, **Trigger:** `SafeIgnition` → DC

### LP7 — Warning LED
- Repurpose `LowPO8` → rename `WarningLED`
- Mode: OVC Protected, 5A
- **Trigger:** `MULTI_WARNING` → DC (or PWM 2Hz/50% for blinking effect)

---

## Step 7: Keypad LED Colors

Go to **CAN Output 2 (Keypad)** → configure `ColorsConditionK01` through `ColorsConditionK10`:

| Key | Off Color | Active Color | Source Variable |
|---|---|---|---|
| K01 Start | Dim green | Bright green | `StarterKYD` |
| K02 Horn | Dim yellow | Bright yellow | `HornKYD` |
| K03 Lights | Dim blue | Bright blue | `LightsKYD` |
| K04 Coolsuit | Dim cyan | Bright cyan | `CoolsuitKYD` |
| K05 Fan | Dim white | Bright red | `FanKYD` (red = manual override) |
| K06 Fuel Override | Dim white | Bright red | `FuelOverride` |
| K07 Pit Limiter | Dim white | Bright white (active) / Red (engaged-but-unsafe) | `PITLIMITER_ACTIVE` / `PitLimiter_KYD AND NOT PITLIMITER_SAFE` |
| K08 Wiper | Dim white | Bright white | `WiperKYD` |
| K09 Comms Yes | Off | Bright green | `COMMS_YN` |
| K10 Pit-In Laps | Off | White dim/med/bright (1/2/3 laps) | `PITIN_LAPS` position |
| K11–12 | Off | — | Spare |

For K07 (pit limiter), if Race Studio allows conditional LED color:
- `PITLIMITER_ACTIVE = 1` → White (all systems go)
- `PitLimiter_KYD = 1 AND PITLIMITER_ACTIVE = 0` → Red (armed but speed-blocked)
- `PitLimiter_KYD = 0` → Dim white (off)

---

## Step 8: Haltech Pit Limiter — CAN Output

To send `PITLIMITER_ACTIVE` to the Haltech:

**Option A (CAN — recommended):**
1. CAN Output 1 → create new CAN message
2. Destination: Haltech CAN address (check Haltech NSP CAN Receive page for the correct message ID and byte)
3. Map `PITLIMITER_ACTIVE` to the correct byte/bit
4. In Haltech NSP: Configure → Speed Limiter → Enable via CAN → set target speed (35 mph for pit lane)

**Option B (Wire):**
1. Assign `PITLIMITER_ACTIVE` → any spare LP output (e.g., remaining LowPO)
2. Wire that LP output → Haltech SPI pin configured as digital input
3. In Haltech NSP: Configure → Speed Limiter → Enable via digital input pin

---

## Step 9: Save and Transmit

1. File → Save (`Tiburon_White_v1.zconfig`)
2. Connect PDM via USB (Binder 5-pin)
3. Device → Transmit Configuration
4. Wait for "Transmission successful"
5. Export backup copy to `C:\Users\Julian\Desktop\Tiburon Project\AIM PDM\Tiburon_White_v1.zconfig`

---

## Step 10: Bench Test Sequence

With PDM powered (via IGN toggle or direct 12V):

| Test | Method | Expected Result |
|---|---|---|
| SafeIgnition active | Flip IGN toggle ON | LP1-LP6 all energize |
| Fuel prime | Flip IGN toggle ON | HP3 (fuel pump) ON for 3s then OFF |
| Keypad responds | Press K01 | `StarterKYD` toggles |
| Start interlock | Press K01 with ENGINE_RUNNING=0 | HP1 (starter) energizes |
| Start interlock | Set RPM > 50 via CAN, press K01 | HP1 stays OFF |
| Fan manual | Press K05 | HP2 (fan) ON at 100% |
| Brake lights | Close Ch11 | MP4 (brake lights) ON |
| Horn | Press K02 | MP3 (horn) ON while held |
| Warning LED | Force `LOW_OIL_P` condition | LP7 ON |
| Pit limiter LED | Press K07 while speed > 60 | K07 LED → RED |
| Pit limiter activate | Press K07 with speed = 0 | K07 LED → WHITE, PITLIMITER_ACTIVE = 1 |

---

## Reference: Output Physical Pin Map

| Output Name | PDM Connector Pins |
|---|---|
| HP1 Starter | A1 + A13 |
| HP2 Fan | A12 + A23 |
| HP3 FuelPump | A24 + A25 |
| MP1 InjectorPwr | A2 |
| MP2 CoilPwr | A3 |
| MP3 Horn | A4 |
| MP4 BrakeLights | A5 |
| MP5 TailLights | A6 |
| MP6 AltExciter | A7 |
| MP7 Coolsuit | A8 |
| LP1–LP7 | A14–A20 |
| IGN Input | B23 |
| Ch09 (Start backup) | B21 |
| Ch11 (Brake switch) | B28 |
| CAN0 H/L | A22 / A11 |
| CAN2 (Keypad) | B pins — see pdm-pinout.md |
