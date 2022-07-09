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
                if [ ! -s $tfile -o ! -s $ufile ]
                then
                        echo " *** $design $instr reports missing"
                        ok=no
                fi
                # Did synthesis exit cleanly?
                if ! grep -q '# report_utilization' ${instr}_proj/vivado.log 2>/dev/null; then ok=no; fi
                if ! grep -q '# report_timing' ${instr}_proj/vivado.log 2>/dev/null; then ok=no; fi
                if ! grep -q '# exit' ${instr}_proj/vivado.log 2>/dev/null; then ok=no; fi
                if [ $ok = yes ]
                then
                        echo " *** $design $instr reports complete, skipping synthesis"
                        continue
                fi
                echo " *** $design $instr not complete, synthesizing"
                bzip2 -k -d -f *.bz2
                rm -rf ${instr}_proj
                mkdir -p ${instr}_proj
#                cd ${instr}_proj
                vivado -mode batch -source $tcl  || true
                echo return code: $?
            )
        done
done

