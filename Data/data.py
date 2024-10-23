import pandas as pd
import json

with open('Scrappers/results.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    
try:
    df = pd.DataFrame(data)
except Exception as e:
    df = pd.json_normalize(data)