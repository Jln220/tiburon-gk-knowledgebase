# Fuel Pump — White Tiburon Signal & Power Diagram
**Car:** White Tiburon | **ECU:** Haltech Elite 2500 | **PDM:** AIM PDM 32

Click any node to open the relevant knowledgebase file.

---

## Power & Control Path

```mermaid
flowchart TD
    IGN(["🔑 Ignition Toggle<br/>PDM Conn B Pin 23<br/><i>SafeIgnition variable</i>"])
    KEY06(["⌨️ Key 06 — Fuel Override<br/>CAN Keypad 12 / CAN2<br/><i>manual override</i>"])
    RPM(["📊 RPM &gt; 50<br/>Haltech → CAN0 → PDM<br/><i>engine-running condition</i>"])
    PRIME(["⏱️ 3s Startup Prime<br/><i>on SafeIgnition rising edge</i>"])

    IGN -->|triggers| PRIME
    PRIME -->|3s then off| HP3
    RPM -->|engine running| HP3
    KEY06 -->|manual hold-on| HP3

    HP3["PDM HP3<br/>Pins A24 + A25<br/>15A OVC Protected<br/><i>freewheeling diode</i>"]

    HP3 -->|"12V switched"| FP["⛽ In-Tank Fuel Pump<br/><i>OEM or aftermarket</i>"]

    FP -->|"pressurized fuel"| FPR["Radium FPR / Damper<br/>OEM spec: 300 ± 1.5 kPa<br/>3.35 ± 0.06 kg/cm²"]

    FPR -->|"regulated supply"| RAIL["Injector Rail<br/>× 6 injectors"]
    FPR -->|"excess return"| TANK["Fuel Tank"]

    click IGN "Knowledgebase/builds/white-tiburon/build-profile.md" "Ignition switch wiring"
    click HP3 "Knowledgebase/hardware/aim-pdm/pdm-configuration-guide.md" "PDM output map"
    click FPR "Knowledgebase/builds/white-tiburon/build-profile.md" "Radium FPR details"
    click RAIL "Knowledgebase/common/shop-manual/fuel-system.md" "FLA-2: injector specs"
```

---

## Sensor & Monitoring Path

```mermaid
flowchart TD
    RAIL["Injector Rail<br/>pressurized fuel"]
    RETURN["Return Line"]

    SENSOR["Lowdoller PN 899404<br/>150 PSI / 500°F<br/>1/8 NPT — tapped on return line<br/><i>5-wire: +5V / GND / pressure / temp / shield</i>"]

    RAIL -->|"tapped"| SENSOR
    RETURN -->|"inline tap"| SENSOR

    PWR5V["Haltech +5V<br/>34-pin Pin 9 — Orange wire<br/><i>100mA ratiometric supply</i>"]
    GND["Signal Ground<br/>dedicated GND wire"]

    PWR5V -->|"supply"| SENSOR
    GND --> SENSOR

    SENSOR -->|"pressure 0.5–4.5V<br/><b>AVI 1</b><br/>26-pin Pin 13 — GY/Y shielded"| ECU["Haltech Elite 2500"]
    SENSOR -->|"temp PTC resistive<br/><b>AVI 2</b><br/>34-pin Pin 16 — O/B"| ECU

    ECU -->|"Fuel P + Fuel T<br/>broadcast on CAN0<br/>500 kbps"| PDM["AIM PDM 32<br/>CAN0 — Pins A22/A11"]

    PDM -->|"Fuel P low<br/>→ MULTI_WARNING"| LED["⚠️ Warning LED<br/>LP7 — Pin A20<br/>5A OVC"]

    click SENSOR "Knowledgebase/hardware/sensors/lowdoller-sensors.md" "Sensor specs and wiring"
    click PWR5V "Knowledgebase/hardware/haltech/main-connector-34-pin-elite2500.md" "34-pin pinout"
    click ECU "Knowledgebase/hardware/haltech/main-connector-26-pin-elite2500.md" "26-pin pinout (AVI 1)"
    click PDM "Knowledgebase/hardware/aim-pdm/pdm-pinout.md" "PDM pinout"
    click LED "Knowledgebase/hardware/aim-pdm/pdm-configuration-guide.md" "MULTI_WARNING logic"
```

---

## Reference Data

| Item | Value | Source |
|------|-------|--------|
| OEM fuel pressure (vac disconnected) | 330–350 kPa (47–50 psi) | `common/shop-manual/fuel-system.md` FLA-3 |
| OEM fuel pressure (vac connected) | ~270 kPa (~38 psi) | FLA-3 |
| Injector resistance | 13–16 Ω at 20°C | FLA-2 |
| Injector torque (delivery pipe bolt) | 10–15 Nm | FLA-4 |
| Sensor supply voltage | 5V DC / 100mA | Haltech 34-pin pin 9 |
| Sensor pressure output | 0.5–4.5V ratiometric | Lowdoller PN 899404 |
| AVI 1 pin (fuel pressure) | 26-pin pin 13 — GY/Y shielded | `build-knowledge-graph.json` |
| AVI 2 pin (fuel temp) | 34-pin pin 16 — O/B | `build-knowledge-graph.json` |
| PDM HP3 current limit | 15A OVC | `pdm-configuration-guide.md` |

---

## Related Files

| File | Contents |
|------|----------|
| [`hardware/aim-pdm/pdm-configuration-guide.md`](../../hardware/aim-pdm/pdm-configuration-guide.md) | HP3 trigger logic, fuel pump prime sequence |
| [`hardware/sensors/lowdoller-sensors.md`](../../hardware/sensors/lowdoller-sensors.md) | PN 899404 full specs, calibration tables |
| [`hardware/haltech/main-connector-26-pin-elite2500.md`](../../hardware/haltech/main-connector-26-pin-elite2500.md) | AVI 1 pin 13 details |
| [`hardware/haltech/main-connector-34-pin-elite2500.md`](../../hardware/haltech/main-connector-34-pin-elite2500.md) | AVI 2 pin 16, +5V pin 9 |
| [`common/shop-manual/fuel-system.md`](../../common/shop-manual/fuel-system.md) | FLA: OEM fuel pressure, injector specs, torques |
| [`build-knowledge-graph.json`](../build-knowledge-graph.json) | Machine-readable node graph for this car |
| [`signal-routing.md`](../signal-routing.md) | End-to-end signal routing table |
