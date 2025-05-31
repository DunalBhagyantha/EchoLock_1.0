import os, bcrypt
from getpass import getpass

USER_DB = "data/users.db"

def register(username: str, password: str):
    os.makedirs(os.path.dirname(USER_DB), exist_ok=True)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open(USER_DB, "a") as f:
        f.write(f"{username}:{hashed.decode()}\n")

def login(username: str, password: str) -> bool:
    if not os.path.exists(USER_DB):
        return False
    with open(USER_DB) as f:
        for line in f:
            user, phash = line.strip().split(":",1)
            if user == username and bcrypt.checkpw(password.encode(), phash.encode()):
                return True
    return False


def prompt_login():
    while True:
        choice = input("[1] Login  [2] Register  [3] Exit > ").strip()
        if choice == "1":
            u = input("Username: ")
            p = getpass("Password: ")
            if login(u,p):
                print(" Logged in!")
                return u
            print(" Invalid.")
        elif choice == "2":
            u = input("New username: ")
            p = getpass("New password: ")
            register(u,p)
            print(" Registered. Please login.")
        else:
            exit()
