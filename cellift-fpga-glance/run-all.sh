set -e
for instr in  vanilla   cellift  glift
do
    for design in ibex  pulpissimo cva6 boom rocket
    do
            tcl=commands_${instr}.tcl
            (
                cd $design
                rm -rf ${instr}_proj
                mkdir -p ${instr}_proj
                cd ${instr}_proj
                vivado -mode tcl -source ../$tcl
            )
        done
done

