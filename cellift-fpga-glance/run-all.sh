set -e
for instr in  vanilla   cellift  glift
do
    for design in ibex pulpissimo boom rocket cva6
    do
            tcl=commands_${instr}.tcl
            (
                cd $design
                tfile=${instr}_proj/report_timing_impl.txt
                ufile=${instr}_proj/report_utilization_impl.txt
                ok=yes
                if [ ! -f $tfile -o ! -f $ufile ]
                then
                        echo " *** $design $instr reports missing"
                        ok=no
                fi
                if ! grep 'report_timing: Time' $PWD/$tfile; then ok=no; fi
                if ! grep 'report_utilization: Time' $PWD/$ufile; then ok=no; fi
                if [ $ok = yes ]
                then
                        echo " *** $design $instr reports complete"
                        continue
                fi
                bzip2 -k -d -f *.bz2
                echo " *** $design $instr not complete, synthesizing"
                rm -rf ${instr}_proj
                mkdir -p ${instr}_proj
                cd ${instr}_proj
                vivado -mode batch -source ../$tcl 
                echo return code: $?
                exit 0
            )
                exit 0
        done
done

