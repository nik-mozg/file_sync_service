# conftest.py
import pytest
from file_sync.file_sync_service import FileSyncService
from unittest.mock import MagicMock

@pytest.fixture
def sync_service():
    """Создает тестовый экземпляр FileSyncService с мок-объектами для uploader и logger."""
    uploader = MagicMock()  # Мок объекта YandexDiskUploader
    logger = MagicMock()    # Мок логгера
    return FileSyncService(local_folder="local_folder", uploader=uploader, logger=logger, sync_mode="files")
