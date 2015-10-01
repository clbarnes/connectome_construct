from combine.paths import phys_root, extrasyn_root, meta_root, tgt_root
import networkx as nx
from os.path import join
import csv
import json


def key_it(start=0):
    while True:
        yield start
        start += 1


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
                G.add_edge(src, tgt, key, edge_data)

    return G


def ma_edge_iter(path):
    with open(path) as f:
        reader = csv.reader(f)
        yield from reader


def add_extrasyn_to_graph(G, np_csv_path, etype):
    for src, tgt, trans, rec in ma_edge_iter(np_csv_path):
        G.add_edge(src, tgt, key='{}_{}->{}_{}->{}'.format(etype, src, tgt, trans, rec),
                   transmitter=trans, receptor=rec, etype=etype)


def add_node_metadata(G):
    with open(join(meta_root, 'node_data.json')) as f:
        node_data = json.load(f)

    for node, data in G.nodes_iter(data=True):
        data.update(node_data[node])


def add_edge_lengths(G):
    with open(join(meta_root, 'dist_info.json')) as f:
        edge_lengths = json.load(f)

    for src, tgt, data in G.edges_iter(data=True):
        data['min_distance'] = edge_lengths[' '.join(sorted([src, tgt]))]


def main():
    for source in ['ac', 'ww']:
        G = json_deserialise(join(phys_root, 'physical_{}.json'.format(source)))

        for include_weak in ['including_weak', 'strong_only']:
            csv_paths = {
                'Monoamine': join(extrasyn_root,
                           'ma_edgelist{}.csv'.format('_include-weak' if include_weak == 'including_weak' else '')),
                'Neuropeptide': join(extrasyn_root, 'np_edgelist.csv')
            }

            for etype in ['Monoamine', 'Neuropeptide']:
                add_extrasyn_to_graph(G, csv_paths[etype], etype)

            add_node_metadata(G)
            add_edge_lengths(G)

            json_serialise(G, join(tgt_root, include_weak, source, 'complete.json'))


if __name__ == '__main__':
    main()