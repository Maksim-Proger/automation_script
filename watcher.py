import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sync import sync_to_server
from config import WATCH_DIR, WATCH_FILENAME, SERVERS, DEBOUNCE_SECONDS

class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, watch_file):
        self.watch_file = os.path.abspath(os.path.join(WATCH_DIR, watch_file))
        self._last_sync_time = 0.0

    def _should_handle(self):
        now = time.time()
        if now - self._last_sync_time < DEBOUNCE_SECONDS:
            return False
        self._last_sync_time = now
        return True

    def handle_change(self):
        try:
            with open(self.watch_file, "r", encoding="utf-8") as f:
                yaml_text = f.read()  # Сохраняем файл в строке
        except Exception as e:
            print("Тут у нас будет лог с ошибкой (Файл прочитать не удалось)")
            return

        print("Тут у нас будет лог (Файл прочитать удалось)")

        # Подключаемся к серверам и обновляем файлы
        for srv in SERVERS:
            try:
                sync_to_server(yaml_text, srv)
                print("Лог об успешной операции")
            except Exception as e:
                print(f"Лог об неуспешной операции: {e}")

    # Наши обработчики (изменение файла в каталоге)
    def on_modified(self, event):
        if os.path.abspath(event.src_path) != self.watch_file:
            return
        if not self._should_handle():
            return
        self.handle_change()

    def on_moved(self, event):
        dest = getattr(event, "dest_path", None)
        if dest and os.path.abspath(dest) == self.watch_file:
            if not self._should_handle():
                return
            self.handle_change()

    def on_created(self, event):
        if os.path.abspath(event.src_path) == self.watch_file:
            if not self._should_handle():
                return
            self.handle_change()

def start_watcher(): # создаем и запускаем наблюдатель
    event_handler = ConfigChangeHandler(WATCH_FILENAME)
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
