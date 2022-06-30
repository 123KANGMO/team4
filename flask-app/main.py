from flask  import Flask
from flask_restful import Api, Resource, reqparse
#db
from pymongo import MongoClient

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
class Data(mongo.Document):
  data_id=mongo.IntField()
  name = mongo.StringField()

  def to_json(self):
    return{
      "data_id":self.data_id,
      "name":self.name
    }

d1 = Data(data_id=1, name="happy")
d1.save()
print("in Data collection d1 added")


# flask api 
class CC (Resource):
  def get(self, url):
    return f"cc.get ,{url}"

  def push(self, ):
    {"lon": "test data"}
    return f"cc.push done"

api.add_resource(CC, "/cc/<string:url>")


if __name__ == "__main__":
  app.run(debug = True)