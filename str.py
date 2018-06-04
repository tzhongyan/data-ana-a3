import json
# from pprint import pprint
import pandas as pd

with open('t.json') as f:
    data = json.load(f)

# print(data[0].split('/')[5])

v = data
df = pd.DataFrame(data=v)
print(df.head())