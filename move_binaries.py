import os
import shutil

source_dir = './dist'
target_dir = '../desktop-assistant/src-tauri/bin'
suffix = '-x86_64-pc-windows-msvc'

os.makedirs(target_dir, exist_ok=True)

for filename in os.listdir(source_dir):
    source_path = os.path.join(source_dir, filename)

    if os.path.isfile(source_path):
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}{suffix}{ext}"
        target_path = os.path.join(target_dir, new_filename)

        shutil.copy2(source_path, target_path)
        print(f"Copiado e renomeado: {filename} → {new_filename}")
