import datetime
import random
import time


class Zoo:
    def __init__ (self):
        self.animals = []
        self.enclosures = []
        self.employees = []
        self.EnclosureCleaningPlanDic = {}
        self.AnimalMedicalPlanDic = {}
        self.AnimalFeedingPlanDic = {}

    def addAnimal(self, animal):
        self.animals.append (animal)

    def addEmployee(self, employee):
        self.employees.append (employee)

    def removeAnimal(self, animal):
        if animal.enclosure != None:
            animal.enclosure.removeAnimal(animal)
        self.animals.remove(animal)

    def getAnimal(self, animal_id):
        for animal in self.animals:
            if animal.animal_id == animal_id:
                return animal

    def addEnclosure(self, enclosure):
        self.enclosures.append (enclosure)

    def getEnclosure(self, enclosure_id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure
        return None

    def getEmployee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee
        return None

    def averageNumOfAnimalsPerEnclosure(self):
        if len(self.animals) != 0:
            return len(self.enclosures) / len(self.animals)
        else:
            return 0

    def enclosureWithMultipleSpecies(self):
        count = 0
        for enclosure in self.enclosures:
            if not enclosure.haveMultipleSpecies():
                count += 1
        return count

    def availableSpace(self):
        dict = {}
        for enclosure in self.enclosures:
            if len(enclosure.animals) != 0:
                dict[enclosure.enclosure_id] = enclosure.area / len(enclosure.animals)
            else:
                dict[enclosure.enclosure_id] = enclosure.area
        return dict

    def removeEnclosure(self, enclosure):
        animals = []
        for animal in enclosure.animals:
            animals.append(animal)
        self.enclosures.remove(enclosure)
        if len(self.enclosures) > 0:
            newEnclusre = random.choice(self.enclosures)
            for animal in animals:
                newEnclusre.addAnimal(animal)
                animal.assignEnclosure(newEnclusre)

    def removeEmployee(self, employee):
        animals = []
        for animal in employee.animals:
            animals.append(animal)
        self.employees.remove(employee)
        if len(self.employees) > 0:
            newEmployee = random.choice(self.employees)
            for animal in animals:
                newEmployee.assignAnimal(animal)
                animal.assignCareTaker(newEmployee)


    def numberOfAnimalsPerSpecies(self):
        dict = {}
        for animal in self.animals:
            if animal.species_name in dict.keys():
                dict[animal.species_name] += 1
            else:
                dict[animal.species_name] = 1
        return dict

    def employeeStats(self):
        dict = {}
        average = 0
        for employee in self.employees:
            dict[employee.employee_id] = len(employee.animals)
            average += len(employee.animals)
        max_value = max(dict)
        min_value = min(dict)
        average = average / len(self.employees)
        return [dict[max_value], dict[min_value],average]

    def enclosureCleaningPlan(self):
        self.EnclosureCleaningPlanDic = {}
        for enclosure in self.enclosures:
            if len(enclosure.clean_records) > 0:
                lastRecord = enclosure.clean_records[-1] + datetime.timedelta(days=3)
            else:
                lastRecord = datetime.datetime.now() + datetime.timedelta(days=3)

            nextRecord = f"{lastRecord.year} - {lastRecord.month} - {lastRecord.day}"
            self.EnclosureCleaningPlanDic[enclosure.enclosure_id] = nextRecord

    def animalMedicalPlan(self):
        AnimalMedicalPlanDic = {}
        for animal in self.animals:
            if len(animal.vet_record) > 0:
                lastRecord = animal.vet_record[-1] + datetime.timedelta(days=35)
            else:
                lastRecord = datetime.datetime.now() + datetime.timedelta(days=35)
            nextRecord = f"{lastRecord.year} - {lastRecord.month} - {lastRecord.day}"
            self.AnimalMedicalPlanDic[animal.animal_id] = nextRecord

    def animalFeedingPlan(self):
        AnimalFeedingPlanDic = {}
        for animal in self.animals:
            if len(animal.feeding_record) > 0:
                lastRecord = animal.feeding_record[-1] + datetime.timedelta(days=2)
            else:
                lastRecord = datetime.datetime.now() + datetime.timedelta(days=2)

            nextRecord = f"{lastRecord.year} - {lastRecord.month} - {lastRecord.day}"
            self.AnimalFeedingPlanDic[animal.animal_id] = nextRecord
