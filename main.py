import time
from file_sync.config_manager import ConfigManager
from sync_logger import setup_logger
from file_sync.file_sync_service import FileSyncService
from cloud_storage.yandex_disk import YandexDiskUploader


def main() -> None:
    """
    Основная функция программы для настройки конфигурации, логгера,
    создания экземпляра загрузчика и запуска цикла синхронизации.

    Функция выполняет следующие шаги:
    1. Загружает конфигурацию из config.ini с помощью ConfigManager.
    2. Настраивает логгер, используя указанный файл лога.
    3. Создает экземпляр YandexDiskUploader с параметрами конфигурации.
    4. Создает и запускает сервис синхронизации файлов в заданном цикле.

    Исключения, возникающие при синхронизации, логируются и не прерывают работу программы.
    """
    # Настройка конфигурации и логгера
    config = ConfigManager.load_config("config.ini")
    logger = setup_logger(config['log_file'])
    
    # Создание экземпляра YandexDiskUploader с передачей local_folder
    uploader = YandexDiskUploader(config['access_token'], config['cloud_folder_name'], config['local_folder'])

    # Создание и запуск сервиса синхронизации с учетом sync_mode
    sync_service = FileSyncService(
        config['local_folder'],
        uploader,
        logger,
        sync_mode=config.get('sync_mode', 'files')
    )
    
    # Запуск цикла синхронизации
    while True:
        try:
            sync_service.run_sync_cycle()
        except Exception as e:
            logger.error(f"Ошибка при синхронизации: {e}")
        time.sleep(config['sync_period'])




if __name__ == "__main__":
    main()
