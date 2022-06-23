import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pprint
import json

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

PLOT_PASSTHROUGH = False
assert not PLOT_PASSTHROUGH

PLOT_FREQ_VANILLA = True
PLOT_LUT_VANILLA = True

pp = pprint.PrettyPrinter(indent=4)

rectangle_colors = {
    "vanilla":     'darkgreen',
    "passthrough": 'gray',
    "cellift":     '#1f77b4', # default blue
    "glift":       'orange', # default orange
}

with open("fpga_critical_paths.json", "r") as f:
    data_paths = json.load(f) #
with open("fpga_luts.json", "r") as f:
    data_luts = json.load(f) #

design_names = list(data_paths.keys())

pp.pprint(data_paths)
pp.pprint(design_names)

##########
# Generate the data to plot
##########

plot_freqs = {}
for design_name in design_names:
    plot_freqs[design_name] = {}
    for instrumentation, data_path in data_paths[design_name].items():
        plot_freqs[design_name][instrumentation] = 1000/data_path if data_path else -1

plot_luts = {}
for design_name in design_names:
    plot_luts[design_name] = {}
    for instrumentation, data_lut in data_luts[design_name].items():
        plot_luts[design_name][instrumentation] = data_lut/1000

#####
# Gen the labels
#####

# Generate tick labels
xlabels = design_names.copy()

#######
# Plot the data
#######

spacing = 0.1
left_offset = spacing
width = 0.1

xticks_novanilla   = []
xticks_withvanilla = []
if PLOT_PASSTHROUGH:
    assert False
    # xticks.append( left_offset + 2*width              )
    # xticks.append( left_offset + 6*width  + spacing   )
    # xticks.append( left_offset + 10*width + 2*spacing )
    # xticks.append( left_offset + 14*width + 3*spacing )
    # xticks.append( left_offset + 18*width + 4*spacing )
else:
    xticks_novanilla.append( left_offset + 1*width                )
    xticks_novanilla.append( left_offset + 3*width    + spacing   )
    xticks_novanilla.append( left_offset + 5*width    + 2*spacing )
    xticks_novanilla.append( left_offset + 6.5*width  + 3*spacing )
    xticks_novanilla.append( left_offset + 7.5*width  + 4*spacing )

    xticks_withvanilla.append( left_offset + 1.5*width             )
    xticks_withvanilla.append( left_offset + 4.5*width + spacing   )
    xticks_withvanilla.append( left_offset + 7.5*width + 2*spacing )
    xticks_withvanilla.append( left_offset + 10*width  + 3*spacing )
    xticks_withvanilla.append( left_offset + 12.5*width  + 4*spacing )

fig, ax = plt.subplots(1, 2, figsize=(8, 2.4))
ax_freq, ax_lut = ax

# Data x coordinates
if PLOT_PASSTHROUGH:
    assert False
    # rects_vanilla_x     = [xticks[0]-1.5*width] + [xticks[1]-1.5*width] + [xticks[2]-1.5*width] + [xticks[3]-1.5*width] + [xticks[4]-1.5*width]
    # rects_passthrough_x = [xticks[0]-0.5*width] + [xticks[1]-0.5*width] + [xticks[2]-0.5*width] + [xticks[3]-0.5*width] + [xticks[4]-0.5*width]
    # rects_cellift_x     = [xticks[0]+0.5*width] + [xticks[1]+0.5*width] + [xticks[2]+0.5*width] + [xticks[3]+0.5*width] + [xticks[4]+0.5*width]
    # rects_glift_x       = [xticks[0]+1.5*width] + [xticks[1]+1.5*width] + [xticks[2]+1.5*width] + [xticks[3]+1.5*width] + [xticks[4]+1.5*width]
else:
    # If we don't print vanilla
    rects_cellift_novanilla_x = [xticks_novanilla[0]-0.5*width] + [xticks_novanilla[1]-0.5*width] + [xticks_novanilla[2]-0.5*width] + [xticks_novanilla[3]] + [xticks_novanilla[4]-0.5*width]
    rects_glift_novanilla_x   = [xticks_novanilla[0]+0.5*width] + [xticks_novanilla[1]+0.5*width] + [xticks_novanilla[2]+0.5*width]                         + [xticks_novanilla[4]-0.5*width]
    # If we also print vanilla
    rects_vanilla_x             = [xticks_withvanilla[0]-1.0*width] + [xticks_withvanilla[1]-1.0*width] + [xticks_withvanilla[2]-1.0*width] + [xticks_withvanilla[3]-0.5*width] + [xticks_withvanilla[4]-1.0*width]
    rects_cellift_withvanilla_x = [xticks_withvanilla[0]-0.0*width] + [xticks_withvanilla[1]-0.0*width] + [xticks_withvanilla[2]-0.0*width] + [xticks_withvanilla[3]+0.5*width] + [xticks_withvanilla[4]-0.0*width]
    rects_glift_withvanilla_x   = [xticks_withvanilla[0]+1.0*width] + [xticks_withvanilla[1]+1.0*width] + [xticks_withvanilla[2]+1.0*width]                                     + [xticks_withvanilla[4]+1.0*width]

