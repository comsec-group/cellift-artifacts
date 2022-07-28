#!/usr/bin/python3

import json
import os
import re
import subprocess
import sys

# sys.argv[1]: Num executions clog2
# sys.argv[2]: Data width
# sys.argv[3]: Step
# sys.argv[4]: Cell abspath, for instance something/cellift-ubenchmarks/add

# This script evaluates the precision and simulation speed of GLIFT vs RTLIFT vs CellIFT.

SUPPORTED_IFT_FLAVORS = ["cellift", "cellift_p", "rtlift"]

# @param cell_abspath: example: something/cellift-ubenchmarks/add
def get_ift_flavors(cell_abspath):
    # Get the current type from the parameter
    curr_cell_type = os.path.basename(cell_abspath)
    # Read targets.json
    with open("../../targets.json", "r") as f:
        targets_content = json.load(f)
    # Get the list of IFT flavors from the target
    if not curr_cell_type in targets_content:
        raise ValueError("Cell type not found in targets.json: {} (basename of path {}).".format(curr_cell_type, cell_abspath))
    ret_list = targets_content[curr_cell_type]
    # Ensure the list is valid, and then return
    if not ret_list:
        raise ValueError("IFT flavor list is empty for cell type {}.".format(curr_cell_type))
    for elem in ret_list:
        if elem not in SUPPORTED_IFT_FLAVORS:
                raise ValueError("IFT flavor not supported: {}".format(elem))
    return ret_list 


NUM_EXECUTIONS_CLOG2 = int(sys.argv[1])
DATA_WIDTHS = [i for i in range(1, int(sys.argv[2]), int(sys.argv[3]))]
ift_flavors = get_ift_flavors(sys.argv[4])

num_tainted_outputs = dict()
execution_times_ms = dict()
num_cells = dict()
for ift_flavor in ift_flavors:
    num_tainted_outputs[ift_flavor] = dict()
    execution_times_ms[ift_flavor] = dict()
    num_cells[ift_flavor] = dict()
    for data_width in DATA_WIDTHS:
        with open("build/outputs/output_{}_{}.txt".format(ift_flavor, data_width), "w") as out_file:
            proc = subprocess.run("make -B fusesoc IFT_FLAVOR={} DATA_WIDTH={} NUM_EXECUTIONS_CLOG2={}".format(ift_flavor, data_width, NUM_EXECUTIONS_CLOG2).split(" "), stdout=out_file)
        print("build/outputs/output_{}_{}.txt".format(ift_flavor, data_width))
        with open("build/outputs/output_{}_{}.txt".format(ift_flavor, data_width), "r") as out_file:
            out_str = out_file.read()

        num_tainted_outputs[ift_flavor][data_width] = int(re.findall("Total tainted outputs: (\d+)\s", out_str)[-1])
        execution_times_ms[ift_flavor][data_width] = int(re.findall("Execution time: (\d+)ms", out_str)[-1])

        # Find the number of cells
        num_cells[ift_flavor][data_width] = int(re.findall("Number of cells:\s*(\d+)\n", out_str)[-1])

print({"num_tainted_outputs": num_tainted_outputs, "execution_times_ms": execution_times_ms, "num_cells": num_cells})
with open("build/outputs.json", "w") as out_file:
    json.dump({"num_tainted_outputs": num_tainted_outputs, "execution_times_ms": execution_times_ms, "num_cells": num_cells}, out_file)
