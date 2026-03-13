# Race Studio 3 — Session 1: Tiburon Config from Webinar Starting Point

**Goal:** Configure PDM32 for white Tiburon starting from `Webinar complete.zconfig`
**Time estimate:** 60–90 minutes
**Source file analysis:** Webinar config has SafeIgnition, FuelSV, FanSpeed, Starter, Siren, Fuel1A/B — output logic and protection settings are ~80% reusable. Keypad variables (`*KYD`, LED colors) are deleted — all controls via physical switch panel.

> **CAN keypad excluded from this build.** Keypad variable names and LED assignments are preserved in `guides/keypad-config-future.md` for future re-addition.

**Before you start:** Export a backup of the webinar config to `AIM PDM/` before making any changes.

---

## What the Webinar Config Already Has

| Webinar Variable | What It Does | Tiburon Action |
|---|---|---|
| `SafeIgnition` | ON when PDM IGN input (B23) active | **Keep as-is** — this is our master permissive |
| `StarterKYD` | Latched toggle from keypad press | **Delete — replaced by Ch09 physical start button** |
| `SirenKYD` | Momentary from keypad press | **Delete — horn via fuse box spade (Phase 1)** |
| `LightsKYD` | Latched toggle from keypad press | **Delete — tail lights always on with SafeIgnition** |
| `FanKYD` | Latched toggle from keypad press | **Delete — replaced by Ch01 physical fan toggle** |
| `IgnitionKYD` | Was Key 05 — keypad-controlled ignition | **Delete — physical IGN switch (B23)** |
| `FuelSV` | Composite fuel pump run condition | **Keep, update logic** |
| `FANOFFSV` | Fan manual off state | **Keep** |
| `FlashSV` | Momentary flash state | **Keep** |
| `momentary_SW` | Physical momentary switch template | **Repurpose → START on Ch09** |
| `ColorsConditionK01–K12` | Keypad LED color logic | **Delete — no keypad. See `guides/keypad-config-future.md`** |
| `BitRed/Green/BlueX15–X1C` | RGB color bits for keypad LEDs | **Delete — no keypad** |

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

## Step 2: ECU Stream — Haltech CAN_V2_40

This is the most important step and must be done first — all sensor channels (RPM, ECT, Oil P, etc.) depend on it.

### 2a. Select Protocol

1. Click the **ECU Stream** tab (top row, second tab)
2. Click **Change ECU** dropdown (top right of ECU Stream panel)
3. Select **HALTECH - CAN_V2_40 (ver. 02.00.03) 1 Mbit/sec**
4. Baud rate is set by the protocol — **1 Mbit/sec** (confirms in the dropdown label)

> **CAN wiring:** PDM A22 = CAN H, A11 = CAN L → Haltech 26-pin pin 23 (W) / pin 24 (L)

> **Enable the CAN Bus 120 Ohm Resistor** ✅ **Leave checked.** The bus is PDM ↔ Haltech only (two endpoints). PDM is one endpoint; Haltech has its own internal termination resistor (enabled by default in NSP). Both must be terminated.

> **Silent on CAN Bus** ☐ **Leave unchecked.** Silent = receive-only. The PDM must transmit on this bus to send the pit limiter CAN message to the Haltech (Step 8). Unchecking is correct.

### 2b. Fix Channel Count — MAX 120

> **WARNING:** The Haltech CAN_V2_40 protocol has ~267 channels. Race Studio enforces a 120-channel maximum. If you accept defaults, it will silently drop anything after the first 120.

1. In the ECU Stream channel list, check the header row: it shows **Enabled Channels (Max. 120) X / 267**
2. **Uncheck the header checkbox** to disable ALL channels
3. Manually enable only the channels in the tables below (≤ 30 total)
4. Re-check the counter — must show **≤ 120 / 267**

### 2c. Channels to Enable — Master List

Enable exactly these channels. Total: **~72**, well under the 120 limit.

**Required — PDM alarm/logic channels:**

| CC ID | Channel Name | Unit | Purpose |
|---|---|---|---|
| CC01 | ECU RPM | rpm | ENGINE_RUNNING, STARTER_SAFE, alarm guards |
| CC04 | ECU ThrottlePos | % | PITLIMITER_ACTIVE (TPS > 60 bypass) |
| CC05 | ECU OilPress | bar | LOW_OIL_P alarm |
| CC06 | ECU FuelPress | bar | LOW_FUEL_P alarm |
| CC30 | ECU BrakePress | bar | Brake pressure (AVI7 Lowdoller sensor) |
| CC45 | ECU VehSpeed | km/h | PITLIMITER_SAFE — **threshold = 97 km/h (= 60 mph)** |
| CC52 | ECU BatteryVolt | V | Battery health |
| CC69 | ECU CoolantTemp | °F | Fan bands, HIGH_COOLANT_T alarm |
| CC71 | ECU OilTemp | °C | HIGH_OIL_T alarm |
| CC94 | ECU Oil Press Li | # | ECU oil pressure warning flag |
| CC117 | PitLane SpLimErr | # | Pit lane speed limiter error feedback |
| CC119 | PitLane SpdLimSS | # | Pit lane set speed reference |
| CC249 | ECU PLIGHT STATE | # | Engine protection / fault flag |

