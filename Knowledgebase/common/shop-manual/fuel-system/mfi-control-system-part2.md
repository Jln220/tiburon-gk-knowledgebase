---
source: FLA.pdf
chapter: FLA
section: FLA-46 to FLA-72
pages: 46-72
engine: V6
title: MFI Control System (Part 2)
---

# MFI Control System (Part 2)

<!-- EFOC4130 -->
## Throttle Position (TP) Sensor

The TP Sensor is a variable resistor type that rotates with the throttle body shaft to sense the throttle valve angle. As the throttle shaft rotates, the output voltage of the TP Sensor changes. The ECM detects the throttle valve opening based on voltage change.

<!-- Figure: Throttle position sensor installed on throttle body, source: FLA.pdf page 46 -->
<!-- Figure: TP sensor terminal voltage vs. throttle shaft turning angle graph (linear rise from minimum to maximum), source: FLA.pdf page 46 -->

### Circuit Diagram [2.7 V6]

<!-- Figure: TP sensor circuit diagram showing 3-pin connector (terminals 1, 2, 3) with resistor network to ECM, source: FLA.pdf page 46 -->

| Pin | Function |
|:----|:---------|
| 1   | Sensor ground |
| 2   | Sensor output |
| 3   | +5V reference |

---

### Sensor Checking

#### Using HI-SCAN

| Check Item | Data Display | Check Conditions | Throttle Valve | Test Specification |
|:-----------|:-------------|:-----------------|:---------------|:-------------------|
| Throttle position sensor | Sensor voltage | Ignition switch: ON | At idle position | 250-800 mV (2.7 V6) |
| | | | Open slowly | Increases with valve opening |
| | | | Open widely | 4,250-4,700 mV |

#### Using Voltmeter

<!-- Figure: Throttle position sensor connector (sensor side, front view) showing 3 terminals, source: FLA.pdf page 47 -->

1. Disconnect the throttle position sensor connector.

2. Measure resistance between terminal 2 (sensor ground) and terminal 1 (sensor power) for 2.7 V6.

   **Standard value: 3.5 - 6.5 kΩ**

3. Connect a pointer type ohmmeter between terminal 2 (sensor ground) and terminal 3 (sensor output) for 2.7 V6.

4. Operate the throttle valve slowly from the idle position to the full open position and check that the resistance changes smoothly in proportion with the throttle valve opening angle.

5. If the resistance is out of specification, or fails to change smoothly, replace the throttle position sensor.

**Tightening torque**
TP Sensor: 1.5-2.5 Nm (15-25 kg.cm, 1.1-1.8 lb.ft)

---

### Harness Inspection Procedure

<!-- Figure: Harness inspection procedure step 1 — voltmeter on harness side connector, source: FLA.pdf page 47 -->

**Step 1**

Measure the power supply voltage of the throttle position sensor.
- Connector: Disconnected
- Ignition switch: ON
- Voltage (V): 4.25-4.7

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFOC413B -->

**Step 2**

Check for continuity of the ground circuit.
- Connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 3 |
| **NG** | Repair the harness. |

<!-- EFOC413C -->

**Step 3**

Check for an open-circuit, or a short-circuit or ground between the powertrain control module and the throttle position sensor.
- Throttle position sensor connector: Disconnected
- PCM connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFOC413D -->

---

### Troubleshooting Hints

The TPS signal is important in the control of the automatic transaxle. Shift shock and other trouble will occur if the sensor is faulty.

---

<!-- EFOC4170 -->
## Idle Speed Control Actuator

The idle speed control actuator is the double coil type. The two coils are driven by separate driver stages in the ECM. Depending on the pulse duty factor, the equilibrium of the magnetic forces of the two coils will result in different angles of the motor. In parallel to the throttle valve, a bypass hose line is arrange, where the idle speed actuator is inserted in.

### Circuit Diagram [2.7 V6]

<!-- Figure: ISA circuit diagram showing double-coil actuator with pins 1, 2, 3. Pin 3 connects to MFI control relay. ECM pins 46 (Open) and 47 (Closing) drive the coils, source: FLA.pdf page 49 -->

| ISA Connector Pin | Function |
|:------------------|:---------|
| 1 | Coil (Open) — to ECM pin 46 |
| 2 | Coil (Closing) — to ECM pin 47 |
| 3 | Power supply — from MFI control relay |

---

