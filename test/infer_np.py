import connectome_utils as utl
from multiplex import MultiplexConnectome
import os
from itertools import product


TEST_ROOT = os.path.dirname(os.path.realpath(__file__))
CONSTRUCT_ROOT = os.path.join(TEST_ROOT, '..')
BARRY_DATA_DIR = os.path.join(TEST_ROOT, 'barry_data')
COMPLETE_PATH = os.path.join(CONSTRUCT_ROOT, 'combine', 'tgt_data', 'strong_only', 'ac', 'complete.json')

G = utl.json_deserialise(COMPLETE_PATH)
M = MultiplexConnectome(G)
np = M['Neuropeptide']


def add_to_set(d, key, item):
    try:
        value = d[key]
    except KeyError:
        value = set()

    value.add(item)
    d[key] = value

mappings = set()
for src, tgt, data in np.edges(data=True):
    add_to_set(np.node[src], 'transmitters', data['transmitter'])
    add_to_set(np.node[src], 'receives', data['transmitter'])
    add_to_set(np.node[tgt], 'receptors', data['receptor'])
    mappings.add((data['transmitter'], data['receptor']))

print('Number of mappings is {}'.format(len(mappings)))


def check_matches(src, tgt):
    out = set()

    try:
        transmitters, receptors = np.node[src]['transmitters'], np.node[tgt]['receptors']
    except KeyError:
        return out

    for mapping in product(transmitters, receptors):
        if mapping in mappings:
            out.add(mapping)

    return out

NP_MISSING = [
    ('ALA', 'AIML'),
    ('ALA', 'AIMR'),
    ('ALA', 'ALA'),
    ('ALA', 'ASKL'),
    ('ALA', 'ASKR'),
    ('ALA', 'AVKL'),
    ('ALA', 'AVKR'),
    ('ASEL', 'AIML'),
    ('ASEL', 'AIMR'),
    ('ASEL', 'ALA'),
    ('ASEL', 'AVKL'),
    ('ASEL', 'AVKR'),
    ('ASER', 'AIML'),
    ('ASER', 'AIMR'),
    ('ASER', 'ALA'),
    ('ASER', 'AVKL'),
    ('ASER', 'AVKR'),
    ('ASGL', 'AIML'),
    ('ASGL', 'AIMR'),
    ('ASGL', 'ALA'),
    ('ASGL', 'AVKL'),
    ('ASGL', 'AVKR'),
    ('ASGR', 'AIML'),
    ('ASGR', 'AIMR'),
    ('ASGR', 'ALA'),
    ('ASGR', 'AVKL'),
    ('ASGR', 'AVKR'),
    ('ASIL', 'AVG'),
    ('ASIL', 'PVPL'),
    ('ASIL', 'PVPR'),
    ('ASIR', 'AVG'),
    ('ASIR', 'PVPL'),
    ('ASIR', 'PVPR'),
    ('ASKL', 'AIML'),
    ('ASKL', 'AIMR'),
    ('ASKL', 'ALA'),
    ('ASKL', 'AVKL'),
    ('ASKL', 'AVKR'),
    ('ASKR', 'AIML'),
    ('ASKR', 'AIMR'),
    ('ASKR', 'ALA'),
    ('ASKR', 'AVKL'),
    ('ASKR', 'AVKR'),
    ('BAGL', 'AIML'),
    ('BAGL', 'AIMR'),
    ('BAGL', 'ALA'),
    ('BAGL', 'ASKL'),
    ('BAGL', 'ASKR'),
    ('BAGL', 'AVKL'),
    ('BAGL', 'AVKR'),
    ('BAGR', 'AIML'),
    ('BAGR', 'AIMR'),
    ('BAGR', 'ALA'),
    ('BAGR', 'ASKL'),
    ('BAGR', 'ASKR'),
    ('BAGR', 'AVKL'),
    ('BAGR', 'AVKR'),
    ('DD1', 'AIML'),
    ('DD1', 'AIMR'),
    ('DD1', 'ALA'),
    ('DD1', 'ASKL'),
    ('DD1', 'ASKR'),
    ('DD1', 'AVKL'),
    ('DD1', 'AVKR'),
    ('DD2', 'AIML'),
    ('DD2', 'AIMR'),
    ('DD2', 'ALA'),
    ('DD2', 'ASKL'),
    ('DD2', 'ASKR'),
    ('DD2', 'AVKL'),
    ('DD2', 'AVKR'),
    ('DD3', 'AIML'),
    ('DD3', 'AIMR'),
    ('DD3', 'ALA'),
    ('DD3', 'ASKL'),
    ('DD3', 'ASKR'),
    ('DD3', 'AVKL'),
    ('DD3', 'AVKR'),
    ('DD4', 'AIML'),
    ('DD4', 'AIMR'),
    ('DD4', 'ALA'),
    ('DD4', 'ASKL'),
    ('DD4', 'ASKR'),
    ('DD4', 'AVKL'),
    ('DD4', 'AVKR'),
    ('DD5', 'AIML'),
    ('DD5', 'AIMR'),
    ('DD5', 'ALA'),
    ('DD5', 'ASKL'),
    ('DD5', 'ASKR'),
    ('DD5', 'AVKL'),
    ('DD5', 'AVKR'),
    ('DD6', 'AIML'),
    ('DD6', 'AIMR'),
    ('DD6', 'ALA'),
    ('DD6', 'ASKL'),
    ('DD6', 'ASKR'),
    ('DD6', 'AVKL'),
    ('DD6', 'AVKR'),
    ('I5', 'AIML'),
    ('I5', 'AIMR'),
    ('I5', 'ALA'),
    ('I5', 'ASKL'),
    ('I5', 'ASKR'),
    ('I5', 'AVKL'),
    ('I5', 'AVKR'),
    ('M3L', 'AIML'),
    ('M3L', 'AIMR'),
    ('M3L', 'ALA'),
    ('M3L', 'AVKL'),
    ('M3L', 'AVKR'),
    ('M3R', 'AIML'),
    ('M3R', 'AIMR'),
    ('M3R', 'ALA'),
    ('M3R', 'AVKL'),
    ('M3R', 'AVKR'),
    ('M5', 'AIML'),
    ('M5', 'AIMR'),
    ('M5', 'ALA'),
    ('M5', 'ASKL'),
    ('M5', 'ASKR'),
    ('M5', 'AVKL'),
    ('M5', 'AVKR')
]