**Logging — keep all of these:**

| CC ID | Channel Name | Unit | Notes |
|---|---|---|---|
| CC02 | ECU ManifPress | bar | Manifold pressure (MAP) |
| CC03 | ECU CoolantPres | bar | Coolant pressure (AVI5 Lowdoller) |
| CC08 | ECU EngineDeman | % | Engine load / demand |
| CC09 | ECU IgnAngLead | deg | Ignition advance — shows retard events |
| CC10 | ECU InjDT2 | % | Injector duty cycle bank 2 |
| CC11 | ECU InjDT1 | % | Injector duty cycle bank 1 |
| CC15 | ECU Avg Inj 1 | ms | Injection pulse width |
| CC16 | ECU Avg Inj 2 | ms | Injection pulse width |
| CC17 | ECU Avg Inj 3 | ms | Injection pulse width |
| CC23 | ECU TrigSyncLev | # | Trigger sync level — tune health |
| CC24 | ECU TrigErrCount | # | Trigger error count — tune health |
| CC26 | ECU KnockLev2 | # | Knock bank 2 — critical for tune |
| CC27 | ECU KnockLev1 | # | Knock bank 1 — critical for tune |
| CC28 | ECU LateralG | g | Lateral acceleration |
| CC36 | ECU ExhCamAng1 | deg | Exhaust cam angle bank 1 (VVT) |
| CC37 | ECU ExhCamAng2 | deg | Exhaust cam angle bank 2 (VVT) |
| CC38 | ECU LongG | g | Longitudinal acceleration |
| CC46 | ECU IntakeCamA1 | deg | Intake cam angle bank 1 (VVT) |
| CC47 | ECU IntakeCamA2 | deg | Intake cam angle bank 2 (VVT) |
| CC50 | ECU BaromPress | bar | Barometric pressure |
| CC65 | ECU Amb Air T | °C | Ambient air temp |
| CC66 | ECU Rel Humidity | % | Relative humidity |
| CC67 | ECU Abs Humidity | # | Absolute humidity |
| CC68 | ECU Spec Humi | # | Specific humidity |
| CC70 | ECU AirTemp | °C | Air temp (°C) |
| CC72 | ECU FuelTemp | °C | Fuel temperature |
| CC73 | ECU DiffOilTemp | °C | Diff/trans oil temp |
| CC74 | ECU GearOilTemp | °C | Gearbox oil temp |
| CC76 | ECU FuelLevel | l | Fuel level |
| CC77 | ECU FuelTrimSTB1 | % | Short-term fuel trim bank 1 |
| CC78 | ECU FuelTrimSTB2 | % | Short-term fuel trim bank 2 |
| CC79 | ECU FuelTrimLTB1 | % | Long-term fuel trim bank 1 |
| CC80 | ECU FuelTrimLTB2 | % | Long-term fuel trim bank 2 |
| CC91 | ECU CheckEngLtSw | # | Check engine light status |
| CC107 | ECU TPSAct | # | TPS active status |
| CC134 | ECU TargLambda | lambda | Target lambda |
| CC138 | ECU CrankCPress | bar | Crankcase pressure |
| CC141 | ECU InjectionDT4 | % | Injector duty cycle 4 |
| CC142 | ECU IgnitionAng1 | deg | Ignition angle cyl 1 |
| CC143 | ECU IgnitionAng2 | deg | Ignition angle cyl 2 |
| CC144 | ECU RaceTimer | ms | Session timing |
| CC149 | ECU TorqCIgnCorr | deg | Torque/ignition correction |
| CC166 | ECU Temperature | °C | ECU internal temperature |
| CC167 | ECU Gear Sel Pos | gear | Gear display |
| CC168 | ECU WIDEBAND B2 | lambda | AFR bank 2 |
| CC169 | ECU WIDEBAND OVE | lambda | AFR average |
| CC170 | ECU WIDEBAND B1 | lambda | AFR bank 1 |
| CC172 | ECU Inj Pres D | bar | Injector pressure delta |
| CC173 | ECU Acc Ped Pos | % | Accelerator pedal position |
| CC210 | ECU VERTICAL G | g | Vertical acceleration |
| CC211 | ECU PITCH RATE | deg/s | Pitch rate |
| CC212 | ECU ROLL RATE | deg/s | Roll rate |
| CC213 | ECU YAW RATE | deg/s | Yaw rate |
| CC227 | ECU ENG LIM MAX | deg/s | Rev limiter threshold |
| CC254 | ECU FUEL TRIPMT | l | Fuel used — endurance reference |
| CC255 | Trip Meter | m | Distance |
| CC261 | ECU AIR TEMP | °F | IAT |

