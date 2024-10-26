from unittest.mock import patch, mock_open
import os
import pytest
from cloud_storage.yandex_disk import YandexDiskUploader

TOKEN = "test_token"
CLOUD_FOLDER = "test_cloud_folder"
LOCAL_FOLDER = "local_folder"

@pytest.fixture
def uploader() -> YandexDiskUploader:
    """
    Фикстура для инициализации экземпляра `YandexDiskUploader`.

    Возвращает:
    - YandexDiskUploader: Экземпляр загрузчика для Yandex Disk с тестовым токеном, папкой и локальной директорией.
    """
    return YandexDiskUploader(TOKEN, CLOUD_FOLDER, LOCAL_FOLDER)

def test_create_remote_directory(uploader: YandexDiskUploader) -> None:
    """
    Тестирует создание удаленной директории.

    Эмулирует отсутствие удаленной папки, что вызывает метод `_create_remote_directory`.
    Проверяет, что отправляется запрос на создание удаленной директории.

    Параметры:
    - uploader (YandexDiskUploader): Экземпляр загрузчика для Yandex Disk.

    Возвращает:
    - None: Тест использует `assert` для проверки вызова метода `put`.
    """
    with patch("requests.Session.put") as mock_put, patch("requests.Session.get") as mock_get:
        mock_get.return_value.status_code = 404  # Симуляция отсутствующей папки
        uploader._create_remote_directory("test_cloud_folder/subfolder")

        # Проверка, что был отправлен запрос на создание директории
        assert mock_put.call_count > 0

def test_upload_file(uploader: YandexDiskUploader) -> None:
    """
    Тестирует загрузку файла в удаленную директорию.

    Эмулирует отсутствие удаленной папки и вызывает `_upload_file`, проверяя,
    что запрос `put` отправляется для загрузки файла.

    Параметры:
    - uploader (YandexDiskUploader): Экземпляр загрузчика для Yandex Disk.

    Возвращает:
    - None: Тест использует `assert` для проверки вызова метода `put`.
    """
    with patch("requests.Session.get") as mock_get, patch("requests.Session.put") as mock_put, \
         patch("builtins.open", mock_open(read_data="file content")):
        
        mock_get.return_value.status_code = 404  # Папка не существует
        uploader._upload_file(os.path.join(LOCAL_FOLDER, "test_file.txt"), overwrite=True)

        # Проверка вызова put для загрузки файла
        assert mock_put.call_count > 0
