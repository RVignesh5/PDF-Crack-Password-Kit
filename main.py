import threading
import tkinter as tk
import os

def run_main():
    os.system("python gen.py")

def run_crack():
    os.system("python crack.py")

if __name__ == "__main__":
    thread1 = threading.Thread(target=run_main)
    thread2 = threading.Thread(target=run_crack)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
