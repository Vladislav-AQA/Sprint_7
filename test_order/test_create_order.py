import allure
import pytest
import urls
import requests


@allure.title("Проверка создания заказа")
class TestCreateOrder:

    @pytest.mark.parametrize('colour', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []])
    @allure.description("Проверка выбора цветов и наличие 'track' в теле ответа")
    def test_create_order(self, colour):
        data = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "Saske, come back to Konoha",
                "color": colour
        }
        response = requests.post(url=f'{urls.BASE_URL}{urls.CREATE_ORDER}', json=data)
        assert 201 == response.status_code and 'track' in response.json()

@allure.title("Проверка возврата списка заказов")
class TestReceiveListOrder:

    @allure.description("Список заказов курьера по 'id'")
    def test_receive_list_order(self):
        response = requests.get(url=f'{urls.BASE_URL}{urls.ORDER_LIST}/12345')
        assert 200 == response.status_code