> ⚠️ **Disable CC260 (ECU H2O INJ DUTY)** — no water injection on this car, uncheck it.

---

## Step 3: Disable CAN2 Keypad

The webinar config includes a CAN2 keypad with buttons K01–K12. This build uses physical switches instead.

1. Click the **CAN2 Keypad** tab
2. **Delete all button definitions** (K01–K12)
3. **Delete all keypad status variables:** `StarterKYD`, `SirenKYD`, `LightsKYD`, `FanKYD`, `CoolsuitKYD`, `FuelOverride`, `PitLimiter_KYD`, `COMMS_YN`, `PITIN_LAPS`, `WiperKYD`
4. **Delete all keypad LED color assignments** (`ColorsConditionK01–K12`, `BitRed/Green/BlueX15–X1C`)
5. CAN2 bus remains available for future expansion

> **Keypad temporarily excluded.** Config below is preserved for future use. When a keypad is added, re-import these settings and update trigger logic to OR keypad + physical switch inputs.

### K33 — Starter
- **Name:** `StarterKYD`
- **Type: Momentary** — crank only while held; releasing stops the starter
- Rest: label `RDY`, value `0`
- Active: label `CRNK`, value `1`
- Use timing: NO
- Variable name: `StarterKYD`

### K34 — Horn
- **Name:** `HornKYD`
- **Type: Momentary**
- Rest: label `OFF`, value `0`
- Active: label `HORN`, value `1`
- Use timing: NO
- Variable name: `HornKYD`

### K35 — Lights
- **Name:** `LightsKYD`
- **Type: Multistatus** — 3 positions, cycles on each press
- Position 0: label `OFF`, value `0`
- Position 1: label `LOW`, value `1`
- Position 2: label `HIGH`, value `2`
- Variable name: `LightsKYD`

### K36 — Coolsuit
- **Name:** `CoolsuitKYD`
- **Type: Toggle**
- Rest: label `OFF`, value `0`
- Active: label `ON`, value `1`
- Variable name: `CoolsuitKYD`

### K37 — Fan Override
- **Name:** `FanKYD`
- **Type: Toggle**
- Rest: label `OFF`, value `0`
- Active: label `ON`, value `1`
- Variable name: `FanKYD`

### K38 — Fuel Override
- **Name / Variable:** `FuelOverrideKYD`
- **Type: Toggle**
- Rest: label `OFF`, value `0`
- Active: label `ON`, value `1`

### K39 — Pit Limiter
- **Name / Variable:** `PitLimiterKYD`
- **Type: Toggle + timing**
- Rest: label `OFF`, value `0`
- Active: label `PIT`, value `1`
- Use timing: YES
  - Short press: toggles state (normal arm/disarm)
  - Long press: label `CLR`, value `0` — forces OFF regardless of current state
  - Time threshold: **2000 ms**

### K40 — Comms
- **Name / Variable:** `CommsKYD`
- **Type: Toggle**
- Rest: label `NO`, value `0`
- Active: label `YES`, value `1`

### K41 — Pit-In Laps
- **Name / Variable:** `PitInKYD`
- **Type: Multistatus** — 4 positions, cycles on each press
- Position 0: label `---`, value `0` (not pitting)
- Position 1: label `L+1`, value `1` (1 lap out)
- Position 2: label `L+2`, value `2`
- Position 3: label `L+3`, value `3`

### K42 — Wiper
- **Name:** `WiperKYD`
- **Type: Multistatus** — 3 positions, cycles on each press
- Position 0: label `OFF`, value `0`
- Position 1: label `SLOW`, value `1`
- Position 2: label `FAST`, value `2`
- Variable name: `WiperKYD`

### K43–K44 — Spare
- Leave unconfigured

---

## Step 4: Channel Inputs — Physical Switches

All driver controls use physical switches wired directly to PDM channel inputs. No CAN keypad.

