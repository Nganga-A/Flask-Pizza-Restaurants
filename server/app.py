from flask import Flask, make_response, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db

myApp = Flask(__name__)
myApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(myApp)
migrate = Migrate(myApp, db)
api = Api(myApp)

@myApp.route('/')
def home():
    response_dict = {"message": "Welcome to Pizza Inn"}
    return make_response(jsonify(response_dict), 200)

if __name__ == '__main__':
    myApp.run()
