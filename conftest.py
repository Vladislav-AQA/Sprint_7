from helpers import register_new_courier_and_return_login_password
import pytest
import requests
import urls

@pytest.fixture
def create_courier():
    data_courier = register_new_courier_and_return_login_password()
    courier = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_COURIER}', json=data_courier)
    login_courier = requests.post(url=f'{urls.BASE_URL}{urls.LOGIN_COURIER}', json=courier.json()["authorization"])
    yield login_courier.json()["id"], login_courier.json()["name"]
    requests.delete(url=f'{urls.BASE_URL}{urls.DELETE_COURIER}{login_courier.json()["id"]}')


