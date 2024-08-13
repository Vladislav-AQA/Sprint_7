import allure
import urls
import requests
from faker import Faker

fake = Faker(locale="ru_RU")

payload_without_password = {
    "login": "ninja"
}

payload_wrong_password = {
    "login": "ninja",
    "password": "111111"
}

@classmethod
def setup_class(cls):
    login = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    cls.courier = {"login": login, "password": password, "firstName": first_name}
    response = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_COURIER}', data=cls.courier)

@allure.title("Проверка авторизации курьера")
class TestLoginCourier:
    courier = {}

    @allure.description("Статус-код 200 при успешной авторизации")
    def test_login_courier(self):
        response = requests.post(url=f'{urls.BASE_URL}{urls.LOGIN_COURIER}', data=self.courier)
        assert 200 == response.status_code

    @allure.description("Получение ошибки при авторизации без пароля")
    def test_required_fields(self):
        response = requests.post(url=f'{urls.BASE_URL}{urls.LOGIN_COURIER}', data=payload_without_password)
        assert 400 == response.status_code

    @allure.description("Получение ошибки 400 при вводе неправильного пароля")
    def test_wrong_password(self):
        response = requests.post(url=f'{urls.BASE_URL}{urls.LOGIN_COURIER}', data=payload_wrong_password)
        assert 400 == response.status_code

    @allure.description("Получение текста ошибки при авторизации без пароля")
    def test_login_without_password(self):
        response = requests.post(url=f'{urls.BASE_URL}{urls.LOGIN_COURIER}', data=payload_wrong_password_password)
        assert '{"code":400,"message":"Учетная запись не найдена"}' == response.text

    @allure.description("Получение ошибки при попытке авторизации с несуществующей парой логин-пароль")
    def test_wrong_user(self):
        response = requests.post(url=f'{urls.BASE_URL}{urls.LOGIN_COURIER}', data=self.courier)
        assert "Учетная запись не найдена" in response.text

    @allure.description("Проверка наличия ID в теле ответа")
    def test_id_user(self):
        data = {
            "login": "ninja",
            "password": "1234"
        }
        response = requests.post(url=f'{urls.BASE_URL}{urls.LOGIN_COURIER}', json=data)
        assert 200 == response.status_code and "id" in response.json()

    @classmethod
    def teardown_class(cls):
        delete_courier = requests.delete(f'{urls.BASE_URL}{urls.DELETE_COURIER}', data=payload_wrong_password)





