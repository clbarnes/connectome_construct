from paths import phys_root, extrasyn_root, meta_root, tgt_root
import networkx as nx
from xml.etree import ElementTree as ET
from os.path import join
import csv
import json


def key_it(start=0):
    while True:
        yield start
        start += 1


def serialise(G, filename):
    nx.write_graphml(G, filename)
    sort_graph(filename, filename)


def deserialise(filename):
    return nx.read_graphml(filename)


def sort_graph(in_path, out_path=None):
    if out_path is None:
        out_path = in_path

    STEM = "{http://graphml.graphdrawing.org/xmlns}"

    tree = ET.parse(in_path)

    for elem in tree.findall(STEM + 'key'):
        if elem.attrib['attr.name'] == 'key' and elem.attrib['for'] == 'edge':
            key_id = elem.attrib['id']
            break

    container = tree.find(STEM + "graph")

    node_data = []
    edge_data = []
    for elem in container:
        if elem.tag == STEM + 'node':
            key = elem.attrib['id']
            node_data.append((key, elem))
        elif elem.tag == STEM + 'edge':
            for data_elem in elem.findall(STEM + 'data'):
                if data_elem.attrib['key'] == key_id:
                    key = int(data_elem.text)
                    edge_data.append((key, elem))
                    break

    data = sorted(node_data) + sorted(edge_data)

    # insert the last item from each tuple
    container[:] = [item[-1] for item in data]

    tree.write(out_path)


def ma_edge_iter(path):
    with open(path) as f:
        reader = csv.reader(f)
        yield from reader


def add_ma_to_graph(G, ma_csv_path):
    max_key = max([key for node, key in G.edges_iter(keys=True)])
    key_gen = key_it(max_key + 1)
    for src, tgt, trans, rec in ma_edge_iter(ma_csv_path):
        G.add_edge(src, tgt, key=next(key_gen), transmitter=trans, receptor=rec)


def add_node_metadata(G):
    with open(join(meta_root, 'node_data.json')) as f:
        node_data = json.load(f)

    for node, data in G.nodes_iter(data=True):
        data.update(node_data[node])


def add_edge_lengths(G):
    with open(join(meta_root, 'node_data.json')) as f:
        edge_lengths = json.load(f)

    for src, tgt, data in G.edges_iter(data=True):
        data['min_distance'] = edge_lengths[' '.join(sorted([src, tgt]))]


phys = dict()

for source in ['ac', 'ww']:
    G = deserialise(join(phys_root, 'physical_{}.graphml'.format(source)))

    for include_weak in ['including_weak', 'strong_only']:
        ma_path = join(extrasyn_root, 'ma_edgelist{}.csv'.format('include-weak' if include_weak == 'including_weak' else ''))

        add_ma_to_graph(G, ma_path)
        add_node_metadata(G)
        add_edge_lengths(G)

        serialise(G, join(tgt_root, include_weak, source, 'complete.graphml'))