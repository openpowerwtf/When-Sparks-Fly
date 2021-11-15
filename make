#!/usr/bin/bash

code=
soc=dshot_no_core.py
top=build/cmod_a7/gateware/cmod_a7

vivado=vivado

program() {
   export PROGRAM_TOP=`basename $top`
   $vivado -mode tcl -source pgmfpga.tcl
   rm vivado*jou
   rm vivado*log
   rm -r .Xil
   echo ""
   echo ""
   echo "Done."
}

if [ "$1" == "-c" ]; then
   cp $code .
   echo "Updated code ($code)."
   echo ""
   echo ""
elif [ "$1" == "-p" ]; then
   program
   exit
elif [ "$1" != "" ]; then
   echo "make [-c|-p] (-c=also copy code, -p=just program"
   exit
fi

# build and program
python3 $soc --build
if [ $? -ne 0 ]; then
   exit
fi

echo "Copying .v and .bit, and programming..."
echo ""
echo ""
cp ${top}.v .
cp ${top}.bit .

program
