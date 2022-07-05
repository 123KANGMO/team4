# http://127.0.0.1:5000/byuserandlist?username=사용자1&listname=리스트명


import requests
import json

res = requests.get('http://127.0.0.1:5000/byuserandlist?username=사용자1&listname=리스트명', headers={"Content-Type":"application/json; charset=utf-8" })

print(res.json())