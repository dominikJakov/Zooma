import pytest
import requests
import json

from animal import Animal
from zoo import Zoo
from enclosure import Enclosure
from employee import Employee

@pytest.fixture
def baseURL ():
    return "http://127.0.0.1:7890"

@pytest.fixture
def tiger1 ():
    return Animal("tiger mum", "btiger1", 21)

@pytest.fixture
def tiger1Clone ():
    return Animal("tiger mum", "btiger1", 21)

@pytest.fixture
def tiger2 ():
    return Animal("tiger child", "btiger2", 2)

@pytest.fixture
def wolf1 ():
    return Animal("wolf 1", "wwolf1", 11)

@pytest.fixture
def wolf2 ():
    return Animal("wolf 2", "wwolf2", 5)


@pytest.fixture
def enclosure1():
    return Enclosure("Wolf Cage", 100)

@pytest.fixture
def enclosure2():
    return Enclosure("Wolf Cage 2", 500)

@pytest.fixture
def employee1():
    return Employee("Mark", "West")

@pytest.fixture
def employee2():
    return Employee("Jack", "East")

@pytest.fixture
def zoo1 ():
    return Zoo ()

@pytest.fixture
def post_tiger1 (baseURL, tiger1):
    tiger1_data = {"species": tiger1.species_name, "name": tiger1.common_name, "age": tiger1.age}
    requests.post(baseURL + "/animal", data=tiger1_data)




def test_addingAnimal(zoo1, tiger1):
        zoo1.addAnimal(tiger1)
        assert (tiger1 in zoo1.animals)
        zoo1.addAnimal(tiger2)
        assert (len(zoo1.animals) == 2)

def test_addEmployee(zoo1, employee1,employee2):
        zoo1.addEmployee(employee1)
        assert (employee1 in zoo1.employees)
        zoo1.addEmployee(employee2)
        assert (len(zoo1.employees) == 2)

def test_removeAnimal(zoo1, tiger1,tiger2):
        zoo1.addAnimal(tiger1)
        zoo1.addAnimal(tiger2)
        zoo1.removeAnimal(tiger1)
        assert not(tiger1 in zoo1.animals)
        assert (len(zoo1.animals) == 1)

def test_getAnimal(zoo1, tiger1,tiger2):
        zoo1.addAnimal(tiger1)
        zoo1.addAnimal(tiger2)
        assert zoo1.getAnimal(tiger1.animal_id) == tiger1

def test_addEnclosure(zoo1, enclosure1, enclosure2):
        zoo1.addEnclosure(enclosure1)
        assert (enclosure1 in zoo1.enclosures)
        assert (len(zoo1.enclosures) == 1)
        zoo1.addEnclosure(enclosure2)
        assert (enclosure2 in zoo1.enclosures)
        assert (len(zoo1.enclosures) == 2)

def test_getEnclosure(zoo1, enclosure1, enclosure2):
        zoo1.addEnclosure(enclosure1)
        zoo1.addEnclosure(enclosure2)
        assert zoo1.getEnclosure(enclosure1.enclosure_id) == enclosure1

def test_getEmployee(zoo1, employee1, employee2):
        zoo1.addEmployee(employee1)
        zoo1.addEmployee(employee2)
        assert zoo1.getEmployee(employee1.employee_id) == employee1

def test_averageNumOfAnimalsPerEnclosure(zoo1, enclosure1, enclosure2, tiger1,tiger2,wolf1,wolf2):
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(wolf1)
    zoo1.addAnimal(wolf2)
    assert zoo1.averageNumOfAnimalsPerEnclosure() == 0.5

def test_enclosureWithMultipleSpecies(zoo1, enclosure1, enclosure2, tiger1, tiger2, wolf1, wolf2):
        enclosure1.addAnimal(tiger1)
        enclosure1.addAnimal(tiger2)
        enclosure2.addAnimal(wolf1)
        zoo1.addEnclosure(enclosure1)
        zoo1.addEnclosure(enclosure2)
        zoo1.addAnimal(tiger1)
        zoo1.addAnimal(tiger2)
        zoo1.addAnimal(wolf1)
        assert zoo1.enclosureWithMultipleSpecies() == 1


def test_enclosureWithMultipleSpecies(zoo1, enclosure1, enclosure2, tiger1, tiger2, wolf1, wolf2):
    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)
    enclosure2.addAnimal(wolf1)
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(wolf1)
    assert zoo1.enclosureWithMultipleSpecies() == 1



def test_availableSpace(zoo1, enclosure1, enclosure2, tiger1, tiger2, wolf1):
    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)
    enclosure2.addAnimal(wolf1)
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)
    av = zoo1.availableSpace()
    assert av[enclosure1.enclosure_id] == 50
    assert av[enclosure2.enclosure_id] == 500


def test_removeEnclosure(zoo1,enclosure1, enclosure2,tiger1):
    enclosure1.addAnimal(tiger1)
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)

    zoo1.removeEnclosure(enclosure1)
    assert not(enclosure1 in zoo1.enclosures)
    assert enclosure2 in zoo1.enclosures
    assert tiger1 in enclosure2.animals
    assert len(zoo1.enclosures) == 1

def test_removeEmployee(zoo1,employee1, employee2,tiger1):
    employee1.assignAnimal(tiger1)
    zoo1.addEmployee(employee1)
    zoo1.addEmployee(employee2)

    zoo1.removeEmployee(employee1)
    assert not(employee1 in zoo1.employees)
    assert employee2 in zoo1.employees
    assert tiger1 in employee2.animals
    assert len(zoo1.employees) == 1


def test_numberOfAnimalsPerSpecies(zoo1, tiger1, tiger2, wolf1,tiger1Clone):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger1Clone)
    zoo1.addAnimal(wolf1)
    zoo1.addAnimal(tiger2)
    av = zoo1.numberOfAnimalsPerSpecies()
    assert av[tiger1.species_name] == 2
    assert av[wolf1.species_name] == 1
    assert av[tiger2.species_name] == 1



def test_employeeStats(zoo1, employee1, employee2, tiger1,tiger2,wolf1):
    employee1.assignAnimal(tiger1)
    employee1.assignAnimal(tiger2)
    employee2.assignAnimal(wolf1)
    zoo1.addEmployee(employee1)
    zoo1.addEmployee(employee2)
    av = zoo1.employeeStats()
    assert av[employee1.employee_id] == 2
    assert av[employee2.employee_id] == 1
    assert av["Average for all employees"] == 1.5

def test_enclosureCleaningPlan(zoo1, enclosure1, enclosure2):
    enclosure1.cleanEnclosure()
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)
    zoo1.enclosureCleaningPlan()
    assert len(zoo1.EnclosureCleaningPlanDic) == 2

def test_animalMedicalPlan(zoo1, tiger1, tiger2):
    tiger1.vetCheckup()
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.animalMedicalPlan()
    assert len(zoo1.AnimalMedicalPlanDic) == 2

def test_animalFeedingPlan(zoo1, tiger1, tiger2):
    tiger1.feed()
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.animalFeedingPlan()
    assert len(zoo1.AnimalFeedingPlanDic) == 2


class Testzoo():
    pass
    # def test_one(self, baseURL, post_tiger1):
    #     x = requests.get (baseURL+"/animals")
    #     js =  x.content
    #     animals = json.loads(js)
    #     assert (len(animals)==1)