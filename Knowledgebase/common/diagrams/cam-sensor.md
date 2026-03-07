# Camshaft Position Sensor (CMP) — Component Diagram
**Applies to:** 2003 Hyundai Tiburon GK | 2.7L V6 Delta (G6BA) | Sensor type: Hall effect

Click any node to open the relevant knowledgebase file.

---

## Signal Path (OEM — Both Cars)

```mermaid
flowchart TD
    CAM["Camshaft<br/><i>G6BA — front bank<br/>cam journal area</i>"]
    CMP["📡 CMP Sensor<br/>Camshaft Position Sensor<br/>Hall effect — 3-wire<br/><i>12V supply / GND / signal</i>"]

    CAM -->|"target wheel passes"| CMP

    PWR["12V Supply<br/><i>from ECM or relay</i>"]
    GND["Signal Ground"]
    PWR --> CMP
    GND --> CMP

    CMP -->|"digital pulse signal"| ECM_OEM["OEM ECM<br/>Siemens SIMK43<br/><i>Blue car only</i>"]
    CMP -->|"digital pulse signal"| ECU_HT["Haltech Elite 2500<br/><i>White car — replaces OEM ECM</i>"]

    ECM_OEM -->|"cam timing data"| TUNE["GKFlasher Tune<br/><i>fuel + ignition maps</i>"]
    ECU_HT -->|"cam timing data"| NSP["NSP — Haltech<br/><i>Sequential injection<br/>Sequential COP ignition</i>"]

    click CMP "../../common/opengk/sensor-information.md" "OpenGK sensor specs + part numbers"
    click ECM_OEM "../../common/opengk/ecm-pinouts.md" "Siemens ECM pinout"
    click ECU_HT "../../hardware/haltech/main-connector-26-pin-elite2500.md" "Haltech 26-pin pinout"
    click TUNE "../../common/opengk/gkflasher.md" "GKFlasher ECU tuning"
```

---

## Connector & Wiring Detail

```mermaid
flowchart LR
    CMP_CONN["CMP Sensor Connector<br/><i>3-pin, engine harness</i>"]

    CMP_CONN -->|"Pin 1 — 12V supply"| FUSE["Fuse / Relay<br/><i>ECM-controlled supply</i>"]
    CMP_CONN -->|"Pin 2 — GND"| CHASSIS["Engine / Chassis Ground"]
    CMP_CONN -->|"Pin 3 — Signal"| ECU_PIN["ECU Signal Pin<br/><i>OEM: C133-1 connector<br/>Haltech: see 26-pin pinout</i>"]

    DTC_P0340["DTC P0340<br/>CMP Circuit Malfunction<br/><i>Open or short to battery<br/>Short between CMP wires</i>"]

    ECU_PIN -->|"if fault"| DTC_P0340

    click CMP_CONN "../../common/electrical-manual/connector-configurations.md" "ETM connector configurations"
    click ECU_PIN "../../common/opengk/ecm-pinouts.md" "OEM ECM connector C133-1"
    click DTC_P0340 "../../common/shop-manual/fuel-system.md" "FLA-73: DTC P0340 procedure"
```

---

## Cross-System References

```mermaid
flowchart TD
    CMP_NODE(["CMP Sensor<br/><b>comp-cmp-sensor</b>"])

    SPEC["Specs — FLA-2<br/>Type: Hall effect<br/>12V supply"]
    MFI["Role — FLA-20<br/>MFI control system<br/>cam phase reference"]
    DTC["DTCs — FLA-73<br/>P0340: Circuit Malfunction<br/>P0341: Range/Performance"]
    EC_SYS["Emission Control — EC<br/>System overview diagram"]
    ETM_LOC["ETM Component Locations<br/>CL section<br/><i>engine harness routing</i>"]
    OPENGK["OpenGK<br/>Replacement Part Numbers<br/>Compatible sensors"]
    FORUM["Forum — NewTiburon.com<br/><i>community-reviewed<br/>installation tips</i>"]

    CMP_NODE --> SPEC
    CMP_NODE --> MFI
    CMP_NODE --> DTC
    CMP_NODE --> EC_SYS
    CMP_NODE --> ETM_LOC
    CMP_NODE -.->|"community data"| OPENGK
    CMP_NODE -.->|"community-verified"| FORUM

    click SPEC "../../common/shop-manual/fuel-system.md" "FLA-2 sensor specifications"
    click MFI "../../common/shop-manual/fuel-system.md" "FLA-20 MFI control system"
    click DTC "../../common/shop-manual/fuel-system.md" "FLA-73 DTC P0340"
    click EC_SYS "../../common/shop-manual/emission-control-system.md" "EC chapter"
    click ETM_LOC "../../common/electrical-manual/component-locations.md" "ETM CL section"
    click OPENGK "../../common/opengk/sensor-information.md" "OpenGK sensor info"
```

---

## Reference Data

| Item | Value | Source |
|------|-------|--------|
| Sensor type | Hall effect | FLA-2 |
| OEM DTC | P0340 — CMP circuit malfunction | FLA-73 |
| Fault conditions | Open/short to battery between CMP and ECM; short between wires | FLA-73 |
| ECM connector | C133-1 | `common/opengk/ecm-pinouts.md` |
| Replacement sensor | See `common/opengk/sensor-information.md` | OpenGK |

---

## Related Files

| File | Contents |
|------|----------|
| [`common/shop-manual/fuel-system.md`](../shop-manual/fuel-system.md) | FLA-2 (specs), FLA-20 (MFI), FLA-73 (DTC P0340/P0341) |
| [`common/shop-manual/emission-control-system.md`](../shop-manual/emission-control-system.md) | EC chapter — system overview |
| [`common/electrical-manual/connector-configurations.md`](../electrical-manual/connector-configurations.md) | Engine harness connector codes |
| [`common/electrical-manual/component-locations.md`](../electrical-manual/component-locations.md) | Physical location on engine |
| [`common/opengk/ecm-pinouts.md`](../opengk/ecm-pinouts.md) | Siemens SIMK43 C133-1 connector |
| [`common/opengk/sensor-information.md`](../opengk/sensor-information.md) | Replacement part numbers |
| [`common/tiburon-knowledge-graph.json`](../tiburon-knowledge-graph.json) | Node: `comp-cmp-sensor` |
