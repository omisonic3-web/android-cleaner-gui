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
- **Individual Android Studio Version Selection:** Detects Android Studio folders across cache, config, and log directories, marking the most recent one so you don't remove it by mistake.
- **Project Build Folder Scanner:** Scans a chosen projects directory for `build/` and `.gradle/` folders, displays their sizes, and lets you select which ones to delete.
- **Stop Gradle Daemon Button:** Runs `gradle --stop` (or `gradlew --stop` if available) before cleanup to release file locks.
- **Dark / Light Theme Toggle:** Switch between dark and light mode directly from the header.

## Requirements

- Python 3.10+
- `customtkinter`

## Installation & Running from Source

1. Clone the repository:
   ```bash
   git clone [https://github.com/omisonic3-web/android-cleaner-gui.git](https://github.com/omisonic3-web/android-cleaner-gui.git)
   cd android-cleaner-gui
