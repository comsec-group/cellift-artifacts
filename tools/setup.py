
from multiprocessing import cpu_count

use_cpus = cpu_count()-2

with open('/cellift-meta/env.sh', 'a') as fp:
    print('export CELLIFT_JOBS=%d' % use_cpus, file=fp)
    print('export LOGRESOURCES=yes', file=fp)
