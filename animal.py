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
        #self.mother = None
        # add more as required here 
        
    # simply store the current system time when this method is called    
    def feed(self): 
        self.feeding_record.append ( datetime.datetime.now())

    def vetCheckup(self):
        self.vet_record.append ( datetime.datetime.now())

    def assignEnclosure(self,encl):
        if encl != None:
            self.enclosure = encl.enclosure_id

    def assignCareTaker(self,careTaker):
        self.care_taker = careTaker.employee_id
            