
# Папка и файл для наблюдения
WATCH_DIR = "/home/vboxuser/ymalfiles"
WATCH_FILENAME = "config.yaml"

# Дебаунс
DEBOUNCE_SECONDS = 1.5

# Настройки вспомогательных серверов
SERVERS = [
    {
        "host": "192.168.56.102",
        "port": 22,
        "username": "vboxuser",
        "key_filename": "/home/vboxuser/.ssh/id_ed25519",
        "remote_path": "/home/vboxuser/ymalfiles"
    }
]
