# DShot Unit

Test verilog integration with Litex

   * verilog module only - host control through CSR

   * verilog module slave integrated with [A2P](https://git.openpower.foundation/cores/A2P) SOC (CSR or WB Slave control)


## Simple test of RTL with Litex Integration (no core)


### Sim

* is litex sim worth the hassle, or just create verilator tb?


### FPGA Test

```
dshot.py --build

litex_server --uart --uart-port /dev/ttyUSB1  # ymmv
```

```
wtf@GatorCountry:~/projects/a2p/rtl/dshot$ client.py
Opening...
CSR
 0            dshot_cfg FFF00000 29A00000
 1         dshot_cmd_01 FFF00004 00000000
 2         dshot_cmd_23 FFF00008 00000000
 3         dshot_status FFF0000C 00000000
 4      dshot_ev_status FFF00010 00000000
 5     dshot_ev_pending FFF00014 00000000
 6      dshot_ev_enable FFF00018 00000000
 7               dna_id FFF00800 140D224E4A2854
 8             leds_out FFF01000 00000000
 9           ctrl_reset FFF01800 00000000
10         ctrl_scratch FFF01804 12345678
11      ctrl_bus_errors FFF01808 00000000
w 8 3
> leds_out=00000003
```