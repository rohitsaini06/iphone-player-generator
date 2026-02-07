import subprocess
import sys


while True:
    subprocess.run(
        [sys.executable, "main.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    input()