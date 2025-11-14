from watcher import start_watcher

if __name__ == "__main__":
    start_watcher()

# import paramiko
#
# def test_ssh_connection():
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#     host = "192.168.0.101"
#     port = 22
#     username = "ubuntu"
#     key_filename = "/home/vboxuser/.ssh/id_ed25519"
#
#     try:
#         # Подключаемся к серверу
#         ssh.connect(
#             hostname=host,
#             port=port,
#             username=username,
#             key_filename=key_filename,
#             allow_agent=False,
#             look_for_keys=False,
#             timeout=10
#         )
#
#         # Выполняем простую команду для проверки
#         stdin, stdout, stderr = ssh.exec_command("echo connected")
#         print(stdout.read().decode().strip())
#
#         ssh.close()
#     except Exception as e:
#         print("ERROR:", e)
#         import traceback
#         traceback.print_exc()
#
#
# if __name__ == "__main__":
#     test_ssh_connection()