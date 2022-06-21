#!/usr/bin/python3

import collections
import os
import re
import sys

from util import get_ift_flavors, get_data_widths

# sys.argv[1]: Num executions clog2
# sys.argv[2]: Cell abspath, for instance something/cellift-ubenchmarks/add

# This script evaluates the precision and simulation speed of GLIFT vs RTLIFT vs CellIFT.

cell_abspath = sys.argv[2]
NUM_EXECUTIONS = int(sys.argv[1])
ift_flavors = get_ift_flavors(cell_abspath)

execution_times = {ift_flavor: collections.defaultdict(list) for ift_flavor in ift_flavors}
num_tainted_outputs = {ift_flavor: collections.defaultdict(list) for ift_flavor in ift_flavors}

def worker(ift_flavor, data_width):
    cell_name = "mycell_{}_{}".format(ift_flavor, data_width)
    verilator_run_output_file_path = os.path.join(cell_abspath, "build/{}/verilator_run_output.txt".format(cell_name))
    with open(verilator_run_output_file_path, "r") as out_file:
        out_str = out_file.read()

    try:
        execution_times[ift_flavor][data_width] = int(re.findall("Execution time: (\d+)\s*micros", out_str)[-1])
    except:
        raise ValueError("Execution time not found in file {}".format(verilator_run_output_file_path))
    try:
        num_tainted_outputs[ift_flavor][data_width] = int(re.findall("Total tainted outputs: (\d+)\n", out_str)[-1])
    except:
        raise ValueError("Num tainted inputs not found in file {}".format(verilator_run_output_file_path))

if __name__ == '__main__':
    for ift_flavor in ift_flavors:
        curr_data_widths = get_data_widths(cell_abspath, ift_flavor)
        print("performance_"+ift_flavor)
        for data_width in curr_data_widths:
            worker(ift_flavor, data_width)
            print(str(data_width)+", "+str(execution_times[ift_flavor][data_width]))
        print("precision_"+ift_flavor)
        for data_width in curr_data_widths:
            worker(ift_flavor, data_width)
            print(str(data_width)+", "+str(num_tainted_outputs[ift_flavor][data_width]))
    print("Collect complete.")
