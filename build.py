import sys

# Docker image tag prefix
tagprefix=''
is_firstfile=True
all_tags=set()

docker_context='./'

def handle_file(builddir, dockerfile, dockertag, all_dirs, fp):
    print('# handling dir %s, file %s' % (builddir, dockerfile), file=fp)
    for line in open(docker_context + '/' + builddir+'/'+dockerfile):
        line=line.rstrip()
        fields=line.split()
        if len(fields) < 1:
            continue
        if  fields[0] == 'FROM' and not is_firstfile:
            continue
        if  fields[0] == 'COPY':
            assert fields[1] == '.'
            fields[1] = builddir
            line=' '.join(fields)
        if fields[0] == 'CMD':
            fields[0] = 'RUN'
            line=' '.join(fields)
        print('%s' % (line,), file=fp)
#        if  fields[0] == 'FROM':
#            for k in all_dirs:
#                print('COPY %s /%s' % (k, k), file=fp)
    print('', file=fp)

dfn='Dockerfile'
filelist=[]
with open(dfn, 'w') as fp:
 for line in open('design-list'):
    line=line.rstrip()
    if line[0] == '#':
        continue
    fields=line.split()
    if len(fields) < 1:
        continue
    if fields[0] == '@tagprefix':
        tagprefix=fields[1]
        continue
    builddir=fields.pop(0)
    while len(fields) > 0:
        if len(fields) < 4:
            raise Exception('not enough words on line remaining: %s line: %s' % (fields,line,))
        if fields.pop(0) != 'FILE:':
            raise Exception('expecting FILE:, line %s' % line)
        dockerfile=fields.pop(0)
        if fields.pop(0) != 'TAG:':
            raise Exception('expecting TAG:, line %s' % line)
        dockertag_fields=fields.pop(0).split(':')
        assert len(dockertag_fields) == 2
        dockertag=dockertag_fields[1]
        filelist.append((builddir,dockerfile))
        assert dockertag not in all_tags
        all_tags.add(dockertag)

 all_dirs=[x[0] for x in filelist]
 print('all dirs: %s' % (all_dirs,))
 for builddir,dockerfile in filelist:
        handle_file(builddir, dockerfile, dockertag, all_dirs, fp)
        is_firstfile=False

print('docker build -f %s %s' % (dfn, docker_context))
