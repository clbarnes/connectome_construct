import json
from metadata.paths import src_root, tgt_root
from os.path import join
import numpy as np
from scipy.spatial.distance import cdist


def get_length(morph):
    arr = np.array([emslice[:3] for emslice in morph])
    dist_mat = cdist(arr, arr)

    return np.max(dist_mat)


def collapse_ntype(options):
    if options is None:
        return 'interneuron'

    if 'motor' in options:
        return 'motor'
    elif 'interneuron' in options:
        return 'interneuron'
    elif 'sensory' in options:
        return 'sensory'
    else:
        return 'interneuron'


def main():
    out = dict()

    with open(join(src_root, 'birthtimes.json')) as f:
        birthtimes = json.load(f)

    with open(join(src_root, 'descriptions.json')) as f:
        descs = json.load(f)

    with open(join(src_root, 'neuron_types.json')) as f:
        ntypes = json.load(f)

    with open(join(src_root, 'morphologies.json')) as f:
        morphologies = json.load(f)

    with open(join(tgt_root, 'sensorimotoy_connections.json')) as f:
        sensmo_conn = json.load(f)

    for node in set(birthtimes) | set(descs) | set(ntypes):
        out[node] = {
            'birthtime': birthtimes.get(node, None),
            'description': descs.get(node, None),
            'ntypes': ntypes.get(node, None),
            'ntype': collapse_ntype(ntypes.get(node, None)),
            'soma_loc': morphologies[node]['soma'][:3],
            'mean_loc': morphologies[node]['mean'][:3],
            'direct_length': get_length(morphologies[node]['neurone']),
            'sensory_connections': sensmo_conn[node]['sensory_connections'] if node in sensmo_conn else 0,
            'sensory_weight': sensmo_conn[node]['sensory_weight'] if node in sensmo_conn else 0,
            'motor_connections': sensmo_conn[node]['motor_connections'] if node in sensmo_conn else 0,
            'motor_weight': sensmo_conn[node]['motor_weight'] if node in sensmo_conn else 0,
        }

    assert len(out) == 302

    with open(join(tgt_root, 'node_data.json'), 'w') as f:
        json.dump(out, f, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()