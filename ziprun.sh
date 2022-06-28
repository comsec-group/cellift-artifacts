set -e
(
	cd cellift-designs
	for k in cellift-chipyard cellift-cva6 cellift-ibex  cellift-pulpissimo-hdac-2018
	do	echo $k
#		tar cjf ${k}.tar.bz2 $k
	done
)
#(cd ../cellift-meta && git diff) >build-patches/cellift-meta-patch
docker build -t ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation . 2>&1 | tee docker-build-log

# don't overwrite backup - backup is submitted image
# docker build -t ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation-backup . 2>&1 | tee docker-build-log-backup

#docker build -t ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation-squashed -f Dockerfile-squash . 2>&1 | tee docker-build-log-suqash
