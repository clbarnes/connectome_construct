"""
Convert the neurone class edge list created by ??_from_xlsx.py into an individual neurone edge list (without zero-padding)
"""

import json
from collections import namedtuple
from itertools import product
from os.path import join
from extrasyn.paths import src_root, tgt_root
# from paths import src_root, tgt_root

etypes = ['ma', 'np']
Edge = namedtuple('Edge', ['src', 'tgt', 'transmitter', 'receptor'])
NODELIST_PATH = join(src_root, 'nodelist.txt')


def edge_gen_from_file(path):
    with open(path) as f:
        try:
            for row in f:
                r = row.strip()
                yield Edge(*r.split(','))
        except ValueError as e:
            if 'unpack' in str(e):
                raise StopIteration



def main(etype, include_weak):
    with open(join(src_root, 'class_to_neurons3.json')) as f:
        class_to_neurons = json.load(f)

    edges = []
    for edge in edge_gen_from_file(
            join(tgt_root, '{}_edgelist_classes{}.csv'.format(etype, '_include-weak' if include_weak else ''))
    ):
        sources = class_to_neurons[edge.src]  # , [edge.src])
        targets = class_to_neurons[edge.tgt]  # , [edge.tgt])
        for src, tgt in product(sources, targets):
            edges.append(Edge(src, tgt, edge.transmitter, edge.receptor))

    with open(join(
            tgt_root, '{}_edgelist{}.csv'.format(etype, '_include-weak' if include_weak else '')
    ), 'w') as f:
        for edge in edges:
            f.write('{},{},{},{}\n'.format(edge.src, edge.tgt, edge.transmitter, edge.receptor))

if __name__ == '__main__':
    for include_weak in [True, False]:
        main('ma', include_weak)

    main('np', False)
    print('done')