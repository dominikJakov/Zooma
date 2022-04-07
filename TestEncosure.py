import pytest

from enclosure import Enclosure
from animal import Animal
from zoo import Zoo


@pytest.fixture
def enclosure1():
    return Enclosure("Wolf Cage", 100)

@pytest.fixture
def enclosure2():
    return Enclosure("Wolf Cage 2", 500)

@pytest.fixture
def tiger1 ():
    return Animal ("tiger", "ti", 12)

@pytest.fixture
def tiger2 ():
    return Animal ("tiger2", "tig", 2)


@pytest.fixture
def zoo1 ():
    return Zoo ()


def test_add_enclosure(zoo1,enclosure1,enclosure2):
    zoo1.addEnclosure(enclosure1)
    assert (enclosure1 in zoo1.enclosures)
    assert(len(zoo1.enclosures)==1)
    zoo1.addEnclosure(enclosure2)
    assert (enclosure2 in zoo1.enclosures)
    assert (len(zoo1.enclosures) == 2)


def test_remove_animal(zoo1,enclosure1,tiger1,tiger2):
    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)
    assert len(enclosure1.animals) == 2
    enclosure1.removeAnimal(tiger1)
    assert len(enclosure1.animals) == 1
    assert not(tiger1 in enclosure1.animals)
    assert (tiger2 in enclosure1.animals)

def test_numbOfAnimal(zoo1,enclosure1,tiger1):
    enclosure1.addAnimal(tiger1)
    assert enclosure1.numbOfAnimal() == 1
    assert len(enclosure1.animals) == 1

def test_haveMultipleSpecies(zoo1,enclosure1,enclosure2,tiger1,tiger2):
    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)
    assert enclosure1.haveMultipleSpecies() == False
    enclosure2.addAnimal(tiger1)
    enclosure2.addAnimal(tiger1)
    assert enclosure2.haveMultipleSpecies() == True



def test_cleanEnclosure(enclosure1,enclosure2):
    enclosure1.cleanEnclosure()
    assert len(enclosure1.clean_records) == 1
    enclosure1.cleanEnclosure()
    assert len(enclosure1.clean_records) == 2
    assert len(enclosure2.clean_records) == 0



