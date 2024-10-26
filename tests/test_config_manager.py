from configparser import ConfigParser
from unittest.mock import patch, MagicMock
from file_sync.config_manager import ConfigManager

@patch.object(ConfigParser, 'read')
@patch.object(ConfigParser, 'get', side_effect=lambda section, option, fallback=None: option)
@patch.object(ConfigParser, 'getint', return_value=30)
def test_load_config(mock_get: MagicMock, mock_getint: MagicMock, mock_read: MagicMock) -> None:
    """
    Тестирует функцию загрузки конфигурации `ConfigManager.load_config`, проверяя корректность возвращаемых значений.
    
    Тест проверяет, что:
    - Параметр `local_folder` установлен как 'local_folder'.
    - Параметр `sync_period` установлен как 30.
    - Параметр `log_file` установлен как 'log_file'.

    Параметры:
    - mock_get (MagicMock): Мок-объект для `ConfigParser.get`.
    - mock_getint (MagicMock): Мок-объект для `ConfigParser.getint`.
    - mock_read (MagicMock): Мок-объект для `ConfigParser.read`.

    Возвращаемое значение:
    - None: Функция теста не возвращает значений, она использует assert для проверки ожидаемого результата.
    """
    config = ConfigManager.load_config("config.ini")
    assert config['local_folder'] == 'local_folder'
    assert config['sync_period'] == 30
    assert config['log_file'] == 'log_file'
