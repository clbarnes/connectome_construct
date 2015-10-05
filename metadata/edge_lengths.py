import numpy as np
from scipy.spatial.distance import cdist
import json
import networkx as nx
from paths import src_root, tgt_root
from os.path import join

node_morphs = json.load(open(join(src_root, 'morphologies.json'), 'r'))


def get_min_dist(src, tgt):
    src_data = np.array(node_morphs[src]['neurone'])
    tgt_data = np.array(node_morphs[tgt]['neurone'])

    dist_mat = cdist(src_data[:, :3], tgt_data[:, :3])

    raw_min_dist = np.min(dist_mat)

    src_ind, tgt_ind = np.unravel_index(np.argmin(dist_mat), dist_mat.shape)

    return max(raw_min_dist - src_data[src_ind, 3]/2 - tgt_data[tgt_ind, 3]/2, 0)


def main():
    nodelist = sorted(node_morphs)

    # distance matrix
    make_dist = np.vectorize(
        lambda i, j: get_min_dist(nodelist[int(i)], nodelist[int(j)]),
        otypes=[np.dtype('float64')]
    )

    dist = np.fromfunction(make_dist, (len(nodelist), len(nodelist)))

    assert dist.shape == (302, 302)

    out = dict()

    for i, row in enumerate(dist):
        src = nodelist[i]
        for j, distance in enumerate(row):
            tgt = nodelist[j]
            out[' '.join(sorted([src, tgt]))] = distance

    with open(join(tgt_root, 'dist_info.json'), 'w') as f:
        json.dump(out, f, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()