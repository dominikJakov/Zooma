import uuid
import datetime

class Enclosure:
    def __init__(self,name,area):
        self.enclosure_id = str(uuid.uuid4())
        self.name = name
        self.area = area
        self.animals = []
        self.clean_records = []


    def addAnimal(self, animal):
        animal.enclosure
        self.animals.append (animal)

    def removeAnimal(self, animal):
        self.animals.remove(animal)

    def numbOfAnimal(self):
        return len(self.animals)

    def haveMultipleSpecies(self):
        spec = []
        for animal in self.animals:
            spec.append(animal.species_name)
        return all(element == spec[0] for element in spec)


    def cleanEnclosure(self):
        self.clean_records.append(datetime.datetime.now())

