import csv
import os
import re

zero_re = re.compile('(?<=[A-Z])0(?=[1-9])')


def ensure_mid_zero(s):
    return zero_re.sub('', s)

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))

barry_root = os.path.join(TEST_ROOT, 'barry_data')


def get_node_tuples():
    nodeset = set()
    for path in os.listdir(barry_root):
        with open(os.path.join(barry_root, path)) as f:
            reader = csv.reader(f, delimiter=' ')
            for src, tgt, weight in reader:
                nodeset.update([src, tgt])

    lst = sorted((node, ensure_mid_zero(node)) for node in nodeset)
    assert len(lst) == 302
    return lst

with open('node_mapping.csv', 'w') as f:
    writer = csv.writer(f)
    for tup in get_node_tuples():
        writer.writerow(tup)


