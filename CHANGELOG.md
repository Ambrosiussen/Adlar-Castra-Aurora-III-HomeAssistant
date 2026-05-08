# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-05-09

### Added

- Initial release.
- Supported models: Adlar Castra Aurora III Pro 7 kW, 9 kW, and 12 kW
  (R290). All share the same Modbus register map.
- 45+ sensors covering full register map from official Adlar Modbus
  documentation (water/refrigerant temperatures, hydraulics, compressor,
  electrical values, valve states, system pressures, error codes).
- Bidirectional control:
  - Zone 1 heating setpoint (register 2107)
  - DHW setpoint and on/off (registers 2102, 2105)
  - Room temperature setpoint (register 2114)
  - HVAC mode select (register 2100)
  - Zone control select (register 2101)
  - Silent mode select (register 2103, bits 4-5)
  - Forced electrical heater toggle (register 2103, bit 3)
- Calculated sensors:
  - DeltaT, thermal power, electrical power (apparent), live COP
  - Pressure delta, outlet-ambient delta
  - HVAC mode and zone control text representations
- Counters: compressor starts, defrost cycles
- Utility meters: starts per hour, defrosts per day
- History stats: runtime, defrost time, DHW time over 24h
- Notifications: water pressure too high, E-errors, P-errors
- Comprehensive README with installation, troubleshooting, and caveats
- Diagnostic Python script for verifying register behavior
- Sample Lovelace dashboard (`dashboard_section_sample.yaml`) covering
  all integration entities, with screenshots in the README

### Known issues

- **AC voltage (register 74) and AC current (register 75) return 0 on at
  least some Aurora III Pro firmware revisions**, even with the compressor
  running. Documented in README under "Important Caveats". As a result,
  `sensor.hp_electrical_power` and `sensor.hp_cop` will not return values
  on affected units. Registers are kept in the package on the assumption
  that a future Adlar firmware update may enable them, or that some unit
  revisions do support them. Workaround: install an external kWh meter.
