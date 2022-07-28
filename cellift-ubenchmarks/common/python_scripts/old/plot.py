#!/usr/bin/python3

import matplotlib.pyplot as plt
import json

with open("build/outputs.json", "r") as json_file:
    outputs = json.load(json_file)

num_tainted_outputs = outputs["num_tainted_outputs"]
execution_times_ms = outputs["execution_times_ms"]
num_cells = outputs["num_cells"]

Xs = num_tainted_outputs["glift"].keys()


fig = plt.figure()
axes = fig.add_subplot(1,1,1)
# axes.minorticks_on()
axes.grid(which='major')
# axes.grid(which='minor', linestyle=':', linewidth='.6')

plt.plot(Xs, num_tainted_outputs["glift"].values(), label="glift", color="orange")
plt.plot(Xs, num_tainted_outputs["cellift_p"].values(), label="cellift_p", color="darkblue")
plt.plot(Xs, num_tainted_outputs["cellift"].values(), label="cellift", color="red")
plt.plot(Xs, num_tainted_outputs["rtlift"].values(), label="rtlift", color="red")



for lbl_id, lbl in enumerate(axes.xaxis.get_ticklabels()):
    if (lbl_id+1) % 10:
        lbl.set_visible(False)

plt.xlabel('Input width (bits)')
plt.ylabel('Total number of tainted outputs')
plt.title('False positive evaluation')
plt.legend()
plt.savefig('build/plots/num_tainted_outputs.png', dpi=300)
plt.close()





fig = plt.figure()
axes = fig.add_subplot(1,1,1)
# axes.minorticks_on()
axes.grid(which='major')
# axes.grid(which='minor', linestyle=':', linewidth='.6')
axes2 = axes.twinx()

axes.plot(Xs, execution_times_ms["glift"].values(), label="glift", color="orange")
axes.plot(Xs, execution_times_ms["cellift_p"].values(), label="cellift_p", color="darkblue")
axes.plot(Xs, execution_times_ms["cellift"].values(), label="cellift", color="red")
axes.plot(Xs, execution_times_ms["rtlift"].values(), label="rtlift", color="red")

axes.set_ylabel('Simulation duration (ms) -- lines')

axes2.plot(Xs, num_cells["glift"].values(), ".", label="glift", color="orange")
axes2.plot(Xs, num_cells["cellift_p"].values(), ".", label="cellift_p", color="darkblue")
axes2.plot(Xs, num_cells["cellift"].values(), ".", label="cellift", color="red")
axes2.plot(Xs, num_cells["rtlift"].values(), ".", label="rtlift", color="red")

axes2.set_ylabel('Number of cells -- dots')


for lbl_id, lbl in enumerate(axes.xaxis.get_ticklabels()):
    if (lbl_id+1) % 10:
        lbl.set_visible(False)

plt.xlabel('Input width (bits)')
plt.title('Speed evaluation')
plt.legend()
plt.savefig('build/plots/execution_times_ms.png', dpi=300)
