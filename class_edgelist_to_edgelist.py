"""
Convert the neurone class edge list created by ??_from_xlsx.py into an individual neurone edge list (without zero-padding)
"""

import json
from collections import namedtuple
from itertools import product
from datetime import date
from construct_extrasyn.paths import src_root, tgt_root
from os.path import join

# etypes = ['np', 'ma']
etypes = ['ma']
Edge = namedtuple('Edge', ['src', 'tgt', 'transmitter', 'receptor'])


def edge_gen_from_file(path):
    with open(path) as f:
        try:
            for row in f:
                r = row.strip()
                yield Edge(*r.split(','))
        except ValueError as e:
            if 'unpack' in str(e):
                raise StopIteration


def main(include_weak=False):
    with open(join(src_root, 'class_to_neurons3.json')) as f:
        class_to_neurons = json.load(f)

    with open(join(src_root, 'dist_info.json')) as f:
        dist_info = json.load(f)

    for etype in etypes:
        edges = []
        for edge in edge_gen_from_file(
                join(tgt_root, '{}_edgelist_classes{}.csv'.format(etype, '_include_weak' if include_weak else ''))
        ):
            sources = class_to_neurons[edge.src]  # , [edge.src])
            targets = class_to_neurons[edge.tgt]  # , [edge.tgt])
            for src, tgt in product(sources, targets):
                edges.append(Edge(src, tgt, edge.transmitter, edge.receptor))

        with open(join(
                tgt_root, '{}_edgelist{}.csv'.format(etype, '_include_weak' if include_weak else '')
        ), 'w') as f:
            for edge in edges:
                f.write('{},{},{},{},{}\n'.format(edge.src, edge.tgt, edge.transmitter, edge.receptor,
                                                  dist_info[' '.join(sorted([edge.src, edge.tgt]))])
                )


if __name__ == '__main__':
    for include_weak in [True, False]:
        main(include_weak)
    print('done')