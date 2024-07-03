import PyInstaller.__main__
import os
import sys

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to your script
script_path = os.path.join(current_dir, 'main.py')

PyInstaller.__main__.run([
    script_path,
    '--onefile',
    '--windowed',
    '--name=TaskReminder',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
    '--icon=spider.ico',  # Uncomment this line if you have an icon file
])