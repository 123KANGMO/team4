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

  def to_json(self):
    return{
      "name":self.name,
      'views': self.views,
      'youtube_id ':self.youtube_id,
      'comment' : self.comment,
      'like_num' : self.like_num
    }

def saveComment(data):
  try:
    for y in data:
        doc = Comment(list_name = y[0], name=y[1], views=y[2], youtube_id=y[3], comment=y[4], like_num=y[5])
        doc.save()
    return True
  except:
    print("Something else went wrong")
    return False
    

# flask api 
class CC (Resource):
  def get(self, url):
    return f"cc.get ,{url}"

  def post(self,url):
    content = request.json
    # content = 크롤링함수() 를 통해, 데이터를 받으려면 이곳에.....
    x = json.loads(content)
    #done = await saveComment(x['data'])
    for y in x['data']:
        doc = Comment(list_name = y[0], name=y[1], views=y[2], youtube_id=y[3], comment=y[4], like_num=y[5])
        doc.save()
        print(y)
    
    # return 
    return f"cc.push, url: {url} saved?: "

# @app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
# def add_message(uuid):
#     content = request.json
#     print(content['mytext'])
#     return jsonify({"uuid":uuid})




api.add_resource(CC, "/cc/<string:url>")


if __name__ == "__main__":
  app.run(debug = True)