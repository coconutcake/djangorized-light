

import datetime
import time
import os
import socket



def append_to_mainlog(func):
    def wrapper(*args, **kwargs):
        with open("../logs/main.log", "a") as file_object:
            return file_object.write(func(*args,**kwargs))
    return wrapper



def now():
    return datetime.datetime.now().strftime("%d.%m / %H:%M:%S")

@append_to_mainlog
def log(text):
    return f"{now()} # {text}"

@append_to_mainlog
def get_logo():
    return """
+---------------------------------------------------+
|              _ _                                  |
|             | (_)                                 |
|           __| |_  __ _ _ __  _ __                 |
|          / _` | |/ _` | '_ \| '_ \                |
|         | (_| | | (_| | |_) | |_) |               |
|          \__,_| |\__,_| .__/| .__/                |
|              _/ |     | |   | |                   |  
|             |__/      |_|   |_|    by @ignatoma   |
|                                                   |
+---------------------------------------------------+
    """

@append_to_mainlog
def get_table():
    return f"""
+-----------------+---------------------------------+
 container name   | {os.environ.get("DJANGO_CONTAINER_NAME")} 
+-----------------+---------------------------------+
 input port       | {os.environ.get("DJANGO_IPORT")}          
+-----------------+---------------------------------+
 output port      | {os.environ.get("DJANGO_OPORT")}          
+-----------------+---------------------------------+
 language         | {os.environ.get("DJANGO_LANGUAGE_CODE")}  
+-----------------+---------------------------------+
 timezone         | {os.environ.get("DJANGO_TIMEZONE")}       
+-----------------+---------------------------------+
 database engine  | {os.environ.get("DB_ENGINE")}             
+-----------------+---------------------------------+
    """


def is_up(host,port,count,sleep):
    cmd = "ping -c 1 {0}  > /dev/null".format(host)
    print("{0} # Checking host availability... {1}:{2}".format(now(),host,port))
    flag = False
    while flag == False:
        for x in range(count):
            time.sleep(sleep)
            host_up = True if os.system(cmd) == 0 else False
            if host_up:
                flag = True
                break
            else:
                print("{0} # Failed to connect...".format(now()))
    else:
        print("{0} # Host {1}:{2} found!".format(now(),host,port))
    return flag


def isOpen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    is_closed = True

    while is_closed:
        try:
            log(f"Probing host {ip}:{port}...")
            s.connect((ip, int(port)))
            s.shutdown(2)
            log(f"Host {ip}:{port} found!")
            return True
        except:
            log(f"Host {ip}:{port} unavailable. Retrying...")
            time.sleep(1)

def purge_logs():
    log(f"Purgeing logs...")
    os.system("> /logs/main.log && > /logs/access.log 2>&1")

def collect_static():
    log(f"Collecting static...")
    os.system("python3 manage.py collectstatic --noinput >> /logs/main.log 2>&1")

def makemigrations():
    log(f"Preparing migrations...")
    os.system("python3 manage.py makemigrations >> /logs/main.log 2>&1")

def migrate():
    log(f"Performing migration to database...")
    os.system("python3 manage.py migrate >> /logs/main.log 2>&1")

def run_server():
    log(f"Executing server...")
    os.system(f"python3 manage.py runserver 0.0.0.0:{os.environ.get('DJANGO_OPORT')} >> /logs/access.log 2>&1")

if __name__ == "__main__":
    purge_logs()
    log(f"Executing django now: {os.environ.get('DJANGO_CONTAINER_NAME')}")
    log(f"{get_logo()}")
    log(f"{get_table()}")
    collect_static()
    if isOpen(
        ip=os.environ.get("DB_ADDRESS"),
        port=os.environ.get("DB_IPORT")
        ):
        #makemigrations()
        migrate()
        run_server()

