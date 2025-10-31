from datetime import datetime
from pathlib import Path
from time import sleep
import requests as rq
import hashlib
import os


def ClientAPIKey():
    folder_path = Path(f'C:/Users/{os.getlogin()}')
    creation_time = folder_path.stat().st_ctime
    creation_time_readable = datetime.fromtimestamp(creation_time)

    def sha256_hash(data):
        data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    hashed_data = sha256_hash(str(creation_time_readable))
    return hashed_data

def Keys():
    keys = rq.get("https://raw.githubusercontent.com/Divy0The0Fire/J4E/main/keys").text.strip()
    keys.splitlines()
    return keys

Key = ClientAPIKey()


if Key not in Keys():
    print("")
    print("------------------------------------------------------------------------------------")
    print("")
    print("Your AI Assistant is not activated, Kindly contact us to activate it.")
    print("Our Instagram : @Jarvis4everyone")
    print(f"Activation Key : {Key}")
    print("")
    print("------------------------------------------------------------------------------------")
    print("")
    sleep(1000)
    exit()

else:
    print("")
    print("------------------------------------------------------------------------------------")
    print("")
    print("Your AI Assistant is activated, Enjoy your time.")
    print("")
    print("------------------------------------------------------------------------------------")
    print("")
    sleep(1000)