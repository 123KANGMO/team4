# 임시데이터를 넣기. 
import requests
import pandas as pd
import json

# doc = Comment(list_name = y[0], name=y[1], views=y[2], youtube_id=y[3], comment=y[4], like_num=y[5])
raw_data = {'list_name': ['리스트명', '리스트명','리스트명','리스트명2','리스트명','리스트명','리스트명',],
            'name': ['영상명', '영상명', '영상명', '영상명2','영상명','영상명','영상명'],
            'views': [10, 20, 30, 40, 5, 6, 9],
            'youtube_id': ['사용자1','사용자1','사용자1','사용자1','사용자1','사용자1','사용자1'],
            'comment': ["애도 어른도 아닌", "나이 때 그저 나일 때 가장 찬란하게",  "빛이 나 어둠이",  "드리워질 때도 겁내지 마",
              "너무 아름다워서 꽃잎 활짝", "펴서 애도 어른도 아닌 나이 때 그저 나일 때", "가장 찬란하게 빛이 나 어둠이 드리워질 때도 겁내지 마"],
            'like_num': [10, 20, 30, 40, 7, 3, 4],
            'emo': ['행복','행복','행복','행복','슬픔','슬픔', '놀람']}

df = pd.DataFrame(raw_data)
print(df.iloc[1])

result = df.to_json(orient="split", force_ascii=False)

parsed = json.loads(result)
myjson=json.dumps(parsed, ensure_ascii=False)#, indent=4)  
print(myjson)

res = requests.post('http://127.0.0.1:5000/cc/abc', json=myjson)
if res.ok:
    print(res.json())