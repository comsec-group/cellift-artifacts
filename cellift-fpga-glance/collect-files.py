import subprocess
import os

# list all designs, mapping fpga eval dir to image cellift dir
designs={
        'boom': '/cellift-designs/cellift-chipyard/cellift-boom',
        'cva6': '/cellift-designs/cellift-cva6/cellift',
        'rocket': '/cellift-designs/cellift-chipyard/cellift-rocket',
        'ibex': '/cellift-designs/cellift-ibex/cellift',
        'pulpissimo': '/cellift-designs/cellift-pulpissimo-hdac-2018/cellift'
}

def create_container():
    containername='cellift-evaluation-container'
    imagename='ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation'
    subprocess.call(['docker', 'rm', containername], stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    container_id=subprocess.check_output(['docker', 'create', '--name', containername, imagename])
    container_id=container_id.decode('ascii').rstrip()
    return container_id

def container_cmd(cmdlist):
    # docker run --rm --entrypoint ls  ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation
    containername='cellift-evaluation-container'
    imagename='ethcomsec/cellift-artifact-evaluation:cellift-artifact-evaluation'
    subprocess.call(['docker', 'rm', containername], stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    fullcmdline=['docker', 'run', '--rm',imagename] + cmdlist
#    print('executing: %s' % fullcmdline)
    output=subprocess.check_output(fullcmdline)
    return output.decode('ascii')

def basepath(file):
    assert file[0:3] == '../'
    bp=file[3:]
    assert os.path.basename(file) == bp
    return bp

def read_commands(tclfile):
    for line in open(tclfile):
        if 'add_files' not in line:
            continue
        assert 'add_files' in line
        assert '{' in line
        assert '}' in line
        filelist=line.split('{')[1].rstrip()
        assert '{' not in filelist
        assert '}' in filelist
        filelist = filelist[:-1]
        assert '}' not in filelist
        filelist = filelist.split()
        filelist=[basepath(f) for f in filelist]
        return filelist
    raise Exception('did not find add_files clause in %s' % tclfile)

for instr in ['cellift','glift','vanilla']:
  for designdir in list(designs):
#    print('%s -> %s' % (designdir,designs[designdir]))
    commands='%s/commands_%s.tcl' % (designdir, instr)
    filelist = read_commands(commands)
    for file in filelist:
        destfile='%s/%s' % (designdir, file)
        if os.path.exists(destfile):
            print('%s: exists' % destfile)
            continue
        result=container_cmd(['find',designs[designdir],'-name',file])
        results=result.split('\n')
        results=[r for r in results if len(r) > 0]
        results=[r for r in results if '/build/' not in r]
        if len(results) == 0:
            print('%s: not found' % destfile)
            continue
        if len(results) > 1:
            print('%s: ambiguous' % destfile)
            continue
        assert len(results) == 1
        result=results.pop()
        assert len(results) == 0
        print('%s for %s, result: %s' % (file, designdir, result))
        cid=create_container()
        cpline=['docker', 'cp', '%s:%s' % (cid, result), destfile]
        print('doing %s' % cpline)
        subprocess.check_call(cpline)
