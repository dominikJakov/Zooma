from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder 
from zoo import Zoo
from enclosure import Enclosure

from animal import Animal
from employee import Employee

my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder 
zooma_api = Api(zooma_app)

animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True, help='The scientific name of the animal, e,g. Panthera tigris')
animal_parser.add_argument('name', type=str, required=True, help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument('age', type=int, required=True, help='The age of the animal, e.g., 12')

enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True, help='The name of the enclosure')
enclosure_parser.add_argument('area', type=int, required=True, help='The dimesion of the area')




@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object 
        new_animal = Animal (species, name, age) 
        #add the animal to the zoo
        my_zoo.addAnimal (new_animal) 
        return jsonify(new_animal) 

@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
     def get(self, animal_id):
        search_result  = my_zoo.getAnimal(animal_id)
        return search_result # this is automatically jsonified by flask-restx
    
     def delete(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)
        return jsonify(f"Animal with ID {animal_id} was removed")

@zooma_api.route('/animals')
class AllAnimals(Resource):
     def get(self):
        return jsonify( my_zoo.animals)  

@zooma_api.route('/animal/<animal_id>/feed')
class FeedAnimal(Resource):
     def post(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.feed()
        return jsonify(targeted_animal)

@zooma_api.route('/animal/<animal_id>/vet')
class VetCheckupAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.vetCheckup()
        return jsonify(targeted_animal)

home_parser = reqparse.RequestParser()
home_parser.add_argument('enclosure_id', type=str, required=True, help='The id of the enclosure')

@zooma_api.route('/animal/<animal_id>/home')
class EnclosureAnimal(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self,animal_id):
        args = home_parser.parse_args()
        enclosure_id = args['enclosure_id']
        targeted_animal = my_zoo.getAnimal(animal_id)
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        old_enclosure = my_zoo.getEnclosure(targeted_animal.enclosure)
        if old_enclosure != None:
            old_enclosure.removeAnimal(targeted_animal)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        targeted_animal.assignEnclosure(targeted_enclosure)
        targeted_enclosure.addAnimal(targeted_animal)
        return jsonify(targeted_animal)

mother_parser = reqparse.RequestParser()
mother_parser.add_argument('mother_id', type=str, required=True, help='The id of the mother animal')

@zooma_api.route('/animal/birth/')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=mother_parser)
    def post(self):
        args = mother_parser.parse_args()
        mother_id = args['mother_id']
        mother_animal = my_zoo.getAnimal(mother_id)
        if not mother_animal:
            return jsonify(f"Animal with ID {mother_id} was not found")
        new_animal = Animal(mother_animal.species_name, mother_animal.common_name, 1)
        new_animal.assignEnclosure(mother_animal.enclosure)
        if mother_animal.enclosure != None:
            encl = my_zoo.getEnclosure(new_animal.enclosure)
            encl.addAnimal(new_animal)
        my_zoo.addAnimal(new_animal)
        return jsonify(new_animal)

death_parser = reqparse.RequestParser()
death_parser.add_argument('dead_animal_id', type=str, required=True, help='The id of the dead animal')
@zooma_api.route('/animal/death/')
class DeathAnimal(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):
        args = death_parser.parse_args()
        animal_id = args['dead_animal_id']
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)
        if targeted_animal.enclosure != None:
            encl = my_zoo.getEnclosure(targeted_animal.enclosure)
            encl.removeAnimal(targeted_animal)
        return jsonify(targeted_animal)

@zooma_api.route('/animals/stat')
class AnimalStats(Resource):
    def get(self):
        animal_stat = {}
        animal_stat["Total number of animals per species"] = my_zoo.numberOfAnimalsPerSpecies()
        animal_stat["Average number of animals per enclosure"] = my_zoo.averageNumOfAnimalsPerEnclosure()
        animal_stat["Number of enclosures with animals from multiple species "] = my_zoo.enclosureWithMultipleSpecies()
        animal_stat["Available space per animal in each enclosure"] = my_zoo.availableSpace()
        return jsonify(animal_stat)

