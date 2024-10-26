import os
import stat
from typing import Dict, Optional, Set


def get_local_files_info(
    folder_path: str, sync_mode: str = "files", ignore_dirs: Optional[Set[str]] = None
) -> Dict[str, float]:
    """
    Получает информацию о файлах в локальной папке и возвращает словарь с именами файлов и временем их последнего изменения.

    Параметры:
    - folder_path (str): Путь к локальной папке для сканирования.
    - sync_mode (str): Режим синхронизации; "files" для файлов, "all" для файлов и папок.
    - ignore_dirs (Optional[Set[str]]): Множество имен директорий, которые нужно игнорировать (по умолчанию включает .git, .vscode, __pycache__).

    Возвращает:
    - Dict[str, float]: Словарь, где ключи — относительные пути к файлам, а значения — время последнего изменения в формате Unix.
    """
    if ignore_dirs is None:
        ignore_dirs = {".git", ".vscode", "__pycache__"}  # Добавьте любые другие игнорируемые папки

    files_info = {}

    for root, dirs, files in os.walk(folder_path):
        # Исключаем игнорируемые директории
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not is_hidden(os.path.join(root, d))]

        for f in files:
            file_path = os.path.join(root, f)
            if f.startswith('.') or is_hidden(file_path):
                continue  # Пропускаем скрытые файлы и папки
            files_info[file_path.replace(folder_path + os.sep, "")] = os.path.getmtime(file_path)

    return files_info


def is_hidden(filepath: str) -> bool:
    """
    Определяет, является ли файл или папка скрытыми или системными.

    Параметры:
    - filepath (str): Путь к файлу или папке.

    Возвращает:
    - bool: True, если файл или папка скрытые или системные; False в противном случае.
    """
    return bool(os.stat(filepath).st_file_attributes & (stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_SYSTEM))
