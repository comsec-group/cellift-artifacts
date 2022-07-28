create_clock -name ref_clk_i -period 10.0 [get_ports ref_clk_i]

set_false_path -from [get_ports rstn_glob_i]
