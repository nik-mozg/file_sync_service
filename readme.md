# File Sync Service

**File Sync Service** – это приложение на Python для синхронизации файлов между локальной папкой и облачным хранилищем, реализованным через API Yandex Disk. Приложение поддерживает создание удаленных папок, загрузку новых файлов и обновление измененных файлов с использованием многопоточности.

**Требования**

Python 3.7 или выше

_Зависимости (указаны в requirements.txt):_
requests
pytest (для тестирования)
pytest-cov (для покрытия тестов)
requests-mock (для тестирования)
configparser (для тестирования)

**Установка**

Клонируйте репозиторий:

```
git clone https://github.com/username/file-sync-service.git
cd file-sync-service
```

Установите зависимости:

```
pip install -r requirements.txt
```

**Настройка**

Перед запуском приложения настройте файл config.ini с указанием основных параметров. Пример конфигурационного файла:

```
[settings]
local_folder = /path/to/local/folder
cloud_folder = /path/to/cloud/folder
sync_period = 30
log_file = sync.log
access_token = your_yandex_disk_api_token
sync_mode = all
```

_Параметры:_

```
local_folder: путь к локальной папке, откуда файлы будут синхронизироваться.
cloud_folder: путь к папке на Yandex Disk, где файлы будут храниться.
sync_period: период времени в секундах между циклами синхронизации.
log_file: файл для записи логов приложения.
access_token: токен доступа к API Yandex Disk.
sync_mode: Определяет, что синхронизировать: "files" — только файлы, "all" — файлы и папки внутри local_folder
```

**Запуск**

Запустите приложение с помощью следующей команды:

```
python main.py
```

**Тестирование**

Для запуска тестов и проверки покрытия используйте команды:

```
pytest tests/
```

**Запуск тестов с покрытием**

```
pytest --cov=.
```

**Структура проекта**

```
file-sync-service/
├── cloud_storage/
│   └── yandex_disk.py        # Класс YandexDiskUploader для работы с Yandex Disk API
├── file_sync/
│   ├── file_sync_service.py  # Основной класс FileSyncService для синхронизации файлов
│   ├── config_manager.py     # Загрузка конфигурации из config.ini
│   └── sync_utils.py         # Утилиты для работы с файлами
├── tests/
│   ├── test_config_manager.py
│   ├── test_file_sync_service.py
│   ├── test_sync_logger.py
│   ├── test_sync_utils.py
│   └── test_yandex_disk_uploader.py
├── config.ini                # Конфигурационный файл
├── main.py                   # Главный файл для запуска приложения
└── README.md                 # Документация проекта
```

**Лицензия**

Этот проект лицензируется под лицензией MIT.

_Примечание:_ Приложение синхронизации разработано с учетом многопоточности и требует токена Yandex Disk API для работы с облачным хранилищем.
