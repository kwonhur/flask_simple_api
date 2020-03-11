from flask import Flask, jsonify
from flask_restful import request, reqparse, abort, Api, Resource
from operator import itemgetter
from parser import parse

app = Flask(__name__)
api = Api(app)

SORTBY = ["id", "reads", "likes", "popularity"]
DIRECTION = ["desc", "asc"]

def process_tags(tags) -> list:
    print ("process tags")
    if tags == None or "":
        abort(400, error="Tags parameter is required")
    return (tags).split(",")

def validate_sortBy(sortBy):
    if sortBy != None or "":
        if sortBy not in SORTBY:
            abort(400, error="sortBy parameter is invalid")
        else:
            return sortBy
    else:
        return "id"

def validate_direction(direction):
    if direction != None or "":
        if direction not in DIRECTION:
            abort(400, error="sortBy parameter is invalid") #same message as validate_sortBy per documentation
        else:
            return False if direction == "asc" else True
    else:
        return False

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Posts(Resource):
    def get(self):
        tags = request.args.get("tags")
        sortBy = request.args.get("sortBy")
        direction = request.args.get("direction")
        tags = process_tags(tags)
        sortBy = validate_sortBy(sortBy)
        direction = validate_direction(direction)
        parsed_dict_list = parse(tags)
        response =  {"posts": sorted(parsed_dict_list, key=itemgetter(sortBy), reverse=direction)}
        response.status_code = 200
        return response

    # def delete(self, todo_id):
    #     abort_if_todo_doesnt_exist(todo_id)
    #     del TODOS[todo_id]
    #     return '', 204

    # def put(self, todo_id):
    #     args = parser.parse_args()
    #     task = {'task': args['task']}
    #     TODOS[todo_id] = task
    #     return task, 201


# ping endpoint
# shows if communication to api is suceessful
class Ping(Resource):
    def get(self):
        response = jsonify({"success": True})
        response.status_code = 200
        return response

    # def post(self):
    #     args = parser.parse_args()
    #     todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
    #     todo_id = 'todo%i' % todo_id
    #     TODOS[todo_id] = {'task': args['task']}
    #     return TODOS[todo_id], 201

##
## Api resource routing here
##
api.add_resource(Posts, '/api/posts')
api.add_resource(Ping, '/api/ping')


if __name__ == '__main__':
    app.run(debug=True)