# Data heights
if PLOT_PASSTHROUGH:
    assert False
    # rects_passthrough_yosys_y = [plot_freqs['yosys'][d][InstrumentationMethod.PASSTHROUGH] for d in design_names]
freq_rects_vanilla_y = [plot_freqs[d]["vanilla"] for d in design_names]
freq_rects_cellift_y = [plot_freqs[d]["cellift"] for d in design_names]
freq_rects_glift_y   = [plot_freqs["Ibex"]["glift"], plot_freqs["Rocket"]["glift"], plot_freqs["PULPissimo"]["glift"], plot_freqs["BOOM"]["glift"]]
lut_rects_vanilla_y  = [plot_luts[d]["vanilla"] for d in design_names]
lut_rects_cellift_y  = [plot_luts[d]["cellift"] for d in design_names]
lut_rects_glift_y    = [plot_luts["Ibex"]["glift"], plot_luts["Rocket"]["glift"], plot_luts["PULPissimo"]["glift"], plot_luts["BOOM"]["glift"]]

# Rectangles
if PLOT_PASSTHROUGH:
    assert False
    # ax.bar(rects_passthrough_x, rects_passthrough_y, width, alpha=1, zorder=3, color=rectangle_colors["passthrough"], ec='black')

if PLOT_FREQ_VANILLA:
    ax_freq.bar(rects_vanilla_x,             freq_rects_vanilla_y, width, alpha=1, zorder=3, color=rectangle_colors["vanilla"], ec='black', label="Original")
    ax_freq.bar(rects_cellift_withvanilla_x, freq_rects_cellift_y, width, alpha=1, zorder=3, color=rectangle_colors["cellift"], ec='black', label="CellIFT")
    ax_freq.bar(rects_glift_withvanilla_x,   freq_rects_glift_y,   width, alpha=1, zorder=3, color=rectangle_colors["glift"],   ec='black', label="GLIFT")
else:
    ax_freq.bar(rects_cellift_novanilla_x, freq_rects_cellift_y, width, alpha=1, zorder=3, color=rectangle_colors["cellift"], ec='black', label="CellIFT")
    ax_freq.bar(rects_glift_novanilla_x,   freq_rects_glift_y,   width, alpha=1, zorder=3, color=rectangle_colors["glift"],   ec='black', label="GLIFT")

if PLOT_LUT_VANILLA:
    ax_lut.bar(rects_vanilla_x,             lut_rects_vanilla_y, width, alpha=1, zorder=3, color=rectangle_colors["vanilla"], ec='black', label="Original")
    ax_lut.bar(rects_cellift_withvanilla_x, lut_rects_cellift_y, width, alpha=1, zorder=3, color=rectangle_colors["cellift"], ec='black', label="CellIFT")
    ax_lut.bar(rects_glift_withvanilla_x,   lut_rects_glift_y,   width, alpha=1, zorder=3, color=rectangle_colors["glift"],   ec='black', label="GLIFT")
else:
    ax_lut.bar(rects_cellift_novanilla_x, lut_rects_cellift_y, width, alpha=1, zorder=3, color=rectangle_colors["cellift"], ec='black', label="CellIFT")
    ax_lut.bar(rects_glift_novanilla_x,   lut_rects_glift_y,   width, alpha=1, zorder=3, color=rectangle_colors["glift"],   ec='black', label="GLIFT")

# ax_freq.legend(framealpha=1)
ax_lut.legend(framealpha=1)

# X ticks
if PLOT_FREQ_VANILLA:
    ax_freq.set_xticks(xticks_withvanilla, xlabels, fontsize=8)
else:
    ax_freq.set_xticks(xticks_novanilla, xlabels, fontsize=8)
if PLOT_LUT_VANILLA:
    ax_lut.set_xticks(xticks_withvanilla, xlabels, fontsize=8)
else:
    ax_lut.set_xticks(xticks_novanilla, xlabels, fontsize=8)

# Y label
ax_freq.set_ylabel("Frequency (MHz)")
ax_lut.set_ylabel("Lookup tables (thousands)")

# Tick LUTs on the right side
ax_lut.yaxis.tick_right()
ax_lut.yaxis.set_label_position("right")

ax_freq.grid(which='major', axis='y')
ax_lut.grid(which='major', axis='y')

fig.tight_layout()

plt.savefig("fpga.png", dpi=300)
plt.savefig("../figures/fpga.pdf", dpi=300)
