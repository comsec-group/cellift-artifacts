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

RUN bash -c "du -hs /.  ; find / -name '*.o' -o -name 'V*.a' | xargs -n50 rm  ; apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ; du -hs /. ; true" || true

COPY build-patches /build-patches/
WORKDIR /cellift-designs/cellift-chipyard
# More last minute changes
RUN /bin/patch -p1 </build-patches/patch-makefiles # apply last-minute patches to cellift-meta repo after image was frozen
RUN cd /cellift-designs/cellift-chipyard/cellift-boom/sw && tar xvf /build-patches/scenario_1_load_tainted_data_ok.tar
RUN mkdir -p /cellift-meta/design-processing/../../cellift-designs/cellift-chipyard/cellift-boom/taint_data/scenario_1_load_tainted_data_ok/ && echo 0 80000100 8 FFFFFFFFFFFFFFFF > /cellift-meta/design-processing/../../cellift-designs/cellift-chipyard/cellift-boom/taint_data/scenario_1_load_tainted_data_ok/taint_data.txt

# Execute Meltdown and Spectre experiments (data for Figure 11).
WORKDIR /cellift-meta/python-experiments
# Build spectre POCs, fdiv and no fdiv, and meltdown POC
RUN bash -c ". /cellift-meta/env.sh && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/boom_attacks_v1_nofdiv/ && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/boom_attacks_v1/ && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_1_load_tainted_data_forbidden/ && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_load_tainted_data_user_mode && make -C /cellift-designs/cellift-chipyard/cellift-boom/sw/scenario_load_tainted_data_user_mode/scenario_1_load_tainted_data_ok"
# Simulate them
RUN bash -c ". /cellift-meta/env.sh && python plot_tainted_elements.py"