### Troubleshooting Procedures

<!-- Figure: ISC actuator troubleshooting flowchart, source: FLA.pdf page 50 -->

1. Engine: Running
2. Check the wiring connection between PCM and ISC Actuator. Is the connection OK?
   - **NO** --> Repair the wiring.
   - **YES** --> Continue
3. Check the coil of actuator. Is the coil OK?
   - **NO** --> Replace the ISC Actuator
   - **YES** --> Continue
4. Erase any diagnostic trouble code from memory. Is same code present after rechecking?
   - **NO** --> OK
   - **YES** --> Replace PCM.

> DTC: Diagnosis Trouble Code
> PCM: Powertrain Control Module

---

### Troubleshooting Hints

The MIL is ON or the DTC is displayed on the HI-SCAN under the following conditions:

- When the primary voltage side of the ECM is a shorted or open circuit.
- The ignition closed loop control in ECM is out of order.
- Open or short circuit is observed in idle air control system when ignition switch is turned on.

#### Using HI-SCAN

| Check Item | Check Condition | HI-SCAN Display | Type |
|:-----------|:----------------|:----------------|:-----|
| Idle speed control actuator - Actuator test | Start the engine | ISCA | Activate |

---

### Harness Inspection Procedure

<!-- Figure: ISC actuator harness inspection step 1 — voltmeter on harness side connector (A), source: FLA.pdf page 51 -->

**Step 1**

Measure the power supply voltage of the actuator.
- Connector: Disconnected
- Ignition switch: ON
- Voltage (V): Battery voltage

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. Check the power supply. |

<!-- EFOC417B -->

**Step 2**

Check for an open-circuit, or a short-circuit to ground between the ECM and the idle speed control actuator.
- ECM connector: Disconnected
- Idle speed actuator connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFOC417C -->

---

### Actuator Inspection

1. Disconnect the connector at the idle speed control actuator.

2. Measure the resistance between terminals.

   **Standard value:**
   - Terminal 3 and 2: 10.5 - 14Ω
   - Terminal 1 and 3: 10 - 12.5Ω [at 20°C (68°F)]

3. Connect the connector to the idle speed control actuator.

<!-- Figure: ISA connector side view showing resistance measurement between terminals, source: FLA.pdf page 51 -->

---

<!-- EFOC4810 -->
## Heated Oxygen Sensor (HO2S) [2.7 V6]

The heated oxygen sensor senses the oxygen concentration in exhaust gas, converts it into a voltage, which is sent to the ECM. The oxygen sensor outputs about 0V when the air fuel ratio is richer than the theoretical ratio, and outputs about 5V when the ratio is leaner (higher oxygen concentration in exhaust gas). The ECM controls the fuel injection ratio based on this signal so that the air fuel ratio is maintained at the theoretical ratio. The oxygen sensor has a heater element which ensures the sensor performance during all driving conditions.

### Circuit Diagram [2.7 V6]

<!-- Figure: HO2S circuit diagram showing 4-pin sensor connector, heater circuit through MFI control relay, signal to ECM pin 20, with 0.5V reference. Harness side connector (H), source: FLA.pdf page 52 -->

<!-- Figure: HO2S output voltage waveform — rich/lean oscillation around theoretical A/F ratio, and relative motive force vs A/F ratio graph, source: FLA.pdf page 52 -->

| Sensor Connector Pin | Function |
|:---------------------|:---------|
| 1 | Heater (+) — from MFI control relay |
| 2 | Signal — to ECM pin 20 |
| 3 | Heater (-) — ground |
| 4 | Sensor ground |

---

### Troubleshooting Hints

1. If the HO2S is defective, abnormally high emissions may occur.

2. If the HO2S check results were normal, but the sensor output voltage is out of specification, check for the following items (related to air fuel ratio control system):
   - Faulty injector
   - Air leaks in the intake manifold
   - Faulty air flow sensor, intake air temperature sensor, engine coolant temperature sensor.

---

### Using GST

| Check Item | Check Conditions | Engine State | Test Specification |
|:-----------|:-----------------|:-------------|:-------------------|
| Oxygen sensor | Engine: Warm-up (make the mixture lean by engine speed reduction, and rich by racing) | When sudden deceleration from 4,000 rpm | 200 mV or lower |
| | | When engine is suddenly raced | 600-1,000 mV |
| | Engine: Warm-up (using the heated oxygen sensor signal, check the air/fuel mixture ratio, and also check the condition of control by the ECU) | 750 rpm (Idle) | 400 mV or lower - (oscillate) 600-1,000 mV |
| | | 2,000 rpm | — |

