from functools import partial
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from yt_dlp import YoutubeDL

from config import AppConfig


class TkGUI:
    def __init__(self, cfg: AppConfig):
        self.cfg = cfg
        self.cfg.params["progress_hooks"].append(self._on_progress_changed)

        # Create components
        window = tk.Tk()
        frame_main = tk.Frame(master=window)
        # self.thumbnail = ImageTk.PhotoImage(Image.open(".thumbnail.webp"))
        with Image.open(".thumbnail.webp") as im:
            im.thumbnail((128, 128))
            self.thumbnail = ImageTk.PhotoImage(im)

        self.component = {
            "WINDOW": {
                "ROOT": window
            },
            "FRAME": {
                "MAIN": frame_main
            },
            "LABEL": {
                "TITLE": tk.Label(
                    master=frame_main,
                    text="Youtube Downloader"
                ),
                "INFO": tk.Label(
                    master=frame_main,
                    text=self.cfg.info_text["IDLE"]
                ),
                "IMG_THUMB": ThumbnailPane(
                    master=frame_main,
                    image=self.thumbnail
                )
            },
            "BUTTON": {
                "GET": tk.Button(
                    master=frame_main,
                    text="Get",
                    command=self._on_download_button_clicked
                ),
                "LOAD": tk.Button(
                    master=frame_main,
                    text="Load",
                    command=self._on_load_button_clicked
                )
            },
            "FIELD": {
                "URL": tk.Entry(
                    master=frame_main
                )
            },
            "OPTS": {
                "DL_PLAYLIST": OptControl(
                    master=frame_main,
                    label_text="Download Playlist",
                    button_text="ON",
                    command=partial(self.toggle_opt, "DL_PLAYLIST"),
                    show_on_panel=True
                ),
                "SKIP_DOWNLOAD": OptControl(
                    master=frame_main,
                    label_text="Skip Download",
                    button_text="ON",
                    command=partial(self.toggle_opt, "SKIP_DOWNLOAD"),
                    show_on_panel=True
                ),
                "SAVE_THUMBNAIL": OptControl(
                    master=frame_main,
                    label_text="Save Thumbnail",
                    button_text="ON",
                    command=partial(self.toggle_opt, "SAVE_THUMBNAIL"),
                    show_on_panel=True
                ),
                "SHOW_THUMBNAIL": OptControl(
                    master=frame_main,
                    label_text="Show Thumbnail",
                    button_text="ON",
                    command=partial(self.toggle_opt, "SHOW_THUMBNAIL"),
                    show_on_panel=True
                )
            }
        }
        self.component["WINDOW"]["ROOT"].title("TubeDL")
        self.component["WINDOW"]["ROOT"].geometry("320x150")

        # Menu Bar
        commands = {
            "ABOUT": self._on_about_pressed,
            "PREFERENCES": self._on_preferences_pressed,
            "EXIT": self._on_exit_pressed
        }
        self.menu_bar = MenuBar(master=window, commands=commands)

        # Layout
        self.component["FRAME"]["MAIN"].grid(row=1, column=1)
        self.component["LABEL"]["TITLE"].grid(row=1, column=1)

        col_start = self.cfg.gui['OPT_START_COL']
        row_start = self.cfg.gui['OPT_START_ROW']
        col_max = col_start + self.cfg.gui['OPT_COLS']
        row_max = row_start + self.cfg.gui['OPT_ROWS']
        row, column = row_start, col_start
        for con in self.component["OPTS"]:
            if self.component["OPTS"][con].show_on_panel:
                self.component["OPTS"][con].show(row=row, column=column)
                column += 1
                if column >= col_max:
                    column = col_start
                    row += 1
        row += 1
        self.component["BUTTON"]["GET"].grid(row=row, column=0)
        self.component["FIELD"]["URL"].grid(row=row, column=1)
        self.component["LABEL"]["IMG_THUMB"].show(row=row, column=2)
        row += 1
        self.component["BUTTON"]["LOAD"].grid(row=row, column=0)
        self.component["LABEL"]["INFO"].grid(row=row, column=1)

        # Initialize opts to default value
        for opt in self.cfg.opts:
            self.set_opt(opt, self.cfg.opts[opt])

    def set_opt(self, _opt, _val):
        print(f"Set {_opt} to: {self.cfg.opts[_opt]}")
        if _opt in self.cfg.opts.keys():
            if (_opt == "DL_PLAYLIST"):
                self.cfg.opts[_opt] = _val
                self.cfg.params["noplaylist"] = _val

            elif (_opt == "SAVE_THUMBNAIL"):
                self.cfg.opts[_opt] = _val
                self.cfg.params["writethumbnail"] = _val

            elif (_opt == "SKIP_DOWNLOAD"):
                self.cfg.opts[_opt] = _val
                self.cfg.params["skip_download"] = _val

            elif (_opt == "SHOW_THUMBNAIL"):
                self.cfg.opts[_opt] = _val
                if _val:
                    self.component["LABEL"]["IMG_THUMB"].show()
                else:
                    self.component["LABEL"]["IMG_THUMB"].hide()

            self.component["OPTS"][_opt].update_panel(_val)

        else:
            print(f"Error setting option: {_opt} with value: {_val}")
            return

    def get_opt(self, _opt):
        return self.cfg.opts[_opt]

    def toggle_opt(self, _opt):
        _val = not self.get_opt(_opt)
        self.set_opt(_opt, _val)

    def _key_handler(self, event):
        match event.keycode:
            case 9:
                self.component["WINDOW"]["ROOT"].destroy()
            case 36:
                self._on_download_button_clicked()
            case _:
                if self.cfg.debug["PRINT_UNHANDLED"]:
                    print("Key Unhandled")
        if self.cfg.debug["PRINT_KEYS"]:
            print(event.char, event.keysym, event.keycode)

    def start(self):
        self.component["WINDOW"]["ROOT"].mainloop()

    def _on_about_pressed(self):
        # Trigger about window
        pass

    def _on_download_button_clicked(self):
        self.cfg.var["URL"] = self.component["FIELD"]["URL"].get()
        self.component["LABEL"]["INFO"]["fg"] = "#7A7A00"
        self.component["LABEL"]["INFO"]["text"] = self.cfg.info_text["IN_PROGRESS"]
        self.component["WINDOW"]["ROOT"].update()
        self.get_video_ytdlp(self.cfg.var["URL"])

    def _on_load_button_clicked(self):
        url = self.component["FIELD"]["URL"].get()
        self.get_info(url)

    def _on_preferences_pressed(self):
        # Trigger preferences window/screen
        pass

    def _on_exit_pressed(self):
        answer = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if answer:
            self.component["WINDOW"]["ROOT"].destroy()

    def get_info(self, url):
        with YoutubeDL(params=self.cfg.params) as ydl:
            ydl.extract_info(url)

    def get_video_ytdlp(self, url):
        _url = [url]
        print("Starting download with params: ")
        for param, val in self.cfg.params.items():
            print(f"{param}: {val}")

        with YoutubeDL(params=self.cfg.params) as ydl:
            try:
                ydl.download(_url)
                self.component["LABEL"]["INFO"]["fg"] = "#00AA00"
                self.component["LABEL"]["INFO"]["text"] = self.cfg.info_text["COMPLETE"]
            except Exception as e:
                self.component["LABEL"]["INFO"]["fg"] = "#FF0000"
                self.component["LABEL"]["INFO"]["text"] = self.cfg.info_text["FAILED"]
                print(f"Download Error: {e}")

    def _on_progress_changed(self, d):
        print(f"HOOK: {d}")


