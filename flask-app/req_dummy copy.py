# 임시데이터를 넣기. 
import requests
import pandas as pd
import json


res = requests.get('http://127.0.0.1:5000/piebylist?listname=%EC%9C%A0%EB%B3%B8%EB%B6%80%EC%9E%A5').
print(res)