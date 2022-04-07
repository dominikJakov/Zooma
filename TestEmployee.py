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
def employee1():
    return Employee("Mark", "West")

@pytest.fixture
def employee2():
    return Enclosure("Jack", "East")

@pytest.fixture
def zoo1 ():
    return Zoo ()


def test_assignAnimal(employee1, tiger1):
    employee1.assignAnimal(tiger1)
    assert (tiger1 in employee1.animals)


def test_removeAnimal(employee1, tiger1, tiger2):
    employee1.assignAnimal(tiger1)
    employee1.assignAnimal(tiger2)
    assert (tiger1 in employee1.animals)
    assert (tiger2 in employee1.animals)
    employee1.removeAnimal(tiger1)
    assert (tiger2 in employee1.animals)
    assert not(tiger1 in employee1.animals)






