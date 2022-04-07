import pytest
import requests
import json

@pytest.fixture
def baseURL ():
    return "http://127.0.0.1:7890/"

@pytest.fixture
def zooWithOneAnimal(baseURL):
    requests.post (baseURL+"/animal", {"species":"tiger", "name":"btiger", "age":3})
    response = requests.get(baseURL + "/animals")

    return response.content

@pytest.fixture
def zooWithTwoAnimal(baseURL):
    requests.post(baseURL + "/animal", {"species": "wolf", "name": "ttwolf", "age": 31})
    response = requests.get(baseURL + "/animals")
    return response.content

@pytest.fixture
def zooWithMotherAnimal(baseURL):
    mother = json.loads(requests.get(baseURL + "/animals").content)[0]
    print (mother)
    requests.post(baseURL + "/animal/birth/", {"mother_id": mother["animal_id"]} )
    response = requests.get(baseURL + "/animals")
    return response.content

@pytest.fixture
def zooWithMotherAnimal(baseURL):
    mother = json.loads(requests.get(baseURL + "/animals").content)[0]
    print (mother)
    requests.post(baseURL + "/animal/birth/", {"mother_id": mother["animal_id"]} )
    response = requests.get(baseURL + "/animals")
    return response.content

@pytest.fixture
def zooWithDeadAnimal(baseURL):
    dead_animal = json.loads(requests.get(baseURL + "/animals").content)[0]
    requests.post(baseURL + "/animal/death/", {"dead_animal_id": dead_animal["animal_id"]} )
    response = requests.get(baseURL + "/animals")
    return response.content

@pytest.fixture
def zooWithfeedAnimal(baseURL):
    animal_feed = json.loads(requests.get(baseURL + "/animals").content)[0]
    requests.post(baseURL + "/animal/"+animal_feed["animal_id"]+"/feed")
    response = requests.get(baseURL + "/animals")
    return response.content

@pytest.fixture
def zooWithVetAnimal(baseURL):
    animal_vet = json.loads(requests.get(baseURL + "/animals").content)[0]
    requests.post(baseURL + "/animal/"+animal_vet["animal_id"]+"/vet")
    response = requests.get(baseURL + "/animals")
    return response.content

@pytest.fixture
def zooWithHomeAnimal(baseURL):
    animal_home = json.loads(requests.get(baseURL + "/animals").content)[0]
    enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
    requests.post(baseURL + "/animal/"+animal_home["animal_id"]+"/home",{"enclosure_id" : enclosure["enclosure_id"]})
    response = requests.get(baseURL + "/animals")
    return response.content

@pytest.fixture
def zooWithAnimalStats(baseURL):
    response = requests.get(baseURL + "/animals/stat")
    return response.content

@pytest.fixture
def zooWithOneEnclosure(baseURL):
    requests.post(baseURL + "/enclosure", {"name": "Park", "area": 10})
    response = requests.get(baseURL + "/enclosures")
    return response.content

@pytest.fixture
def zooWithTwoEnclosure(baseURL):
    requests.post(baseURL + "/enclosure", {"name": "West", "area": 50})
    response = requests.get(baseURL + "/enclosures")
    return response.content

@pytest.fixture
def zooWithCleanEnclosure(baseURL):
    enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
    requests.post(baseURL + "/enclosures/" + enclosure["enclosure_id"]+ "/clean")
    response = requests.get(baseURL + "/enclosures")

    return response.content

@pytest.fixture
def zooWithAnimalsEnclosure(baseURL):
    enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
    requests.post(baseURL + "/enclosures/" + enclosure["enclosure_id"] + "/animals")
    response = requests.get(baseURL + "/enclosures")
    return response.content

@pytest.fixture
def zooWithRemoveEnclosure(baseURL):
    enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[-1]
    requests.delete(baseURL + "/enclosure/" + enclosure["enclosure_id"])
    response = requests.get(baseURL + "/enclosures")
    return response.content

@pytest.fixture
def zooWithOneEmployee(baseURL):
    requests.post(baseURL + "/employee", {"name": "Mark", "address": "West Side"})
    response = requests.get(baseURL + "/employees")
    return response.content

@pytest.fixture
def zooWithTwoEmployee(baseURL):
    requests.post(baseURL + "/employee", {"name": "Jack", "address": "South 12"})
    response = requests.get(baseURL + "/employees")
    return response.content

@pytest.fixture
def zooWithEmployeeCareAnimal(baseURL):
    employee = json.loads(requests.get(baseURL + "/employees").content)[0]
    animal = json.loads(requests.get(baseURL + "/animals").content)[0]
    requests.post(baseURL + "/employee/"+employee["employee_id"]+"/care/"+ animal["animal_id"]+"/")
    response_employee = requests.get(baseURL + "/employees")
    response_animal = requests.get(baseURL + "/animals")
    return (response_employee.content, response_animal.content)

@pytest.fixture
def zooWithEmployeeStats(baseURL):
    return (requests.get(baseURL + "/employees/stats").content)

@pytest.fixture
def zooWithEmployeeAllAnimals(baseURL):
    employee = json.loads(requests.get(baseURL + "/employees").content)[0]
    response_animals = requests.get(baseURL + "/animals")
    response = requests.get(baseURL + "/employee/"+ employee["employee_id"] +"/care/animals")
    return (response.content,response_animals.content)

