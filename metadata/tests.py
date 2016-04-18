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


if __name__ == '__main__':
    unittest.main()
