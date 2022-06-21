# CellIFT microbenchmarks

## Dependencies

This requires sourcing the CellIFT meta-repository.

## Parameters

You can change the number of repetitions and steps in `common/include.mk`.

## How to use the unit tests

First, run `make verilator_build -j <number_of_cores/SOME_FACTOR>` where SOME_FACTOR should be typically 8 to 32 (because the Verilator synthesis step takes 32 cores per job).
Second, `make verilator_run -j <number_of_jobs>`.
Finally, `make collect -j <number_of_cores>`.

The results are collected per cell in the `collected/` directory.

Each text file in this directory is in the format:

```
performance_<ift_flavor>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
precision_<ift_flavor>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
performance_<another_ift_flavor>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
precision_<another_ift_flavor>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
<cell_width>, <exec_time_micros>
```

The `mul` and `add` cells have 3 ift_flaviors: cellift_p (aka. GLIFT+), rtlift and cellift.
The other cells have 2 ift_flaviors: cellift_p (aka. GLIFT+) and cellift.

The performance numbers of 0 in `mul` are several times failed builds.
The precision numbers of 0 are correct and expected when they happen.

## How to plot

Once the three steps above are done (i.e., the information is collected), run `python3 plot_separate_perf_prec.py`.

