from config import AppConfig, config_error
from tk_gui import TkGUI

AppVersion = "0.0.1"
Frontend = "Tk"
Backend = "yt_dlp"


if (__name__ == "__main__"):
    cfg = AppConfig(
        AppVersion,
        Frontend,
        Backend,
        {
            "DL_PLAYLIST": False,
            "SAVE_THUMBNAIL": True,
            "SHOW_THUMBNAIL": False,
            "SKIP_DOWNLOAD": False,
        },
        {
            "download_archive": ".ledger",
            "list_thumbnails": False,
            "quiet": True,
            "no_warnings": True,
            "forcefilename": True,
            "simulate": False,
            "progress_hooks": []
        },
        {
            "OPT_START_COL": 1,
            "OPT_COLS": 2,
            "OPT_START_ROW": 2,
            "OPT_ROWS": 4,
        },
        {
            "IDLE": "Downloads highest quality\n \
                     progressive stream available.",
            "IN_PROGRESS": "Download in progress...",
            "COMPLETE": "Download Complete!",
            "FAILED": "Download Failed, check URL."
        },
        {
            "SIZE": (128, 128)
        },
        {
            "PRINT_KEYS": False,
            "PRINT_UNHANDLED": False
        },
        {
            "URL": "",
            "THREADS": 0
        }
    )

    if cfg.gui_framework == "Tk":
        app = TkGUI(cfg)
        app.component["WINDOW"]["ROOT"].bind("<Key>", app._key_handler)
        app.start()
    else:
        config_error("UnknownFramework")


# PyTube
# from pytube import YouTube
    # def get_video_pytube(self, url):
        # try:
            # yt = YouTube(url)
            # yt.streams.first().download()
            # self.component["LABEL"]["INFO"]["fg"] = "#00AA00"
            # self.component["LABEL"]["INFO"]["text"] = self.cfg.info_text["COMPLETE"]
            # # self.window.update()
            # self.component["WINDOW"]["ROOT"].update()
        # except Exception as e:
            # self.component["LABEL"]["INFO"]["fg"] = "#FF0000"
            # self.component["LABEL"]["INFO"]["text"] = self.cfg.info_text["FAILED"]
            # print(e)
