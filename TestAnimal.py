import pytest

from animal import Animal
from enclosure import Enclosure
from employee import Employee
from zoo import Zoo


@pytest.fixture
def tiger1 ():
    return Animal ("tiger", "ti", 12)

@pytest.fixture
def tiger2 ():
    return Animal ("tiger2", "ti", 2)

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
    return Enclosure("Jack", "East")

@pytest.fixture
def zoo1 ():
    return Zoo ()


def test_addingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    assert (tiger1 in zoo1.animals)
    zoo1.addAnimal(tiger2)

    assert (len(zoo1.animals)==2)

def test_feedingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    tiger1.feed()
    assert (len(tiger1.feeding_record)==1)

def test_vetAnimal(zoo1,tiger1):
    zoo1.addAnimal(tiger1)
    tiger1.vetCheckup()
    assert (len(tiger1.vet_record) == 1)

def test_EnclosureAnimal(enclosure1, tiger1):
    encl = enclosure1
    tiger1.assignEnclosure(encl)
    assert tiger1.enclosure == encl.enclosure_id

def test_EmployeeAnimal(employee1, tiger1):
    caretaker = employee1
    tiger1.assignCareTaker(employee1)
    assert tiger1.care_taker == caretaker.employee_id




