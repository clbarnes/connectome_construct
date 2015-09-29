import unittest
import os
from paths import src_root, tgt_root
import csv


class MetadataIntegrity(unittest.TestCase):
    def listdir_rec(self, path):
        """
        Recursively lists all files in the given directory
        """
        outlst = []
        for dirpath, dirnames, filenames in os.walk(path):
            outlst.extend([os.path.join(dirpath, filename) for filename in filenames])

        return outlst

    def metadata_exists(self, path):
        filenames = self.listdir_rec(path)

        for filename in filenames:
            if not filename.endswith('.meta'):
                self.assertIn(filename + '.meta', filenames)

    def test_src_metadata_exists(self):
        self.metadata_exists(src_root)

    def test_tgt_metadata_exists(self):
        self.metadata_exists(tgt_root)

    def metadata_not_empty(self, path):
        filenames = self.listdir_rec(path)

        for filename in filenames:
            if '.meta' in filename:
                with open(filename) as f:
                    self.assertNotEqual(f.read().strip(), '')

    def test_src_metadata_not_empty(self):
        self.metadata_not_empty(src_root)

    def test_tgt_metadata_not_empty(self):
        self.metadata_not_empty(tgt_root)


class DataIntegrity(unittest.TestCase):
    nodeset = None
    ma_edgelist = None
    np_edgelist = None

    @classmethod
    def get_edge_list(cls, path):
        with open(path) as f:
            reader = csv.reader(f)
            return [tuple(row[:2]) for row in reader]

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(src_root, 'nodelist.txt')) as f:
            cls.nodeset = set(f.read().splitlines())

        cls.ma_edgelist = cls.get_edge_list(os.path.join(tgt_root, 'ma_edgelist.csv'))
        cls.np_edgelist = cls.get_edge_list(os.path.join(tgt_root, 'np_edgelist.csv'))

    def test_fixtures(self):
        self.assertTrue(self.nodeset, 'nodeset did not populate correctly')
        self.assertTrue(self.ma_edgelist, 'ma_edgelist did not populate correctly')
        self.assertTrue(self.np_edgelist, 'np_edgelist did not populate correctly')

    def validate_nodes_are_neurons(self, edgelist):
        vertex_set = {node for edge in edgelist for node in edge}
        diff = vertex_set - self.nodeset
        self.assertEqual(len(diff), 0, 'The below vertices are not real neurons:\n\t{}'.format(str(diff)))

    def test_validate_ma_nodes_are_neurons(self):
        self.validate_nodes_are_neurons(self.ma_edgelist)

    def test_validate_np_nodes_are_neurons(self):
        self.validate_nodes_are_neurons(self.np_edgelist)


if __name__ == '__main__':
    unittest.main()
