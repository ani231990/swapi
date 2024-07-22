import requests
from pathlib import Path


class APIRequester:
    """Родительский класс APIRequester для обработки сетевого запроса.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url=''):
        """Метод для выполнения сетевого запроса,
        а также обработки возможных ошибок.
        """
        full_url = f'{self.base_url}{url}'
        try:
            # Выполняем запрос, получаем объект класса Response.
            response = requests.get(full_url)
            # Вызываем ошибку HTTPError, если код ответа неуспешный.
            response.raise_for_status()
        # Обработка ошибки HTTPError
        except requests.HTTPError:
            print('При обработке запроса возникла ошибка HTTPError.')
            return None
        # Обработка сетевой ошибки
        except requests.ConnectionError:
            print('При обработке запроса возникла сетевая ошибка.')
            return None
        # Обрабатка других ошибок при выполнении запроса.
        except requests.RequestException:
            print('Возникла ошибка при выполнении запроса')
            return None
        else:
            return response


class SWRequester(APIRequester):
    """Унаследованный от APIRequester класс SWRequester.
    Класс имеет 2 дополнительных метода:
    get_sw_categories и get_sw_info.
    """

    def get_sw_categories(self):
        """Метод выводит список доступных категорий сайта SWAPI.
        """
        response = self.get('/')
        if isinstance(response, requests.models.Response):
            return response.json().keys()
        else:
            print('Доступные категории отсутствуют. '
                  'Убедитесь, что сайт работает корректно.'
                  )
            return None

    def get_sw_info(self, sw_type):
        """Метод выполняет запрос вида: https://swapi.dev/api/<имя категории>/
        и возвращает весь полученный ответ в виде строки.
        """
        url = f'/{sw_type}/'
        response = self.get(url)
        if isinstance(response, requests.models.Response):
            return response.text
        else:
            print('Информация о выбранной категории отсутствует. '
                  'Убедитесь, что сайт работает корректно.'
                  )
            return None


def save_sw_data():
    """Функция создает директорию data.
    В директории создаются файлы data/<категория>.txt с данными
    по каждой категории сайта SWAPI.
    """
    Path("data").mkdir(exist_ok=True)
    url = 'https://swapi.dev/api'
    swapi = SWRequester(url)
    categories_swapi = swapi.get_sw_categories()
    for category in categories_swapi:
        category_info = swapi.get_sw_info(category)
        file_name = f'data/{category}.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(category_info)


if __name__ == '__main__':
    save_sw_data()