---

### Inspection (Using Voltmeter)

> **NOTE**
> Before checking, warm up the engine until the engine coolant temperature reaches 80 to 95°C (176 to 205°F).

<!-- Figure: Heated oxygen sensor side connector showing 4 terminals — Pin 1 (Heater -), Pin 2 (Sensor ground), Pin 3 (Sensor source), Pin 4 (Heater +), source: FLA.pdf page 53 -->

1. Apply battery voltage directly between terminal 3 and terminal 4.

> **NOTE**
> *Take care when applying the voltage. Damage will result if the terminals are incorrect or are short circuited.*

2. Connect a digital-type voltmeter between terminal 1 and terminal 2.

3. While repeatedly racing the engine, measure the oxygen sensor output voltage.

| Engine | Oxygen Sensor Output Voltage | Remarks |
|:-------|:-----------------------------|:--------|
| Race | 4.5 V | Makes the air/fuel mixture rich by increasing engine speed |

4. If there is a problem, there may be an oxygen sensor malfunction.

**Tightening torque**
Heated oxygen sensor: 40-50 Nm (400-500 kg.cm, 29-36 lb.ft)

---

### Harness Inspection Procedure [2.7 V6]

<!-- Figure: HO2S harness inspection steps 1-3, harness side connector (H), source: FLA.pdf page 54 -->

**Step 1**

Measure the power supply voltage of the heated oxygen sensor.
- Connector: Disconnected
- Ignition switch: ON
- Voltage (V): Battery voltage

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFAA731B -->

**Step 2**

Check for open-circuit, or a short-circuit to ground between the engine control module and the heated oxygen sensor.
- Heated oxygen sensor connector: Disconnected
- ECM connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 3 |
| **NG** | Repair the harness. |

<!-- EFOC481C -->

**Step 3**

Check for continuity of the ground circuit.
- Connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFAA731D -->

---

<!-- EFOC4230 -->
## Camshaft Position Sensor

The CMP sensor senses the camshaft position on compression stroke of the No.1 cylinder, converts it into a pulse signal, and inputs it to the ECM. The ECM then computes the fuel injection sequence, etc. based on the input signal.

### Circuit Diagram

#### [2.7 V6]

<!-- Figure: CMP sensor circuit diagram showing 3-pin connector. Harness side connector (H). ECM connections: GND, Signal, +5V. Also shows CMP and CKP signal waveforms relative to TDC for cylinders #1-#6, with junction block, source: FLA.pdf page 55 -->

| CMP Connector Pin | Function |
|:------------------|:---------|
| 1 | Power supply (battery voltage, from junction block via SNSR FUSE 10A) |
| 2 | Signal (to ECM) |
| 3 | Ground (to ECM) |

---

### Harness Inspection Procedure [2.7 V6]

<!-- Figure: CMP sensor harness inspection steps 1-3, harness side connector (H), source: FLA.pdf page 56 -->

**Step 1**

Measure the power supply voltage.
- Connector: Disconnected
- Ignition switch: ON
- Voltage (V): Battery voltage

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFAA723F -->

**Step 2**

Check for continuity of the ground circuit.
- Connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 3 |
| **NG** | Repair the harness. |

<!-- EFOC4935 -->

**Step 3**

Check for an open-circuit, or a short-circuit to ground between the engine control module and CMP sensor.

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFOC4935H -->

---

### Troubleshooting Hints

If the camshaft position sensor does not operate correctly, correct sequential injection is not made so that the engine may stall or run irregularly at idle or fail to accelerate normally.

---

<!-- EFOC4250 -->
## Crankshaft Position Sensor

The crankshaft position sensor senses the crank angle (piston position) of each cylinder and converts it into a pulse signal. Based on the input signal, the ECM computes the engine speed and controls the fuel injection timing and ignition timing.

### Circuit Diagram

#### [2.7 V6]

<!-- Figure: CKP sensor circuit diagram showing 3-pin connector. Harness side connector (H). ECM connections: GND, +5V, Signal. Shows CMP and CKP waveforms relative to TDC for cylinders #1-#6, with junction block, source: FLA.pdf page 57 -->