@zooma_api.route('/enclosure')
class AddEnclosure(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):
        args = enclosure_parser.parse_args()
        name = args['name']
        area = args['area']
        new_enclosure = Enclosure (name, area)
        my_zoo.addEnclosure (new_enclosure)
        return jsonify(new_enclosure)

@zooma_api.route('/enclosures')
class AllEnclosures(Resource):
     def get(self):
        return jsonify(my_zoo.enclosures)

@zooma_api.route('/enclosures/<enclosure_id>/clean')
class CleanEnclosure(Resource):
    def post(self,enclosure_id):
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        targeted_enclosure.cleanEnclosure()
        return jsonify(targeted_enclosure)

@zooma_api.route('/enclosures/<enclosure_id>/animals')
class EnclosuresAnimals(Resource):
     def get(self,enclosure_id):
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        return jsonify(targeted_enclosure.animals)


@zooma_api.route('/enclosure/<enclosure_id>')
class DeleteEnclosure(Resource):
    def delete(self, enclosure_id):
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        my_zoo.removeEnclosure(targeted_enclosure)
        return jsonify(f"Enclosure with ID {enclosure_id} was removed")

emplyee_parser = reqparse.RequestParser()
emplyee_parser.add_argument('name', type=str, required=True, help='The name of the employee')
emplyee_parser.add_argument('address', type=str, required=True, help='The address of the employee')

@zooma_api.route('/employee')
class AddEmployee(Resource):
    @zooma_api.doc(parser=emplyee_parser)
    def post(self):
        args = emplyee_parser.parse_args()
        name = args['name']
        address = args['address']
        new_emplyee = Employee (name, address)
        my_zoo.addEmployee (new_emplyee)
        return jsonify(new_emplyee)

@zooma_api.route('/employees')
class AllEmployees(Resource):
     def get(self):
        return jsonify(my_zoo.employees)

@zooma_api.route('/employee/<employee_id>/care/<animal_id>/')
class EmployeeCareAnimal(Resource):
    def post(self,employee_id,animal_id):
        # get the post parameters
        targeted_employee = my_zoo.getEmployee(employee_id)
        if not targeted_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        if targeted_animal.care_taker != None:
            old_employee = my_zoo.getEmployee(targeted_animal.employee_id)
            old_employee.removeAnimal(targeted_animal)
        targeted_animal.assignCareTaker(targeted_employee)
        targeted_employee.assignAnimal(targeted_animal)
        return jsonify(targeted_animal)

@zooma_api.route('/employee/<employee_id>/care/animals')
class EmployeeAllAnimals(Resource):
     def get(self,employee_id):
        target_employee = my_zoo.getEmployee(employee_id)
        if not target_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        return jsonify(target_employee.animals)

@zooma_api.route('/employees/stats')
class EmployeeStats(Resource):
     def get(self):
        stats = my_zoo.employeeStats()
        return jsonify(stats)

@zooma_api.route('/employee/<employee_id>')
class DeleteEmployee(Resource):
    def delete(self, employee_id):
        targeted_employee = my_zoo.getEmployee(employee_id)
        if not targeted_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        my_zoo.removeEmployee(targeted_employee)
        return jsonify(f"Employee with ID {employee_id} was removed")

@zooma_api.route('/tasks/cleaning/')
class CleaninPlan(Resource):
     def get(self):
        my_zoo.enclosureCleaningPlan()
        return jsonify(my_zoo.EnclosureCleaningPlanDic)


@zooma_api.route('/tasks/medical')
class MedicalPlan(Resource):
     def get(self):
        my_zoo.animalMedicalPlan()
        return jsonify(my_zoo.AnimalMedicalPlanDic)


@zooma_api.route('/tasks/feeding')
class FeedingPlan(Resource):
     def get(self):
        my_zoo.animalFeedingPlan()
        return jsonify(my_zoo.AnimalFeedingPlanDic)

    
if __name__ == '__main__':
    zooma_app.run(debug = False, port = 7890)