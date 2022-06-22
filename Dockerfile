# Base our tests on the tools image; the hash is a snapshot of docker.io/ethcomsec/cellift:cellift-tools-main
#FROM ethcomsec/cellift@sha256:d9e837252e499feb4a9fb852947bcf16da8bfbc8c6e5144ef9decafc2da70ded
FROM docker.io/ethcomsec/cellift@sha256:61fd0d2e0ad79329dba62805f9ebe418aae65fd9adbd4c1fb013b4b4726d434b
COPY cellift-designs/*.tar.bz2 /cellift-designs/
WORKDIR /cellift-designs/
RUN for k in *.tar.bz2; do echo $k; tar -xjf $k; done
COPY tools /tools/
RUN /bin/python3 /tools/setup.py
WORKDIR /cellift-meta
RUN /bin/patch -p1 </tools/cellift-meta-patch # apply last-minute patches to cellift-meta repo after image was frozen
RUN /root/prefix-cellift/python-venv/bin/pip install -r /cellift-meta/design-processing/python-requirements.txt 

WORKDIR /cellift-designs/cellift-ibex/cellift
RUN bash tests.sh vanilla_trace
RUN bash tests.sh vanilla_notrace

WORKDIR /cellift-designs/cellift-chipyard/
RUN chown -R root /cellift-designs/cellift-chipyard ; bash ./scripts/init-submodules-no-riscv-tools.sh --skip-validate

WORKDIR /cellift-designs/cellift-chipyard/sims/verilator
RUN bash -c ". ../../../../cellift-meta/env.sh ; make CONFIG=MySmallVMRocketConfig"
WORKDIR /cellift-designs/cellift-chipyard/cellift-rocket
RUN bash tests.sh vanilla_trace
RUN bash tests.sh vanilla_notrace

WORKDIR /cellift-designs/cellift-chipyard/sims/verilator
RUN bash -c ". ../../../../cellift-meta/env.sh ; make CONFIG=MySmallBoomConfig"
WORKDIR /cellift-designs/cellift-chipyard/cellift-boom
RUN bash tests.sh vanilla_trace
RUN bash tests.sh vanilla_notrace
#RUN bash tests.sh glift_notrace

WORKDIR /cellift-designs/cellift-cva6/cellift
RUN bash tests.sh vanilla_trace
RUN bash tests.sh vanilla_notrace
#RUN bash tests.sh glift_notrace

WORKDIR /cellift-designs/cellift-pulpissimo-hdac-2018/cellift
RUN bash tests.sh vanilla_trace
RUN bash tests.sh vanilla_notrace

WORKDIR /cellift-designs/cellift-pulpissimo-hdac-2018/cellift
RUN bash tests.sh cellift_trace
RUN bash tests.sh cellift_notrace

WORKDIR /cellift-designs/cellift-cva6/cellift
RUN bash tests.sh cellift_trace
RUN bash tests.sh cellift_notrace

WORKDIR /cellift-designs/cellift-chipyard/cellift-boom
RUN bash tests.sh cellift_trace
RUN bash tests.sh cellift_notrace

WORKDIR /cellift-designs/cellift-chipyard/cellift-rocket
RUN bash tests.sh cellift_trace
RUN bash tests.sh cellift_notrace

WORKDIR /cellift-designs/cellift-ibex/cellift
RUN bash tests.sh cellift_trace
RUN bash tests.sh cellift_notrace

WORKDIR /cellift-designs/cellift-pulpissimo-hdac-2018/cellift
RUN bash tests.sh glift_notrace

WORKDIR /cellift-designs/cellift-ibex/cellift
RUN bash tests.sh glift_notrace

WORKDIR /cellift-designs/cellift-chipyard/cellift-rocket
RUN bash tests.sh glift_notrace

RUN bash -c "du -hs /.  ; find / -name 'V*.a' | xargs -n50 rm  ; apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ; du -hs /. ; true" || true

COPY build-patches /build-patches/
WORKDIR /cellift-designs/cellift-chipyard
# More last minute changes
RUN /bin/patch -p1 </build-patches/patch-makefiles # apply last-minute patches to cellift-meta repo after image was frozen
WORKDIR /cellift-meta/
RUN /bin/patch -p1 </build-patches/cellift-meta-patch # apply last-minute patches to cellift-meta repo after image was frozen
RUN cd /cellift-designs/cellift-chipyard/cellift-boom/sw && tar xvf /build-patches/scenario_1_load_tainted_data_ok.tar
RUN mkdir -p /cellift-meta/design-processing/../../cellift-designs/cellift-chipyard/cellift-boom/taint_data/scenario_1_load_tainted_data_ok/ && echo 0 80000100 8 FFFFFFFFFFFFFFFF > /cellift-meta/design-processing/../../cellift-designs/cellift-chipyard/cellift-boom/taint_data/scenario_1_load_tainted_data_ok/taint_data.txt

# Execute Meltdown and Spectre experiments (data for Figure 11).
WORKDIR /cellift-meta/python-experiments
# Build spectre POC, fdiv and no fdiv, and meltdown POC, allowed and unallowed load
RUN bash -c ". /cellift-meta/env.sh && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/boom_attacks_v1_nofdiv/ && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/boom_attacks_v1/ && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_1_load_tainted_data_forbidden/ && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_load_tainted_data_user_mode && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_1_load_tainted_data_ok"
# Simulate the POCs (4 executables)
RUN bash -c ". /cellift-meta/env.sh && python plot_tainted_elements.py"

# build glift trace, needed for instrumentation, synthesis, and benchmark performance plots
WORKDIR /cellift-designs/cellift-ibex/cellift
RUN bash tests.sh glift_trace

WORKDIR /cellift-designs/cellift-ibex/cellift
RUN bash tests.sh passthrough_notrace
WORKDIR /cellift-designs/cellift-cva6/cellift
RUN bash tests.sh passthrough_notrace
WORKDIR /cellift-designs/cellift-chipyard/cellift-boom
RUN bash tests.sh passthrough_notrace
WORKDIR /cellift-designs/cellift-chipyard/cellift-rocket
RUN bash tests.sh passthrough_notrace
WORKDIR /cellift-designs/cellift-pulpissimo-hdac-2018/cellift
RUN bash tests.sh passthrough_notrace

# Reproduce instrumentation & synthesis performance (Figure 7)
WORKDIR /cellift-meta/python-experiments
RUN bash -c ". ../env.sh && python3 plot_instrumentation_performance.py"
RUN bash -c ". ../env.sh && python3 plot_rss.py"

# Reproduce benchmark performance (Figure 8)
WORKDIR /cellift-meta/python-experiments
RUN bash -c ". ../env.sh && python3 plot_benchmark_performance.py"

# Reproduce scenarios experiments (described in Section 8.4)
WORKDIR /cellift-designs/cellift-pulpissimo-hdac-2018/cellift
RUN chown root /cellift-designs/cellift-pulpissimo-hdac-2018
RUN sed -i 's/riscv64-unknown-elf/riscv32-unknown-elf/' `git grep -l RISCV_PREFIX sw/bug*`
RUN bash -c ". /cellift-meta/env.sh && bash -e run_scenarios.sh"

# Reproduce ubench metrics (Figure 6)
COPY cellift-ubenchmarks /cellift-meta/cellift-ubenchmarks
WORKDIR /cellift-meta/cellift-ubenchmarks
RUN bash -c ". ../env.sh && make verilator_build NUM_EXECUTIONS=10 -j8"
RUN echo 100000 | tee `find . -name num_executions.txt`
RUN bash -c ". ../env.sh && make verilator_run NUM_EXECUTIONS=100000 -j$CELLIFT_JOBS"
RUN bash -c ". ../env.sh && make collect -j$CELLIFT_JOBS NUM_EXECUTIONS=100000"
RUN bash -c ". ../env.sh && python3 plot_separate_perf_prec.py"

# Generate FPGA dependencies for Ibex
WORKDIR /cellift-designs/cellift-ibex/cellift
COPY cellift-fpga-glance/morty_deps.sh /cellift-designs/cellift-ibex/cellift/
RUN bash -c ". /cellift-meta/env.sh && bash morty_deps.sh"

# Generate glift .sv files for FPGA
WORKDIR /cellift-designs/cellift-cva6/cellift 
RUN bash -c ". /cellift-meta/env.sh && make generated/out/glift.sv"
WORKDIR /cellift-designs/cellift-chipyard/cellift-boom
RUN bash -c ". /cellift-meta/env.sh && make generated/out/glift.sv"

# Reproduce instrumentation & synthesis performance (Figure 7)
# (Repeated)
WORKDIR /cellift-meta/python-experiments
RUN bash -c ". ../env.sh && python3 plot_instrumentation_performance.py"
RUN bash -c ". ../env.sh && python3 plot_rss.py"

# Reproduce benchmark precision performance (Figure 8)
WORKDIR /cellift-meta/python-experiments
RUN bash -c ". ../env.sh && python3 plot_num_tainted_states_ibex.py"