| CKP Connector Pin | Function |
|:------------------|:---------|
| 1 | Power supply (battery voltage, from junction block via SNSR FUSE 10A) |
| 2 | Signal (to ECM C133-3 pin 8) |
| 3 | Ground (to ECM) |

---

### Troubleshooting Hints

1. If unexpected shocks are felt during driving or the engine stalls suddenly, shake the crankshaft position sensor harness. If this causes the engine to stall, check for poor sensor connector contact.

2. If the tachometer reads 0 rpm when the engine is cranked, check for faulty crank angle sensor, broken timing belt or ignition system problems.

3. If the engine can be run at idle even if the crank angle sensor reading is out of specification, check the following:
   - Faulty engine coolant temperature sensor
   - Faulty idle speed control motor
   - Poorly adjusted reference idle speed

---

### Using GST

| Check Item | Check Conditions | Check Content | Normal State |
|:-----------|:-----------------|:--------------|:-------------|
| Crankshaft position sensor | Engine cranking, Tachometer connected (check on and off ignition coil by tachometer) | Compare cranking speed and multi-tester reading | Indicated speed agrees |

| Check Item | Check Conditions | Coolant Temperature | Test Specification |
|:-----------|:-----------------|:--------------------|:-------------------|
| Crankshaft position sensor | Engine: Running at idle, Idle position switch: ON | When -20°C (-4°F) | 1,500-1,700 rpm |
| | | When 0°C (-32°F) | 1,300-1,550 rpm |
| | | When 20°C (68°F) | 1,000-1,400 rpm |
| | | When 40°C (104°F) | 1,000-1,200 rpm |
| | | When 80°C (176°F) | 650-850 rpm |

---

### Harness Inspection Procedure [2.7 V6]

<!-- Figure: CKP sensor harness inspection steps 1-3, harness side connector (H), source: FLA.pdf page 58 -->

**Step 1**

Measure the power supply voltage.
- Connector: Disconnected
- Ignition switch: ON
- Voltage (V): Battery voltage

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFAA725F -->

**Step 2**

Check for continuity of the ground circuit.
- Connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 3 |
| **NG** | Repair the harness. |

<!-- EFOC4B5G -->

**Step 3**

Check for continuity of the ground circuit.
- Connector: Disconnected
- Ignition switch: ON
- Voltage: 4.8-5.2 V

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFOC4925H -->

---

<!-- EFOC4090 -->
## Fuel Injector [2.7 V6]

The injectors inject fuel according to a signal coming from the ECM. The amount of fuel injected by the injectors is determined by the time during which the solenoid valve is energized.

### Circuit Diagram [2.7 V6]

<!-- Figure: Fuel injector circuit diagram showing 6 injectors (No.1-No.6), each with 2 pins. Pin 2 of each injector receives 12V from junction block. Pin 1 of each connects to ECM pins 33, 34, 35, 36, 37, 38 respectively, source: FLA.pdf page 59 -->

| Injector | ECM Pin |
|:---------|:--------|
| No. 1 | Pin 33 |
| No. 2 | Pin 34 |
| No. 3 | Pin 35 |
| No. 4 | Pin 36 |
| No. 5 | Pin 37 |
| No. 6 | Pin 38 |

**Injector Connector:**
- Pin 1: ECM drive signal (ground side)
- Pin 2: +12V supply from junction block

**Harness side connector (ABCDEF):**

<!-- Figure: Injector side connector (2-pin) and harness side connector (2-pin) views, source: FLA.pdf page 59 -->

---

### Injector Checking

#### Using HI-SCAN

| Check Item | Data Display | Check Conditions | Check Content | Test Specification |
|:-----------|:-------------|:-----------------|:--------------|:-------------------|
| Injector | Drive time | Engine: Cranking | 0°C (32°F) | Approx. 17 ms |
| | | | 20°C (68°F) | Approx. 35 ms |
| | | | 80°C (176°F) | Approx. 8.5 ms |

| Check Item | Data Display | Check Conditions | Engine State | Test Specification |
|:-----------|:-------------|:-----------------|:-------------|:-------------------|
| Injector | Drive time | Engine coolant temperature: 80 to 95°C (176 to 205°F), Lamps, electric cooling fan, accessory modules: All OFF, Transaxle: Neutral (P range for vehicle with A/T), Steering wheel: Neutral | Idle rpm | 2.2-2.9 ms |
| | | | 2,000 rpm | 1.8-2.8 ms |
| | | | Rapid racing | To increase |

