# Artifacts Evaluation - README - Usenix Security 2022

## For Paper: CELLIFT: Leveraging Cells for Scalable and Precise Dynamic Information Flow Tracking in RTL

### Overview

Steps needed after this git repo is cloned:
1. Obtain the Docker image. (Human time: 1 minute. Computer time: likely many hours.)
2. Install Xilinx Vivado. (Human time: 2 minutes. Computer time: several hours.)
   (Optional, we included our own Vivado logs)
3. Run experiments. (Human time: 30 minutes, on and off. Computer time: several days.)

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
(figure 7), 256GB of RAM will be required. If such a machine is not available,
re-using already-generated binaries in the Docker image is possible, but of
course this memory measurement step can't be done. Under these circumstances a
desktop with 64GB of RAM should be able to run all the remaining experiments.

Hardware: storage:
The Docker image is 330GB. A squashed and tidied image will be vastly
smaller, but it may be harder to provide incremental updates if needed,
hence our decision to make the huge, layered image available.
To download the image and download and install Vivado, together, we estimate
a total of 500GB of storage will be needed.
Installing Vivado is optional.

Software: OS:
we tested our Docker image on a Ubuntu 22.04 host machine.
But we expect any reasonable modern docker-capable distro will work.
The OS requirements for Vivado are of course entirely up to Xilinx,
but some recent Ubuntu distro's are supported.

Software: FPGA synthesis tool (no fpga hardware required):
We depend on Xilinx Vivado (we tested v2019.3) and a large device
target. This requires a license. If no license is available, a 30-day
trial license can be obtained automatically. If you don't wish to
do this, you can use our Vivado logs.

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

(This is optional if you re-use the Vivado logs we provide; see later.)

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
targets. For Ariane (cellift-cva6 dir) and Boom (cellift-chipyard/cellift-boom dir) the
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

#### Execute RISCV benchmarks on vanilla and instrumented designs to reproduce Figure 8 (human time: several minutes at a time. computer time: several hours on a fast machine.)

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

First we show how to reproduce our results with our provided Vivado logs.
We go to the repo and execute the chart script. that takes as an
argument the root path where all the FPGA experiments and outputs are stored.
We provided our own in GITREPO/our-fpga-results. Let's reproduce these
first:

        cd GITREPO/cellift-fpga-glance/plot_fpga
        python3 plot.py ../../our-fpga-results

This gives output like:

        BOOM vanilla /home/beng/development/cellift-ae/our-fpga-results/boom_vanila/report_utilization_impl.txt
        BOOM vanilla /home/beng/development/cellift-ae/our-fpga-results/boom_vanila/report_timing_impl.txt
        data for paths:
        {   'Ariane': {'cellift': 25.64, 'vanilla': 11.693},
            'BOOM': {'cellift': 31.041, 'glift': 37.108, 'vanilla': 9.363},
            'Ibex': {'cellift': 14.305, 'glift': 19.345, 'vanilla': 9.509},
            'PULPissimo': {'cellift': 21.517, 'glift': 20.561, 'vanilla': 18.228},
            'Rocket': {'cellift': 18.705, 'glift': 29.265, 'vanilla': 6.94}}
        data for LUTs:
        {   'Ariane': {'cellift': 970154, 'vanilla': 41192},
            'BOOM': {'cellift': 1625704, 'glift': 1856776, 'vanilla': 73536},
            'Ibex': {'cellift': 17417, 'glift': 25871, 'vanilla': 3469},
            'PULPissimo': {'cellift': 154555, 'glift': 232830, 'vanilla': 32318},
            'Rocket': {'cellift': 104128, 'glift': 118598, 'vanilla': 11965}}
        ['BOOM', 'Ariane', 'PULPissimo', 'Ibex', 'Rocket']

And output in:

        fpga.png

Which should look like Figure 9. (Some re-ordering is likely.)

To reproduce all FPGA experiments, we need Vivado. This will take several
days.  First we source the settings file for Vivado. On our machine:

        source ~/tools/xilinx/Vivado/2022.1/settings64.sh

Now go to the Artifacts repo, to the `cellift-fpga-glance` dir.
Now, in each design directory, for each instrumentation type, create a
run directory, and execute `vivado` from there. To automate this, we do:

        cd GITREPO/cellift-fpga-glance
        sh run-all.sh

This will take a long time in total. The script does have some incremental
logic to skip fully complete synthesis runs, but it will take a little 
flexibility from the operator to abort the GLIFT runs when they take too
long. Intermediate results (see next step) can be generated continually,
as the output .txt files are generated at each synthesis step, so
long running synthesis cases are no disaster.

The end result of this step is `report_timing_impl.txt`,
`report_timing.txt`, `report_utilization_impl.txt`, and
`report_utilization.txt` in dirs `DESIGN/INSTR_proj` (for 5 DESIGN values
and 3 INSTR values).

To generate the plots for your own data, point the plot script to the
root of all the output files:

        cd GITREPO/cellift-fpga-glance/plot_fpga
        python3 plot.py ../

This again produces this output:

        fpga.png

Which should look like Figure 9. (Some re-ordering is likely.)

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
in the image, as they take quite some time to produce (instrumentation).

To generate the plot from this data:

        cd /cellift-meta/python-experiments
        python3 plot_cellstats.py

this produces

        /cellift-meta/python-experiments/cellstats.png

This should look like Figure 12.

If you wish to regenerate the stats
file from scratch, remove the .log files in
`/cellift-designs/cellift-pulpissimo-hdac-2018/cellift/statistics`
and all other design dir. Then in each design dir, run:

        make statistics/glift.log statistics/cellift.log statistics/vanilla.log

and re-run the `plot_cellstats.py` script.
