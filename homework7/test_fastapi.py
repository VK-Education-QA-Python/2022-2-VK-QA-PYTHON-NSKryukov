import requests

url = 'http://127.0.0.1:8081'


def test_create_person():
    response = requests.post(f'{url}/add_person', json={'name': 'Nikita', 'job': 'student'})
    assert response.status_code == 201


def test_create_and_delete_person():
    person_name = 'Nikita'
    requests.post(f'{url}/add_person', json={'name': person_name, 'job': 'student'})
    response = requests.delete(f'{url}/persons/{person_name}')
    assert response.status_code == 200


def test_create_and_update_person():
    person_name = 'Nikita'
    new_job = "teacher"
    requests.post(f'{url}/add_person', json={'name': person_name, 'job': 'student'})
    response = requests.put(f'{url}/persons/{person_name}', json={"name": person_name, "job": new_job})
    assert response.status_code == 201


def test_negative_delete_person():
    requests.post(f'{url}/add_person', json={'name': 'Nikita', 'job': 'student'})
    response = requests.delete(f'{url}/persons/Dima')
    assert response.status_code == 400
