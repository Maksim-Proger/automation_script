import os
import paramiko
import traceback
from paramiko import util

def sync_to_server(yaml_text: str, server: dict):
    host = server["host"]
    port = server.get("port", 22)
    username = server.get("username")
    key_filename = server.get("key_filename")
    password = server.get("password")
    remote_path = server["remote_path"]

    print("="*40)
    print(f"[INFO] Attempting sync to {host}:{port} as {username}")
    print(f"[INFO] Key file: {key_filename}")
    print(f"[INFO] Exists: {os.path.exists(key_filename)}")
    print(f"[INFO] Password provided: {'Yes' if password else 'No'}")
    print(f"[INFO] Remote path: {remote_path}")
    print("="*40)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    util.log_to_file("paramiko_debug.log")  # Полный лог Paramiko

    try: # Пробуем подключиться к вспомогательным серверам
        if key_filename:
            print("[INFO] Connecting via SSH...")
            ssh.connect(
                hostname=host,
                port=port,
                username=username,
                key_filename=key_filename,
                password=password,
                allow_agent=False,
                look_for_keys=False,
                timeout=10,
                banner_timeout=200
            )
        # elif password:
        #     ssh.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        # else:
        #     ssh.connect(hostname=host, port=port, username=username, timeout=10)
        print("[INFO] SSH connection established")

        print("[INFO] Opening SFTP session...")
        sftp = ssh.open_sftp()
        print("[INFO] SFTP session opened")

        # Проверяем, существует ли нужная директория
        remote_dir = os.path.dirname(remote_path)
        try:
            sftp.stat(remote_dir)
            print(f"[INFO] Remote directory exists: {remote_dir}")
        except IOError:
            print(f"[INFO] Remote directory does not exist, creating: {remote_dir}")
            parts = remote_dir.split("/")
            cur = ""
            for p in parts:
                if not p:
                    continue
                cur += "/" + p
                try:
                    sftp.stat(cur)
                except IOError:
                    print(f"[INFO] Creating directory: {cur}")
                    sftp.mkdir(cur)

        # Обновляем файл на вспомогательном сервере
        print(f"[INFO] Writing to remote file: {remote_path}")
        with sftp.file(remote_path, "w") as remote_file:
            remote_file.write(yaml_text.encode("utf-8"))
            remote_file.flush()
        print("[INFO] File written successfully")

        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"[ERROR] SSH connection failed to {host}: {e}")
        traceback.print_exc()
        try:
            ssh.close()
        except paramiko.SSHException:
            pass
        raise e
