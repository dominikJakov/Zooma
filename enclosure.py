import uuid
import datetime

class Enclosure:
    def __init__(self,name,area):
        self.enclosure_id = str(uuid.uuid4())
        self.name = name
        self.area = area
        self.animals = []
        self.clean_records = []


    def addAnimal(self, animal): # add the animal to the enclosure
        animal.enclosure
        self.animals.append (animal)

    def removeAnimal(self, animal): # remove the animal from the zoo
        self.animals.remove(animal)

    def numbOfAnimal(self): # return the number of the animals
        return len(self.animals)

    def haveMultipleSpecies(self): # returns if the enclosure if the enclosure has more animal species
        spec = []
        for animal in self.animals:
            spec.append(animal.species_name)
        return all(element == spec[0] for element in spec)


    def cleanEnclosure(self): # save the cleaning time
        self.clean_records.append(datetime.datetime.now())

