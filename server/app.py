from flask import Flask, make_response, jsonify , request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db,Restaurant,Pizza,Restaurant_pizzas

myApp = Flask(__name__)
myApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(myApp)
migrate = Migrate(myApp, db)
api = Api(myApp)

class Home(Resource):
    def get(self):
        response_message = {
            "message": "WELCOME TO OUR PIZZERIA."
        }
        return make_response(response_message, 200)

api.add_resource(Home, '/')


class Restaurants(Resource):
    def get(self):
        restaurants_dicts = []
        for restaurant in Restaurant.query.all():
            dict_restaurant = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
            }
            restaurants_dicts.append(dict_restaurant)
        return make_response(restaurants_dicts, 200)
    
api.add_resource(Restaurants, '/restaurants')


class RestaurantsByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
            }
            response = make_response(restaurant_dict, 200)
        else:
            response_body = {
                "error": "Restaurant not found"
            }
            response = make_response(response_body,404)
        return response
    
    def delete(self,id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            response_body = {
                "delete_successful":True,
                "message":"Deleted Successfully"
            }
            response = make_response(response_body,200)
        else:
            response_body = {
                "error": "Restaurant not found"
            }
            response = make_response(response_body,404)
        return response
    

    def patch(self,id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(restaurant, attr, request.form.get(attr))
        db.session.add(restaurant)
        db.session.commit()
        restaurant_dict = restaurant.to_dict()
        return make_response(restaurant_dict,200)

api.add_resource(RestaurantsByID, '/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        pizzas_dicts = []
        for pizza in Pizza.query.all():
            dict_pizza = {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients,
            }
            pizzas_dicts.append(dict_pizza)
        return make_response(pizzas_dicts, 200)
    
api.add_resource(Pizzas,'/pizzas')


class PizzaByID(Resource):
    def get(self, id):
        pizza = Pizza.query.filter_by(id=id).first()
        if pizza:
            pizza_dict = pizza.to_dict()
            response = make_response(pizza_dict, 200)
        else:
            response_body = {
                "error": "Pizza not found"
            }
            response = make_response(response_body,404)
        return response
    
api.add_resource(PizzaByID, '/pizzas/<int:id>')

class RestaurantPizzas(Resource):
    def post(self):
        new_restaurant_pizza = Restaurant_pizzas(
            price = int(request.form.get('price')),
            pizza_id = request.form.get('pizza_id'),
            restaurant_id = request.form.get('restaurant_id'),
        )
        try:
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            restaurant_pizza_dict = new_restaurant_pizza.to_dict()
            response_body = {
                "message": "Restaurant_pizza created for...",
                "pizza": restaurant_pizza_dict['pizza'],
                "restaurant": restaurant_pizza_dict['restaurant']
            }
            response = make_response(response_body, 200)
        except Exception as e:
            response_body = {
                "Validation errors": f"An exception of type {type(e).__name__} occurred: {str(e)}"
            }
            response = make_response(response_body, 404)
        finally:
            return response


api.add_resource(RestaurantPizzas,'/restaurant_pizzas')


if __name__ == '__main__':
    myApp.run(port=5555, debug=True)
