#!/usr/bin/env python3
from typing import Optional
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import requests
import json
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Person(BaseModel):
    name: str
    job: str
    person_id: Optional[int] = None


app_data = {}
person_id_seq = 1


@app.get('/')
def read_root():
    return {"This is": "root page"}


@app.post('/add_person', status_code=201)
def create_person(person: Person):
    global person_id_seq

    person_name = person.name
    if person_name not in app_data:
        response = requests.post('127.0.0.1:8082/add_person',
                                 json={"name": person_name,
                                       "job": person.job,
                                       "person_id": person_id_seq})
        person_id_seq += 1
        return response
    else:
        content = json.dumps(f'Person {person_name} already exists id: {app_data[person_name]["person_id"]}')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@app.put('/persons/{name}', status_code=201)
def update_person(person: Person, name: str):
    person_name = name
    if person_name in app_data:
        response = requests.put(f'127.0.0.1:8082/persons/{person_name}',
                                json={"name": person_name, "job": person.job})
        return response
    else:
        content = json.dumps(f'Person {name} is not existing')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@app.get('/get_person_id/{name}', status_code=200)
def get_person_id(name: str):
    if app_data.get(name):
        mock_host = '127.0.0.1'
        mock_port = 8081

        mocked_person_id = None
        try:
            response = requests.get(f'http://{mock_host}:{mock_port}/get_person_id/{name}')
            if response.status_code == 200:
                mocked_person_id = response.json()
        except Exception as e:
            print(f'Unable to get person id from external system:\n{e}')

        return json.dumps(f'Person id is {mocked_person_id}')

    else:
        content = json.dumps(f'Person {name} is not existing')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@app.delete('/persons/{name}', status_code=200)
def delete_person(name: str):
    if name in app_data:
        mock_host = '127.0.0.1'
        mock_port = 8081
        response = requests.delete(f'http://{mock_host}:{mock_port}/persons/{name}')
        return response
    else:
        content = json.dumps(f'Person {name} is not existing')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True,
        port=8081,
        # log_config="log.ini",
    )
