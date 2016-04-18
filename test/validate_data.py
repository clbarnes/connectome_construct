import csv
import json
import re
import os
import unittest

BARRY_DATA_DIR = 'barry_data'
BARRY_DATA = {
    'gap': os.path.join(BARRY_DATA_DIR, 'edgeL_AC_gap.txt'),
    'syn': os.path.join(BARRY_DATA_DIR, 'edgeL_AC_syn.txt'),
    'ma': os.path.join(BARRY_DATA_DIR, 'edgeL_monoamine_min.txt'),
    'np': os.path.join(BARRY_DATA_DIR, 'edgeL_neuropeptide.txt')
}

MY_DATA = {
    'gap': os.path.join('..', 'physical', 'src_data', 'gap_edgelist_ac.csv'),
    'syn': os.path.join('..', 'physical', 'src_data', 'syn_edgelist_ac.csv'),
    'ma': os.path.join('..', 'extrasyn', 'tgt_data', 'ma_edgelist.csv'),
    'np': os.path.join('..', 'extrasyn', 'tgt_data', 'np_edgelist.csv')
}

zero_re = re.compile('(?<=[A-Z])0(?=[1-9])')


def ensure_no_mid_zero(s):
    return zero_re.sub('', s)


def csv2edgedict(filename, delim=','):
    d = dict()
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delim)
        for src, tgt, *other in reader:
            d[(zero_re.sub('', src), zero_re.sub('', tgt))] = other

    return d


def json2edgedict(filename):
    d = dict()
    with open(filename) as f:
        data = json.load(f)

    for src, src_dict in data['edges'].items():
        for tgt, edge_data in src_dict.items():
            d[(zero_re.sub('', src), zero_re.sub('', tgt))] = edge_data['weight']

    return d


def file2edgedict(filename, **kwargs):
    if filename.endswith('.json'):
        return json2edgedict(filename)
    else:
        return csv2edgedict(filename, **kwargs)


def load_data(name):
    tst = file2edgedict(MY_DATA[name])
    ref = file2edgedict(BARRY_DATA[name], delim=' ')

    return tst, ref


def check_identical(name):
    tst, ref = load_data(name)
    assert set(tst) == set(ref)


def get_diff(name):
    tst, ref = [set(data) for data in load_data(name)]
    



class EdgeListTests(unittest.TestCase):
    def test_same_gaps(self):
        check_identical('gap')

    def test_same_syns(self):
        check_identical('syn')

    def test_same_ma(self):
        check_identical('ma')

    def test_same_np(self):
        check_identical('np')
