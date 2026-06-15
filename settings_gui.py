import re
import tkinter as tk
from tkinter import ttk, messagebox
from config import get_config, update_config, get_default_screenshots_folder
from watcher import show_notification


class SettingsWindow:
    active_instance = None

    def __init__(self, watcher, on_save_callback=None):
        if SettingsWindow.active_instance is not None:
            return

        SettingsWindow.active_instance = self
        self.watcher = watcher
        self.on_save_callback = on_save_callback

        # Configure crisp DPI on Windows
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        # Initialize Tkinter root
        self.root = tk.Tk()
        self.root.title("SnapRenamr v1.0.0 - Settings")
        self.root.geometry("380x220")
        self.root.resizable(False, False)

        # Premium dark theme background
        self.root.configure(bg="#1e1e2e")

        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 380) // 2
        y = (screen_height - 220) // 2
        self.root.geometry(f"380x220+{x}+{y}")

        # Set topmost to prevent window from hiding behind explorer
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Listen to custom events
        self.root.bind("<<BringToFront>>", lambda e: self.bring_to_front())
        self.root.bind("<<ExitApp>>", lambda e: self.root.destroy())

        # Configure custom styling
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background='#1e1e2e')
        style.configure(
            'TLabel', background='#1e1e2e',
            foreground='#cdd6f4', font=('Segoe UI', 10)
        )
        style.configure(
            'TEntry', fieldbackground='#313244',
            foreground='#cdd6f4', insertcolor='#cdd6f4',
            font=('Segoe UI', 10), borderwidth=0
        )

        # Button styles
        style.configure(
            'Save.TButton', background='#89b4fa',
            foreground='#11111b', font=('Segoe UI', 10, 'bold'),
            borderwidth=0, padding=6
        )
        style.map('Save.TButton', background=[('active', '#b4befe')])

        style.configure(
            'Reset.TButton', background='#fab387',
            foreground='#11111b', font=('Segoe UI', 10, 'bold'),
            borderwidth=0, padding=6
        )
        style.map('Reset.TButton', background=[('active', '#f9e2af')])

        style.configure(
            'Cancel.TButton', background='#585b70',
            foreground='#cdd6f4', font=('Segoe UI', 10),
            borderwidth=0, padding=6
        )
        style.map('Cancel.TButton', background=[('active', '#7f849c')])

        # Preview Card Styles
        style.configure('Preview.TFrame', background='#181825', relief='flat')
        style.configure(
            'Preview.TLabel', background='#181825',
            foreground='#a6e3a1', font=('Segoe UI', 9, 'italic')
        )

        # Main container frame
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Load configuration
        config = get_config()

        # StringVars for tracking inputs
        self.prefix_var = tk.StringVar(value=config.get("prefix", "US14"))
        self.number_var = tk.StringVar(value=str(config.get("next_number", 1)))

        # Bind traces for real-time live preview
        self.prefix_var.trace_add("write", lambda *args: self.update_preview())
        self.number_var.trace_add("write", lambda *args: self.update_preview())

        # Two-column layout for Prefix & Next Number
        top_fields = ttk.Frame(main_frame)
        top_fields.pack(fill=tk.X, pady=(0, 10))
        top_fields.columnconfigure(0, weight=3)
        top_fields.columnconfigure(1, weight=1)

        # Prefix
        lbl_prefix = ttk.Label(top_fields, text="Filename Prefix:")
        lbl_prefix.grid(row=0, column=0, sticky=tk.W, pady=(0, 4), padx=(0, 10))
        self.ent_prefix = ttk.Entry(top_fields, textvariable=self.prefix_var)
        self.ent_prefix.grid(row=1, column=0, sticky=tk.EW, padx=(0, 10))

        # Next Number
        lbl_number = ttk.Label(top_fields, text="Next Number:")
        lbl_number.grid(row=0, column=1, sticky=tk.W, pady=(0, 4))
        self.ent_number = ttk.Entry(top_fields, textvariable=self.number_var)
        self.ent_number.grid(row=1, column=1, sticky=tk.EW)

        # Live Preview Box
        preview_frame = ttk.Frame(main_frame, style='Preview.TFrame', padding=10)
        preview_frame.pack(fill=tk.X, pady=(0, 15))

        self.lbl_preview = ttk.Label(
            preview_frame, text="",
            style='Preview.TLabel', wraplength=330
        )
        self.lbl_preview.pack(fill=tk.X)

        # Buttons Frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.btn_reset = ttk.Button(
            btn_frame, text="Reset to 1",
            command=self.on_reset_counter, style='Reset.TButton'
        )
        self.btn_reset.pack(side=tk.LEFT)

        self.btn_cancel = ttk.Button(
            btn_frame, text="Cancel",
            command=self.on_cancel, style='Cancel.TButton'
        )
        self.btn_cancel.pack(side=tk.RIGHT, padx=(8, 0))

        self.btn_save = ttk.Button(
            btn_frame, text="Save & Apply",
            command=self.on_save, style='Save.TButton'
        )
        self.btn_save.pack(side=tk.RIGHT)

        # Initial preview and focus
        self.update_preview()
        self.ent_prefix.focus_set()
        self.root.focus_force()

    def bring_to_front(self):
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.attributes("-topmost", False)
        self.root.focus_force()

    def update_preview(self):
        prefix = self.prefix_var.get().strip()
        number_str = self.number_var.get().strip()

        if not prefix:
            self.lbl_preview.configure(
                text="Preview: Prefix cannot be empty",
                foreground="#f38ba8"
            )
            return

        if not re.match(r"^[a-zA-Z0-9_-]+$", prefix):
            self.lbl_preview.configure(
                text="Preview: Invalid prefix characters "
                     "(only alphanumeric, _ and - allowed)",
                foreground="#f38ba8"
            )
            return

        try:
            if number_str:
                number = int(number_str)
                if number <= 0:
                    raise ValueError
            else:
                number = 1
        except ValueError:
            self.lbl_preview.configure(
                text="Preview: Next Number must be a positive integer",
                foreground="#f38ba8"
            )
            return

        # Generates example filenames
        ex1 = f"{prefix}_{number}.png"
        ex2 = f"{prefix}_{number + 1}.png"
        ex3 = f"{prefix}_{number + 2}.png"
        self.lbl_preview.configure(
            text=f"Next screenshots will be named: {ex1}, {ex2}, {ex3}...",
            foreground="#a6e3a1"
        )

    def on_reset_counter(self):
        self.number_var.set("1")
        self.update_preview()

    def on_save(self):
        prefix = self.prefix_var.get().strip()
        number_str = self.number_var.get().strip()
        watch_folder = get_default_screenshots_folder()

        # Validations
        if not prefix:
            messagebox.showerror(
                "Validation Error",
                "Prefix cannot be empty.", parent=self.root
            )
            return

        if not re.match(r"^[a-zA-Z0-9_-]+$", prefix):
            messagebox.showerror(
                "Validation Error",
                "Prefix can only contain alphanumeric characters, "
                "underscores, and hyphens.", parent=self.root
            )
            return

        try:
            next_number = int(number_str)
            if next_number <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Next Number must be a positive integer.", parent=self.root
            )
            return

        # Update config
        new_config = {
            "prefix": prefix,
            "next_number": next_number,
            "watch_folder": watch_folder
        }
        update_config(new_config)

        # Notify watcher if folder changed and sync memory state
        if self.watcher:
            self.watcher.config = get_config()
            if self.watcher.watch_folder != watch_folder:
                self.watcher.update_watch_folder(watch_folder)

        # Trigger tray refresh
        if self.on_save_callback:
            self.on_save_callback()

        # Desktop notification
        show_notification(
            "Settings Saved",
            f"Prefix: {prefix} | Next Number: {next_number}"
        )

        # Brief confirmation and close
        self.lbl_preview.configure(text="Settings saved!", foreground="#a6e3a1")
        self.btn_save.configure(state='disabled')
        self.btn_reset.configure(state='disabled')
        self.btn_cancel.configure(state='disabled')

        self.root.after(1500, self.root.destroy)

    def on_cancel(self):
        self.on_close()

    def on_close(self):
        SettingsWindow.active_instance = None
        self.root.destroy()

    def run(self):
        self.root.mainloop()
