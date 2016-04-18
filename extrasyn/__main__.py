"""
Constructs monoamine and neuropeptide edge lists from gene expression spreadsheets
"""

from extrasyn import np_from_xlsx
from extrasyn import ma_from_xlsx
from extrasyn import class_edgelist_to_edgelist


for include_weak in [True, False]:
    ma_from_xlsx.main(include_weak)
    class_edgelist_to_edgelist.main('ma', include_weak)

np_from_xlsx.main()
class_edgelist_to_edgelist.main('np', False)
