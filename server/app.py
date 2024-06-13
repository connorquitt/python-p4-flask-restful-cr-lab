#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()

        plant_response = [p.to_dict() for p in plants]

        return plant_response
    
    def post(self):
        new_plant = Plant(
            name = request.json.get('name'),
            image = request.json.get('image'),
            price = request.json.get('price')
        )

        db.session.add(new_plant)
        db.session.commit()

        new_plant_dict = new_plant.to_dict()

        response = make_response(new_plant_dict, 201)

        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return plant
api.add_resource(PlantByID, '/plants/<int:id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
