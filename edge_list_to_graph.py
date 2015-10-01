import networkx as nx
from construct_physical.paths import src_root, tgt_root
# from paths import src_root, tgt_root
from os.path import join
import csv
import xml.etree.ElementTree as ET
import json


def key_it(start=0):
    while True:
        yield start
        start += 1


def edge_iter(etype, source):
    assert etype in ['gap', 'syn']
    assert source in ['ac', 'ww']
    with open(join(src_root, '{}_edgelist_{}.csv'.format(etype, source))) as f:
        reader = csv.reader(f)
        for row in reader:
            yield tuple(row)


def edge_lists_to_graph(source):
    G = nx.MultiDiGraph()

    with open(join(src_root, 'nodelist.txt')) as f:
        nodelist = f.read().splitlines()

    for node in nodelist:
        G.add_node(node)

    n_nodes = G.number_of_nodes()

    for etype, edge_file_prefix in [('GapJunction', 'gap'), ('Synapse', 'syn')]:
        for src, tgt, weight_str in edge_iter(edge_file_prefix, source):
            G.add_edge(src, tgt, key='{}_{}->{}'.format(etype, src, tgt), weight=int(weight_str), etype=etype)

    assert n_nodes == G.number_of_nodes()

    return G


def json_serialise(G, filename=None):
    d = dict()
    d['nodes'] = dict(G.node)
    d['edges'] = dict(G.edge)

    if filename:
        with open(filename, 'w') as f:
            json.dump(d, f, indent=2, sort_keys=True)
    else:
        return json.dumps(d, indent=2, sort_keys=True)


def json_deserialise(filename):
    G = nx.MultiDiGraph()
    try:
        with open(filename) as f:
            data = json.load(f)
    except FileNotFoundError:
        try:
            json.loads(filename)
        except ValueError:
            raise ValueError('Argument is neither a file path nor valid JSON')

    for node, node_data in data['nodes'].items():
        G.add_node(node, node_data)

    for src, tgt_dict in data['edges'].items():
        for tgt, key_dict in tgt_dict.items():
            for key, edge_data in key_dict.items():
                G.add_edge(src, tgt, int(key), edge_data)

    return G


def main():
    for source in ['ac', 'ww']:
        G = edge_lists_to_graph(source)
        json_serialise(G, join(tgt_root, 'physical_{}.json'.format(source)))

if __name__ == '__main__':
    main()