import speech_recognition as sr
import threading
import subprocess
import ujson

# Define the hotkey and commands
HOTKEY = "system"
COMMANDS = {
    "status": 1,
    "inventory": 2,
    "storage": 2,
    "quests": 3,
    "quest": 3,
    "daily          ": 4,
    "strength training": 4,
    "skills": 5,
    "skill": 5,
    "equipment": 6,
    "armor": 6,
    "exit": 7,
    "dungeon": 8,
    "dungeons": 8,
    "credits": 9,
    "setting": 10,
    "settings": 10,
    "demon castle": 11,
    "demons castle": 11,
    "castle": 11,
    "store":12,
    "shop":12,
    "intro":13,
    "introduction":13,
    "Fatigue":14
}

# A flag to control the listening state
listening = True

def recognize_speech():
    global listening
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Thread started, listening for '{hotkey} [command]'...")
    while listening:
        try:
            with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                theme_data=ujson.load(themefile)
                theme=theme_data["Theme"]
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)

            # Recognize the speech
            command = recognizer.recognize_google(audio).lower()

            # Check for hotkey and commands
            if HOTKEY in command:
                for keyword, value in COMMANDS.items():
                    if keyword in command:
                        print(f"Hotkey and command '{keyword}' detected. Output: {value}")
                        subprocess.Popen(['python', 'Files/Mod/default/sfx_button.py'])
                        if value==1:
                            subprocess.Popen(['python', f'{theme} Version/Status Tab/gui.py'])
                        elif value==2:
                            subprocess.Popen(['python', f'{theme} Version/Inventory/gui.py'])
                        elif value==3:
                            subprocess.Popen(['python', f'{theme} Version/Quests/gui.py'])
                        elif value==4:
                            subprocess.Popen(['python', f'{theme} Version/Daily Quest/gui.py'])
                        elif value==5:
                            subprocess.Popen(['python', f'{theme} Version/Skills Tab/gui.py'])
                        elif value==6:
                            subprocess.Popen(['python', f'{theme} Version/Equipment/gui.py'])
                        elif value==8:
                            subprocess.Popen(['python', f'{theme} Version/Dungeon/gui.py'])
                        elif value==9:
                            subprocess.Popen(['python', f'{theme} Version/Credits/gui.py'])
                        elif value==10:
                            subprocess.Popen(['python', f'{theme} Version/Settings/gui.py'])
                        elif value==11:
                            subprocess.Popen(['python', f'{theme} Version/Demon Castle/gui.py'])
                        elif value==12:
                            subprocess.Popen(['python', f'{theme} Version/Shop/gui.py'])
                        elif value==13:
                            subprocess.Popen(['python', f'{theme} Version/Intro/gui.py'])
                        elif value==14:
                            subprocess.Popen(['python', f'{theme} Version/Fatigue/gui.py'])
                        break  # Continue listening after processing the command
        except sr.UnknownValueError:
            pass  # Ignore unrecognized speech
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
        except sr.WaitTimeoutError:
            pass  # Timeout if no speech is detected

def main():
    global listening

    # Create and start a thread for speech recognition
    speech_thread = threading.Thread(target=recognize_speech, daemon=True)
    speech_thread.start()

    try:
        while True:
            with open("Files/Player Data/Settings.json", 'r') as fson:
                data=ujson.load(fson)
            listening = data["Settings"]["Microphone"]
            if listening == "False":
                listening = False
                speech_thread.join()  # Wait for the thread to finish
                print("Speech recognition stopped.")
                break
    except KeyboardInterrupt:
        listening = False
        speech_thread.join()
        print("\nProgram terminated.")

if __name__ == "__main__":
    main()