1. Device tree → **Channels** (or Inputs section)
2. **Ch01** (Connector B, pin 26):
   - Name: `FAN_OVERRIDE`
   - Type: Digital, latching toggle
   - Active: 12V when ON
3. **Ch02** (Connector B, pin 27):
   - Name: `WIPER_LOW`
   - Type: Digital, latching toggle
   - Active: 12V when ON
4. **Ch03** (Connector B, pin 28):
   - Name: `WIPER_HIGH`
   - Type: Digital, latching toggle
   - Active: 12V when ON
5. **Ch04** (Connector B, pin 29):
   - Name: `COOLSUIT`
   - Type: Digital, latching toggle
   - Active: 12V when ON
6. **Ch05** (Connector B, pin 30):
   - Name: `DEFOGGER`
   - Type: Digital, latching toggle
   - Active: 12V when ON
7. **Ch09** (Connector B, pin 21):
   - Name: `START`
   - Type: Digital, momentary (push button)
   - Active: Ground (closed = active)
8. **Ch11** (Connector A, pin 26):
   - Name: `BRAKE_SWITCH`
   - Type: Digital
   - Mode: Bistable (closed when brake pressed)
   - Active: Ground
9. Ch06–Ch08, Ch10, Ch12: leave at defaults (available for future)

---

## Step 5: Math Channels — Status Variables

Go to **Math Channels** (or Calculated Channels). Add/modify in this order:

### 5a. Keep and Update Existing

**`FuelSV` — update trigger logic:**
```
FuelSV = FUEL_PRIME OR ENGINE_RUNNING
```
(FuelOverride removed — no manual override switch. Cycle IGN off/on to re-trigger 3s fuel prime.)

**`momentary_SW` — rename to `START`:**
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
Condition: Ch09 AND SafeIgnition AND NOT ENGINE_RUNNING
```
*Prevents cranking into a running engine; requires IGN on. Ch09 = physical start button.*

---

Fan temperature bands (use ECT channel from CAN1 Haltech):

**`FAN_TEMP_25`**
```
Condition: ECT > 77
Hysteresis: 5°C (turns off at 72°C)
```
*170°F thermostat installed — begins opening at 77°C. Fan starts as thermostat opens.*

**`FAN_TEMP_50`**
```
Condition: ECT > 82
Hysteresis: 5°C
```

**`FAN_TEMP_75`**
```
Condition: ECT > 87
Hysteresis: 5°C
```

**`FAN_TEMP_100`**
```
Condition: ECT > 92
Hysteresis: 5°C
```
*Thermostat estimated fully open ~92°C with 170°F unit — fan at 100% when thermostat maxed out.*

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
Condition: ECT > 95
```
*170°F thermostat — normal operating range is 77–87°C. At 95°C the thermostat is fully open and fan is maxed; something is wrong.*

**`HIGH_OIL_T`**
```
Condition: Oil_Temp > 130
```

**`LOW_FUEL_P`**
```
Condition: Fuel_Pressure < 40 AND ENGINE_RUNNING AND RPM > 500
```
*Factory idle fuel pressure is 46–49 PSI. 40 PSI catches a failing pump/regulator while still above injector deadband.*

**`MULTI_WARNING`**
```
Condition: LOW_OIL_P OR HIGH_COOLANT_T OR HIGH_OIL_T OR LOW_FUEL_P
```

---

Pit limiter:

> **Pit limiter not available without keypad.** No physical switch assigned. See `guides/keypad-config-future.md` for PitLimiter_KYD, PITLIMITER_SAFE, and PITLIMITER_ACTIVE variable definitions when a keypad is added.

PodiumConnect:

> **COMMS_YN and PITIN_LAPS not available without keypad.** These require multi-position or toggle inputs not present on the physical switch panel. See `guides/keypad-config-future.md`.

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

| Priority | Trigger | Duty | Threshold |
|---|---|---|---|
| 1 (lowest) | `FAN_TEMP_25` | 25% | ECT > 77°C (170°F thermostat opens) |
| 2 | `FAN_TEMP_50` | 50% | ECT > 82°C |
| 3 | `FAN_TEMP_75` | 75% | ECT > 87°C |
| 4 | `FAN_TEMP_100` | 100% | ECT > 92°C (est. fully open) |
| 5 (highest) | `FanKYD OR FAN_FAILSAFE` | 100% | Manual override or CAN timeout |

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

### MP3 — Wiper Low
- `Siren` → rename `WiperLow`
- Mode: OVC Protected, 10A, inductive (wiper motor)
- **Trigger:** Ch02 AND NOT Ch03 → DC
- Horn: no dedicated switch. **Phase 1:** spade connector to fuse box. **Phase 2:** direct splice to horn harness.

