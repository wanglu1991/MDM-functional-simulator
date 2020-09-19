# MDM-functional-simulator

This directory includes code for running MDM with a functional simulator to collect trace. 

The directory GPGPUsim-generating-trace is developed from GPGPUsim to collect instruction/memory trace for GPU applications.
You need first run the Simulator in the function simulation mode. The trace is like "interval_info_i.txt" and "memory_access_i.txt". I equals to the kernel id.

Then copy the trace to the model directory.
The scripts to run the performance model is included in DRAM_run. We implement a script for sweeping different DRAM bandwidth in this directory.
In particular, generate_L2_access.py is used to analyze memory trace and generate miss information.
interval_warp_E_DRAM_sensitivity.py is the main MDM model script including interval analysis and MSHR/NOC/DRAM model.

