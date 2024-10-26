from configparser import ConfigParser
from typing import Dict, Union

class ConfigManager:
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Union[str, int]]:
        """
        Загружает конфигурацию из указанного файла и возвращает ее в виде словаря.

        Параметры:
        - config_path (str): Путь к файлу конфигурации.

        Возвращаемое значение:
        - dict: Словарь с параметрами конфигурации, включающий следующие ключи:
            - 'local_folder' (str): Путь к локальной папке для синхронизации.
            - 'cloud_folder_name' (str): Имя папки в облачном хранилище для резервных копий.
            - 'access_token' (str): Токен доступа для работы с API облачного хранилища.
            - 'sync_period' (int): Период синхронизации в секундах.
            - 'log_file' (str): Путь к файлу для логирования.
            - 'sync_mode' (str): Режим синхронизации, по умолчанию "files".
        """
        config = ConfigParser()
        config.read(config_path, encoding="utf-8")
        return {
            'local_folder': config.get("settings", "local_folder"),
            'cloud_folder_name': config.get("settings", "cloud_folder_name"),
            'access_token': config.get("settings", "access_token"),
            'sync_period': config.getint("settings", "sync_period"),
            'log_file': config.get("settings", "log_file"),
            'sync_mode': config.get("settings", "sync_mode", fallback="files")  # добавили sync_mode
        }
