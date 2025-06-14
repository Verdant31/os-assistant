import subprocess
from assistant import Assistant
from utils import normalize_text
from playsound import playsound
import os
import dotenv
from chat import Chat
from ui import SettingsWindow

dotenv.load_dotenv()

# Show settings UI first
settings_window = SettingsWindow()
settings = settings_window.run()

WAKE_PHRASE = settings['wake_phrase']
ahk_exe_path = settings['ahk_path']
ACTION_GROUPS = settings['action_groups']

assistant = Assistant()
chat = Chat()


def execute_action_group(group_name: str):
    """Execute a predefined action group by name."""
    for group in ACTION_GROUPS:
        if group['name'].lower() == group_name.lower():
            for action in group['actions']:
                script = f"{action['type']}.ahk"
                params = [action['target']]

                # Add optional parameters based on action type
                if action['type'] == 'move_window':
                    if 'position' in action:
                        params.append(action['position'])
                    if 'monitor_index' in action:
                        params.append(str(action['monitor_index']))
                elif action['type'] == 'update_app_volume':
                    if 'volume_change' in action:
                        params.append(str(action['volume_change']))
                elif action['type'] == 'monitor_control':
                    if 'position' in action:  # using position field for enable/disable
                        params.append(action['position'])
                    if 'monitor_index' in action:
                        params.append(str(action['monitor_index']))

                cmd_full_path = os.path.join(os.getcwd(), "./modules", script)
                call_params = [ahk_exe_path, str(
                    cmd_full_path)] + [str(p) for p in params]
                subprocess.call(call_params, shell=True)
            return True
    return False


while True:
    captured_text = assistant.listen()
    normalized_text = normalize_text(captured_text)

    if (normalized_text == "encerrar"):
        break

    if WAKE_PHRASE in normalized_text:
        print("Wake phrase detected! Jarvis will now listen to the user request.")
        playsound('./notification.mp3')
        while True:
            user_request = assistant.listen()
            if user_request:
                # First try to match against action groups
                words = user_request.lower().split()
                if len(words) >= 2 and words[0] in ['execute', 'run', 'start']:
                    group_name = ' '.join(words[1:])
                    if execute_action_group(group_name):
                        print(f"Executed action group: {group_name}")
                        break

                # If no action group matched, process as a normal command
                commands = chat.map_prompt_scripts(user_request)
                for cmd in commands['commands']:
                    cmd_full_path = os.path.join(
                        os.getcwd(), "./modules", cmd["script"])
                    call_params = [ahk_exe_path, str(
                        cmd_full_path)] + [str(p) for p in cmd["params"]]
                    subprocess.call(
                        call_params, shell=True
                    )
                break
        break  # Exit loop after wake word is detected, remove to keep listening
    else:
        print("Listening...")
