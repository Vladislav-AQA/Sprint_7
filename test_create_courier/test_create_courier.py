import allure
import urls
import requests
from faker import Faker


fake = Faker(locale="ru_RU")


payload = {
    "login": "ninja",
    "password": "1234",
    "firstName": "saske"
}

payload_without_password = {
    "login": "ninja",
    "firstName": "saske"
}


@allure.title("Проверка успешного создания курьера")
class TestSuccessCreateCourier:

    courier = {}
    @classmethod
    def setup_class(cls):
        login = fake.email()
        password = fake.password()
        first_name = fake.first_name()
        cls.courier = {"login": login, "password": password, "firstName": first_name}

    @allure.description("Проверка получения статус-кода 201 при создании курьера")
    def test_success_create_courier(self):
        response = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_COURIER}', data=self.courier)
        assert 201 == response.status_code


    @allure.title("Проверка сценария создания двух одинаковых курьеров")
    class TestSameLogin:

        @allure.description("Получение статус-кодапопытке создать аналогичного курьера")
        def test_same_login(self):
            response = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_COURIER}', data=payload)
            assert 409 == response.status_code

    @allure.title("Проверка сценария создания курьера без обязательного поля")
    class TestRequirementFields:

        @allure.description("Получение статус-кода 400 Bad Request без использования обязательных полей")
        def test_requirement_fields(self):
            response = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_COURIER}', data=payload_without_password)
            assert 400 == response.status_code

    @allure.title("Проверка возврата правильного кода-ответа")
    class TestResponseText:

        @allure.description("Запрос возвращает '{ok:true}'")
        def test_response_text(self):
            response = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_COURIER}', data=self.courier)
            assert '{"ok":true}' == response.text

    @allure.title("Проверка наличия ошибки, если нет одного из полей")
    class TestErrorCreate:

        @allure.description("Получение кода и текста ошибки при попытке создать курьера без пароля")
        def test_error_create(self):
            response = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_COURIER}', data=payload_without_password)
            assert '{"code":400,"message":"Недостаточно данных для создания учетной записи"}' == response.text

    @allure.title("Создание курьера с уже занятым логином")
    class TestSameLogin:

        @allure.description("Получение статус-кода и сообщения при попытке создать аналогичного курьера")
        def test_same_login(self):
            response = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_COURIER}', json=payload)
            assert '{"code":409,"message":"Этот логин уже используется. Попробуйте другой."}' in response.text

    @classmethod
    def teardown_class(cls):
        cls.courier = requests.delete(f'{urls.BASE_URL}{urls.DELETE_COURIER}', data=cls.courier)
