import flet as ft
import os
import sys
import tabbycat_api as tc
from dotenv import load_dotenv
import logging
import coloredlogs
load_dotenv()
tc.config.set_tabbycat_config(null_exception=False, lazy_load=False)
from app import TabbycatApp

def main(page: ft.Page):
    #page.client_storage.clear()
    1
    app = TabbycatApp(page)

coloredlogs.install(logging.DEBUG, logger=logging.getLogger("app"))
coloredlogs.install(logging.WARNING, logger=logging.getLogger())

ft.app(
    main,
    port=8550,
    view=ft.WEB_BROWSER,
    assets_dir="assets",
    upload_dir="assets/uploads"
)