class ComponentPane(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

    @property
    def show_on_panel(self):
        return self._show_on_panel

    @show_on_panel.setter
    def show_on_panel(self, val):
        self._show_on_panel = val
        self.show() if val else self.hide()

    def hide(self):
        self.grid_forget()

    def show(self, row=-1, column=-1):
        if row == -1:
            row = self.row
        else:
            self.row = row

        if column == -1:
            column = self.column
        else:
            self.column = column

        self.grid(row=row, column=column)

    def update_panel(self, _val):
        self.button.configure(
            bg="green" if _val else "red",
            text="ON" if _val else "OFF"
        )


class OptControl(ComponentPane):
    def __init__(self, master=None, label_text="", button_text="", command=None, row=0, column=0, show_on_panel=True):
        super().__init__(master=master)
        self.label = tk.Label(
            master=self,
            text=label_text
        )
        self.button = tk.Button(
            master=self,
            text=button_text,
            bg="green",
            command=command
        )
        self.button.pack(side="left")
        self.label.pack(side="left")

        self._show_on_panel = show_on_panel
        self.row = row
        self.column = column


class ThumbnailPane(ComponentPane):
    def __init__(self, master=None, row=0, column=0, image=None, show_on_panel=True):
        super().__init__(master=master)
        self.image_label = tk.Label(
            master=self,
            image=image
        )
        self.image_label.pack(side="left")

        self._show_on_panel = show_on_panel
        self.row = row
        self.column = column


class MenuBar(tk.Menu):
    def __init__(self, master=None, commands={}):
        super().__init__(master=master)
        self.file_menu = tk.Menu(self, tearoff=False)
        self.edit_menu = tk.Menu(self, tearoff=False)
        self.help_menu = tk.Menu(self, tearoff=False)
        self.prefs_menu = tk.Menu(self.file_menu, tearoff=0)
        self.commands = commands
        # Menu bar setup
        master.configure(menu=self)
        self.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0,
        )
        self.add_cascade(
            label="Edit",
            menu=self.edit_menu,
            underline=0
        )
        self.add_cascade(
            label="Help",
            menu=self.help_menu,
            underline=0
        )

        # File menu
        self.file_menu.add_command(
            label="Preferences",
            command=self.commands["PREFERENCES"],
            underline=0
        )
        self.file_menu.add_command(
            label="Exit",
            command=self.commands["EXIT"],
            underline=1
        )

        # Edit menu

        # Help menu
        self.help_menu.add_command(
            label="About",
            command=self.commands["ABOUT"]
        )

        # Prefs sub - menu
        self.prefs_menu.add_command(label="Keyboard Shortcuts")
        self.prefs_menu.add_command(label="Color Themes")

    def _on_about_pressed(self):
        pass
