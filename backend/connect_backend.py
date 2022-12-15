from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import pandas as pd
import ast
import gentleman_agent_reactive as ga
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
my_agent = ga.Gouldilocks()

class Move(Resource):
    def post(self):
      request_data = request.get_json()
      move = my_agent.get_move(request_data["data"]["board"], request_data["data"]["player"])
      print("move gotten: ", move)
      return {
        "statusCode": 200,
        "body": {"got": move},
        "headers": {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": True,
          "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
          "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
        },
      } 

class Utility(Resource):
    def post(self):
      request_data = request.get_json()
      utility = my_agent.utility(request_data["data"]["board"], request_data["data"]["player"])
      print("utility gotten: ", utility)
      send = None
      if utility == 1:
        send = "win"
      elif utility == -1:
        send = "loss"
      else:
        send = "draw"
      return {
        "statusCode": 200,
        "body": {"got": send},
        "headers": {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": True,
          "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
          "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
        },
      }

class Terminal(Resource):
    def post(self):
      request_data = request.get_json()
      terminal = my_agent.terminal(request_data["data"]["board"])
      print("terminal gotten: ", terminal)
      send = None
      if terminal:
        send = "true"
      else:
        send = "false"
      return {
        "statusCode": 200,
        "body": {"got": send},
        "headers": {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": True,
          "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
          "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
        },
      }

api.add_resource(Move, '/getMove')
api.add_resource(Utility, '/getUtility')
api.add_resource(Terminal, '/getTerminal')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)  # run our Flask app