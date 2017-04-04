import os

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

phys_root = os.path.join(ROOT, 'physical', 'tgt_data')
extrasyn_root = os.path.join(ROOT, 'extrasyn', 'tgt_data')
meta_root = os.path.join(ROOT, 'metadata', 'tgt_data')

tgt_root = os.path.join(ROOT, 'combine', 'tgt_data')
