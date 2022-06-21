ifndef CELLIFT_ENV_SOURCED
$(error Please re-source env.sh in the meta-repository first, see README.md)
endif

# This Makefile part is included by each cell

# Configuration
NUM_INSTANCES ?= 10
NUM_EXECUTIONS ?= 1000000 # The number of times the precision and performance tests are run for averaging.

# Supplied by the verilation or run script.
IFT_FLAVOR ?=
CELL_NAME ?=

STEP ?= 4

CELL_ABSPATH = $(shell pwd)
CELL_BUILD_PATH = $(CELL_ABSPATH)/build/$(CELL_NAME)
SRC = $(CELL_BUILD_PATH)/mycell.sv
YOSYS_SCRIPT = ../../common/yosys_scripts/$(IFT_FLAVOR).ys.template

verilator_build:
	python3 ../../common/python_scripts/verilator_build.py $(NUM_EXECUTIONS) $(CELL_ABSPATH)

verilator_run:
	python3 ../../common/python_scripts/verilator_run.py $(NUM_EXECUTIONS) $(CELL_ABSPATH)

collect:
	python3 ../../common/python_scripts/collect.py $(NUM_EXECUTIONS) $(CELL_ABSPATH)

yosys: $(CELL_BUILD_PATH)/yosys_out.sv
$(CELL_BUILD_PATH)/yosys_out.sv: $(CELL_BUILD_PATH)/sv2v_out.v $(YOSYS_SCRIPT) | $(CELL_BUILD_PATH)
	CELL_NAME=$(CELL_NAME) yosys -c $(YOSYS_SCRIPT)
	python3 ../../common/python_scripts/compress_concats.py $@ $@
	python3 ../../common/python_scripts/compress_right_side_concat.py $@ $@

$(CELL_BUILD_PATH)/sv2v_out.v: $(SRC) | $(CELL_BUILD_PATH)
	sv2v $< > $@

$(CELL_BUILD_PATH)/dv: | $(CELL_BUILD_PATH)
	rm -rf $@
	cp -r dv $@

$(SRC): templates/mycell.sv.template | $(CELL_BUILD_PATH)
	sed 's/<TEMPLATE_DATA_WIDTH>/$(DATA_WIDTH)/g' $< > $@
	sed -i 's/<TEMPLATE_NUM_INSTANCES>/$(NUM_INSTANCES)/g' $@

#
# FuseSoC
#

# $(CELL_BUILD_PATH)/mycell.core: ../../common/fusesoc/mycell.core.template | $(CELL_BUILD_PATH)
# 	sed 's/<TEMPLATE_DATA_WIDTH>/$(DATA_WIDTH)/g' $< > $@
# 	sed -i 's/<TEMPLATE_NUM_INSTANCES>/$(NUM_INSTANCES)/g' $@

fusesoc_build: $(CELL_BUILD_PATH)/yosys_out.sv $(CELL_BUILD_PATH)/dv
	echo $(NUM_INSTANCES) > $(CELL_BUILD_PATH)/num_instances.txt
	echo $(NUM_EXECUTIONS) > $(CELL_BUILD_PATH)/num_executions.txt
	cd $(CELL_BUILD_PATH); rm -rf fusesoc.conf; fusesoc library add mycell ../../../..; CELL_BUILD_PATH=$(CELL_BUILD_PATH) CELL_PATH=$(CELL_ABSPATH) CELL_DATA_WIDTH=$(DATA_WIDTH) CELL_NUM_INSTANCES=$(NUM_INSTANCES) fusesoc run --build mycell

fusesoc_run:
	cd $(CELL_BUILD_PATH); rm -rf fusesoc.conf; fusesoc library add mycell ../../../..; CELL_BUILD_PATH=$(CELL_BUILD_PATH) CELL_PATH=$(CELL_ABSPATH) CELL_DATA_WIDTH=$(DATA_WIDTH) CELL_NUM_INSTANCES=$(NUM_INSTANCES) fusesoc run --build mycell

$(CELL_BUILD_PATH)/fusesoc.conf:

build $(CELL_BUILD_PATH) $(CELL_BUILD_PATH)/plots:
	mkdir -p $@

clean:
	rm -rf build
