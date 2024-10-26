import os
import concurrent.futures
from file_sync.sync_utils import get_local_files_info
import logging


class FileSyncService:
    def __init__(self, local_folder: str, uploader, logger: logging.Logger, sync_mode: str = "files", max_workers: int = 10) -> None:
        """
        Инициализирует сервис синхронизации файлов с указанными параметрами.

        Параметры:
        - local_folder (str): Путь к локальной папке для синхронизации.
        - uploader: Объект, представляющий облачное хранилище, с методами для загрузки, обновления и удаления файлов.
        - logger (logging.Logger): Логгер для записи событий и ошибок.
        - sync_mode (str): Режим синхронизации; "files" для синхронизации только файлов, "all" для файлов и папок.
        - max_workers (int): Максимальное количество потоков для многопоточности.
        """
        self.local_folder = local_folder
        self.uploader = uploader
        self.logger = logger
        self.sync_mode = sync_mode
        self.max_workers = max_workers  # Количество потоков для многопоточности


    def run_sync_cycle(self) -> None:
        """
        Запускает цикл синхронизации файлов и записывает результаты в лог.
        В случае ошибки записывает сообщение об ошибке и продолжает работу.
        """
        self.logger.info("Запуск цикла синхронизации")
        try:
            self.synchronize_files()
        except Exception as e:
            self.logger.error(f"Общая ошибка при синхронизации: {e}", exc_info=True)


    def synchronize_files(self) -> None:
        """
        Выполняет синхронизацию файлов между локальной папкой и облачным хранилищем.
        
        Метод использует многопоточность для параллельной загрузки, обновления и удаления файлов.
        Ожидает завершения всех задач и обрабатывает результаты, записывая ошибки при возникновении исключений.
        """
        # Получаем информацию о файлах в облаке
        cloud_files = self.uploader.get_info()
        
        # Получаем информацию о локальных файлах и папках в зависимости от sync_mode
        local_files = get_local_files_info(self.local_folder, self.sync_mode)

        # Создаем пул потоков для загрузки и удаления файлов
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []

            # Добавляем задачи на загрузку и обновление файлов
            for filename, local_mtime in local_files.items():
                if filename in cloud_files:
                    cloud_mtime = cloud_files[filename]
                    if local_mtime == cloud_mtime:
                        continue  # Пропускаем файл, если он не изменился

                    # Обновляем измененные файлы
                    self.logger.info(f"Файл {filename} обновляется в облаке.")
                    futures.append(executor.submit(self.uploader.reload, os.path.join(self.local_folder, filename)))
                else:
                    # Загружаем новый файл
                    self.logger.info(f"Новый файл {filename} загружается в облако.")
                    futures.append(executor.submit(self.uploader.load, os.path.join(self.local_folder, filename)))

            # Добавляем задачи на удаление файлов, отсутствующих локально
            for filename in cloud_files:
                if filename not in local_files:
                    self.logger.info(f"Файл {filename} удаляется из облака.")
                    futures.append(executor.submit(self.uploader.delete, filename))

            # Ожидаем завершения всех задач и обрабатываем результаты
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # Получаем результат задачи и обрабатываем исключения, если есть
                except Exception as e:
                    self.logger.error(f"Ошибка при выполнении задачи: {e}", exc_info=True)
