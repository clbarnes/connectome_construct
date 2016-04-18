import json
import re

path = "src_data/NeuronFixedPoints-1.csv"

data = []

with open(path) as f:
    next(f)
    for row in f:
        data.append(row.split(','))


mid_zero_re = re.compile('(?<=[A-Z])0(?=[1-9])')
output = dict()

for node, tgt, _, weight in data:
    node = mid_zero_re.sub('', node)
    if node not in output:
        output[node] = {
            'sensory_connections': 0,
            'sensory_weight': 0,
            'motor_connections': 0,
            'motor_weight': 0
        }
    if 'sensory' in tgt.lower():
        output[node]['sensory_connections'] += 1
        output[node]['sensory_weight'] += float(weight)
    else:
        output[node]['motor_connections'] += 1
        output[node]['motor_weight'] += float(weight)

with open('tgt_data/sensorimotor_connections.json', 'w') as f:
    json.dump(output, f, sort_keys=True, indent=2)
