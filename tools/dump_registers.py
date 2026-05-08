#!/usr/bin/env python3
"""
Dump all documented Adlar Aurora III Pro Modbus registers via the Waveshare
TCP-to-RTU gateway, and print the raw and ÷10 (scaled) values in a table.

Useful for:
  - Verifying which registers are populated on your firmware revision
    (e.g. checking whether registers 74/75 — AC voltage/current — return
    zero on your unit; see README "Important Caveats").
  - Comparing values between the Adlar documentation and the live unit.
  - Discovering scale-factor inconsistencies before wiring a sensor.

Usage:
  pip3 install pymodbus
  python3 dump_registers.py [HOST] [PORT] [SLAVE]

  HOST   Waveshare gateway IP (default: 10.57.16.59)
  PORT   TCP port (default: 8899)
  SLAVE  Modbus slave ID (default: 1; try 251 if no response)

Run while the compressor is actively running for the most informative output.
"""

import sys
from pymodbus.client import ModbusTcpClient

REGISTERS = [
    # (address, type, name from Adlar documentation)
    (38,   '3X', 'System status bits'),
    (40,   '3X', 'Room temp Tidr'),
    (42,   '3X', 'Inlet water TA'),
    (43,   '3X', 'Outlet water TB'),
    (46,   '3X', 'DHW tank TW'),
    (49,   '3X', 'Outdoor coil T3'),
    (50,   '3X', 'Ambient T4'),
    (52,   '3X', 'Discharge TP'),
    (53,   '3X', 'Suction TH'),
    (61,   '3X', 'Outlet water pressure'),
    (64,   '3X', 'Water flow'),
    (70,   '3X', 'EEV main opening'),
    (72,   '3X', 'No.1 DC fan speed'),
    (74,   '3X', 'AC input voltage'),       # <-- check this
    (75,   '3X', 'AC input current'),       # <-- and this
    (76,   '3X', 'DC bus voltage'),
    (77,   '3X', 'Compressor current'),
    (79,   '3X', 'Compressor actual freq'),
    (86,   '3X', 'High pressure'),
    (87,   '3X', 'Low pressure'),
    (2100, '4X', 'HVAC mode'),
    (2103, '4X', 'Function A bits'),
    (2107, '4X', 'Z1 heating setpoint'),
    (2114, '4X', 'Room temp setpoint'),
]


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else '10.57.16.59'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8899
    slave = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    c = ModbusTcpClient(host, port=port, timeout=5)
    c.connect()

    print(f"Host {host}:{port}  slave {slave}")
    print(f"{'Addr':>6} {'Type':<4} {'Name':<30} {'Raw':>8} {'÷10':>8}")
    print("-" * 65)

    for addr, reg_type, name in REGISTERS:
        try:
            if reg_type == '3X':
                try:
                    r = c.read_input_registers(address=addr, count=1, device_id=slave)
                except TypeError:
                    r = c.read_input_registers(address=addr, count=1, slave=slave)
            else:
                try:
                    r = c.read_holding_registers(address=addr, count=1, device_id=slave)
                except TypeError:
                    r = c.read_holding_registers(address=addr, count=1, slave=slave)

            if r.isError():
                print(f"{addr:>6} {reg_type:<4} {name:<30} {'ERROR':>8}")
            else:
                val = r.registers[0]
                print(f"{addr:>6} {reg_type:<4} {name:<30} {val:>8} {val/10:>8.1f}")
        except Exception as e:
            print(f"{addr:>6} {reg_type:<4} {name:<30} EXC: {e}")

    c.close()


if __name__ == '__main__':
    main()
