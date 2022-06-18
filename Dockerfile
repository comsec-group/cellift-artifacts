# handling dir cellift-designs/cellift-ibex, file Dockerfile
# Base our tests on the tools image
FROM docker.io/ethcomsec/cellift:cellift-tools-main
COPY cellift-designs/cellift-ibex /cellift-designs/cellift-ibex
WORKDIR /cellift-designs/cellift-ibex/cellift
RUN bash tests.sh

# handling dir cellift-designs/cellift-cva6, file Dockerfile
COPY cellift-designs/cellift-cva6 /cellift-designs/cellift-cva6
WORKDIR /cellift-designs/cellift-cva6/cellift
RUN bash tests.sh

# handling dir cellift-designs/cellift-pulpissimo-hdac-2018, file Dockerfile
# Base our tests on the tools image
COPY cellift-designs/cellift-pulpissimo-hdac-2018 /cellift-designs/cellift-pulpissimo-hdac-2018
WORKDIR /cellift-designs/cellift-pulpissimo-hdac-2018/cellift
RUN bash tests.sh

# handling dir cellift-designs/cellift-chipyard, file Dockerfile-base
# Base our tests on the tools image
COPY cellift-designs/cellift-chipyard /cellift-designs/cellift-chipyard
WORKDIR /cellift-designs/cellift-chipyard/
RUN bash ./scripts/init-submodules-no-riscv-tools.sh --skip-validate

# handling dir cellift-designs/cellift-chipyard, file Dockerfile-rocket
# Base our tests on the tools image
WORKDIR /cellift-designs/cellift-chipyard/sims/verilator
RUN bash -c ". ../../../../cellift-meta/env.sh ; make CONFIG=MySmallVMRocketConfig"
WORKDIR /cellift-designs/cellift-chipyard/cellift-rocket
RUN bash tests.sh

# handling dir cellift-designs/cellift-chipyard, file Dockerfile-boom
# Base our tests on the tools image
WORKDIR /cellift-designs/cellift-chipyard/sims/verilator
RUN bash -c ". ../../../../cellift-meta/env.sh ; make CONFIG=MySmallBoomConfig"
WORKDIR /cellift-designs/cellift-chipyard/cellift-boom
RUN bash tests.sh

