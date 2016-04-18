from combine.paths import phys_root, extrasyn_root, meta_root, tgt_root
import networkx as nx
from os.path import join
import csv
import json
from connectome_utils import json_deserialise, json_serialise
import subprocess as sp
from warnings import warn
from datetime import datetime

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


def get_commit_hash(path, check_clean=True):
    """
    Checks that git repo is up to date in target directory and gets the commit hash
    """
    # if check_clean and sp.check_output(['git', '-C', path, 'status', '--porcelain']).strip():
    #     warn('Source data directory {} has uncommitted changes'.format(path))

    return sp.check_output(['git', '-C', path, 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()


def add_edge_lengths(G):
    with open(join(meta_root, 'dist_info.json')) as f:
        edge_lengths = json.load(f)

    for src, tgt, data in G.edges_iter(data=True):
        data['min_distance'] = edge_lengths[' '.join(sorted([src, tgt]))]


def main():
    commit_hash = get_commit_hash('.')
    date_str = datetime.now().isoformat()

    for source in ['ac', 'ww']:
        G = json_deserialise(join(phys_root, 'physical_{}.json'.format(source)))
        G.graph['commit_hash'] = commit_hash
        G.graph['created'] = date_str

        for include_weak in ['including_weak', 'strong_only']:
            G2 = G.copy()
            csv_paths = {
                'Monoamine': join(extrasyn_root,
                           'ma_edgelist{}.csv'.format('_include-weak' if include_weak == 'including_weak' else '')),
                'Neuropeptide': join(extrasyn_root, 'np_edgelist.csv')
            }

            for etype in ['Monoamine', 'Neuropeptide']:
                add_extrasyn_to_graph(G2, csv_paths[etype], etype)

            add_node_metadata(G2)
            add_edge_lengths(G2)

            json_serialise(G2, join(tgt_root, include_weak, source, 'complete.json'))


if __name__ == '__main__':
    main()