> **NOTE**
> 1. *The injector drive time is when the supply voltage is 11V and the cranking speed is less than 250 rpm.*
> 2. *When engine coolant temperature is lower than 0°C (32°F), the ECM fires all four cylinders simultaneously.*
> 3. *When the vehicle is new (within initial operation of about 500 km [300 miles]), the injector drive time may be about 10% longer.*

#### Actuator Test

| Check Item | Item No. | Drive Content | Check Condition | Normal State |
|:-----------|:---------|:--------------|:----------------|:-------------|
| Injector | 01 | No. 1 injector shut off | Engine: Idling after warm-up (Shut off the injectors in sequence during and after engine warm-up, check the idle condition) | Idle should become unstable as injector shuts off. |
| | 02 | No. 2 injector shut off | | |
| | 03 | No. 3 injector shut off | | |
| | 04 | No. 4 injector shut off | | |
| | 05 | No. 5 injector shut off | | |
| | 06 | No. 6 injector shut off | | |

#### Using Stethoscope and Voltmeter

**Operation Sound Check:**

1. Using a stethoscope, check the injectors for clicking sound at idle. Check that the sound is produced at shorter intervals as the engine speed increases.

<!-- Figure: Stethoscope being used on fuel injector, source: FLA.pdf page 60 -->

> **NOTE**
> *Ensure that the sound from an adjacent injector is not being transmitted along the delivery pipe to an inoperative injector.*

2. If a stethoscope is not available, check the injector operation with your finger. If no vibrations are felt, check the wiring connector, injector, or injection signal from ECM.

**Resistance Measurement Between Terminals:**

3. Disconnect the connector at the injector.

4. Measure the resistance between terminals.

   **Standard value: 13 - 16Ω [at 20°C (68°F)]**

5. Connect the connector to the injector.

<!-- Figure: Measuring injector resistance with ohmmeter, source: FLA.pdf page 61 -->
<!-- Figure: Reconnecting injector connector, source: FLA.pdf page 61 -->

---

### Harness Inspection Procedure

<!-- Figure: Injector harness inspection steps 1-2, harness side connector (F/I) and connector (A), source: FLA.pdf page 61 -->

**Step 1**

Measure the power supply voltage.
- Connector: Disconnected
- Ignition switch: ON
- Voltage (V): Battery voltage

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFAA7309 -->

**Step 2**

Check for an open-circuit, or a short-circuit to ground between the engine control module and the injector.
- ECM connector: Disconnected
- Injector connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFAA730C -->

---

<!-- EFOC4310 -->
## Evaporative Emission Canister Purge Solenoid Valve

The evaporative emission canister purge solenoid valve is a duty control type, which controls purge air from the evaporative emission canister.

<!-- Figure: EVAP canister purge solenoid valve installed on engine, source: FLA.pdf page 62 -->

### Circuit Diagram

<!-- Figure: EVAP canister purge solenoid valve circuit diagram. Pin 1 receives 12V from MFI control relay. Pin 2 connects to ECM pin 42 (ground side drive). Harness side connector (H), source: FLA.pdf page 62 -->

| EVAP Purge Valve Connector Pin | Function |
|:-------------------------------|:---------|
| 1 | +12V supply from MFI control relay |
| 2 | ECM drive (pin 42) — ground side |

---

### Troubleshooting Procedures

<!-- Figure: EVAP canister purge solenoid valve troubleshooting flowchart, source: FLA.pdf page 63 -->

1. Engine: Running
2. Check wiring harness and connection. Is the connection OK?
   - **NO** --> Repair the wiring.
   - **YES** --> Continue
3. Check the electrical part of EVAP Canister Purge Control Solenoid Valve. Is the electrical part OK?
   - **NO** --> Replace the EVAP Canister Purge Control Solenoid Valve
   - **YES** --> Continue
4. Erase any diagnostic trouble codes from memory. Is same code present after rechecking?
   - **NO** --> OK
   - **YES** --> Replace PCM.

> DTC: Diagnosis Trouble Code
> PCM: Powertrain Control Module

#### Using HI-SCAN

| Check Item | Check Conditions | HI-SCAN Display | Type |
|:-----------|:-----------------|:----------------|:-----|
| Evaporative emission canister purge solenoid valve - Actuator test | IG. S/W ON (Do not start) | PCSV | Activate |

