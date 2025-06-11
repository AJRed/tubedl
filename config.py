import os
from dataclasses import dataclass


def config_error(e):
    print(f"App config error: {e}\nExiting.")
    os.exit()


@dataclass
class AppConfig:
    version: str
    gui_framework: str
    downloader_backend: str
    opts: dict
    params: dict
    gui: dict
    info_text: dict
    thumbnail: dict
    debug: dict
    var: dict
