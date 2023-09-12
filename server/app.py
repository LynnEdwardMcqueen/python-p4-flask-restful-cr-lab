#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)

# This is where we create the flask-restful object.
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plant_dictionary_list = [plant.to_dict() for plant in Plant.query.all()]
        print(f"The plant dictionary list is {plant_dictionary_list}")

        response = make_response(
            plant_dictionary_list,
            200
        )

        return response
    
    def post(self):
        # print ("Here in post!!!!!")
        new_plant_dictionary = request.get_json()
        new_plant = Plant(name = new_plant_dictionary['name'], price = new_plant_dictionary['price'], image = new_plant_dictionary['image'])
        print (new_plant)
        db.session.add(new_plant)
        db.session.commit()

        response_dictionary = new_plant.to_dict()

        response = make_response (
            response_dictionary,
            201
        )
        
        return response

        pass

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        print(plant)
        plant_dictionary = plant.to_dict()
        print(plant_dictionary)
        response = make_response(
            plant_dictionary,
            200
        )
        return response
        

api.add_resource(PlantByID, '/plants/<int:id>')            

if __name__ == '__main__':
    app.run(port=3000, debug=True)
