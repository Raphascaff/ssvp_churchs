import pandas as pd
import json


with open('Scrappers/results.json') as json_file:
    data = json.load(json_file)

df = pd.json_normalize(data)