### MP4 — Brake Lights
- Repurpose `Low Beams` → rename `BrakeLights`
- Mode: Fused, 10A
- **Trigger:** `BRAKE_SWITCH` (Ch11) → DC
- **Must work independently of ignition — brake switch always active**

### MP5 — Tail Lights
- Repurpose `MidPO3` → rename `TailLights`
- Mode: Fused, 10A
- **Trigger:** `SafeIgnition` → DC (always on when car is on)

### MP6 — Wiper High
- Repurpose `MidPO4` → rename `WiperHigh`
- Mode: OVC Protected, 10A, Inductive: YES (wiper motor)
- **Trigger:** Ch03 → DC (overrides low speed — MP3 has AND NOT Ch03 guard)

### MP7 — Coolsuit
- Repurpose `MidPO5` → rename `Coolsuit`
- Mode: OVC Protected, 10A, Inductive: YES (pump motor)
- **Trigger:** Ch04 AND SafeIgnition → DC

### MP8 — Defogger
- Repurpose `MidPO6` (or spare) → rename `Defogger`
- Mode: OVC Protected, 10A, Inductive: NO (resistive heating element)
- **Trigger:** Ch05 AND SafeIgnition → DC

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

### LP8 — Alternator Exciter
- Repurpose remaining spare → rename `AltExciter`
- Mode: OVC Protected, 5A
- **Trigger:** `SafeIgnition` → DC
- OEM alternator D+ field wire cut and routed through LP8 (A21). Kill switch drops field immediately.

---

## Step 7: Keypad LED Colors — SKIP

> **No CAN keypad in this build.** All keypad LED color assignments were deleted in Step 3.
> Full LED configuration preserved in `guides/keypad-config-future.md` for future re-addition.

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
| Start interlock | Press START (Ch09) with ENGINE_RUNNING=0 | HP1 (starter) energizes |
| Start interlock | Set RPM > 50 via CAN, press START (Ch09) | HP1 stays OFF |
| Fan override | Flip Fan toggle (Ch01) ON | HP2 (fan) ON at 98% |
| Wiper low | Flip Wiper Low (Ch02) ON | MP3 (wiper low) ON |
| Wiper high | Flip Wiper High (Ch03) ON | MP6 (wiper high) ON, MP3 OFF |
| Coolsuit | Flip Coolsuit (Ch04) ON | MP7 ON |
| Defogger | Flip Defogger (Ch05) ON | MP8 ON |
| Brake lights | Press brake pedal (Ch11) | MP4 (brake lights) ON |
| Tail lights | Flip IGN toggle ON | MP5 (tail lights) ON |
| Warning LED | Force `LOW_OIL_P` condition | LP7 ON |
| Alt exciter | Flip IGN toggle ON | LP8 (alt exciter) ON |

---

## Reference: Output Physical Pin Map

**Black connector = power outputs, CAN, Ch11–Ch12**
**Grey connector = additional outputs, Ch01–Ch10, IGN, analog ref**

| Output / Signal | Connector | Pin(s) |
|---|---|---|
| HP1 Starter | Black | 1 + 13 |
| HP2 Fan | Black | 12 + 23 |
| HP3 FuelPump | Black | 24 + 25 |
| MP1 InjectorPwr | Black | 2 |
| MP2 CoilPwr | Black | 3 |
| MP3 Horn | Black | 4 |
| MP4 BrakeLights | Black | 5 |
| MP5 TailLights | Black | 6 |
| MP6 AltExciter | Black | 7 |
| MP7 Coolsuit | Black | 8 |
| LP1–LP7 | Black | 14–20 |
| Ch11 (Brake switch) | Black | 26 |
| Ch12 (spare) | Black | 27 |
| CAN0 H / CAN0 L (Haltech) | Black | 22 / 11 |
| CAN2 H / CAN2 L (Unused — future keypad) | Black | 28 / 29 |
| CAN1 H / CAN1 L (AIM Expansion → DataHub) | Black | 30 / 31 |
| +Vb out CAN (power to expansion devices) | Black | 33 |
| +Vb ext CAN (external CAN power input) | Black | 32 |
| IGN Input | Grey | 23 |
| Ch09 (Start backup) | Grey | 21 |
| Ch10 (spare) | Grey | 22 |
| Ch01–Ch08 (spare) | Grey | 26–33 |
| +5V Analog Vref (sensor reference) | Grey | 16 |
| +Vb output (sensor supply) | Grey | 17 |
| Speed 1 input | Grey | 20 |
| Speed 2 input | Grey | 19 |
