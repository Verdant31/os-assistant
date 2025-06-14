import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import List, Dict, Any


class ActionGroup:
    def __init__(self, name: str, actions: List[Dict[str, Any]] = None):
        self.name = name
        self.actions = actions or []


class ChromeProfile:
    def __init__(self, name: str, shortcut_path: str):
        self.name = name
        self.shortcut_path = shortcut_path


class ActionEditor(tk.Toplevel):
    def __init__(self, parent, action=None):
        super().__init__(parent)
        self.title("Edit Action")
        self.geometry("500x400")
        self.action = action or {}

        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Action type
        ttk.Label(main_frame, text="Action Type:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.action_type = tk.StringVar(
            value=action.get('type', '') if action else '')
        action_types = [
            'launch_app', 'move_window', 'split_screen', 'close_app',
            'max', 'min', 'update_app_volume', 'monitor_control'
        ]
        self.action_type_combo = ttk.Combobox(
            main_frame, textvariable=self.action_type, values=action_types)
        self.action_type_combo.grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.action_type_combo.bind(
            '<<ComboboxSelected>>', self.on_action_type_change)

        # Create all possible fields but don't show them yet
        self.fields = {}

        # Target field (common to most actions)
        self.fields['target'] = {
            'label': ttk.Label(main_frame, text="Target:"),
            'entry': ttk.Entry(main_frame),
            'var': tk.StringVar(value=action.get('target', '') if action else '')
        }
        self.fields['target']['entry'].configure(
            textvariable=self.fields['target']['var'])

        # Position field (for move_window)
        self.fields['position'] = {
            'label': ttk.Label(main_frame, text="Position:"),
            'entry': ttk.Combobox(main_frame, values=['Maximized', 'Top', 'Bottom', 'Left', 'Right']),
            'var': tk.StringVar(value=action.get('position', '') if action else '')
        }
        self.fields['position']['entry'].configure(
            textvariable=self.fields['position']['var'])

        # Monitor index field (for move_window, split_screen, monitor_control)
        self.fields['monitor_index'] = {
            'label': ttk.Label(main_frame, text="Monitor Index:"),
            'entry': ttk.Entry(main_frame),
            'var': tk.StringVar(value=str(action.get('monitor_index', '')) if action else '')
        }
        self.fields['monitor_index']['entry'].configure(
            textvariable=self.fields['monitor_index']['var'])

        # Volume change field (for update_app_volume)
        self.fields['volume_change'] = {
            'label': ttk.Label(main_frame, text="Volume Change:"),
            'entry': ttk.Entry(main_frame),
            'var': tk.StringVar(value=str(action.get('volume_change', '')) if action else '')
        }
        self.fields['volume_change']['entry'].configure(
            textvariable=self.fields['volume_change']['var'])

        # Second app field (for split_screen)
        self.fields['second_app'] = {
            'label': ttk.Label(main_frame, text="Second App:"),
            'entry': ttk.Entry(main_frame),
            'var': tk.StringVar(value=action.get('second_app', '') if action else '')
        }
        self.fields['second_app']['entry'].configure(
            textvariable=self.fields['second_app']['var'])

        # Monitor action field (for monitor_control)
        self.fields['monitor_action'] = {
            'label': ttk.Label(main_frame, text="Action:"),
            'entry': ttk.Combobox(main_frame, values=['enable', 'disable']),
            'var': tk.StringVar(value=action.get('monitor_action', '') if action else '')
        }
        self.fields['monitor_action']['entry'].configure(
            textvariable=self.fields['monitor_action']['var'])

        # Save button
        self.save_button = ttk.Button(
            main_frame, text="Save Action", command=self.save_action)
        self.save_button.grid(row=20, column=0, columnspan=2, pady=20)

        # Configure grid
        main_frame.columnconfigure(1, weight=1)

        # Show initial fields based on action type
        self.on_action_type_change(None)

    def on_action_type_change(self, event):
        # Hide all fields first
        for field in self.fields.values():
            field['label'].grid_remove()
            field['entry'].grid_remove()

        action_type = self.action_type.get()
        current_row = 1

        # Show relevant fields based on action type
        if action_type in ['launch_app', 'close_app', 'max', 'min']:
            # Only target field needed
            self.fields['target']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['target']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)

        elif action_type == 'move_window':
            # Target, position, and optional monitor index
            self.fields['target']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['target']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
            current_row += 1

            self.fields['position']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['position']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
            current_row += 1

            self.fields['monitor_index']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['monitor_index']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)

        elif action_type == 'split_screen':
            # Target (first app), second app, and optional monitor index
            self.fields['target']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['target']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
            current_row += 1

            self.fields['second_app']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['second_app']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
            current_row += 1

            self.fields['monitor_index']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['monitor_index']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)

        elif action_type == 'update_app_volume':
            # Target (app name) and volume change
            self.fields['target']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['target']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
            current_row += 1

            self.fields['volume_change']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['volume_change']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)

        elif action_type == 'monitor_control':
            # Monitor action (enable/disable) and monitor index
            self.fields['monitor_action']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['monitor_action']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
            current_row += 1

            self.fields['monitor_index']['label'].grid(
                row=current_row, column=0, sticky=tk.W, pady=5)
            self.fields['monitor_index']['entry'].grid(
                row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)

    def save_action(self):
        action = {
            'type': self.action_type.get()
        }

        # Add fields based on action type
        action_type = self.action_type.get()

        if action_type in ['launch_app', 'close_app', 'max', 'min']:
            action['target'] = self.fields['target']['var'].get()

        elif action_type == 'move_window':
            action['target'] = self.fields['target']['var'].get()
            if self.fields['position']['var'].get():
                action['position'] = self.fields['position']['var'].get()
            if self.fields['monitor_index']['var'].get():
                action['monitor_index'] = int(
                    self.fields['monitor_index']['var'].get())

        elif action_type == 'split_screen':
            action['target'] = self.fields['target']['var'].get()
            action['second_app'] = self.fields['second_app']['var'].get()
            if self.fields['monitor_index']['var'].get():
                action['monitor_index'] = int(
                    self.fields['monitor_index']['var'].get())

        elif action_type == 'update_app_volume':
            action['target'] = self.fields['target']['var'].get()
            if self.fields['volume_change']['var'].get():
                action['volume_change'] = int(
                    self.fields['volume_change']['var'].get())

        elif action_type == 'monitor_control':
            action['monitor_action'] = self.fields['monitor_action']['var'].get()
            if self.fields['monitor_index']['var'].get():
                action['monitor_index'] = int(
                    self.fields['monitor_index']['var'].get())

        self.action = action
        self.destroy()


