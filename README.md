# Artifacts Evaluation - README - Usenix Security 2022

## For Paper: CELLIFT: Leveraging Cells for Scalable and Precise Dynamic Information Flow Tracking in RTL

### Overview

Steps needed after this git repo is cloned:
1. Obtain the Docker image. (Human time: 1 minute. Computer time: likely many hours.)
2. Install Xilinx Vivado. (Human time: 2 minutes. Computer time: several hours.)
3. Run experiments. (Human time: 5 minutes, on and off. Computer time: several days.)

Welcome to the Artifact of this paper. We have made considerable effort to
make the process of reproducing experiments both reliable and painless,
and we hope that this shows. We will estimate the required computer time
and human time for each step.

Requirements:
Hardware: memory:
this is unfortunately a very heavyweight artifact, due to
the resource-intensive nature of the Verilog transformation and
synthesis into C++ code (especially by the competition, GLIFT), and of FPGA synthesis.
To reproduce all results, including memory requirements for C++ synthesis
(figure 7), 256GB will be required. If such a machine is not available,
re-using already-generated binaries in the Docker image is possible, but of
course this memory measurement step can't be done. Under these circumstances a
64GB desktop should be able to run all the remaining experiments.

Hardware: storage:
The Docker image is 330GB. A squashed and tidied image will be vastly
smaller, but it may be harder to provide incremental updates if needed,
hence our decision to make the huge, layered image available.
To download the image and download and install Vivado, together, we estimate
a total of 500GB of storage will be needed.

Software: OS:
we tested our Docker image on a Ubuntu 22.04 host machine.
But we expect any reasonable modern docker-capable distro will work.
The OS requirements for Vivado are of course entirely up to Xilinx,
but some recent Ubuntu distro's are supported.

Software: FPGA synthesis tool (no fpga hardware required):
We depend on Xilinx Vivado (we tested v2022.1) and a large device
target. This requires a license. If no license is available, a 30-day
trial license can be obtained automatically.

## Steps to reproduce this work

### Obtain the Docker image. (Human time: 1 minute. Computer time: likely many hours.)

First thing to do: retrieve evaluation image from dockerhub. This includes
all of the source code of CellIFT, and of target designs that were used
throughout the paper. This is excluding the FPGA results.

Pull image:

        docker pull docker.io/ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation

Stable digest:

        Digest: sha256:9a15d4070d321026ad4d5d9ba5a236842c6c456279f9c08f4fa4132de7b399ce

### Install Xilinx Vivado. (Human time: 5 minutes. Computer time: several hours.)

Download Vivado full edition from the Xilinx website. Install it in a
path of its own.  We use HOMEDIR/tools/xilinx/. To use it later, source
the settings file:

        ~/tools/xilinx/Vivado/2022.1/settings64.sh

### Start a container using the Docker image to run experiments. (Human time: 5 minutes, on and off. Computer time: several days.)

All experiments have already been reproduced inside this image, as can
be seen in the comments and commands in the Dockerfile. The Dockerfile
is also a convenient reference on how to run each experiment.

First, start a new container with the image:

        docker run -it docker.io/ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation /bin/bash

WARNING: if you exit this shell (thereby stopping the container), the
state will not be saved. If you wish to save the state, run a 'docker
commit' on the container to save its state.

This procedure assumes you don't want to rebuild *everything* from
scratch. If you do, the full source code for it is in /cellift-meta/
in the Docker image. The Dockerfile in there has the steps to produce
the base image that the artifact Dockerfile is based on (see hash-addressed
FROM line in the Dockerfile).

In the container, lots of the tools assume this environment, so we first do this:

        . /cellift-meta/env.sh

Assign `CELLIFT_JOBS` the desired degree of parallelism:

        export CELLIFT_JOBS=16

All the previously created experimental results are in
`/cellift-meta/experimental-data/`, so let's move them so the scripts
won't skip work because there are already results:

        mv /cellift-meta/experimental-data/ /cellift-meta/experimental-data-prev

