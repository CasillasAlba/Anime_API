from src.app import app

route = '/aaa'

@app.route(route + '/hello')
def hello_world2():
  return {'message': 'hello world from service'};