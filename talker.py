import tkinter as tk
from tkinter import ttk
import pygame
from gtts import gTTS
import pyttsx3
import os
import tempfile
import uuid
import re
import platform

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lovable Text-to-Speech")
        self.root.geometry("450x650")
        self.root.configure(bg="#f0e4f7")  # Soft pastel purple background

        # Initialize pygame for audio playback (used in online mode)
        pygame.mixer.init()

        # Initialize pyttsx3 for offline mode
        self.tts_engine = pyttsx3.init()
        self.offline_voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('rate', 150)  # Moderate speed
        self.tts_engine.setProperty('volume', 0.9)  # Near max volume

        # Try to select a female voice for offline mode (e.g., Microsoft Zira)
        self.offline_voice_id = None
        for voice in self.offline_voices:
            if "Zira" in voice.name or "female" in voice.name.lower():
                self.offline_voice_id = voice.id
                break
        if self.offline_voice_id:
            self.tts_engine.setProperty('voice', self.offline_voice_id)

        # Available voices/languages for gTTS (online mode)
        self.online_voices = [
            ("en-us", "English (US)"),
            ("en-uk", "English (UK)"),
            ("en-au", "English (Australia)"),
            ("fr-fr", "French"),
            ("es-es", "Spanish"),
            ("de-de", "German")
        ]

        # Mode and voice variables
        self.mode = tk.StringVar(value="Online")  # Default to online mode
        self.online_voice = tk.StringVar(value=self.online_voices[0][0])  # Default to en-us
        self.offline_voice = tk.StringVar(value=self.offline_voice_id or self.offline_voices[0].id if self.offline_voices else "Default")

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title label
        title_label = tk.Label(
            self.root,
            text="💬 Sweet Talker",
            font=("Comic Sans MS", 20, "bold"),
            bg="#f0e4f7",
            fg="#6b4e71"
        )
        title_label.pack(pady=20)

        # Mode selection (Online/Offline)
        mode_frame = tk.Frame(self.root, bg="#f0e4f7")
        mode_frame.pack(pady=10)
        tk.Label(
            mode_frame,
            text="Mode:",
            font=("Arial", 12),
            bg="#f0e4f7",
            fg="#6b4e71"
        ).pack(side=tk.LEFT, padx=5)
        mode_dropdown = ttk.Combobox(
            mode_frame,
            textvariable=self.mode,
            values=["Online", "Offline"],
            state="readonly",
            width=10
        )
        mode_dropdown.pack(side=tk.LEFT, padx=5)
        mode_dropdown.bind("<<ComboboxSelected>>", self.update_voice_dropdown)

        # Voice selection dropdown
        self.voice_frame = tk.Frame(self.root, bg="#f0e4f7")
        self.voice_frame.pack(pady=10)
        tk.Label(
            self.voice_frame,
            text="Choose Voice:",
            font=("Arial", 12),
            bg="#f0e4f7",
            fg="#6b4e71"
        ).pack(side=tk.LEFT, padx=5)
        
        self.voice_dropdown = ttk.Combobox(
            self.voice_frame,
            textvariable=self.online_voice,
            values=[voice[1] for voice in self.online_voices],
            state="readonly",
            width=20
        )
        self.voice_dropdown.pack(side=tk.LEFT, padx=5)

        # Scrollable text input area
        text_frame = tk.Frame(self.root, bg="#f0e4f7")
        text_frame.pack(pady=20)
        self.text_area = tk.Text(
            text_frame,
            height=12,
            width=40,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#333333",
            relief=tk.FLAT,
            borderwidth=2,
            wrap=tk.WORD
        )
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, "Type or paste something sweet for me to say! 😊")

        # Speak button
        speak_button = tk.Button(
            self.root,
            text="Speak! 🎶",
            font=("Comic Sans MS", 14, "bold"),
            bg="#ffcccb",
            fg="#6b4e71",
            activebackground="#ffb6b9",
            relief=tk.FLAT,
            command=self.speak_text
        )
        speak_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to talk!",
            font=("Arial", 10, "italic"),
            bg="#f0e4f7",
            fg="#6b4e71"
        )
        self.status_label.pack(pady=10)

        # Decorative elements
        tk.Label(
            self.root,
            text="✨ Made with love ✨",
            font=("Arial", 10),
            bg="#f0e4f7",
            fg="#6b4e71"
        ).pack(pady=20)

    def update_voice_dropdown(self, event=None):
        """Update voice dropdown based on mode."""
        self.voice_dropdown.destroy()
        if self.mode.get() == "Online":
            self.voice_dropdown = ttk.Combobox(
                self.voice_frame,
                textvariable=self.online_voice,
                values=[voice[1] for voice in self.online_voices],
                state="readonly",
                width=20
            )
        else:
            offline_voice_names = [voice.name for voice in self.offline_voices] if self.offline_voices else ["Default"]
            self.voice_dropdown = ttk.Combobox(
                self.voice_frame,
                textvariable=self.offline_voice,
                values=offline_voice_names,
                state="readonly",
                width=20
            )
        self.voice_dropdown.pack(side=tk.LEFT, padx=5)

    def split_text(self, text, max_length=1000):
        """Split text into smaller chunks for gTTS (avoiding API limits)."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    def speak_text(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            self.status_label.config(text="Please enter some text! 😅")
            return

        self.status_label.config(text="Speaking... 🎙️")
        self.root.update()

        try:
            if self.mode.get() == "Online":
                # Online mode with gTTS
                lang_code = self.online_voice.get()
                for code, name in self.online_voices:
                    if name == lang_code:
                        lang_code = code
                        break

                # Split text for long inputs
                chunks = self.split_text(text)
                temp_files = []

                for chunk in chunks:
                    if not chunk:
                        continue
                    # Generate speech with gTTS
                    tts = gTTS(text=chunk, lang=lang_code, slow=False)
                    temp_dir = tempfile.gettempdir()
                    temp_file = os.path.join(temp_dir, f"tts_{uuid.uuid4()}.mp3")
                    tts.save(temp_file)
                    temp_files.append(temp_file)

                    # Play audio with pygame
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

                # Clean up temporary files
                for temp_file in temp_files:
                    try:
                        os.remove(temp_file)
                    except Exception:
                        pass

            else:
                # Offline mode with pyttsx3
                selected_voice_name = self.offline_voice.get()
                for voice in self.offline_voices:
                    if voice.name == selected_voice_name:
                        self.tts_engine.setProperty('voice', voice.id)
                        break

                # pyttsx3 can handle long texts without splitting
                if platform.system() == "Emscripten":
                    import asyncio
                    async def async_speak():
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
                    asyncio.ensure_future(async_speak())
                else:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()

            self.status_label.config(text="Done! Ready for more! 😊")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)} 😢")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()