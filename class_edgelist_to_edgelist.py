"""
Convert the neurone class edge list created by ??_from_xlsx.py into an individual neurone edge list (without zero-padding)
"""

import json
from collections import namedtuple
from itertools import product
from datetime import date
from construct2.paths import src_root, tgt_root
from os.path import join

# etypes = ['np', 'ma']
etypes = ['ma']


def main(include_weak=False):
    with open(join(src_root, 'class_to_neurons2.json')) as f:
        class_to_neurons = json.load(f)

    Edge = namedtuple('Edge', ['src', 'tgt', 'transmitter', 'receptor'])

    def edge_gen_from_file(etype):
        with open(join(
                tgt_root, '{}_edgelist_classes{}.csv'.format(etype, '_include_weak' if include_weak else '')
        )) as f:
            try:
                for row in f:
                    r = row.strip()
                    yield Edge(*r.split(','))
            except ValueError as e:
                if 'unpack' in str(e):
                    raise StopIteration

    for etype in etypes:
        edges = []
        for edge in edge_gen_from_file(etype):
            sources = class_to_neurons.get(edge.src, [edge.src])
            targets = class_to_neurons.get(edge.tgt, [edge.tgt])
            for src, tgt in product(sources, targets):
                edges.append(Edge(src, tgt, edge.transmitter, edge.receptor))

        with open(join(
                tgt_root, '{}_edgelist{}.csv'.format(etype, '_include_weak' if include_weak else '')
        ), 'w') as f:
            for edge in edges:
                f.write('{},{},{},{}\n'.format(edge.src, edge.tgt, edge.transmitter, edge.receptor))


if __name__ == '__main__':
    for include_weak in [True, False]:
        main(include_weak)
    print('done')