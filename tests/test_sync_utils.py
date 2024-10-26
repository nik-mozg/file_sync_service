import os
import ctypes
from file_sync.sync_utils import is_hidden

def test_is_hidden() -> None:
    """
    Тестирует функцию `is_hidden` для определения скрытых файлов.

    Тест проверяет:
    - Создание скрытого файла и его определение как скрытого через `is_hidden`.
    - На платформе Windows устанавливается атрибут "Скрытый" для файла.
    - Очищает файл после проверки, снимая атрибуты и удаляя его.

    Возвращает:
    - None: Функция теста не возвращает значения, а использует `assert` для проверки результатов.
    """
    hidden_file = ".hidden_file"
    open(hidden_file, 'w').close()

    # Устанавливаем атрибут "Скрытый" в Windows
    if os.name == 'nt':
        ctypes.windll.kernel32.SetFileAttributesW(hidden_file, 0x02)
    
    # Проверка, что скрытый файл определяется корректно
    assert is_hidden(hidden_file) is True

    # Очистка
    if os.name == 'nt':
        ctypes.windll.kernel32.SetFileAttributesW(hidden_file, 0x80)  # Снимаем скрытие
    os.remove(hidden_file)
