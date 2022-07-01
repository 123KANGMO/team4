import requests
import pandas as pd
import json

# r = requests.post('http://127.0.0.1:5000/cc', json={"key": "value"})
# print(r)

df = pd.read_excel("test.xlsx" )#, encoding='utf-8')
df = df.head(3)
print(df.iloc[1])

result = df.to_json(orient="split", force_ascii=False)

parsed = json.loads(result)
myjson=json.dumps(parsed, ensure_ascii=False)#, indent=4)  
print(myjson)

res = requests.post('http://127.0.0.1:5000/cc/abc', json=myjson)
if res.ok:
    print(res.json())