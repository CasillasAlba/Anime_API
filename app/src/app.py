from flask import Flask, request, Response, render_template
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__, template_folder='../templates')

client = MongoClient("mongo", 27017)
db = client.SampleCollections


@app.route('/hello-world', methods=['GET'])
def hello_world():
  return {'message': 'Hello World!'}


@app.route('/anime', methods=['GET'])
def list_anime():
  anime_list = db.anime.find()
  response = json_util.dumps(anime_list)
  return Response(response, mimetype='application/json')


@app.route('/anime/<id>', methods=['GET'])
def get_anime(id):
  anime = db.anime.find_one({'_id': ObjectId(id)})
  response = json_util.dumps(anime)
  return Response(response, mimetype='application/json')


@app.route('/anime', methods=['POST'])
def create_anime():
  title = request.json['title']
  img = request.json['img']
  n_episodes = request.json['n_episodes']
  status = request.json['status']

  if title and img and n_episodes and status:
    id = db.anime.insert_one(
      {
        'title': title,
        'img': img,
        'n_episodes': n_episodes,
        'status': status
      }
    ).inserted_id

    response = {
      'id': str(id),
      'title': title,
      'img': img,
      'n_episodes': n_episodes,
      'status': status
    }

    return response

  else:
    return {'error': 'Invalid data'}

@app.route('/anime/<id>', methods=['PUT'])
def edit_anime(id):
  title = request.json['title']
  img = request.json['img']
  n_episodes = request.json['n_episodes']
  status = request.json['status']

  if title and img and n_episodes and status:
    db.anime.update_one({'_id': ObjectId(id)},
      {
        '$set': {
          'title': title,
          'img': img,
          'n_episodes': n_episodes,
          'status': status
        }
      }
    )
    response = {
      'id': id,
      'title': title,
      'img': img,
      'n_episodes': n_episodes,
      'status': status
    }

    return response


@app.route('/anime/<id>', methods=['DELETE'])
def delete_anime(id):
  db.anime.delete_one({'_id': ObjectId(id)})
  return {'message': 'Deleted succesfully'};


@app.route('/hello/<name>')
def index(name):
  return render_template('index.html', name=name)