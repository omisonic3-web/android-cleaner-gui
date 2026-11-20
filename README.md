# Android Studio, Gradle & Project Cleaner

A modern desktop GUI utility built with Python and `customtkinter` to scan and clean up disk space taken by Gradle caches, old Android Studio versions/caches, AVD cache/snapshots, and project `build/` or `.gradle/` directories.

## Features

- **Selective System & Toolchain Cleanup:**
  - Gradle caches and wrapper distributions (`~/.gradle/caches`, `~/.gradle/wrapper/dists`)
  - Gradle daemon logs (`~/.gradle/daemon`)
  - Android build cache (`~/.android/cache`, `~/.android/build-cache`)
  - AVD emulator cache and snapshots (`~/.android/avd`)
  - Kotlin Native / Konan cache (`~/.konan`)
  - Temporary Android/Gradle files in `%TEMP%` (on Windows)
  - 
- **Individual Android Studio Version Selection:** Detects Android Studio folders across cache, config, and log directories, marking the most recent one so you don't remove it by mistake.
- **Project Build Folder Scanner:** Scans a chosen projects directory for `build/` and `.gradle/` folders, displays their sizes, and lets you select which ones to delete.
- **Stop Gradle Daemon Button:** Runs `gradle --stop` (or `gradlew --stop` if available) before cleanup to release file locks.
- **Dark / Light Theme Toggle:** Switch between dark and light mode directly from the header.

## Requirements

- Python 3.10+
- `customtkinter`
- cu instrucțiuni clare pentru rularea din sursă și compilarea în executabil .exe pe Windows:Markdown## Running from Source

1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   
Run the GUI application:Bashpython android_cleaner_premium.py

Building the Windows Executable (.exe)

Install PyInstaller:Bashpython -m pip install pyinstaller

Build the standalone .exe (with customtkinter assets bundled and no console window):Bashpython -m PyInstaller --onefile --windowed --clean --collect-all customtkinter --name "AndroidCleanerPro" android_cleaner_premium.py

Find the compiled executable at dist/AndroidCleanerPro.exe.  

Note: If pyinstaller is not recognized in your terminal, use python -m PyInstaller as shown above.
Temporary build/, dist/, and AndroidCleanerPro.spec files are ignored by .gitignore.   

## Installation & Running from Source

2. Clone the repository:
   ```bash
   git clone [https://github.com/omisonic3-web/android-cleaner-gui.git](https://github.com/omisonic3-web/android-cleaner-gui.git)
   cd android-cleaner-gui
