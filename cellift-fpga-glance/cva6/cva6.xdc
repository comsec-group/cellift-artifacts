create_clock -name clk_i -period 10.0 [get_ports clk_i]

set_false_path -from [get_ports rst_ni]
