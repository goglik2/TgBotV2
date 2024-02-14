import subprocess
import time
import threading

def bot():
    time.sleep(250)
    while True:
        process2 = subprocess.Popen(['python', 'main.py'])
        time.sleep(300)
        process2.terminate()

threading.Thread(target=bot).start()

while True:
    process = subprocess.Popen(['python', 'main.py'])
    time.sleep(300)
    process.terminate()