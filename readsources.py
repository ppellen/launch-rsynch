
def get_sources_from(f):
    sources = []
    f = open('sources.txt','r')
    for line in f.readlines():
        line = line.strip()
        if line.startswith('#') or len(line)==0:
            continue
        source = line  # r'"{src}"'.format(src=line)  NOK
        sources.append(source)
    return sources

if __name__ == '__main__':

    sources = get_sources_from('sources.txt')

    for s in sources:
        print(s)