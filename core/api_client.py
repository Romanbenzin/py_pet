import allure
import json
import logging
import requests
import requests_to_curl
from requests.exceptions import RequestException


logger = logging.getLogger(__name__)


class ApiClient():
    """Клиент для работы с API."""

    def __init__(self, base_address):
        """Инициализация клиента с базовым адресом API."""
        self.base_address = base_address

    def _request(self, method, path="/", **kwargs):
        url = f"{self.base_address}{path}"
        with allure.step(f"Выполняем {method.upper()} запрос на: {url}"):
            try:
                response = requests.request(method,
                                            url,
                                            timeout=10,
                                            **kwargs)
                ApiClient.log_request_response(response)
                # response.raise_for_status()
                return response
            except RequestException as e:
                logger.error(f"Request failed: {e}")
                raise

    def post(self, path="/", params=None, data=None, json=None, headers=None):
        return self._request("POST",
                             path,
                             params=params,
                             data=data,
                             json=json,
                             headers=headers)

    def get(self, path="/", params=None, headers=None):
        return self._request("GET",
                             path,
                             params=params,
                             headers=headers)

    @staticmethod
    def log_request_response(resp):
        curl = requests_to_curl.parse(resp.request,
                                      return_it=True,
                                      print_it=False)
        pretty_curl = (curl.replace(" -H ", " \\\n-H ")
                       .replace(" -d ", " \\\n-d "))
        try:
            response = (
                f"\n{json.dumps(resp.json(), indent=4, ensure_ascii=False)}"
                )
        except requests.exceptions.JSONDecodeError:
            response = resp.text
        logger.info(f"Send request: \n{pretty_curl}")
        logger.info(f"Response status: {resp.status_code}")
        logger.info(f"Response body: {response}")
        with allure.step("Request"):
            allure.attach(
                    pretty_curl,
                    name="Request curl",
                    attachment_type=allure.attachment_type.TEXT,
                )
        with allure.step(f"Response status: {resp.status_code}"):
            allure.attach(
                response,
                name="Response body",
                attachment_type=allure.attachment_type.TEXT,
            )
