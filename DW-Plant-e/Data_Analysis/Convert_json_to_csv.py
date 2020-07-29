import pandas as pd
import os

path = r'C:\Users\JK\Desktop'

df = pd.read_json (path + r"\Plant-e-00002103.json")
df.to_csv (path + r'\Plant-e-00002103.csv', index = None)
