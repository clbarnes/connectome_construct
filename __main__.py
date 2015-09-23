"""
Constructs extrasynaptic edge lists, including minimum edge lengths
"""

from construct_extrasyn import class_edgelist_to_edgelist
from construct_extrasyn import ma_from_xlsx
# import np_from_xlsx

for include_weak in [True, False]:
    ma_from_xlsx.main(include_weak)
    class_edgelist_to_edgelist.main(include_weak)
# np_from_xlsx.main()
