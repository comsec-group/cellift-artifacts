# Artifacts Evaluation - README - Usenix Security 2022

## For Paper: CELLIFT: Leveraging Cells for Scalable and Precise Dynamic Information Flow Tracking in RTL

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
The Docker image is 300GB. A squashed and tidied image will be vastly
smaller, but it may be harder to provide incremental updates if needed,
hence our decision to make the huge, layered image available.

Software: OS:
we tested our Docker image on a Ubuntu 22.04 host machine.

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
docker pull ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation

### Start a container using the Docker image

All experiments have already been reproduced inside this image, as can
be seen in the comments and commands in the Dockerfile.

Start a new container with the image:
docker run -it ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation /bin/bash

