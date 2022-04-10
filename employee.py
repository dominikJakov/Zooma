import uuid
import datetime

class Employee:
    def __init__(self,name,address):
        self.employee_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals = []

    def assignAnimal(self,animal): # assign the animal to the employee
        self.animals.append(animal)

    def removeAnimal(self, animal): # remove the animal from the employee
        self.animals.remove(animal)