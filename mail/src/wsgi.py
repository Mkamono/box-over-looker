import os
import sys

from dotenv import load_dotenv

project_folder: str = "/home/kakerururu/box-over-looker"
load_dotenv(os.path.join(project_folder, ".env"))

path: str = "/home/kakerururu/box-over-looker/mail/src"
if path not in sys.path:
    sys.path.append(path)

# 起動時に読み込むファイルをmain.pyに指定
from main import app as application
