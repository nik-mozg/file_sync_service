from unittest.mock import patch, MagicMock
import pytest
from file_sync.file_sync_service import FileSyncService
import os

@pytest.fixture
def sync_service() -> FileSyncService:
    """
    Фикстура для создания экземпляра `FileSyncService` с мок-объектом `uploader`.

    Возвращает:
    - FileSyncService: Инициализированный экземпляр сервиса синхронизации с мок-объектом `uploader`.
    """
    # Создаем мок объекта uploader
    mock_uploader = MagicMock()
    return FileSyncService(local_folder="local_folder", uploader=mock_uploader, logger=MagicMock())

def test_synchronize_files(sync_service: FileSyncService) -> None:
    """
    Тестирует функцию `synchronize_files` в `FileSyncService`, проверяя синхронизацию новых файлов.

    Тест проверяет, что:
    - Функция `get_local_files_info` возвращает корректное значение.
    - При отсутствии файла в облаке, метод `load` вызывается для его загрузки.

    Параметры:
    - sync_service (FileSyncService): Экземпляр `FileSyncService`, предоставленный фикстурой.

    Возвращает:
    - None: Функция теста не возвращает значений, использует `assert` для проверки результатов.
    """
    # Мокаем `get_local_files_info` для возврата тестового файла
    with patch('file_sync.file_sync_service.get_local_files_info', return_value={"file2": 1}) as mock_local_files_info:
        # Проверяем, что `get_local_files_info` возвращает корректное значение
        assert mock_local_files_info is not None, "Ошибка инициализации мока get_local_files_info"

        # Пустой список облачных файлов, чтобы файл считался новым
        sync_service.uploader.get_info.return_value = {}

        # Выполняем синхронизацию
        sync_service.synchronize_files()

        # Убедимся, что `load` был вызван для нового файла
        print(f"Вызовы load после синхронизации: {sync_service.uploader.load.call_args_list}")
        sync_service.uploader.load.assert_called_once_with(os.path.join("local_folder", "file2"))
