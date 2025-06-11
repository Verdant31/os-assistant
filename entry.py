import subprocess
from assistant import Assistant
from utils import normalize_text
from playsound import playsound
import os
import dotenv
from chat import Chat
dotenv.load_dotenv()

WAKE_PHRASE = "ola jarvis"
ahk_exe_path = r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe"

assistant = Assistant()
chat = Chat()

while True:
    captured_text = assistant.listen()
    normalized_text = normalize_text(captured_text)

    if WAKE_PHRASE in normalized_text:
        print("Wake phrase detected! Jarvis will now listen to the user request.")
        playsound('./notification.mp3')
        while True:
            user_request = assistant.listen()
            if user_request:
                commands = chat.map_prompt_scripts(user_request)
                for cmd in commands['commands']:
                    cmd_full_path = os.path.join(
                        os.getcwd() + "./modules", cmd["script"])
                    call_params = [ahk_exe_path, str(
                        cmd_full_path)] + [str(p) for p in cmd["params"]]
                    subprocess.call(
                        call_params, shell=True
                    )

                break
        break  # Exit loop after wake word is detected, remove to keep listening
    else:
        print("Listening...")
