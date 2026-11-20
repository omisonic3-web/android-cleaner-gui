import os
import shutil
import platform
import subprocess
import threading
from pathlib import Path
from tkinter import messagebox, filedialog
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


TRANSLATIONS = {
    "ro": {
        "window_title": "Android Studio, Gradle & Project Cleaner — Pro",
        "header_title": "Android Studio & Gradle Cleaner",
        "header_subtitle": "Închide Android Studio și oprește Gradle daemon înainte de ștergerea fișierelor.",
        "dark_mode": "Dark Mode",
        "tab_system": "Sistem, Gradle & IDE",
        "tab_projects": "Foldere Build Proiecte",
        "total_selected": "Total selectat pentru ștergere: {size}",
        "initializing": "Inițializare...",
        "ready": "Gata.",
        "select_safe": "Bifează Sigure",
        "deselect_all": "Debifează Tot",
        "rescan": "Rescanează",
        "stop_gradle": "Oprește Gradle",
        "delete_selected": "Șterge Selectate",
        "projects_folder_lbl": "Folder proiecte:",
        "browse": "Alege...",
        "scan": "Scanează",
        "select_all_build": "Selectează toate folderele build/",
        "deselect_projects": "Deselectează proiectele",
        "group_cache": "Cache Sistem & Toolchains",
        "group_studio": "Versiuni & Date Android Studio",
        "gradle_caches_title": "Gradle Caches & Wrapper Distributions",
        "gradle_caches_desc": "Librării descărcate și distribuții Gradle wrapper (~/.gradle/caches, ~/.gradle/wrapper/dists).",
        "gradle_daemon_title": "Gradle Daemon Logs",
        "gradle_daemon_desc": "Log-uri vechi generate de procesele Gradle daemon (~/.gradle/daemon).",
        "android_cache_title": "Android Build Cache (.android/cache & build-cache)",
        "android_cache_desc": "Fișiere temporare de compilare Android din directorul utilizatorului.",
        "avd_cache_title": "Emulator Cache & Snapshots (.android/avd)",
        "avd_cache_desc": "Cache.img și snapshot-uri din emulatoare (păstrează dispozitivele AVD).",
        "konan_cache_title": "Kotlin Native / Konan Cache (.konan)",
        "konan_cache_desc": "Toolchains și dependențe Kotlin Native / Multiplatform descărcate.",
        "win_temp_title": "Fișiere Temporare Windows (%TEMP% - Android & Gradle)",
        "win_temp_desc": "Fișiere temporare rămase în Temp de la build-uri sau instalări SDK.",
        "studio_latest": " • CEL MAI RECENT",
        "studio_older": " • Versiune anterioară",
        "loc_local": "Local Cache/Data",
        "loc_roaming": "Roaming Config/Plugins",
        "loc_legacy": "Legacy Home Dir",
        "loc_cache": "Cache",
        "loc_config": "Config & Plugins",
        "loc_logs": "Logs",
        "stopping_gradle": "Se opresc procesele Gradle daemon...",
        "gradle_title": "Gradle",
        "gradle_stopped_ok": "Procesele Gradle daemon au fost oprite cu succes.",
        "gradle_stop_err": "A apărut o problemă la oprirea Gradle:\n{err}",
        "gradle_not_found": "Nu s-a găsit un executabil Gradle activ/în PATH. Asigură-te că Android Studio este închis.",
        "calculating_sizes": "Se calculează dimensiunile...",
        "scan_done_no_proj": "Scanare completă (folder proiecte nesetat/inexistent).",
        "scanning_projects": "Se caută foldere build/ și .gradle/...",
        "scan_done_count": "Scanare completă ({count} foldere găsite).",
        "info_title": "Info",
        "nothing_selected": "Nu ai selectat niciun element existent pentru ștergere.",
        "confirm_title": "Confirmare Ștergere Definitivă",
        "confirm_body": (
            "Urmează să ștergi {count} locații (~{size}).\n\n"
            "Asigură-te că Android Studio, emulatorii și procesele Gradle sunt închise.\n"
            "Continui?"
        ),
        "deleting_item": "Se șterge: {label}...",
        "clean_finished": "Curățare finalizată.",
        "warn_title": "Finalizat cu avertismente",
        "warn_body": "Unele fișiere/foldere nu au putut fi șterse (posibil blocate de un proces activ):\n\n{preview}",
        "success_title": "Succes",
        "success_body": "Toate elementele selectate au fost șterse cu succes!",
    },
    "en": {
        "window_title": "Android Studio, Gradle & Project Cleaner — Pro",
        "header_title": "Android Studio & Gradle Cleaner",
        "header_subtitle": "Close Android Studio and stop Gradle daemons before deleting files.",
        "dark_mode": "Dark Mode",
        "tab_system": "System, Gradle & IDE",
        "tab_projects": "Project Build Folders",
        "total_selected": "Total selected for deletion: {size}",
        "initializing": "Initializing...",
        "ready": "Ready.",
        "select_safe": "Select Safe",
        "deselect_all": "Deselect All",
        "rescan": "Rescan",
        "stop_gradle": "Stop Gradle",
        "delete_selected": "Delete Selected",
        "projects_folder_lbl": "Projects folder:",
        "browse": "Browse...",
        "scan": "Scan",
        "select_all_build": "Select all build/ folders",
        "deselect_projects": "Deselect projects",
        "group_cache": "System & Toolchain Caches",
        "group_studio": "Android Studio Versions & Data",
        "gradle_caches_title": "Gradle Caches & Wrapper Distributions",
        "gradle_caches_desc": "Downloaded dependencies and Gradle wrapper distributions (~/.gradle/caches, ~/.gradle/wrapper/dists).",
        "gradle_daemon_title": "Gradle Daemon Logs",
        "gradle_daemon_desc": "Old log files generated by Gradle daemon processes (~/.gradle/daemon).",
        "android_cache_title": "Android Build Cache (.android/cache & build-cache)",
        "android_cache_desc": "Temporary Android build files in your user home directory.",
        "avd_cache_title": "Emulator Cache & Snapshots (.android/avd)",
        "avd_cache_desc": "Emulator cache.img and snapshots (keeps your AVD devices intact).",
        "konan_cache_title": "Kotlin Native / Konan Cache (.konan)",
        "konan_cache_desc": "Downloaded Kotlin Native / Multiplatform toolchains and dependencies.",
        "win_temp_title": "Windows Temp Files (%TEMP% - Android & Gradle)",
        "win_temp_desc": "Temporary files left in Temp from builds or SDK installations.",
        "studio_latest": " • MOST RECENT",
        "studio_older": " • Older version",
        "loc_local": "Local Cache/Data",
        "loc_roaming": "Roaming Config/Plugins",
        "loc_legacy": "Legacy Home Dir",
        "loc_cache": "Cache",
        "loc_config": "Config & Plugins",
        "loc_logs": "Logs",
        "stopping_gradle": "Stopping Gradle daemon processes...",
        "gradle_title": "Gradle",
        "gradle_stopped_ok": "Gradle daemon processes were stopped successfully.",
        "gradle_stop_err": "There was a problem stopping Gradle:\n{err}",
        "gradle_not_found": "No active Gradle executable found in PATH. Make sure Android Studio is closed.",
        "calculating_sizes": "Calculating sizes...",
        "scan_done_no_proj": "Scan complete (projects folder unset or missing).",
        "scanning_projects": "Scanning for build/ and .gradle/ folders...",
        "scan_done_count": "Scan complete ({count} folders found).",
        "info_title": "Info",
        "nothing_selected": "No existing items selected for deletion.",
        "confirm_title": "Confirm Permanent Deletion",
        "confirm_body": (
            "You are about to delete {count} locations (~{size}).\n\n"
            "Make sure Android Studio, emulators, and Gradle processes are closed.\n"
            "Continue?"
        ),
        "deleting_item": "Deleting: {label}...",
        "clean_finished": "Cleanup finished.",
        "warn_title": "Finished with warnings",
        "warn_body": "Some files or folders could not be deleted (possibly locked by an active process):\n\n{preview}",
        "success_title": "Success",
        "success_body": "All selected items were deleted successfully!",
    },
}


class PremiumCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lang = "ro"
        self.os_type = platform.system()
        self.home = Path.home()

        self.selectable_items = {}
        self.project_items = {}
        self.projects_root_var = ctk.StringVar(value=str(self.guess_projects_dir()))
        self.lang_var = ctk.StringVar(value="RO")

        self.title(self.t("window_title"))
        self.geometry("940x740")
        self.minsize(860, 640)

        self.setup_ui()
        self.apply_language_texts()
        self.populate_system_items()
        self.scan_all_async()

    def t(self, key: str, **kwargs) -> str:
        template = TRANSLATIONS.get(self.lang, TRANSLATIONS["ro"]).get(key, key)
        return template.format(**kwargs) if kwargs else template

    def on_language_change(self, choice: str):
        new_lang = "en" if choice.upper() == "EN" else "ro"
        if new_lang == self.lang:
            return
        self.lang = new_lang
        self.title(self.t("window_title"))
        self.apply_language_texts()
        self.scan_all_async()

    def apply_language_texts(self):
        self.header_title_lbl.configure(text=self.t("header_title"))
        self.header_sub_lbl.configure(text=self.t("header_subtitle"))
        self.theme_switch.configure(text=self.t("dark_mode"))

        # Actualizare etichete tab-uri CTkTabview
        try:
            self.tabview._segmented_button._buttons_dict["Sistem, Gradle & IDE"].configure(text=self.t("tab_system"))
        except Exception:
            pass
        try:
            self.tabview._segmented_button._buttons_dict["Foldere Build Proiecte"].configure(text=self.t("tab_projects"))
        except Exception:
            pass

        self.proj_folder_lbl.configure(text=self.t("projects_folder_lbl"))
        self.browse_btn.configure(text=self.t("browse"))
        self.scan_proj_btn.configure(text=self.t("scan"))
        self.select_build_btn.configure(text=self.t("select_all_build"))
        self.deselect_proj_btn.configure(text=self.t("deselect_projects"))

        self.safe_btn.configure(text=self.t("select_safe"))
        self.deselect_all_btn.configure(text=self.t("deselect_all"))
        self.scan_btn.configure(text=self.t("rescan"))
        self.stop_gradle_btn.configure(text=self.t("stop_gradle"))
        self.clean_btn.configure(text=self.t("delete_selected"))
        self.status_lbl.configure(text=self.t("ready"))
        self.update_total_selected()

    def guess_projects_dir(self) -> Path:
        candidates = [
            self.home / "AndroidStudioProjects",
            self.home / "StudioProjects",
            self.home / "Projects",
            self.home / "Documents",
        ]
        for c in candidates:
            if c.exists() and c.is_dir():
                return c
        return self.home

    def find_android_studio_dirs(self):
        found = []

        if self.os_type == "Windows":
            local_app = Path(os.environ.get("LOCALAPPDATA", self.home / "AppData" / "Local"))
            roaming_app = Path(os.environ.get("APPDATA", self.home / "AppData" / "Roaming"))
            for b in [local_app / "Google", roaming_app / "Google"]:
                if b.exists():
                    for item in b.iterdir():
                        if item.is_dir() and "AndroidStudio" in item.name:
                            loc = self.t("loc_local") if "Local" in str(b) else self.t("loc_roaming")
                            found.append((item, loc))
            for item in self.home.iterdir():
                if item.is_dir() and item.name.startswith(".AndroidStudio"):
                    found.append((item, self.t("loc_legacy")))

        elif self.os_type == "Darwin":
            lib = self.home / "Library"
            mapping = [
                (lib / "Caches" / "Google", self.t("loc_cache")),
                (lib / "Application Support" / "Google", self.t("loc_config")),
                (lib / "Logs" / "Google", self.t("loc_logs")),
            ]
            for b, loc in mapping:
                if b.exists():
                    for item in b.iterdir():
                        if item.is_dir() and "AndroidStudio" in item.name:
                            found.append((item, loc))

        else:
            mapping = [
                (self.home / ".cache" / "Google", self.t("loc_cache")),
                (self.home / ".config" / "Google", self.t("loc_config")),
            ]
            for b, loc in mapping:
                if b.exists():
                    for item in b.iterdir():
                        if item.is_dir() and "AndroidStudio" in item.name:
                            found.append((item, loc))

        unique = {}
        for p, loc in found:
            unique[str(p.resolve())] = (p, loc)

        items = list(unique.values())
        items.sort(key=lambda pair: pair[0].stat().st_mtime if pair[0].exists() else 0, reverse=True)

        latest_mtime = items[0][0].stat().st_mtime if items and items[0][0].exists() else None
        result = []
        for p, loc in items:
            mtime = p.stat().st_mtime if p.exists() else 0
            is_latest = latest_mtime is not None and abs(mtime - latest_mtime) < 5
            result.append((p, loc, is_latest))
        return result

    def find_avd_cache_and_snapshots(self):
        avd_root = self.home / ".android" / "avd"
        targets = []
        if not avd_root.exists():
            return targets

        for item in avd_root.iterdir():
            if item.is_dir():
                for sub_name in ["cache.img", "snapshots"]:
                    candidate = item / sub_name
                    if candidate.exists():
                        targets.append(candidate)
                for f in item.rglob("*"):
                    if f.is_file() and (f.name.endswith(".tmp") or "cache" in f.name.lower()):
                        targets.append(f)
        return targets

    def build_system_definitions(self):
        defs = [
            {
                "key": "sys_gradle_caches",
                "group": self.t("group_cache"),
                "title": self.t("gradle_caches_title"),
                "desc": self.t("gradle_caches_desc"),
                "paths": [
                    self.home / ".gradle" / "caches",
                    self.home / ".gradle" / "wrapper" / "dists",
                ],
                "default": True,
            },
            {
                "key": "sys_gradle_daemon",
                "group": self.t("group_cache"),
                "title": self.t("gradle_daemon_title"),
                "desc": self.t("gradle_daemon_desc"),
                "paths": [self.home / ".gradle" / "daemon"],
                "default": True,
            },
            {
                "key": "sys_android_cache",
                "group": self.t("group_cache"),
                "title": self.t("android_cache_title"),
                "desc": self.t("android_cache_desc"),
                "paths": [
                    self.home / ".android" / "cache",
                    self.home / ".android" / "build-cache",
                ],
                "default": True,
            },
            {
                "key": "sys_avd_cache",
                "group": self.t("group_cache"),
                "title": self.t("avd_cache_title"),
                "desc": self.t("avd_cache_desc"),
                "paths": self.find_avd_cache_and_snapshots(),
                "default": False,
            },
            {
                "key": "sys_konan_cache",
                "group": self.t("group_cache"),
                "title": self.t("konan_cache_title"),
                "desc": self.t("konan_cache_desc"),
                "paths": [self.home / ".konan"],
                "default": False,
            },
        ]

        if self.os_type == "Windows":
            local_app = Path(os.environ.get("LOCALAPPDATA", self.home / "AppData" / "Local"))
            temp_dir = local_app / "Temp"
            temp_android = [p for p in temp_dir.glob("*android*") if p.exists()] if temp_dir.exists() else []
            temp_gradle = [p for p in temp_dir.glob("*gradle*") if p.exists()] if temp_dir.exists() else []
            defs.append({
                "key": "sys_os_temp",
                "group": self.t("group_cache"),
                "title": self.t("win_temp_title"),
                "desc": self.t("win_temp_desc"),
                "paths": temp_android + temp_gradle,
                "default": False,
            })

        studio_dirs = self.find_android_studio_dirs()
        for idx, (path, loc, is_latest) in enumerate(studio_dirs):
            tag = self.t("studio_latest") if is_latest else self.t("studio_older")
            defs.append({
                "key": f"as_ver_{idx}_{abs(hash(str(path)))}",
                "group": self.t("group_studio"),
                "title": f"{path.name} ({loc}){tag}",
                "desc": str(path),
                "paths": [path],
                "default": False,
            })

        return defs

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_card = ctk.CTkFrame(self, corner_radius=14)
        header_card.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        header_card.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header_card, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w", padx=18, pady=14)

        self.header_title_lbl = ctk.CTkLabel(
            title_box,
            text="",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.header_title_lbl.pack(anchor="w")

        self.header_sub_lbl = ctk.CTkLabel(
            title_box,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
        )
        self.header_sub_lbl.pack(anchor="w", pady=(2, 0))

        controls_box = ctk.CTkFrame(header_card, fg_color="transparent")
        controls_box.grid(row=0, column=1, padx=18, pady=14)

        self.lang_seg = ctk.CTkSegmentedButton(
            controls_box,
            values=["RO", "EN"],
            variable=self.lang_var,
            command=self.on_language_change,
            width=96,
        )
        self.lang_seg.pack(side="left", padx=(0, 14))

        self.theme_switch = ctk.CTkSwitch(
            controls_box,
            text="",
            command=self.toggle_theme,
        )
        self.theme_switch.select()
        self.theme_switch.pack(side="left")

        self.tabview = ctk.CTkTabview(self, corner_radius=14)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=16, pady=4)

        self.tab_sys = self.tabview.add("Sistem, Gradle & IDE")
        self.tab_proj = self.tabview.add("Foldere Build Proiecte")

        self.tab_sys.grid_columnconfigure(0, weight=1)
        self.tab_sys.grid_rowconfigure(0, weight=1)

        self.sys_scroll = ctk.CTkScrollableFrame(self.tab_sys, corner_radius=10, fg_color="transparent")
        self.sys_scroll.grid(row=0, column=0, sticky="nsew")
        self.sys_scroll.grid_columnconfigure(0, weight=1)

        self.setup_projects_tab()

        footer_card = ctk.CTkFrame(self, corner_radius=14)
        footer_card.grid(row=2, column=0, sticky="ew", padx=16, pady=(8, 14))
        footer_card.grid_columnconfigure(0, weight=1)

        info_row = ctk.CTkFrame(footer_card, fg_color="transparent")
        info_row.grid(row=0, column=0, sticky="ew", padx=18, pady=(12, 6))
        info_row.grid_columnconfigure(0, weight=1)

        self.total_lbl = ctk.CTkLabel(
            info_row,
            text="",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.total_lbl.grid(row=0, column=0, sticky="w")

        self.status_lbl = ctk.CTkLabel(
            info_row,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
        )
        self.status_lbl.grid(row=0, column=1, sticky="e")

        self.progress = ctk.CTkProgressBar(footer_card, height=8, corner_radius=4)
        self.progress.set(0)
        self.progress.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))

        btn_row = ctk.CTkFrame(footer_card, fg_color="transparent")
        btn_row.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 14))

        self.safe_btn = ctk.CTkButton(
            btn_row,
            text="",
            width=125,
            command=self.select_safe_defaults,
        )
        self.safe_btn.pack(side="left", padx=(0, 8))

        self.deselect_all_btn = ctk.CTkButton(
            btn_row,
            text="",
            width=120,
            fg_color=("gray75", "gray30"),
            text_color=("gray10", "gray95"),
            hover_color=("gray65", "gray40"),
            command=self.deselect_all,
        )
        self.deselect_all_btn.pack(side="left", padx=(0, 8))

        self.scan_btn = ctk.CTkButton(
            btn_row,
            text="",
            width=110,
            command=self.scan_all_async,
        )
        self.scan_btn.pack(side="left", padx=(0, 8))

        self.stop_gradle_btn = ctk.CTkButton(
            btn_row,
            text="",
            width=130,
            fg_color="#8a5a00",
            hover_color="#a86e00",
            command=self.stop_gradle_daemons,
        )
        self.stop_gradle_btn.pack(side="left")

        self.clean_btn = ctk.CTkButton(
            btn_row,
            text="",
            width=160,
            font=ctk.CTkFont(weight="bold"),
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=self.confirm_and_clean,
        )
        self.clean_btn.pack(side="right")

    def setup_projects_tab(self):
        self.tab_proj.grid_columnconfigure(0, weight=1)
        self.tab_proj.grid_rowconfigure(2, weight=1)

        top_bar = ctk.CTkFrame(self.tab_proj, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", pady=(4, 8))
        top_bar.grid_columnconfigure(1, weight=1)

        self.proj_folder_lbl = ctk.CTkLabel(top_bar, text="", font=ctk.CTkFont(weight="bold"))
        self.proj_folder_lbl.grid(row=0, column=0, padx=(0, 8))

        ctk.CTkEntry(top_bar, textvariable=self.projects_root_var).grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.browse_btn = ctk.CTkButton(top_bar, text="", width=90, command=self.choose_projects_folder)
        self.browse_btn.grid(row=0, column=2, padx=(0, 6))

        self.scan_proj_btn = ctk.CTkButton(top_bar, text="", width=95, command=self.scan_projects_async)
        self.scan_proj_btn.grid(row=0, column=3)

        sub_bar = ctk.CTkFrame(self.tab_proj, fg_color="transparent")
        sub_bar.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        self.select_build_btn = ctk.CTkButton(
            sub_bar,
            text="",
            width=210,
            command=lambda: self.set_projects_selection(True),
        )
        self.select_build_btn.pack(side="left", padx=(0, 8))

        self.deselect_proj_btn = ctk.CTkButton(
            sub_bar,
            text="",
            width=175,
            fg_color=("gray75", "gray30"),
            text_color=("gray10", "gray95"),
            hover_color=("gray65", "gray40"),
            command=lambda: self.set_projects_selection(False),
        )
        self.deselect_proj_btn.pack(side="left")

        self.proj_scroll = ctk.CTkScrollableFrame(self.tab_proj, corner_radius=10)
        self.proj_scroll.grid(row=2, column=0, sticky="nsew")
        self.proj_scroll.grid_columnconfigure(0, weight=1)

    def toggle_theme(self):
        ctk.set_appearance_mode("Dark" if self.theme_switch.get() else "Light")

    def stop_gradle_daemons(self):
        self.stop_gradle_btn.configure(state="disabled")
        self.status_lbl.configure(text=self.t("stopping_gradle"))

        def worker():
            creation_flags = (
                subprocess.CREATE_NO_WINDOW
                if (self.os_type == "Windows" and hasattr(subprocess, "CREATE_NO_WINDOW"))
                else 0
            )
            cmds = [["gradle", "--stop"]]
            proj_root = Path(self.projects_root_var.get().strip()) if self.projects_root_var.get().strip() else None
            if proj_root and proj_root.exists():
                gradlew_bat = proj_root / "gradlew.bat"
                gradlew_sh = proj_root / "gradlew"
                if self.os_type == "Windows" and gradlew_bat.exists():
                    cmds.append([str(gradlew_bat), "--stop"])
                elif gradlew_sh.exists():
                    cmds.append([str(gradlew_sh), "--stop"])

            executed_ok = False
            last_error = None

            for cmd in cmds:
                try:
                    proc = subprocess.run(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        creationflags=creation_flags,
                        timeout=20,
                    )
                    if proc.returncode == 0:
                        executed_ok = True
                        break
                    last_error = proc.stderr.strip() or proc.stdout.strip()
                except FileNotFoundError:
                    continue
                except Exception as exc:
                    last_error = str(exc)

            def finish_ui():
                self.stop_gradle_btn.configure(state="normal")
                self.status_lbl.configure(text=self.t("ready"))
                if executed_ok:
                    messagebox.showinfo(self.t("gradle_title"), self.t("gradle_stopped_ok"))
                elif last_error:
                    messagebox.showwarning(self.t("gradle_title"), self.t("gradle_stop_err", err=last_error))
                else:
                    messagebox.showinfo(self.t("gradle_title"), self.t("gradle_not_found"))

            self.after(0, finish_ui)

        threading.Thread(target=worker, daemon=True).start()

    def choose_projects_folder(self):
        chosen = filedialog.askdirectory(initialdir=self.projects_root_var.get() or str(self.home))
        if chosen:
            self.projects_root_var.set(chosen)
            self.scan_projects_async()

    def populate_system_items(self):
        prev_states = {k: info["var"].get() for k, info in self.selectable_items.items()}

        for w in self.sys_scroll.winfo_children():
            w.destroy()
        self.selectable_items.clear()

        defs = self.build_system_definitions()
        groups = {}
        for d in defs:
            groups.setdefault(d["group"], []).append(d)

        row_idx = 0
        for group_name, items in groups.items():
            grp_card = ctk.CTkFrame(self.sys_scroll, corner_radius=12)
            grp_card.grid(row=row_idx, column=0, sticky="ew", pady=(0, 10))
            grp_card.grid_columnconfigure(0, weight=1)
            row_idx += 1

            ctk.CTkLabel(
                grp_card,
                text=group_name,
                font=ctk.CTkFont(size=14, weight="bold"),
            ).grid(row=0, column=0, sticky="w", padx=14, pady=(10, 6))

            for i, item in enumerate(items, start=1):
                item_box = ctk.CTkFrame(grp_card, fg_color="transparent")
                item_box.grid(row=i, column=0, sticky="ew", padx=14, pady=4)
                item_box.grid_columnconfigure(0, weight=1)

                initial_val = prev_states.get(item["key"], item["default"])
                var = ctk.BooleanVar(value=initial_val)
                cb = ctk.CTkCheckBox(
                    item_box,
                    text=item["title"],
                    variable=var,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=self.update_total_selected,
                )
                cb.grid(row=0, column=0, sticky="w")

                size_badge = ctk.CTkLabel(
                    item_box,
                    text="...",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=("#1f6feb", "#58a6ff"),
                )
                size_badge.grid(row=0, column=1, sticky="e")

                ctk.CTkLabel(
                    item_box,
                    text=item["desc"],
                    font=ctk.CTkFont(size=11),
                    text_color=("gray45", "gray65"),
                ).grid(row=1, column=0, columnspan=2, sticky="w", padx=(26, 0), pady=(1, 4))

                self.selectable_items[item["key"]] = {
                    "paths": item["paths"],
                    "var": var,
                    "size": 0,
                    "size_lbl": size_badge,
                    "default": item["default"],
                }

    def get_dir_size(self, path: Path) -> int:
        total = 0
        if not path.exists():
            return 0
        try:
            if path.is_file() and not path.is_symlink():
                return path.stat().st_size
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        try:
                            total += os.path.getsize(fp)
                        except OSError:
                            pass
        except OSError:
            pass
        return total

    def format_size(self, size_bytes: int) -> str:
        if size_bytes <= 0:
            return "0 B"
        val = float(size_bytes)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if val < 1024.0:
                return f"{val:.2f} {unit}"
            val /= 1024.0
        return f"{val:.2f} PB"

    def scan_all_async(self):
        self.populate_system_items()
        self.scan_btn.configure(state="disabled")
        self.clean_btn.configure(state="disabled")
        self.status_lbl.configure(text=self.t("calculating_sizes"))

        def worker():
            for _, info in self.selectable_items.items():
                sz = sum(self.get_dir_size(p) for p in info["paths"] if p.exists())
                info["size"] = sz
                self.after(0, lambda lbl=info["size_lbl"], s=sz: lbl.configure(text=self.format_size(s)))

            self.after(0, self.scan_projects_async)

        threading.Thread(target=worker, daemon=True).start()

    def scan_projects_async(self):
        root_str = self.projects_root_var.get().strip()
        root_path = Path(root_str) if root_str else None
        prev_proj_states = {str(item["path"]): item["var"].get() for item in self.project_items.values()}

        for w in self.proj_scroll.winfo_children():
            w.destroy()
        self.project_items.clear()

        if not root_path or not root_path.exists() or not root_path.is_dir():
            self.scan_btn.configure(state="normal")
            self.clean_btn.configure(state="normal")
            self.status_lbl.configure(text=self.t("scan_done_no_proj"))
            self.update_total_selected()
            return

        self.status_lbl.configure(text=self.t("scanning_projects"))

        def worker():
            found_targets = []
            base_depth = len(root_path.parts)
            for dirpath, dirnames, _ in os.walk(root_path):
                cur_path = Path(dirpath)
                depth = len(cur_path.parts) - base_depth
                if depth > 5:
                    dirnames[:] = []
                    continue

                pruned = []
                for d in dirnames:
                    if d in {"build", ".gradle", ".git", "node_modules", ".idea", ".cxx"}:
                        if d in {"build", ".gradle"}:
                            target_dir = cur_path / d
                            proj_name = cur_path.name if cur_path != root_path else "root"
                            found_targets.append((proj_name, d, target_dir))
                    else:
                        pruned.append(d)
                dirnames[:] = pruned

            calculated = []
            for proj_name, f_type, target_dir in found_targets:
                sz = self.get_dir_size(target_dir)
                calculated.append((proj_name, f_type, target_dir, sz))

            calculated.sort(key=lambda x: x[3], reverse=True)
            self.after(0, lambda data=calculated, states=prev_proj_states: self.render_projects_list(data, states))

        threading.Thread(target=worker, daemon=True).start()

    def render_projects_list(self, data, prev_states=None):
        prev_states = prev_states or {}
        for idx, (proj_name, f_type, target_dir, sz) in enumerate(data):
            key = f"proj_{idx}"
            default_checked = f_type == "build"
            checked = prev_states.get(str(target_dir), default_checked)
            var = ctk.BooleanVar(value=checked)

            row = ctk.CTkFrame(self.proj_scroll, corner_radius=8)
            row.grid(row=idx, column=0, sticky="ew", pady=3, padx=2)
            row.grid_columnconfigure(1, weight=1)

            cb = ctk.CTkCheckBox(
                row,
                text=f"{proj_name}  [{f_type}]",
                variable=var,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=self.update_total_selected,
            )
            cb.grid(row=0, column=0, sticky="w", padx=10, pady=8)

            ctk.CTkLabel(
                row,
                text=str(target_dir),
                font=ctk.CTkFont(size=11),
                text_color=("gray45", "gray65"),
            ).grid(row=0, column=1, sticky="w", padx=8)

            ctk.CTkLabel(
                row,
                text=self.format_size(sz),
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("#1f6feb", "#58a6ff"),
            ).grid(row=0, column=2, sticky="e", padx=12)

            self.project_items[key] = {
                "var": var,
                "size": sz,
                "path": target_dir,
            }

        self.scan_btn.configure(state="normal")
        self.clean_btn.configure(state="normal")
        self.status_lbl.configure(text=self.t("scan_done_count", count=len(data)))
        self.update_total_selected()

    def set_projects_selection(self, state: bool):
        for item in self.project_items.values():
            item["var"].set(state)
        self.update_total_selected()

    def select_safe_defaults(self):
        for info in self.selectable_items.values():
            info["var"].set(bool(info.get("default", False)))
        self.set_projects_selection(True)
        self.update_total_selected()

    def deselect_all(self):
        for info in self.selectable_items.values():
            info["var"].set(False)
        self.set_projects_selection(False)
        self.update_total_selected()

    def update_total_selected(self):
        sys_total = sum(info["size"] for info in self.selectable_items.values() if info["var"].get())
        proj_total = sum(item["size"] for item in self.project_items.values() if item["var"].get())
        self.total_lbl.configure(text=self.t("total_selected", size=self.format_size(sys_total + proj_total)))

    def gather_paths_to_delete(self):
        to_delete = []
        for key, info in self.selectable_items.items():
            if info["var"].get():
                for p in info["paths"]:
                    if p.exists():
                        to_delete.append((key, p))

        for key, item in self.project_items.items():
            if item["var"].get() and item["path"].exists():
                to_delete.append((key, item["path"]))

        return to_delete

    def confirm_and_clean(self):
        targets = self.gather_paths_to_delete()
        if not targets:
            messagebox.showinfo(self.t("info_title"), self.t("nothing_selected"))
            return

        total_bytes = sum(self.get_dir_size(p) for _, p in targets)
        ans = messagebox.askyesno(
            self.t("confirm_title"),
            self.t("confirm_body", count=len(targets), size=self.format_size(total_bytes)),
        )
        if not ans:
            return

        self.clean_btn.configure(state="disabled")
        self.scan_btn.configure(state="disabled")
        self.progress.set(0)

        def worker():
            errors = []
            total_count = len(targets)
            for idx, (label, path) in enumerate(targets, start=1):
                self.after(0, lambda l=label: self.status_lbl.configure(text=self.t("deleting_item", label=l)))
                try:
                    if path.is_symlink() or path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path, ignore_errors=False)
                except Exception as exc:
                    errors.append(f"{path}: {exc}")

                prog = idx / total_count
                self.after(0, lambda v=prog: self.progress.set(v))

            self.after(0, lambda errs=errors: self.on_clean_finished(errs))

        threading.Thread(target=worker, daemon=True).start()

    def on_clean_finished(self, errors):
        self.status_lbl.configure(text=self.t("clean_finished"))
        if errors:
            preview = "\n".join(errors[:6])
            messagebox.showwarning(self.t("warn_title"), self.t("warn_body", preview=preview))
        else:
            messagebox.showinfo(self.t("success_title"), self.t("success_body"))

        self.scan_all_async()


if __name__ == "__main__":
    app = PremiumCleanerApp()
    app.mainloop()
