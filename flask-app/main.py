from flask import Flask, request, jsonify, render_template, make_response
from flask_restful import Api, Resource, reqparse
import json
from jinja2 import Template

#db

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #서버로 부터 받은 데이터의 한글 사용 가능

api = Api(app)
parser = reqparse.RequestParser()
# parser.add_argument('username',type=str, help='@@cannot be converted')
# parser.add_argument('listname',type=str, help='@@cannot be converted')




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
  def get(self, videoname): # 제목을 파라미터? 로 받으면 안되네요 제목 속에 "?" 를 처리 하지 못함.
    query_set = Comment.objects(name=videoname)
    json_data = query_set.to_json()
    dicts = json.loads(json_data) 
    print(videoname)
    print(dicts)
    # 동영상 별로 볼때, 그 동영상의 주요 키워드를 주자.
    e_counter = {}
    for x in dicts:
      if x['emo'] in e_counter:
        e_counter[x['emo']]+=1
      else:
        e_counter[x['emo']]=1

    data = {'Task' : f' 해당 영상 댓글의 감정분포',
      '불안' : e_counter['불안'] if '불안'in e_counter.keys() else 7,
      '분노' : e_counter['분노'] if '분노'in e_counter.keys() else 7,
      '슬픔' : e_counter['슬픔'] if '슬픔'in e_counter.keys() else 7,
      '기쁨' : e_counter['기쁨'] if '기쁨'in e_counter.keys() else 7,
      '당황' : e_counter['당황'] if '당황'in e_counter.keys() else 7,
      '상처' : e_counter['상처'] if '상처'in e_counter.keys() else 7
    }
    
    return make_response(render_template('piec.html', data=data))

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
    vn = request.args.get('videoname')
    query_set = Comment.objects(list_name=vn)
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

class Username (Resource):

  def get(self):
    user = request.args.get('username')
    list = request.args.get('listname')
    print('userlist')

    query_set = Comment.objects(youtube_id=user, list_name = list)
    json_data = query_set.to_json()
    dicts = json.loads(json_data) 
    e_counter = {}
    for x in dicts:
      if x['emo'] in e_counter:
        e_counter[x['emo']]+=1
      else:
        e_counter[x['emo']]=1
    # return f"keywordsaved?: {e_counter}"
    data = {'Task' : f'재생목록 {list} 안에서 사용자 {user}의 감정분포',
      '불안' : e_counter['불안'] if '불안'in e_counter.keys() else 7,
      '분노' : e_counter['분노'] if '분노'in e_counter.keys() else 7,
      '슬픔' : e_counter['슬픔'] if '슬픔'in e_counter.keys() else 7,
      '기쁨' : e_counter['기쁨'] if '기쁨'in e_counter.keys() else 7,
      '당황' : e_counter['당황'] if '당황'in e_counter.keys() else 7,
      '상처' : e_counter['상처'] if '상처'in e_counter.keys() else 7
    }
    
    #return render_template('piec.html', data=data)
    #return render_template("piec2.html", row_data=values)
    #return render_template('test.html')
    return make_response(render_template('piec.html', data=data))


class word (Resource):
  def get(self):
    videoname = request.args.get('videoname')
    print('userlist')
    words_set = Keywords.objects(video_name=videoname)
    json_words = words_set.to_json()
    wordslist = json.loads(json_words)
    print(len(wordslist))
    if len(wordslist) == 0:#;;
      return '해당 제목의 데이터가 없습니다!'
    words = wordslist[0]
    print(len(words))
    print(type(words['counts'][0]))
    words['words'][0]
    mylist = [
      # ['단어', '언급횟수', { role: 'style' } ],
      [words['words'][0], words['counts'][0], 'stroke-color: #703593; stroke-width: 4; fill-color: #C5A5CF'],
      [words['words'][1], words['counts'][1], 'stroke-color: #871B47; stroke-opacity: 0.6; stroke-width: 8; fill-color: #BC5679; fill-opacity: 0.2'],
      [words['words'][2], words['counts'][2], "gold"],
      [words['words'][3], words['counts'][3], "silver"],
      [words['words'][4], words['counts'][4], 'color: gray'],
      [words['words'][5], words['counts'][5], 'color: #76A7FA'],
      [words['words'][6], words['counts'][6], 'opacity: 0.2'],
      [words['words'][7], words['counts'][7], "#b87333"],
    ]

    return make_response(render_template('barchar3.html', mylist=mylist))

class PieByVideo (Resource):
  def get(self):
    videoname = request.args.get('videoname')
    query_set = Comment.objects(name=videoname)
    json_data = query_set.to_json()
    dicts = json.loads(json_data) 
    print(videoname)
    print(dicts)
    # 동영상 별로 볼때, 그 동영상의 주요 키워드를 주자.
    e_counter = {}
    for x in dicts:
      if x['emo'] in e_counter:
        e_counter[x['emo']]+=1
      else:
        e_counter[x['emo']]=1

    data = {'Task' : f' 해당 영상 댓글의 감정분포',
      '불안' : e_counter['불안'] if '불안'in e_counter.keys() else 7,
      '분노' : e_counter['분노'] if '분노'in e_counter.keys() else 7,
      '슬픔' : e_counter['슬픔'] if '슬픔'in e_counter.keys() else 7,
      '기쁨' : e_counter['기쁨'] if '기쁨'in e_counter.keys() else 7,
      '당황' : e_counter['당황'] if '당황'in e_counter.keys() else 7,
      '상처' : e_counter['상처'] if '상처'in e_counter.keys() else 7
    }

    return make_response(render_template('piec.html', data=data))

class PieByList (Resource):
  def get(self):
    listname = request.args.get('listname')
    query_set = Comment.objects(list_name=listname)

    json_data = query_set.to_json()
    j2=json.dumps(json_data, ensure_ascii=False, encoding='utf8')
    dicts = json.loads(json_data) 
    print(listname)
    print(dicts)
    # 동영상 별로 볼때, 그 동영상의 주요 키워드를 주자.
    e_counter = {}
    for x in dicts:
      if x['emo'] in e_counter:
        e_counter[x['emo']]+=1
      else:
        e_counter[x['emo']]=1

    data = {'Task' : f' 해당 영상 댓글의 감정분포',
      '불안' : e_counter['불안'] if '불안'in e_counter.keys() else 7,
      '분노' : e_counter['분노'] if '분노'in e_counter.keys() else 7,
      '슬픔' : e_counter['슬픔'] if '슬픔'in e_counter.keys() else 7,
      '기쁨' : e_counter['기쁨'] if '기쁨'in e_counter.keys() else 7,
      '당황' : e_counter['당황'] if '당황'in e_counter.keys() else 7,
      '상처' : e_counter['상처'] if '상처'in e_counter.keys() else 7
    }

    return make_response(render_template('piec.html', data=data))






api.add_resource(CC, "/cc/<string:videoname>") #비디오 별, 
api.add_resource(list_name, "/bylist/<string:listname>") # 리스트 별  파이차트
api.add_resource(Username, "/byuserandlist") # 리스트 + 유저 별 파이차트
#
api.add_resource(word, "/word") 
api.add_resource(PieByVideo, "/piebyvideo") 
api.add_resource(PieByList, "/piebylist") 



if __name__ == "__main__":
  app.run(debug = True)