import logging
from logging import Logger

def setup_logger(log_file: str) -> Logger:
    """
    Настраивает и возвращает логгер для синхронизации файлов.

    Параметры:
    log_file (str): Путь к файлу, в который будут записываться логи.

    Возвращаемое значение:
    Logger: Настроенный экземпляр логгера для записи событий.

    Настройки:
    - Уровень логирования установлен на INFO, чтобы фиксировать важные события.
    - Формат логов: дата и время, уровень сообщения и само сообщение.
    - Кодировка файла лога — UTF-8.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,  
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8"
    )
    return logging.getLogger("synchronizer")
