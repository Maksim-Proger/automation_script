
# Папка и файл для наблюдения
WATCH_DIR = "etc/myapp/"
WATCH_FILENAME = "config.yaml"

# Дебаунс
DEBOUNCE_SECONDS = 1.5

# Настройки вспомогательных серверов
SERVERS = [
    {
        "host": "192.168.56.102",
        "port": 22,
        "username": "vboxuser",
        "key_filename": "/home/vboxuser/.ssh/vm2",
        "remote_path": "etc/myapp/"
    },
    # {
    #     "host": "192.168.0.102",
    #     "port": 22,
    #     "username": "имя пользователя на вспомогательном сервере",
    #     "key_filename": "путь к SSH-ключу",
    #     "remote_path": "адрес файла на вспомогательном сервере"
    # }
]
