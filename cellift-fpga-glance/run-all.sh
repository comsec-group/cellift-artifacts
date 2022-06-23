set -e
for instr in  vanilla   cellift  glift
do
    for design in ibex  pulpissimo cva6 boom rocket
    do
            tcl=commands_${instr}.tcl
            (
                cd $design
                if [ -f ${instr}_proj/report_timing_impl.txt -a -f ${instr}_proj/report_timing.txt -a -f ${instr}_proj/report_utilization_impl.txt -a -f ${instr}_proj/report_utilization.txt ]
                then
                        echo " *** $design $instr report complete, skipping"
                        continue
                fi
                bzip2 -k -d -f *.bz2
                echo " *** $design $instr not complete, synthesizing"
                rm -rf ${instr}_proj
                mkdir -p ${instr}_proj
                cd ${instr}_proj
                vivado -mode batch -source ../$tcl 2>&1 | tee vivado-log-$design-$instr.txt
            )
        done
done

