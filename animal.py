import uuid 
import datetime 
class Animal: 
    def __init__ (self, species_name, common_name, age): 
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name 
        self.common_name = common_name 
        self.age = age 
        self.feeding_record = [] 
        self.enclosure = None
        self.care_taker = None
        self.vet_record = []

        

    def feed(self): # save the time when animals was feed
        self.feeding_record.append ( datetime.datetime.now())

    def vetCheckup(self): # save the time when animal had a vet check up
        self.vet_record.append ( datetime.datetime.now())

    def assignEnclosure(self,encl): # assign the animal to an enclosure
        if encl != None:
            self.enclosure = encl.enclosure_id

    def assignCareTaker(self,careTaker): # assign the caretaker to the animal
        self.care_taker = careTaker.employee_id
            