class ActionGroupEditor(tk.Toplevel):
    def __init__(self, parent, group=None):
        super().__init__(parent)
        self.title("Edit Action Group")
        self.geometry("600x500")
        self.group = group or ActionGroup("")
        self.result = None

        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Group name
        ttk.Label(main_frame, text="Group Name:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.group_name = tk.StringVar(value=self.group.name)
        ttk.Entry(main_frame, textvariable=self.group_name).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Actions list
        ttk.Label(main_frame, text="Actions:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.actions_frame = ttk.Frame(main_frame)
        self.actions_frame.grid(row=2, column=0, columnspan=2, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=5)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(buttons_frame, text="Add Action",
                   command=self.add_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Edit Action",
                   command=self.edit_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Remove Action",
                   command=self.remove_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Save Group",
                   command=self.save_group).pack(side=tk.LEFT, padx=5)

        # Actions listbox
        self.actions_listbox = tk.Listbox(self.actions_frame, height=10)
        self.actions_listbox.pack(fill=tk.BOTH, expand=True)

        # Load existing actions
        self.refresh_actions_list()

        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        self.actions_frame.columnconfigure(0, weight=1)

    def refresh_actions_list(self):
        self.actions_listbox.delete(0, tk.END)
        for action in self.group.actions:
            action_text = f"{action['type']} - {action['target']}"
            if 'position' in action:
                action_text += f" ({action['position']})"
            self.actions_listbox.insert(tk.END, action_text)

    def add_action(self):
        editor = ActionEditor(self)
        self.wait_window(editor)
        if editor.action:
            self.group.actions.append(editor.action)
            self.refresh_actions_list()

    def edit_action(self):
        selection = self.actions_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Warning", "Please select an action to edit")
            return

        index = selection[0]
        editor = ActionEditor(self, self.group.actions[index])
        self.wait_window(editor)
        if editor.action:
            self.group.actions[index] = editor.action
            self.refresh_actions_list()

    def remove_action(self):
        selection = self.actions_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Warning", "Please select an action to remove")
            return

        index = selection[0]
        del self.group.actions[index]
        self.refresh_actions_list()

    def save_group(self):
        name = self.group_name.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a group name")
            return

        if not self.group.actions:
            messagebox.showwarning("Warning", "Please add at least one action")
            return

        self.group.name = name
        self.result = self.group
        self.destroy()


class ChromeProfileEditor(tk.Toplevel):
    def __init__(self, parent, profile=None):
        super().__init__(parent)
        self.title("Edit Chrome Profile")
        self.geometry("500x200")
        self.profile = profile or ChromeProfile("", "")
        self.result = None

        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Profile name
        ttk.Label(main_frame, text="Profile Name:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.profile_name = tk.StringVar(value=self.profile.name)
        ttk.Entry(main_frame, textvariable=self.profile_name).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Shortcut path
        ttk.Label(main_frame, text="Shortcut Path:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.shortcut_path = tk.StringVar(value=self.profile.shortcut_path)
        path_entry = ttk.Entry(main_frame, textvariable=self.shortcut_path)
        path_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Browse button
        ttk.Button(main_frame, text="Browse", command=self.browse_shortcut).grid(
            row=1, column=2, padx=5)

        # Save button
        ttk.Button(main_frame, text="Save Profile", command=self.save_profile).grid(
            row=2, column=0, columnspan=3, pady=20)

        # Configure grid
        main_frame.columnconfigure(1, weight=1)

    def browse_shortcut(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Select Chrome Profile Shortcut",
            filetypes=[("Shortcut files", "*.lnk"), ("All files", "*.*")]
        )
        if filename:
            self.shortcut_path.set(filename)

    def save_profile(self):
        name = self.profile_name.get().strip()
        path = self.shortcut_path.get().strip()

        if not name:
            messagebox.showwarning("Warning", "Please enter a profile name")
            return

        if not path:
            messagebox.showwarning("Warning", "Please select a shortcut path")
            return

        self.profile.name = name
        self.profile.shortcut_path = path
        self.result = self.profile
        self.destroy()


class SettingsWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis Assistant Settings")
        self.root.geometry("800x600")

        # Center the window
        self.root.eval('tk::PlaceWindow . center')

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Basic settings tab
        basic_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(basic_frame, text="Basic Settings")

        # Wake phrase setting
        ttk.Label(basic_frame, text="Wake Phrase:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.wake_phrase = tk.StringVar(value="ola jarvis")
        ttk.Entry(basic_frame, textvariable=self.wake_phrase).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # AutoHotkey path setting
        ttk.Label(basic_frame, text="AutoHotkey Path:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.ahk_path = tk.StringVar(
            value=r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe")
        ttk.Entry(basic_frame, textvariable=self.ahk_path).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Action groups tab
        groups_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(groups_frame, text="Action Groups")

        # Groups list
        ttk.Label(groups_frame, text="Action Groups:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.groups_listbox = tk.Listbox(groups_frame, height=10)
        self.groups_listbox.grid(row=1, column=0, columnspan=2, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=5)

        # Buttons frame for groups
        groups_buttons = ttk.Frame(groups_frame)
        groups_buttons.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(groups_buttons, text="Add Group",
                   command=self.add_group).pack(side=tk.LEFT, padx=5)
        ttk.Button(groups_buttons, text="Edit Group",
                   command=self.edit_group).pack(side=tk.LEFT, padx=5)
        ttk.Button(groups_buttons, text="Remove Group",
                   command=self.remove_group).pack(side=tk.LEFT, padx=5)

        # Chrome Profiles tab
        chrome_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(chrome_frame, text="Chrome Profiles")

        # Profiles list
        ttk.Label(chrome_frame, text="Chrome Profiles:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.profiles_listbox = tk.Listbox(chrome_frame, height=10)
        self.profiles_listbox.grid(row=1, column=0, columnspan=2, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=5)

        # Buttons frame for profiles
        profiles_buttons = ttk.Frame(chrome_frame)
        profiles_buttons.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(profiles_buttons, text="Add Profile",
                   command=self.add_chrome_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(profiles_buttons, text="Edit Profile",
                   command=self.edit_chrome_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(profiles_buttons, text="Remove Profile",
                   command=self.remove_chrome_profile).pack(side=tk.LEFT, padx=5)

        # Save settings button
        ttk.Button(self.root, text="Save and Start",
                   command=self.save_and_start).pack(pady=10)

        # Load existing settings
        self.load_settings()

        # Configure grid
        basic_frame.columnconfigure(1, weight=1)
        groups_frame.columnconfigure(0, weight=1)
        groups_frame.rowconfigure(1, weight=1)
        chrome_frame.columnconfigure(0, weight=1)
        chrome_frame.rowconfigure(1, weight=1)

        self.action_groups = []
        self.chrome_profiles = []

    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.wake_phrase.set(settings.get(
                        'wake_phrase', 'ola jarvis'))
                    self.ahk_path.set(settings.get(
                        'ahk_path', r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe"))
                    self.action_groups = [ActionGroup(
                        **group) for group in settings.get('action_groups', [])]
                    self.chrome_profiles = [ChromeProfile(
                        **profile) for profile in settings.get('chrome_profiles', [])]
                    self.refresh_groups_list()
                    self.refresh_profiles_list()
        except Exception as e:
            print(f"Error loading settings: {e}")

    def refresh_groups_list(self):
        self.groups_listbox.delete(0, tk.END)
        for group in self.action_groups:
            self.groups_listbox.insert(tk.END, group.name)

    def add_group(self):
        editor = ActionGroupEditor(self.root)
        self.root.wait_window(editor)
        if editor.result:
            self.action_groups.append(editor.result)
            self.refresh_groups_list()

    def edit_group(self):
        selection = self.groups_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a group to edit")
            return

        index = selection[0]
        editor = ActionGroupEditor(self.root, self.action_groups[index])
        self.root.wait_window(editor)
        if editor.result:
            self.action_groups[index] = editor.result
            self.refresh_groups_list()

    def remove_group(self):
        selection = self.groups_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Warning", "Please select a group to remove")
            return

        index = selection[0]
        del self.action_groups[index]
        self.refresh_groups_list()

    def refresh_profiles_list(self):
        self.profiles_listbox.delete(0, tk.END)
        for profile in self.chrome_profiles:
            self.profiles_listbox.insert(
                tk.END, f"{profile.name} - {profile.shortcut_path}")

    def add_chrome_profile(self):
        editor = ChromeProfileEditor(self.root)
        self.root.wait_window(editor)
        if editor.result:
            self.chrome_profiles.append(editor.result)
            self.refresh_profiles_list()

    def edit_chrome_profile(self):
        selection = self.profiles_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Warning", "Please select a profile to edit")
            return

        index = selection[0]
        editor = ChromeProfileEditor(self.root, self.chrome_profiles[index])
        self.root.wait_window(editor)
        if editor.result:
            self.chrome_profiles[index] = editor.result
            self.refresh_profiles_list()

    def remove_chrome_profile(self):
        selection = self.profiles_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Warning", "Please select a profile to remove")
            return

        index = selection[0]
        del self.chrome_profiles[index]
        self.refresh_profiles_list()

    def save_settings(self):
        settings = {
            'wake_phrase': self.wake_phrase.get(),
            'ahk_path': self.ahk_path.get(),
            'action_groups': [vars(group) for group in self.action_groups],
            'chrome_profiles': [vars(profile) for profile in self.chrome_profiles]
        }
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def save_and_start(self):
        self.save_settings()
        self.root.quit()

    def run(self):
        self.root.mainloop()
        return {
            'wake_phrase': self.wake_phrase.get(),
            'ahk_path': self.ahk_path.get(),
            'action_groups': [vars(group) for group in self.action_groups],
            'chrome_profiles': [vars(profile) for profile in self.chrome_profiles]
        }
