set -e
(
	cd cellift-designs
	for k in cellift-chipyard cellift-cva6 cellift-ibex  cellift-pulpissimo-hdac-2018
	do	echo $k
		tar cjf ${k}.tar.bz2 $k
	done
)
(cd ../cellift-meta && git diff) >tools/cellift-meta-patch
docker build . 2>&1 | tee docker-build-log
