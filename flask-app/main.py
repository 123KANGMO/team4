from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import json
#db

app = Flask(__name__)
api = Api(app)

HOST = 'cluster0.unmvh.mongodb.net'
USER = 'dba'
PASSWORD = 'eU-NheYjN2rQM!8'
DATABASE_NAME = 'ai11'
COLLECTION_NAME = 'comments'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"



# mongodb+srv://dba:eU-NheYjN2rQM!8@cluster0.unmvh.mongodb.net/ai11?retryWrites=true&w=majority
# client = MongoClient(MONGO_URI)
# db = client.ai11
# db = client.comments
 # pymongo -> flask-mongoengin -> mongoengine

import mongoengine as mongo
mongo.connect(host=MONGO_URI)

# DB Collection
class Comment(mongo.Document):
  list_name = mongo.StringField()
  name = mongo.StringField()
  views = mongo.IntField()#int
  youtube_id = mongo.StringField()
  comment = mongo.StringField()
  like_num = mongo.IntField()#int
  emo = mongo.StringField()
  def to_json(self):
    return{
      "list_name":self.list_name,
      "name":self.name,
      'views': self.views,
      'youtube_id ':self.youtube_id,
      'comment' : self.comment,
      'like_num' : self.like_num,
      'emo':self.emo
    }

class Keywords(mongo.Document):  
  words = mongo.ListField()
  counts = mongo.ListField()
  list_name  = mongo.StringField()
  video_name = mongo.StringField()
  def to_json(self):
    return{
      "words":self.words,
      "counts":self.counts,
      "list_name":self.list_name,
      "video_name":self.video_name
    }

def saveComment(data):
  try:
    word_counter={}
    for y in data:
        doc = Comment(list_name = y[0], name=y[1], views=y[2], youtube_id=y[3], comment=y[4], like_num=y[5], emo=y[6])
        doc.save()
        #
        for word in y[4].split():
          if word in word_counter:
              word_counter[word]+=1
          else:
              word_counter[word]=1
    
    # top 15 추출
    words = sorted(word_counter, key=word_counter.get, reverse=True)[:15]
    c = []
    for w in words:
      c.append(word_counter[w])
    dict1 = Keywords(words =words, counts = c, video_name = data[1][1], list_name=data[1][0] )
    dict1.save()
    return True
  except:
    print("Something else went wrong")
    return False



    

# flask api 
class CC (Resource):
  def get(self, videoname):
    query_set = Comment.objects(name=videoname)
    json_data = query_set.to_json()
    dicts = json.loads(json_data) 
    #print(dicts)
    # 동영상 별로 볼때, 그 동영상의 주요 키워드를 주자.
    words_set = Keywords.objects(video_name=videoname)
    json_words = words_set.to_json()
    words = json.loads(json_words) 
    e_counter = {}
    for x in dicts:
      if x['emo'] in e_counter:
        e_counter[x['emo']]+=1
      else:
        e_counter[x['emo']]=1
    return f"cc.get ,{e_counter} \n words{words}"

  def post(self,videoname):
    content = request.json
    x = json.loads(content)  
    if not Comment.objects(list_name=x['data'][0][0], name = x['data'][0][1] ):  
      done = saveComment(x['data'])
      if done: 
        return ("save done")
    
    # 단어를 하나하나 다 저장하는 함수가 필요해 . 
    return f"not saved "


class list_name (Resource):
  def get(self,listname):
    query_set = Comment.objects(list_name=listname)
    json_data = query_set.to_json()
    dicts = json.loads(json_data) 
    e_counter = {}
    for x in dicts:
      if x['emo'] in e_counter:
        e_counter[x['emo']]+=1
      else:
        e_counter[x['emo']]=1

    # pipeline =[
    #   {"$match" : {"list_name" : listname}},
    #   {"$group" : { "_id ": "$emo", "count" : {"$sum ": 1}}} 
    # ] 
    # query_set = Comment.objects().aggregate(pipeline)
    # json_data = query_set.to_json()
    # dicts = json.loads(json_data) 
    # 왜 안되는지, 알수가 없습니다.
    return f"keywordsaved?: {e_counter}"

class user_name (Resource):
  def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('listname', type = str, default='None')
        self.reqparse.add_argument('username', type = str, default='None')
        super(user_name, self).__init__()


  def post(self):
    args = self.reqparse.parse_args()
    print(args['username'], args['listname'])
    query_set = Comment.objects(youtube_id=args['username'], list_name = args['listname'])
    json_data = query_set.to_json()
    dicts = json.loads(json_data) 
    e_counter = {}
    for x in dicts:
      if x['emo'] in e_counter:
        e_counter[x['emo']]+=1
      else:
        e_counter[x['emo']]=1
    return f"keywordsaved?: "


api.add_resource(CC, "/cc/<string:videoname>")
api.add_resource(list_name, "/bylist/<string:listname>")
api.add_resource(user_name, "/byuserandlist")


if __name__ == "__main__":
  app.run(debug = True)