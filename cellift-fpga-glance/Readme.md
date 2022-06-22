# CellIFT FPGA Glance

This repository helps reproducing the FPGA results provided in the CellIFT paper.

## Prerequisites

- Have Vivado installed.
- Be in a CellIFT environment.
- Have instrumented the designs. 

## Instructions

For each design and for each instrumentation method, we provide a command script for Vivado.

These scripts require the SystemVerilog representation of the design instrumented with the design of your choice (vanilla (not instrumented), CellIFT or GLIFT).
You must first generate these files in the corresponding design repositories.
For example using the `make run_vanilla_notrace` command in the `cellift` directory of the `ibex` repository will generate `vanilla.sv` in `cellift/generated/out` in the `ibex` repository.
You can then copy `<ibex_repository>/cellift/generated/out/vanilla.sv` into `<this repository>/ibex`.
You can proceed in the same way for all the other designs and instrumentation methods.

The FPGA toplevel SystemVerilog files are provided in the respective repositories as well, for example `ibex_fpga_top.sv` (for Vanilla) and `ibex_fpga_top_taints.sv` (for CellIFT and GLIFT).

Special design-specific instructions are present in some subfolders of this repository.