this path contains charts and data from experiments captured on our own
systems and can be used as comparison material.

#### Cell microbenchmarks for reproducing Figure 6 (human time: several minutes at a time. computer time: a day)

        cd /cellift-meta/cellift-ubenchmarks
        make verilator_build NUM_EXECUTIONS=100000 
        make verilator_run NUM_EXECUTIONS=100000 -j$CELLIFT_JOBS
        make collect -j$CELLIFT_JOBS NUM_EXECUTIONS=100000"
        python3 plot_separate_perf_prec.py

The `verilator_build` step in particular takes a very long time unless there are many cores.
The final chart will be saved in

        /cellift-meta/cellift-ubenchmarks/fig/ubench_separate.png

and can be retrieved with `docker cp`. The result should look like Figure
6 in the paper.  Example:

        docker cp b446538f950c:/cellift-meta/cellift-ubenchmarks/fig/ubench_separate.png .           

#### Instrument and synthesize the design files for reproducing Figure 7 (human time: several minutes at a time. computer time: many hours)

The CellIFT-specific files for each verilog design target are in each of these
directories:

        /cellift-designs/cellift-chipyard/cellift-boom
        /cellift-designs/cellift-chipyard/cellift-rocket
        /cellift-designs/cellift-cva6/cellift
        /cellift-designs/cellift-ibex/cellift
        /cellift-designs/cellift-pulpissimo-hdac-2018/cellift

If you wish to rebuild the binaries to simulate the designs in the various
instrumentation modes, go to each of these directories, and build the
desired simulation binary targets. Building these is necessary to reproduce
Figure 7, the instrumentation and synthesis time.

        make clean # Otherwise nothing will happen, the binaries are already there
        bash tests.sh cellift_notrace
        bash tests.sh cellift_trace
        bash tests.sh glift_notrace
        bash tests.sh glift_trace
        bash tests.sh passthrough_notrace
        bash tests.sh vanilla_notrace
        bash tests.sh vanilla_trace

All of these have to be executed in each of the design directories
above. This will take a long time, in particular for the glift
targets. For Ariane (cellift-cva6 dir) and Boom (cellift-boom dir) the
glift targets eventually fail (timeout or OOM), so we recommend these
are skipped, although they can be tried if they are running on a machine
with a lot of memory and the evaluator has much patience.

The results are logged in `/cellift-meta/experimental-data/resources/`.
This data is collected and charted with:

        cd /cellift-meta/python-experiments
        python3 plot_instrumentation_performance.py
        python3 plot_rss.py

These scripts will print the path names of the output charts they produced:

    /cellift-meta/experimental-data/perfinstr-plot-1.png
    /cellift-meta/experimental-data/rss-perfbenchmark-plot-1.png

To copy the chart out and view it, `docker cp` can be used. The result should look
like Figure 7 in the paper.

#### Execute RISCV benchmarks on vanilla and instrumented designs to reproduce Figure 8 (human time: several minutes at a time. computer time: a few minutes on a fast machine)

To reproduce Figure 8 we execute benchmarks on many design variants. This is driven
by the plotting target, so we only have to do this:

        cd /cellift-meta/python-experiments
        python3 plot_benchmark_performance.py
        python3 plot_num_tainted_states_ibex.py

The result is in respectively:

        /cellift-meta/experimental-data/perf-slowdowns-perfbenchmark-plot-1-10.png
        /cellift-meta/python-experiments/numtaintedstates.png

Together these should look like Figure 8.

#### FPGA synthesis to reproduce Figure 9 (human time: several minutes at a time. computer time: several days)

Reproducing the FPGA synthesis experiments is outside a Docker container. 

Go to the Artifacts repo, to the `cellift-fpga-glance` dir. In each design directory, for each instrumentation
type, create a run directory, and execute `vivado` from there:

        cd cellift-fpga-glance/ibex
        mkdir run-vanilla
        cd run-vanilla
        vivado -mode tcl -source ../commands_vanilla.tcl

