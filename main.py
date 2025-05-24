# main.py
from ui.login import show_login
from ui.chat import start_chat_window

def main():
    show_login(start_chat_window)

if __name__ == "__main__":
    main()
