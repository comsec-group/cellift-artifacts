#!/usr/bin/python3

import itertools
import multiprocessing
import os
import pathlib
import re
import subprocess
import sys

from util import get_ift_flavors, get_data_widths

# sys.argv[1]: Num executions clog2
# sys.argv[2]: Cell abspath, for instance something/cellift-ubenchmarks/add

# This script evaluates the precision and simulation speed of GLIFT vs RTLIFT vs CellIFT.

DIVISION_FACTOR = 16
NUM_PROCESSES = (multiprocessing.cpu_count()+DIVISION_FACTOR)//DIVISION_FACTOR

cell_abspath = sys.argv[2]
NUM_EXECUTIONS = int(sys.argv[1])
ift_flavors = get_ift_flavors(cell_abspath)

def worker(ift_flavor_data_width_pair):
    ift_flavor, data_width = ift_flavor_data_width_pair
    cell_name = "mycell_{}_{}".format(ift_flavor, data_width)
    fusesoc_build_output_file_path = os.path.join(cell_abspath, "build/{}/yosys_output.txt".format(cell_name))
    pathlib.Path("build/{}".format(cell_name)).mkdir(parents=True, exist_ok=True)
    print(fusesoc_build_output_file_path)
    with open(fusesoc_build_output_file_path, "w") as out_file:
        proc = subprocess.run("make -B fusesoc_build IFT_FLAVOR={} DATA_WIDTH={} NUM_EXECUTIONS={} CELL_NAME={}".format(ift_flavor, data_width, NUM_EXECUTIONS, cell_name).split(" "), env=os.environ , stdout=out_file)

if __name__ == '__main__':
    my_pool = multiprocessing.Pool(NUM_PROCESSES)

    worker_data = []
    for ift_flavor in ift_flavors:
        curr_data_widths = get_data_widths(cell_abspath, ift_flavor)
        worker_data += [(ift_flavor, w) for w in curr_data_widths]

    my_pool.map(worker, worker_data)
    print("Verilate build complete.")
