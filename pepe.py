import json

with open('pathway.json', 'r') as f:
    data = json.load(f)

metabolism = data['1. Metabolism']

for key, value in metabolism.items():
    print(key)
    print(value)