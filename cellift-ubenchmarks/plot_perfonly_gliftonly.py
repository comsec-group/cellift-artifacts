
from collections import defaultdict
import copy
import matplotlib.pyplot as plt
import numpy as np
import os
import pathlib
import re
import sys

PERF_DIV_FACTOR = 1000 # Display time in ms
PREC_DIV_FACTOR = 1000000 # Display precision in Mbits

cells = [
    "add",
    # "eq",
    # "ge",
    # "ge_signed",
    "shl_8",
    # "gt_signed",
    # "le",
    # "lt",
    "mul",
    # "neg",
    # "neq",
    # "reduce_and",
    "reduce_or",
    "reduce_xor",
    "gt",
    # "shr_8",
    # "sshr_8",
    # "sub"
]

# Graph style.
line_color = {
    'performance': {
        'cellift':   'green',
        'cellift_p': 'orange',
        'rtlift':    'grey'
    },
    'precision': {
        'cellift':   'black',
        'cellift_p': 'blue',
        'rtlift':    'brown'
    }
}
line_marker = {
    'performance': {
        'cellift':   ',',
        'cellift_p': ',',
        'rtlift':    ','
    },
    'precision': {
        'cellift':   ',',
        'cellift_p': ',',
        'rtlift':    ','
    }
}
line_width = {
    'performance': {
        'cellift':   '1.2',
        'cellift_p': '1.2',
        'rtlift':    '1.2'
    },
    'precision': {
        'cellift':   '1.4',
        'cellift_p': '1.4',
        'rtlift':    '1'
    }
}
line_style = {
    'performance': {
        'cellift':   '-',
        'cellift_p': '-',
        'rtlift':    '-'
    },
    'precision': {
        'cellift':   '--',
        'cellift_p': ':',
        'rtlift':    '--'
    }
}
instr_method_names = {
    'cellift':   'CellIFT',
    'cellift_p': 'GLIFT',
    'rtlift':    'RTLIFT'
}
cell_names = {
    "add":        "Adder",
    "eq":         "eq",
    "ge":         "ge",
    "ge_signed":  "ge (sign)",
    "gt":         "Greater Than",
    "gt_signed":  "gt (sign)",
    "le":         "le",
    "lt":         "lt",
    "mul":        "Multiplier",
    "neg":        "neg",
    "neq":        "neq",
    "reduce_and": "red_and",
    "reduce_or":  "Reduce OR",
    "reduce_xor": "Reduce XOR",
    "shl_8":      "Left Shift",
    "shr_8":      "shr",
    "sshr_8":     "sshr",
    "sub":        "sub"
}


num_cells = len(cells)
cell_data = {c: defaultdict(lambda : defaultdict(lambda : defaultdict(dict))) for c in cells}
# cell_data is a Dict[cell][instrmethod] = {
#                                             performance: {x: [], y: []},
#                                             precision:   {x: [], y: []}
#                                          }

# Prepare the high-level figure.
fig, axes = plt.subplots(1, num_cells, figsize=(12,2.5))
axes[0].set_ylabel('Simulation runtime (ms)')
fig.tight_layout()

# Print the grids.
for cell_id in range(num_cells):
    axes[cell_id].xaxis.set_major_locator(plt.MultipleLocator(16))
    axes[cell_id].grid()

# Add all the necessary axes.
performance_axes = []
precision_axes   = []
for cell_id in range(num_cells):
    # newx = axes[cell_id].twinx()
    # precision_axes.append(newx)
    performance_axes.append(axes[cell_id])
    axes[cell_id].set_xlabel(cell_names[cells[cell_id]])

# Display the axes in non-scientific format for readability.
for cell_id in range(num_cells):
    performance_axes[cell_id].ticklabel_format(axis='y', style='plain')
    # precision_axes[cell_id].ticklabel_format(axis='y', style='plain')


# Graph logic.
for cell_id, cell in enumerate(cells):
    # Prepare the first plot
    # plt.subplots(1, num_cells, cell_id) TODO
    # Read the content
    with open("collected/{}.txt".format(cell)) as f:
        cell_lines = f.readlines()
    # Read for each instrumentation type
    curr_instrumentation_method = None
    performance_or_precision = "performance" # Else precision
    curr_x = np.array([], dtype=np.int32)
    curr_y = np.array([], dtype=np.int32)
    for line in cell_lines:
        # Try to find the pattern `number, number` in the line
        curr_search = re.search(r"^(\d+), (\d+)[\s\n]*$", line)
        if curr_search:
            x = int(curr_search.group(1))
            y = int(curr_search.group(2))
            curr_x.append(x)
            curr_y.append(y)
        else:
            # First, save the current data.
            if curr_instrumentation_method:
                assert performance_or_precision in ["performance", "precision"]
                cell_data[cell][curr_instrumentation_method][performance_or_precision]['x'] = curr_x
                if performance_or_precision == "performance":
                    cell_data[cell][curr_instrumentation_method][performance_or_precision]['y'] = np.divide(curr_y, PERF_DIV_FACTOR)
                else:
                    cell_data[cell][curr_instrumentation_method][performance_or_precision]['y'] = np.divide(curr_y, PREC_DIV_FACTOR)

            # Second, open a new measurement window if requested.
            curr_search = re.search(r"^(performance|precision)_([a-z_]+)$", line)
            if curr_search:
                curr_x = []
                curr_y = []
                performance_or_precision = curr_search.group(1)
                curr_instrumentation_method = curr_search.group(2)
                assert curr_instrumentation_method in instr_method_names
    # Now, cell_data is populated. Populate the corresponding subfigure.
    for instr_method in cell_data[cell]:
        assert "performance" in cell_data[cell][instr_method]
        assert "precision" in cell_data[cell][instr_method]
    axes[cell_id].set_title(" ", fontsize=10)
    for instr_method in cell_data[cell]:
        if instr_method != "cellift_p":
            continue
        performance_axes[cell_id].plot(cell_data[cell][instr_method]["performance"]['x'], cell_data[cell][instr_method]["performance"]['y'], line_style["performance"][instr_method], marker=line_marker["performance"][instr_method], color=line_color["performance"][instr_method], linewidth=line_width["performance"][instr_method], label="Performance {}".format(instr_method_names[instr_method]))
        # precision_axes[cell_id].plot(cell_data[cell][instr_method]["precision"]['x'], cell_data[cell][instr_method]["precision"]['y'], line_style["precision"][instr_method], marker=line_marker["precision"][instr_method], color=line_color["precision"][instr_method], linewidth=line_width["precision"][instr_method], label="Precision {}".format(instr_method_names[instr_method]))

# Get legend from the "add" cell.
if not "add" in cells:
    raise ValueError("Expected the `add` cell to be displayed. Intended to use it to get the legend.")
performance_handles, performance_labels = performance_axes[cells.index("add")].get_legend_handles_labels()
# precision_handles, precision_labels = precision_axes[cells.index("add")].get_legend_handles_labels()

fig.legend(performance_handles, performance_labels, bbox_to_anchor=(0, 0.02, 1, 1), loc='upper center', ncol=len(performance_handles))

# Adjust the plot.
fig.subplots_adjust(wspace=1.0, hspace=0.1, top=0.8)
fig.tight_layout()

# Write the plot.
pathlib.Path("fig").mkdir(parents=True, exist_ok=True)

plt.savefig('fig/ubench-perfonly-gliftonly.png', dpi=300)
plt.savefig('fig/ubench-perfonly-gliftonly.pdf', dpi=300)
