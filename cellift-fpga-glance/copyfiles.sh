
# fail on error
set -e

# Container name to create from image, just so we can copy files
# we don't even have to start it
containername=cellift-evaluation-container

# Remove the temporary container
docker rm $containername >/dev/null || true

# Create container so we can copy files
docker_cid=`docker create --name $containername ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation-2` 

docker cp ${containername}:/cellift-designs/cellift-ibex/cellift/generated/dependencies.sv ibex/
