from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'pkmn'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pkmn'

mongo = PyMongo(app)

@app.route('/hello-world', methods=['GET'])
def hello_world():
  return {'message': 'hello world'};