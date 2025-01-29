import allure
import logging
import random
import pytest

from core.assertions import Assertions
from core.constants import STATUS_INT_SER_ERROR, STATUS_OK


logger = logging.getLogger(__name__)


@allure.description("Проверка получения ингредиентов")
@allure.title("Проверка успешности получения ингредиентов")
def test_get_ingredients_page(base_api):
    response = base_api.get(path="ingredients")
    Assertions.assert_that_value_is_equal_to('ingredients_response',
                                             response.status_code,
                                             STATUS_OK)


@allure.description("Проверка получения статуса ответа ingredients")
@allure.title("Проверка получения 'success'")
def test_get_success_ingredients_response(base_api):
    response = base_api.get(path="ingredients")
    Assertions.assert_that_value_is_equal_to(
        't', response.json()['success'], True
        )


@pytest.mark.parametrize("name, email, password, status_code",
                         (
                            ('qwes',
                             f'qew{random.randint(1, 1000)}@qwe.ryd',
                             'qew@qwe.ryf',
                             STATUS_OK),
                            ('qwe2',
                             'qew@',
                             'qew@qwe.ry',
                             STATUS_INT_SER_ERROR)
                         ))
@allure.description("Проверка регистрации юзера")
@allure.title("Проверка успешности регистрации пользователя")
def test_to_register(base_api, name, email, password, status_code):
    json_data = {
        'name': name,
        'email': email,
        'password': password,
        }
    response = base_api.post(path="auth/register",
                             json=json_data)
    Assertions.assert_that_value_is_equal_to('status_code',
                                             response.status_code,
                                             status_code)
