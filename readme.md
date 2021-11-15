# DShot Test

Test verilog integration with Litex.

   * verilog module only - host control through CSR

   * verilog module slave integrated with [A2P](https://git.openpower.foundation/cores/a2p) SOC (CSR or WB Slave control)

## fpga (no core)

```
make

wtf@GatorCountry:~/projects/a2p/rtl/dshotlitex_server --uart --uart-port /dev/ttyUSB1
[CommUART] port: /dev/ttyUSB1 / baudrate: 115200 / tcp port: 1234
Connected with 127.0.0.1:35646

wtf@GatorCountry:~/projects/a2p/rtl/dshot$ client.py
Opening...
CSR
 0            dshot_cfg FFF00000 0000529A
 1         dshot_cmd_01 FFF00008 00000000
 2         dshot_cmd_23 FFF0000C 00000000
 3         dshot_status FFF00010 00000000
 4      dshot_ev_status FFF00014 00000000
 5     dshot_ev_pending FFF00018 00000000
 6      dshot_ev_enable FFF0001C 00000000
 7             leds_out FFF00800 00000000
 8           ctrl_reset FFF01000 00000000
 9         ctrl_scratch FFF01004 12345678
10      ctrl_bus_errors FFF01008 00000000
w 0 x8000529a
> dshot_cfg=8000529A
w 1 x0ffc0ffc
> dshot_cmd_01=0FFC0FFC
```

## sim soc (no core) with uart

* need to ```touch mem.init``` - what is this?

```
reg [7:0] mem[0:34];
reg [5:0] memadr;
always @(posedge sys_clk) begin
	memadr <= basesoc_csr_bankarray_adr;
end

assign basesoc_csr_bankarray_dat_r = mem[memadr];

initial begin
	$readmemh("mem.init", mem);
end
```

```
verilator --cc --exe -Iunisims -Wno-TIMESCALEMOD -Wno-fatal cmod_a7.v uartsim.cpp tb.cpp --trace
cd obj_dir;make -f Vcmod_a7.mk;cd ..
obj_dir/Vcmod_a7

wtf@GatorCountry:~/projects/a2p/rtl/dshot$ obj_dir/Vcmod_a7
Initializing UART...
Listening on port 8675
Resetting...
Go!
cyc=0000000005   LED0=0
cyc=0000000005   LED1=0
cyc=0005000000
cyc=0010000000
cyc=0010434401   Enabled!
cyc=0012774169   LED0=1
cyc=0012774169   LED1=1
cyc=0012887877 Frames received=100
cyc=0015000000
cyc=0015355777 Frames received=200
cyc=0017823677 Frames received=300
cyc=0020000000
cyc=0020291577 Frames received=400
cyc=0022759477 Frames received=500
cyc=0025000000
cyc=0025227377 Frames received=600
cyc=0027695277 Frames received=700
cyc=0030000000
cyc=0030163177 Frames received=800
cyc=0032631077 Frames received=900
cyc=0035000000
cyc=0035098977 Frames received=1000
cyc=0037566877 Frames received=1100
cyc=0040000000
cyc=0040034777 Frames received=1200
cyc=0042502677 Frames received=1300
cyc=0044970577 Frames received=1400
cyc=0045000000
cyc=0047438477 Frames received=1500
cyc=0049906377 Frames received=1600
cyc=0050000000
Done.

You has opulence.
```

* start litex_server

```
wtf@GatorCountry:~/projects/a2p/rtl/dshot$ litex_server --uart --uart-port socket://localhost:8675
[CommUART] port: socket://localhost:8675 / baudrate: 115200 / tcp port: 1234
Connected with 127.0.0.1:59750
```

* start client app

```
wtf@GatorCountry:~/projects/a2p/rtl/dshot$ client.py
Opening...
CSR
 0            dshot_cfg FFF00000 0000529A
 1         dshot_cmd_01 FFF00008 00000000
 2         dshot_cmd_23 FFF0000C 00000000
 3         dshot_status FFF00010 00000000
 4      dshot_ev_status FFF00014 00000000
 5     dshot_ev_pending FFF00018 00000000
 6      dshot_ev_enable FFF0001C 00000000
 7             leds_out FFF00800 00000000
 8           ctrl_reset FFF01000 00000000
 9         ctrl_scratch FFF01004 12345678
10      ctrl_bus_errors FFF01008 00000000
w 0 0x8000529a
> dshot_cfg=8000529A
w 7 3
> leds_out=00000003
```
