#!/usr/bin/python3
#
# SOC controllable through host bridge CSR read/writes
#
# python3 dshot_no_core.py --no-compile-software --build

import os
import argparse

from litex.build.generic_platform import *
from cmod_a7 import cmod_a7

from migen import *
from litex.soc.cores.clock import *
from litex.soc.integration.soc import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores import dna
from litex.soc.cores.uart import *
from litex.soc.cores.led import LedChaser

from dshot import DShot

# CRG ----------------------------------------------------------------------------------------------
class _CRG(Module):

   def __init__(self, platform, sys_clk_freq):
     self.rst = Signal()
     self.clock_domains.cd_sys       = ClockDomain()
     self.clock_domains.cd_sys2x     = ClockDomain(reset_less=True)
     self.clock_domains.cd_sys2x_dqs = ClockDomain(reset_less=True)
     self.clock_domains.cd_idelay    = ClockDomain()

     self.submodules.pll = pll = S7MMCM(speedgrade=-1)
     self.comb += pll.reset.eq(platform.request('user_btn', 0) | self.rst)
     pll.register_clkin(platform.request('clk12'), 12e6)
     pll.create_clkout(self.cd_sys,       sys_clk_freq)
     pll.create_clkout(self.cd_sys2x,     2*sys_clk_freq)
     pll.create_clkout(self.cd_sys2x_dqs, 2*sys_clk_freq, phase=90)
     pll.create_clkout(self.cd_idelay,    200e6)
     platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin) # Ignore sys_clk to pll.clkin path created by SoC's rst.

     self.submodules.idelayctrl = S7IDELAYCTRL(self.cd_idelay)

# BaseSoC ----------------------------------------------------------------------------------------
class BaseSoC(SoCMini):

   def __init__(self, sys_clk_freq=100E6, with_analyzer=False, **kwargs):

      platform = cmod_a7.Platform()
      platform.add_source('dshot.v')

      SoCMini.__init__(self, platform, sys_clk_freq, csr_data_width=32,
                       ident='A2P DShot Test', ident_version=True)

      self.mem_map = {
         'csr':      0xFFF00000
      }

      # CRG --------------------------------------------------------------------------------------
      self.submodules.crg = _CRG(platform, sys_clk_freq)

      # Serial Controller (host master) ----------------------------------------------------------
      self.submodules.serial_bridge = UARTWishboneBridge(platform.request('serial'), sys_clk_freq)
      self.add_wb_master(self.serial_bridge.wishbone)

      # DShot Unit -------------------------------------------------------------------------------
      pins = {
         'chan_0': platform.request('digital', 40),  # P45
         'chan_1': platform.request('digital', 41),  # P46
         'chan_2': platform.request('digital', 42),  # P47
         'chan_3': platform.request('digital', 43)   # P48
      }

      dshot = DShot(pins)
      self.submodules.dshot = dshot
      self.add_csr('dshot')

      # Bling ------------------------------------------------------------------------------------
      self.submodules.leds = LedChaser(
         pads         = platform.request_all('user_led'),
         sys_clk_freq = sys_clk_freq)
      self.add_csr('leds')

      # Analyzer ---------------------------------------------------------------------------------
      if with_analyzer:
         analyzer_signals = [
             self.dshot.i_cfg,
             self.dshot.i_cmd_01,
             self.dshot.i_cmd_23,
             self.dshot.o_cmd_taken,
             self.chan_0,
             self.chan_1,
             self.chan_2,
             self.chan_3,
         ]
         self.submodules.analyzer = LiteScopeAnalyzer(analyzer_signals,
             depth        = 512,
             clock_domain = 'sys',
             csr_csv      = 'analyzer.csv')
         self.add_csr('analyzer')


# Build --------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='A2P DShot Test')

sys.argv.extend(['--csr-csv', 'csr.csv'])  # default

parser.add_argument('--sys-clk-freq', default=100e6, help='System clock frequency (default: 100MHz)')
parser.add_argument('--with-analyzer', action='store_true', help='Include analyzer')
parser.add_argument('--build', action='store_true', help='Do full build')

builder_args(parser)
soc_core_args(parser)
args = parser.parse_args()

soc = BaseSoC(
   sys_clk_freq           = int(float(args.sys_clk_freq)),
   with_analyzer          = args.with_analyzer,
   **soc_core_argdict(args)
)

builder = Builder(soc, **builder_argdict(args))
builder.build(run=args.build)
