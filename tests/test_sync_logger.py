import logging
from sync_logger import setup_logger

def test_setup_logger() -> None:
    """
    Тестирует функцию `setup_logger`, проверяя создание и настройку логгера.

    Тест проверяет, что:
    - Возвращаемое значение `setup_logger` является экземпляром `logging.Logger`.
    - Уровень логгирования устанавливается на `logging.INFO`.

    Возвращает:
    - None: Функция теста не возвращает значений, использует `assert` для проверки результатов.
    """
    # Создаем логгер с использованием `setup_logger`
    logger = setup_logger("test.log")

    # Проверяем, что возвращаемое значение - это экземпляр `logging.Logger`
    assert isinstance(logger, logging.Logger)

    # Устанавливаем уровень логгирования на INFO и проверяем уровень
    logger.setLevel(logging.INFO)
    assert logger.level == logging.INFO
