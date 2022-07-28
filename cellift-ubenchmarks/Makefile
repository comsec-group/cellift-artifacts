ifndef CELLIFT_ENV_SOURCED
$(error Please re-source env.sh in the meta-repository first, see README.md)
endif

.PHONY: verilator_run

# ALL_CELL_TYPES = add eq ge ge_signed gt gt_signed le lt neg neq reduce_and reduce_or reduce_xor sub mul shr_8 sshr_8 shl_8
# We only plot the cells below
ALL_CELL_TYPES = add gt mul reduce_or reduce_xor shl_8

ALL_VERILATOR_BUILD_TARGETS = $(patsubst %,verilator_build_cell_%, $(ALL_CELL_TYPES))
.PHONY: verilator_build $(ALL_VERILATOR_BUILD_TARGETS)
verilator_build: $(ALL_VERILATOR_BUILD_TARGETS)
$(ALL_VERILATOR_BUILD_TARGETS): verilator_build_cell_%:
	make -C cells/$* verilator_build

ALL_VERILATOR_RUN_TARGETS = $(patsubst %,verilator_run_cell_%, $(ALL_CELL_TYPES))
.PHONY: verilator_run $(ALL_VERILATOR_RUN_TARGETS)
verilator_run: $(ALL_VERILATOR_RUN_TARGETS)
$(ALL_VERILATOR_RUN_TARGETS): verilator_run_cell_%:
	make -C cells/$* verilator_run

ALL_VERILATOR_COLLECT_TARGETS = $(patsubst %,collect_cell_%, $(ALL_CELL_TYPES))
.PHONY: collect $(ALL_VERILATOR_COLLECT_TARGETS)
collect: $(ALL_VERILATOR_COLLECT_TARGETS)
$(ALL_VERILATOR_COLLECT_TARGETS): collect_cell_%: | collected
	make -C cells/$* collect > collected/$*.txt

ALL_VERILATOR_CLEAN_TARGETS = $(patsubst %,clean_cell_%, $(ALL_CELL_TYPES))
.PHONY: clean $(ALL_VERILATOR_CLEAN_TARGETS)
clean: $(ALL_VERILATOR_CLEAN_TARGETS)
	rm -rf collected

$(ALL_VERILATOR_CLEAN_TARGETS): clean_cell_%:
	make -C cells/$* clean


collected:
	mkdir -p collected
