import csv
import json
import re
import os
import unittest

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))
CONSTRUCT_ROOT = os.path.join(TEST_ROOT, '..')
DIFF_DIR = os.path.join(TEST_ROOT, 'diffs')

BARRY_DATA_DIR = os.path.join(TEST_ROOT, 'barry_data')
BARRY_DATA = {
    'gap': os.path.join(BARRY_DATA_DIR, 'edgeL_AC_gap.txt'),
    'syn': os.path.join(BARRY_DATA_DIR, 'edgeL_AC_syn.txt'),
    'ma': os.path.join(BARRY_DATA_DIR, 'edgeL_monoamine_min.txt'),
    'np': os.path.join(BARRY_DATA_DIR, 'edgeL_neuropeptide.txt')
}

MY_DATA = {
    'gap': os.path.join(CONSTRUCT_ROOT, 'physical', 'src_data', 'gap_edgelist_ac.csv'),
    'syn': os.path.join(CONSTRUCT_ROOT, 'physical', 'src_data', 'syn_edgelist_ac.csv'),
    'ma': os.path.join(CONSTRUCT_ROOT, 'extrasyn', 'tgt_data', 'ma_edgelist.csv'),
    'np': os.path.join(CONSTRUCT_ROOT, 'extrasyn', 'tgt_data', 'np_edgelist.csv')
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

    return sorted(tst - ref), sorted(ref - tst)


def write_diff_csv(name, filename):
    tst, ref = load_data(name)
    added, subtracted = sorted(set(tst) - set(ref)), sorted(set(ref) - set(tst))
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for item in added:
            writer.writerow(['+'] + list(item) + tst[item])
        for item in subtracted:
            writer.writerow(['-'] + list(item) + ['?', '?'])


def find_extra(name):
    tst, ref = load_data(name)
    return {key: value for key, value in tst.items() if key not in ref}


def find_missing(name):
    tst, ref = load_data(name)
    return {key: value for key, value in ref.items() if key not in tst}


class EdgeListTests(unittest.TestCase):
    def test_same_gaps(self):
        check_identical('gap')

    def test_same_syns(self):
        check_identical('syn')

    # @unittest.skipIf(get_diff('ma') == MA_DIFF, 'MA diff is as discussed with Barry')
    def test_same_ma(self):
        check_identical('ma')

    def test_same_np(self):
        check_identical('np')


if __name__ == '__main__':
    # ma_diff = get_diff('ma')
    # np_diff = get_diff('np')
    for etype in ['gap', 'syn', 'ma', 'np']:
        write_diff_csv(etype, os.path.join(DIFF_DIR, 'diff_{}.csv'.format(etype)))