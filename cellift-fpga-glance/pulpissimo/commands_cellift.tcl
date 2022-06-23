create_project pulpissimo_cellift ./pulpissimo_cellift -part xcvu440-flga2892-3-e
add_files {../cellift.sv ../ift_boot_rom_hdac_fpga.sv ../model_6144x32_2048x32scm.sv ../ift_sram_fpga.sv ../soc_domain_dummy_fpga_top_taints.sv}
import_files -force -norecurse
import_files -fileset constrs_1 ../../constraints.xdc
set_property steps.synth_design.args.flatten_hierarchy full [get_runs synth_1]

set_property top soc_domain_fpga_top [current_fileset]
set_property top_file {pulpissimo_cellift.srcs/sources_1/imports/vivado_test/soc_domain_dummy_fpga_top_taints.sv} [current_fileset]

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
exit
