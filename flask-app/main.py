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
  views = mongo.StringField()
  youtube_id = mongo.StringField()
  comment = mongo.StringField()
  like_num = mongo.StringField()
  emo = mongo.StringField()
  def to_json(self):
    return{
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
      "vidoe_name":self.video_name
    }

def saveComment(data):
  try:
    word_counter={}
    for y in data:
        doc = Comment(list_name = y[0], name=y[1], views=y[2], youtube_id=y[3], comment=y[4], like_num=y[5])
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
  def get(self, url):
    query_set = Comment.objects(name='여행계획')

    json_data = query_set.to_json()
    dicts = json.loads(json_data)   
    
    return f"cc.get ,{dicts}"

  def post(self,url):
    content = request.json
    x = json.loads(content)    
    saveComment(x['data'])
    print("save done")
   
    
    # 단어를 하나하나 다 저장하는 함수가 필요해 . 
    return f"cc.push, url: {url} saved?: "


class Test (Resource):
  def post(self):

    
    # 단어를 하나하나 다 저장하는 함수가 필요해 . 
    return f"keywordsaved?: "



api.add_resource(Test, "/sw")
api.add_resource(CC, "/cc/<string:url>")


if __name__ == "__main__":
  app.run(debug = True)