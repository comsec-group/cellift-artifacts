create_project boom_vanilla ./boom_vanilla -part xcvu440-flga2892-3-e
add_files {../boom_fpga_top.sv ../vanilla.sv}
import_files -force -norecurse
import_files -fileset constrs_1 ../../constraints.xdc
set_property steps.synth_design.args.flatten_hierarchy full [get_runs synth_1]

set_property top boom_fpga_top [current_fileset]
set_property top_file {boom_vanilla.srcs/sources_1/imports/vivado_test/boom_fpga_top.sv} [current_fileset]

launch_runs -jobs 8 synth_1
wait_on_run synth_1
open_run synth_1
report_timing > report_timing.txt
report_utilization > report_utilization.txt

launch_runs -jobs 8 impl_1
wait_on_run impl_1
open_run impl_1
report_timing > report_timing_impl.txt
report_utilization > report_utilization_impl.txt
