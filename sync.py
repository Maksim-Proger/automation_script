import os
import paramiko

def sync_to_server(yaml_text: str, server: dict):
    host = server["host"]
    port = server.get("port", 22)
    username = server.get("username")
    key_filename = server.get("key_filename")
    password = server.get("password")
    remote_path = server["remote_path"]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try: # Пробуем подключиться к вспомогательным серверам
        if key_filename:
            ssh.connect(hostname=host, port=port, username=username, key_filename=key_filename, timeout=10)
        elif password:
            ssh.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        else:
            ssh.connect(hostname=host, port=port, username=username, timeout=10)

        sftp = ssh.open_sftp()

        # Проверяем, существует ли нужная директория
        remote_dir = os.path.dirname(remote_path)
        try:
            sftp.stat(remote_dir)
        except IOError:
            parts = remote_dir.split("/")
            cur = ""
            for p in parts:
                if not p:
                    continue
                cur += "/" + p
                try:
                    sftp.stat(cur)
                except IOError:
                    sftp.mkdir(cur)

        # Обновляем файл на вспомогательном сервере
        with sftp.file(remote_path, "w") as remote_file:
            remote_file.write(yaml_text.encode("utf-8"))
            remote_file.flush()

        sftp.close()
        ssh.close()

    except Exception as e:
        try:
            ssh.close()
        except paramiko.SSHException:
            pass
        raise e
