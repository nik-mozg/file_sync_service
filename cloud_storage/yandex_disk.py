import threading
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from typing import Dict


class YandexDiskUploader:
    def __init__(self, token: str, cloud_folder: str, local_folder: str) -> None:
        """
        Инициализирует загрузчик для работы с Яндекс.Диском.

        :param token: OAuth-токен для доступа к Яндекс.Диску.
        :param cloud_folder: Путь к папке в облаке для хранения резервных копий.
        :param local_folder: Путь к локальной папке для синхронизации.
        """
        self.token = token
        self.cloud_folder = cloud_folder
        self.local_folder = local_folder
        self.headers = {"Authorization": f"OAuth {self.token}"}
        
        # Настройка сессии с повторными попытками при ошибках подключения
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        # Блокировка для исключения конфликта при создании папок
        self.folder_lock = threading.Lock()


    def get_info(self) -> Dict[str, str]:
        """
        Получает информацию о файлах, хранящихся в облаке.

        :return: Словарь с именами файлов в облаке и временем их последнего изменения.
        """
        url = f"https://cloud-api.yandex.net/v1/disk/resources?path={self.cloud_folder}"
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            items = response.json().get('_embedded', {}).get('items', [])
            return {item['name']: item['modified'] for item in items}
        except requests.RequestException as e:
            print(f"Ошибка при подключении к Яндекс.Диску: {e}")
            return {}


    def load(self, path: str) -> None:
        """
        Загружает новый файл в облако.

        :param path: Путь к файлу, который нужно загрузить.
        """
        self._upload_file(path, overwrite=False)

    def reload(self, path: str) -> None:
        """
        Перезаписывает существующий файл в облаке.

        :param path: Путь к файлу, который нужно перезаписать.
        """
        self._upload_file(path, overwrite=True)


    def delete(self, filename: str) -> None:
        """
        Удаляет файл из облака.

        :param filename: Имя файла для удаления.
        """
        url = f"https://cloud-api.yandex.net/v1/disk/resources?path={self.cloud_folder}/{filename}"
        try:
            response = self.session.delete(url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при удалении файла {filename} из облака: {e}")


    def _upload_file(self, path: str, overwrite: bool) -> None:
        """
        Загружает файл в облако. Создает все вложенные папки, если они отсутствуют.

        :param path: Путь к файлу, который нужно загрузить.
        :param overwrite: Флаг, указывающий, нужно ли перезаписывать файл, если он уже существует.
        """
        relative_path = os.path.relpath(path, start=self.local_folder).replace("\\", "/")
        upload_path = f"{self.cloud_folder}/{relative_path}"
        parent_folder = "/".join(upload_path.split("/")[:-1])

        # Создаем поддиректории, если они отсутствуют
        self._create_remote_directory(parent_folder)

        check_url = f"https://cloud-api.yandex.net/v1/disk/resources?path={upload_path}"
        try:
            response = self.session.get(check_url, headers=self.headers)
            if response.status_code == 200 and not overwrite:
                print(f"Файл {upload_path} уже существует и не будет перезаписан.")
                return
            elif response.status_code == 404 or (response.status_code == 200 and overwrite):
                url = f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={upload_path}&overwrite={str(overwrite).lower()}"
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                upload_url = response.json()["href"]
                with open(path, "rb") as file:
                    response = self.session.put(upload_url, files={"file": file})
                    response.raise_for_status()
                    print(f"Файл {upload_path} успешно загружен.")
        except requests.RequestException as e:
            print(f"Ошибка при загрузке файла {path}: {e}")
    
    
    def _create_remote_directory(self, path: str) -> None:
        """
        Рекурсивно создает все вложенные папки на Яндекс.Диске с блокировкой для многопоточности.

        :param path: Путь к папке, которую нужно создать в облаке.
        """
        parts = path.split("/")
        for i in range(1, len(parts) + 1):
            sub_path = "/".join(parts[:i])
            url = f"https://cloud-api.yandex.net/v1/disk/resources?path={sub_path}"

            # Блокируем доступ для проверки и создания папки
            with self.folder_lock:
                try:
                    response = self.session.get(url, headers=self.headers)
                    if response.status_code == 200:
                        continue  # Папка существует
                    elif response.status_code == 404:
                        # Папка не существует, создаем её
                        response = self.session.put(url, headers=self.headers)
                        response.raise_for_status()
                        print(f"Папка {sub_path} успешно создана.")
                    elif response.status_code == 409:
                        # Папка уже существует, конфликт устранен
                        print(f"Папка {sub_path} уже существует.")
                        continue
                except requests.RequestException as e:
                    print(f"Ошибка при создании директории {sub_path}: {e}")
                    break