---

### Harness Inspection Procedure

<!-- Figure: EVAP purge solenoid harness inspection steps 1-2, harness side connectors (A) and (H), source: FLA.pdf page 64 -->

**Step 1**

Measure the power supply voltage.
- Connector: Disconnected
- Ignition switch: ON
- Voltage (V): Battery voltage

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFAA731C -->

**Step 2**

Check for an open-circuit, or a short-circuit to ground between the evaporative emission canister purge solenoid valve and the engine control module.
- Engine control module connector: Disconnected
- Evaporative emission canister purge solenoid valve connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFOC431D -->

---

<!-- EFOC4330 -->
## Knock Sensor

The knock sensor is attached to the cylinder block and senses engine knocking conditions. A knocking vibration from the cylinder block is applied as pressure to the piezoelectric element. This vibrational pressure is then converted into a voltage signal which is delivered as output. If engine knocking occurs, ignition timing is retarded to suppress it.

<!-- Figure: Knock sensor installed on cylinder block, source: FLA.pdf page 65 -->

### Circuit Diagram

#### [2.7 V6]

<!-- Figure: Knock sensor circuit diagram showing 3-pin connector. Harness side connector (A). ECM connections: pin 48 (Ground), pin 29/21 (Knock sensor), pin 30/32 (Knock sensor ground). Knock sensor mounted on engine block, source: FLA.pdf page 65 -->

| Knock Sensor Connector Pin | Function |
|:---------------------------|:---------|
| 1 | Knock sensor ground — to ECM pin 30/32 |
| 2 | Knock sensor signal — to ECM pin 29/21 |
| 3 | Ground — to ECM pin 48 |

---

### Troubleshooting Procedures

<!-- Figure: Knock sensor troubleshooting flowchart, source: FLA.pdf page 66 -->

1. Engine: Running
2. Check the wiring connection between knock sensor and PCM. Is the connection OK?
   - **NO** --> Repair the sensor.
   - **YES** --> Continue
3. Check the torque of the knock sensor. With the specification? (20 ± 5Nm)
   - **NO** --> Retorque the knock sensor bolt.
   - **YES** --> Continue
4. Is the knock sensor OK? (test by substitution)
   - **NO** --> Replace the knock sensor.
   - **YES** --> Continue
5. Erase any diagnostic trouble codes from memory. Is same code present after rechecking?
   - **NO** --> OK
   - **YES** --> Replace PCM.

> DTC: Diagnosis Trouble Code
> PCM: Powertrain Control Module

---

### Harness Inspection Procedure

<!-- Figure: Knock sensor harness inspection steps 1-2, harness side connector (A), source: FLA.pdf page 67 -->

**Step 1**

Check for an open-circuit, or a short-circuit to ground between the ECM and the knock sensor.
- ECM connector: Disconnected
- Knock sensor connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFOC433C -->

**Step 2**

Check for continuity of the ground circuit.
- Connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFAA733D -->

---

### Sensor Inspection

1. Disconnect the knock sensor connector.

2. Measure resistance between the terminal 2 and 3.

   **Standard value: about 5MΩ [at 20°C (68°F)]**

3. If the resistance is continual, replace the knock sensor.

**Tightening torque**
Knock sensor: 16-28Nm (160-250 kg.cm, 11.8-18.4 lb.ft)

4. Measure the capacitance between the terminal 2 and 3.

   **Standard value: 800-1600 pF**

<!-- Figure: Knock sensor side connector showing resistance and capacitance measurement between terminals 2 and 3, source: FLA.pdf page 67 -->

---

<!-- EFOC0080 -->
## Canister Close Valve

The canister close valve is an ON/OFF type which controls the inner pressure of fuel tank caused by fuel evaporation. It is used to close the evaporative system and to observe tank pressure respectively with the fuel tank pressure sensor.

<!-- Figure: Canister close valve installed location, source: FLA.pdf page 68 -->

### Circuit Diagram

<!-- Figure: Canister close valve circuit diagram. Pin 1 receives 12V from junction block. Pin 2 connects to ECM pin 30 (CCV Control). Harness side connector (A), source: FLA.pdf page 68 -->