repeat this step for each design (ibex, cva6, pulpissimo, rocket, boom) and for each commands file
(`commands_cellift.tcl`, `commands_glift.tcl`, `commands_vanilla.tcl`). The results will be text files in
the run directories.

#### Execute Spectre and Meltdown POCs to reproduce Figure 11 (human time: a few minutes. computer time: a few minutes.)

To execute the code that reproduces Meltdown and Spectre and analyze the results:

        cd /cellift-meta/python-experiments
        make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/boom_attacks_v1_nofdiv/
        make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/boom_attacks_v1/
        make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_1_load_tainted_data_forbidden/
        make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_load_tainted_data_user_mode
        make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_1_load_tainted_data_ok
        python plot_tainted_elements.py

The final plot script produces 4 charts, each showing us the number of tainted elements as a function of time in
the 4 cases shown in Figure 11. The script prints the 4 output files. In our test run we see:

        /cellift-meta/experimental-data/experiments/plotcountelems-1-2147483904_255-2147483905_255-2147483906_255-2147483907_255-2147483908_255-2147483909_255-2147483910_255-2147483911_255-bin1680370330-5000-boom-3-meltdown-forbidden.png
        /cellift-meta/experimental-data/experiments/plotcountelems-1-2147483904_255-2147483905_255-2147483906_255-2147483907_255-2147483908_255-2147483909_255-2147483910_255-2147483911_255-bin1986445640-5000-boom-3-meltdown-not-forbidden.png
        /cellift-meta/experimental-data/experiments/plotcountelems-1-2147495992_255-2147495993_255-2147495994_255-2147495995_255-2147495996_255-2147495997_255-2147495998_255-2147495999_255-bin4243091483-2000-boom-3-spectre-fdiv.png
        /cellift-meta/experimental-data/experiments/plotcountelems-1-2147495992_255-2147495993_255-2147495994_255-2147495995_255-2147495996_255-2147495997_255-2147495998_255-2147495999_255-bin3832908077-2000-boom-3-spectre-nofdiv.png

The result should resemble the individual curves in Figure 11.

#### Execute architectural scenarios to support Section 8.4.

        cd /cellift-designs/cellift-pulpissimo-hdac-2018/cellift
        bash -e run_scenarios.sh

The expected output ends with:

        Bug 1 detected:  SPI and GPIO are tainted with the same store operation.
        Bug 6 detected:  SoC control and GPIO (APB) are tainted with the same store operation.
        Bug 8 detected:  SoC control and SPI and GPIO are tainted with the same store operation.
        Bug 4 detected:  GPIO lock has been written to by software.
        Bug 27 detected: Interrupt mask written from user mode.
        Bug 5 detected:  GPIO lock has been reset.
        Bug 25 hinted:   No mismatch in taint occurrence clock cycles.
        Experiment complete.

The experiments are described in Section 8.4 - we execute deliberately
buggy programs that our taint policy detects as such.  This is done by
analyzing the signal trace that each simulation in `scenarios.py`. The
control flow of that script is very readable and shows us how these
conclusions are reached in detail.

#### Execute stats to support Section 8.4. (human time: a few minutes. computer time: many hours.)

To reproduce the cellstats figure in the appendix, we provide the raw data
in the image, as they take quite some time to produce (instrmentation).

To generate the plot from this data:

        cd /cellift-meta/python-experiments
        python3 plot_cellstats.py

this produces

        /cellift-meta/python-experiments/cellstats.png

If you wish to regenerate the stats
file from scratch, remove the .log files in
`/cellift-designs/cellift-pulpissimo-hdac-2018/cellift/statistics`
and all other design dir. Then in each design dir, run:

        make statistics/glift.log statistics/cellift.log statistics/vanilla.log

and re-run the `plot_cellstats.py` script.
