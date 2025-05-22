# Sweet Talker: Lovable Text-to-Speech App

Welcome to **Sweet Talker**, a charming text-to-speech application that reads your text aloud with a friendly, pastel-themed GUI! Whether you’re reading a heartfelt devotional, a long story, or just some sweet notes, Sweet Talker brings your words to life with both **online** (high-quality Google Text-to-Speech) and **offline** (system-based voices) modes. Paste your text, choose a voice, and let Sweet Talker do the talking! 💬✨

## Features

- **Online and Offline Modes**:
  - **Online**: Uses Google Text-to-Speech (`gTTS`) for natural-sounding voices in multiple languages (e.g., English US, UK, French). Requires internet.
  - **Offline**: Uses `pyttsx3` for system voices (e.g., Microsoft Zira on Windows). Works without internet.
- **Voice Options**:
  - Online: English (US, UK, Australia), French, Spanish, German (most sound female-like).
  - Offline: System-dependent voices, with a preference for female voices if available.
- **Long Text Support**: Handles large texts (like devotionals) by splitting them into chunks for online mode or processing directly in offline mode.
- **Lovable Interface**: Pastel purple background, pink buttons, Comic Sans font, and emojis for a warm, inviting feel.
- **Scrollable Text Area**: Easily input and view long texts with a scrollbar.
- **Standalone Executable**: Package the app into a single `.exe` for Windows using PyInstaller, no Python installation needed!

## Requirements

- **Python 3.11+** (if running the script directly)
- **Libraries**:
  - `gtts`: For online text-to-speech.
  - `pyttsx3`: For offline text-to-speech.
  - `pygame`: For audio playback in online mode.
  - `pyinstaller`: For creating the `.exe`.
  - `tkinter`: Included with Python for the GUI.
- **Internet Connection**: Required for online mode (`gTTS`).
- **Operating System**: Tested on Windows; compatible with macOS/Linux (adjust PyInstaller commands for non-Windows).

## Installation

1. **Install Python** (if not already installed):

   - Download and install Python 3.11 or later from python.org.
   - Ensure `pip` is installed and added to your PATH.

2. **Install Dependencies**: Open a command prompt or terminal and run:

   ```bash
   pip install gtts pyttsx3 pygame pyinstaller
   ```

3. **Download the Script**:

   - Save `talker.py` to your project directory (e.g., `Talker`).

## Usage

1. **Run the Script**: Navigate to your project directory and run:

   ```bash
   cd Talker
   python talker.py
   ```

2. **Using the GUI**:

   - **Mode Selection**: Choose "Online" (requires internet, high-quality voices) or "Offline" (system voices, no internet needed) from the "Mode" dropdown.
   - **Voice Selection**: Select a voice from the "Choose Voice" dropdown. Online mode offers languages like English (US, UK), French, etc. Offline mode lists system voices (e.g., Microsoft Zira).
   - **Text Input**: Paste or type your text (e.g., a devotional like "COUNTING YOUR BLESSINGS II") into the scrollable text area.
   - **Speak**: Click the "Speak! 🎶" button to hear your text read aloud.
   - **Status**: The status label shows progress (e.g., "Speaking...", "Done!") or errors.

3. **Testing with Long Texts**:

   - Copy and paste a long text (e.g., a devotional) into the text area.
   - Select a mode and voice, then click "Speak!" to listen.
   - Online mode splits long texts into chunks for smooth playback; offline mode handles them directly.

## Creating a Standalone Executable

To create a single `.exe` file that runs on any Windows machine without Python installed:

1. **Open Command Prompt**: Navigate to your project directory:

   ```bash
   cd Talker
   ```

2. **Run PyInstaller**:

   ```bash
   pyinstaller --onefile --noconsole --icon=icon.ico talker.py
   ```

   - `--onefile`: Creates a single `.exe`.
   - `--noconsole`: Runs without a console window (GUI-only).
   - `--icon=icon.ico`: (Optional) Use a custom `.ico` file for the app icon. Create one at convertio.co or omit this flag.

3. **Find the Executable**:

   - The `.exe` will be in `..\Talker\dist\talkerv.exe`.
   - Double-click `talker.exe` to run the app.

4. **Notes**:

   - The `.exe` is \~50-100 MB due to bundled dependencies.
   - Online mode requires an internet connection; offline mode works without one.

## Troubleshooting

- **No Sound**:
  - **Online Mode**: Ensure an internet connection and check speakers. Look at the status label for errors (e.g., network issues).
  - **Offline Mode**: Verify system voices are installed (e.g., on Windows, check Control Panel &gt; Speech).
- **PyInstaller Issues**:
  - If the `.exe` fails, run it from the command prompt (`dist\talkerv.exe`) to see errors.
  - Try running PyInstaller without `--onefile` for debugging:

    ```bash
    pyinstaller --noconsole talkerv.py
    ```
- **Voice Issues**:
  - Online: If a voice doesn’t work, try another language (e.g., "English (UK)").
  - Offline: List available voices by adding this to `talkerv.py`:

    ```python
    for i, voice in enumerate(self.offline_voices):
        print(f"Voice {i}: {voice.name}")
    ```

    Run the script to see available offline voices.
- **GUI Errors**: If the GUI doesn’t open, ensure `tkinter` is installed (included with Python) and check for error messages in the terminal.

## Example: Reading a Devotional

To read a devotional like "COUNTING YOUR BLESSINGS II":

1. Open the app (`python talker.py` or `talkerv.exe`).
2. Paste the devotional text into the text area.
3. Select a mode ("Online" or "Offline") and a voice (e.g., "English (US)" for online, or a system voice like "Zira" for offline).
4. Click "Speak!" to hear the text read aloud in a natural, female-like voice (online) or system voice (offline).

## Customization

- **Add More Voices**: Edit the `online_voices` list in `talker.py` to include more `gTTS` languages (see gTTS documentation).
- **Change Theme**: Modify colors (e.g., `#f0e4f7` for background, `#ffcccb` for buttons) or fonts in `create_widgets`.
- **Additional Features**: Contact the developer to add features like saving audio as MP3, adjusting speech speed, or changing the GUI layout.

## Contributing

Found a bug or have a feature idea? Feel free to share your thoughts or submit improvements to make Sweet Talker even more lovable! 💖

## License

This project is for personal use and provided as-is. Enjoy spreading joy with Sweet Talker!

---

✨ Made with love by Blessed ✨