@pytest.fixture
def zooWithRemoveEmployee(baseURL):
    employee = json.loads(requests.get(baseURL + "/employees").content)[0]
    requests.delete(baseURL + "/employee/" + employee["employee_id"])
    response = requests.get(baseURL + "/employees")
    response_animals = requests.get(baseURL + "/animals")
    return (response.content,response_animals.content)

@pytest.fixture
def zooWithTaskCleaning(baseURL):
    return requests.get(baseURL + "/tasks/cleaning/").content

@pytest.fixture
def zooWithTaskMedical(baseURL):
    response = requests.get(baseURL + "/tasks/medical")
    return response.content

@pytest.fixture
def zooWithTaskFeeding(baseURL):
    return requests.get(baseURL + "/tasks/feeding").content

def test_zoo1 (zooWithOneAnimal):
    jo = json.loads(zooWithOneAnimal)
    print (jo)
    assert jo[0]["common_name"] =="btiger"
    assert jo[0]["species_name"] == "tiger"
    assert jo[0]["age"] == 3
    assert (len(jo) == 1)

def test_zoo2 (zooWithTwoAnimal):
    jo = json.loads(zooWithTwoAnimal)
    print (jo)
    assert jo[1]["common_name"] == "ttwolf"
    assert jo[1]["species_name"] == "wolf"
    assert jo[1]["age"] == 31
    assert (len(jo) == 2)

def test_zoo3 (zooWithOneEnclosure):
    jo = json.loads(zooWithOneEnclosure)
    print (jo)
    assert jo[0]["name"] == "Park"
    assert jo[0]["area"] == 10
    assert (len(jo) == 1)

def test_zoo_two_enclosure (zooWithTwoEnclosure):
    jo = json.loads(zooWithTwoEnclosure)
    print (jo)
    assert jo[1]["name"] == "West"
    assert jo[1]["area"] == 50
    assert (len(jo) == 2)

def test_zoo_mother_animal (zooWithMotherAnimal):
    jo = json.loads(zooWithMotherAnimal)
    print (jo)
    assert (len(jo) == 3)
    assert jo[0]["common_name"] == jo[-1]["common_name"]
    assert jo[0]["species_name"] == jo[-1]["species_name"]
    assert jo[0]["enclosure"] == jo[-1]["enclosure"]

def test_zoo_dead_animal (zooWithDeadAnimal):
    jo = json.loads(zooWithDeadAnimal)
    print (jo)
    assert (len(jo) == 2)

def test_zoo_feed_animal (zooWithfeedAnimal):
    jo = json.loads(zooWithfeedAnimal)
    assert len(jo[0]["feeding_record"]) == 1

def test_zoo_vet_animal (zooWithVetAnimal):
    jo = json.loads(zooWithVetAnimal)
    assert len(jo[0]["vet_record"]) == 1


def test_zoo_home_animal (zooWithHomeAnimal):
    jo = json.loads(zooWithHomeAnimal)
    assert jo[0]["enclosure"] != None

def test_zoo_animal_stat (zooWithAnimalStats):
    jo = json.loads(zooWithAnimalStats)
    assert jo != None

def test_zoo_clean_enclosure(zooWithCleanEnclosure):
    jo = json.loads(zooWithCleanEnclosure)
    assert len(jo[0]["clean_records"]) == 1

def test_zoo_animals_enclosure(zooWithAnimalsEnclosure):
    jo = json.loads(zooWithAnimalsEnclosure)
    assert len(jo) != 0

def test_zoo_remove_enclosure (zooWithRemoveEnclosure):
    jo = json.loads(zooWithRemoveEnclosure)
    assert (len(jo) == 1)

def test_zoo_one_employee (zooWithOneEmployee):
    jo = json.loads(zooWithOneEmployee)
    assert jo[0]["name"] == "Mark"
    assert jo[0]["address"] == "West Side"
    assert (len(jo) == 1)

def test_zoo_two_employee (zooWithTwoEmployee):
    jo = json.loads(zooWithTwoEmployee)
    assert jo[1]["name"] == "Jack"
    assert jo[1]["address"] == "South 12"
    assert (len(jo) == 2)

def test_zoo_care_animals (zooWithEmployeeCareAnimal):
    jo = (json.loads(zooWithEmployeeCareAnimal[0]) , json.loads(zooWithEmployeeCareAnimal[1]))
    assert len(jo[0][0]["animals"]) == 1
    assert jo[1][0]["care_taker"] == jo[0][0]["employee_id"]

def test_zoo_employee_all_animals (zooWithEmployeeAllAnimals):
    jo = (json.loads(zooWithEmployeeAllAnimals[0]), json.loads(zooWithEmployeeAllAnimals[1]))
    assert len(jo[0]) == 1
    assert jo[0][0] == jo[1][0]

def test_zoo_remove_employee (zooWithEmployeeStats):
    jo = json.loads(zooWithEmployeeStats)
    assert len(jo) == 3

def test_zoo_cleaning_task(zooWithTaskCleaning):
    jo = json.loads(zooWithTaskCleaning)
    assert len(jo) == 1

def test_zoo_medical_task(zooWithTaskMedical):
    jo = json.loads(zooWithTaskMedical)
    assert len(jo) == 2

def test_zoo_feeding_task(zooWithTaskFeeding):
    jo = json.loads(zooWithTaskFeeding)
    assert len(jo) == 2






