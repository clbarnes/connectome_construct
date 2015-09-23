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
    keys = key_it()

    with open(join(src_root, 'nodelist.txt')) as f:
        nodelist = f.read().splitlines()

    for node in nodelist:
        G.add_node(node)

    n_nodes = G.number_of_nodes()

    for edge in edge_iter('gap', source):
        G.add_edge(edge[0], edge[1], key=next(keys), weight=int(edge[2]), etype='GapJunction')

    for edge in edge_iter('syn', source):
        G.add_edge(edge[0], edge[1], key=next(keys), weight=int(edge[2]), etype='Synapse')

    assert n_nodes == G.number_of_nodes()

    return G


def serialise(G, filename):
    nx.write_graphml(G, filename)
    sort_graph(filename, filename)


def deserialise(filename):
    return nx.read_graphml(filename)


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
                key = edge_data.pop('key')
                G.add_edge(src, tgt, key, edge_data)

    return G

# def sort_graph(in_path, out_path=None):
#     if out_path is None:
#         out_path = in_path
#
#     STEM = "{http://graphml.graphdrawing.org/xmlns}"
#
#     tree = ET.parse(in_path)
#
#     for elem in tree.findall(STEM + 'key'):
#         if elem.attrib['attr.name'] == 'key' and elem.attrib['for'] == 'edge':
#             key_id = elem.attrib['id']
#             break
#
#     container = tree.find(STEM + "graph")
#
#     node_data = []
#     edge_data = []
#     for elem in container:
#         if elem.tag == STEM + 'node':
#             key = elem.attrib['id']
#             node_data.append((key, elem))
#         elif elem.tag == STEM + 'edge':
#             for data_elem in elem.findall(STEM + 'data'):
#                 if data_elem.attrib['key'] == key_id:
#                     key = int(data_elem.text)
#                     edge_data.append((key, elem))
#                     break
#
#     data = sorted(node_data) + sorted(edge_data)
#
#     # insert the last item from each tuple
#     container[:] = [item[-1] for item in data]
#
#     tree.write(out_path)


def main():
    for source in ['ac', 'ww']:
        G = edge_lists_to_graph(source)
        json_serialise(G, join(tgt_root, 'physical_{}.json'.format(source)))

if __name__ == '__main__':
    main()