| Canister Close Valve Connector Pin | Function |
|:-----------------------------------|:---------|
| 1 | +12V supply from junction block |
| 2 | ECM drive (pin 30) — CCV Control |

---

### Harness Inspection Procedure

<!-- Figure: Canister close valve harness inspection steps 1-2, harness side connector (A), source: FLA.pdf page 68-69 -->

**Step 1**

Check for an open-circuit, or a short-circuit to ground between the canister close valve and engine control module.
- ECM connector: Disconnected
- Canister close valve connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFOC0A08 -->

**Step 2**

Measure the power supply voltage.
- Connector: Disconnected
- Ignition switch: On
- Voltage: Battery voltage

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFAA739C -->

---

### Valve Inspection

Refer to EC GROUP - Emission Control System

---

### Troubleshooting Procedures

<!-- Figure: Canister close valve troubleshooting flowchart, source: FLA.pdf page 69 -->

1. Engine: Running
2. Check the wiring connection. Is the connection OK?
   - **NO** --> Repair the wiring.
   - **YES** --> Continue
3. Check the canister close valve. Is the valve OK?
   - **NO** --> Repair the valve.
   - **YES** --> Continue
4. Erase diagnostic trouble code from memory. Is same code No. present after rechecking?
   - **NO** --> (End)
   - **YES** --> Replace ECM.

> DTC: Diagnosis Trouble Code
> ECM: Engine Control Module

---

<!-- EFOC4410 -->
## Fuel Tank Pressure Sensor

The fuel tank pressure sensor is a pressure sensitive variable resistor. It measures the change of pressure in the fuel tank and monitors leakage detection. It is used to close the evaporative system and observes tank pressure respectively with canister close valve.

<!-- Figure: Fuel tank pressure sensor installed location, source: FLA.pdf page 70 -->

### Circuit Diagram

<!-- Figure: Fuel tank pressure sensor circuit diagram showing 3-pin connector. Harness side connector (A). ECM connections: pin 34 (Sensor supply voltage), pin 14 (Signal), pin 20 (Ground), source: FLA.pdf page 70 -->

| Fuel Tank Pressure Sensor Connector Pin | Function |
|:----------------------------------------|:---------|
| 1 | Signal — to ECM pin 14 |
| 2 | Ground — to ECM pin 20 |
| 3 | Sensor supply voltage — to ECM pin 34 |

---

### Harness Inspection Procedures

<!-- Figure: Fuel tank pressure sensor harness inspection steps 1-3, harness side connector (A), source: FLA.pdf page 71 -->

**Step 1**

Measure the power supply voltage.
- Connector: Disconnected
- Ignition switch: ON
- Voltage: 4.8-5.2V

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 2 |
| **NG** | Repair the harness. |

<!-- EFAA741B -->

**Step 2**

Check for an open-circuit, or a short-circuit to ground between the engine control module and the fuel tank pressure sensor.
- Fuel tank pressure sensor connector: Disconnected
- ECM connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | Go to Step 3 |
| **NG** | Repair the harness. |

<!-- EFOC441C -->

**Step 3**

Check for continuity of the ground circuit.
- Connector: Disconnected

| Result | Action |
|:-------|:-------|
| **OK** | END! |
| **NG** | Repair the harness. |

<!-- EFOC441D -->

---

### Sensor Inspection

Refer to EC GROUP - Emission Control System

---

### Troubleshooting Procedures

<!-- Figure: Fuel tank pressure sensor troubleshooting flowcharts (two procedures), source: FLA.pdf page 72 -->

**Procedure 1 — Evaporative System Leak Check:**

1. Engine: Running
2. Check the wiring connection. Is the connection OK?
   - **NO** --> Repair the wiring.
   - **YES** --> Continue
3. Check the leakage at evaporative system. Is it OK?
   - **NO** --> Repair or replace as necessary.
   - **YES** --> (End)

**Procedure 2 — Sensor/Valve Check:**

1. Engine: Running
2. Check the wiring connection. Is the connection OK?
   - **NO** --> Repair the wiring.
   - **YES** --> Continue
3. Check the fuel tank pressure sensor. Is the valve OK?
   - **NO** --> Repair the sensor.
   - **YES** --> Continue
4. Erase diagnostic trouble code from memory. Is same code No. present after rechecking?
   - **NO** --> (End)
   - **YES** --> Replace ECM.

> DTC: Diagnosis Trouble Code
> ECM: Engine Control Module
