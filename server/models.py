from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship

#metadata specifying naming convections for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = ('-restaurant_pizzas.pizza',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    #Relationships
    restaurant_pizzas = db.relationship('Restaurant_pizzas', back_populates='restaurant', cascade='all, delete-orphan')   #The cascade parameter specifies a list of operations that should be cascaded from the parent object to the related objects. The delete-orphan parameter is used in conjunction with the cascade parameter, specifically when dealing with the deletion of related objects.

    def __repr__(self):
        return f'(id={self.id}, name={self.name} address={self.address})'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    serialize_rules = ('-restaurant.pizzas',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    #Relationships
    restaurant_pizzas = db.relationship('Restaurant_pizzas', back_populates='pizza', cascade='all, delete-orphan')

    def __repr__(self):
        return f'(id={self.id}, name={self.name} ingredients={self.ingredients})'

    @validates('name')
    def check_name(self,key,name):
        if len(name) > 50:
            raise ValueError("Name must be less than 50 characters")
        else:
            return name


class Restaurant_pizzas(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    serialize_rules = ('-pizza.restaurants', '-restaurant.pizzas')

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), default=0.00)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    #Relationships
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    def __repr__(self):
        return f'(id={self.id}, price={self.price} pizza={self.pizza_id} restaurant={self.restaurant_id})'

    @validates('price')
    def check_price(self, key, price):
        if price not in range(1, 31):
            raise ValueError("Price must be between 1 and 30")
        else:
            return price