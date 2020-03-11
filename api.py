from flask import Flask, jsonify
from flask_caching import Cache
from flask_restful import request, reqparse, abort, Api, Resource
from operator import itemgetter
from parser import parse

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
api = Api(app)

SORTBY = ["id", "reads", "likes", "popularity"]
DIRECTION = ["desc", "asc"]

def process_tags(tags) -> list:
    if tags == None or tags == "":
        abort(400, error="Tags parameter is required")
    return (tags).split(",")

def validate_sortBy(sortBy):
    if sortBy != None or sortBy == "":
        if sortBy not in SORTBY:
            abort(400, error="sortBy parameter is invalid")
        else:
            return sortBy
    else:
        return "id"

def validate_direction(direction):
    if direction != None or direction == "":
        if direction not in DIRECTION:
            abort(400, error="sortBy parameter is invalid") #same message as validate_sortBy per documentation
        else:
            return False if direction == "asc" else True
    else:
        return False

# Posts
class Posts(Resource):
    @cache.cached(timeout=10, query_string=True)
    def get(self):
        tags = request.args.get("tags")
        sortBy = request.args.get("sortBy")
        direction = request.args.get("direction")
        tags = process_tags(tags)
        sortBy = validate_sortBy(sortBy)
        direction = validate_direction(direction)
        parsed_dict_list = parse(tags)
        response =  jsonify({"posts": sorted(parsed_dict_list, key=itemgetter(sortBy), reverse=direction)})
        response.status_code = 200
        return response

# ping endpoint
# shows if communication to api is suceessful
class Ping(Resource):
    def get(self):
        response = jsonify({"success": True})
        response.status_code = 200
        return response

## Api resource routing here
api.add_resource(Posts, '/api/posts')
api.add_resource(Ping, '/api/ping')


if __name__ == '__main__':
    app.run(debug=True)