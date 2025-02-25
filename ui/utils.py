#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QMessageBox

def show_error_message(parent, title, message):
    QMessageBox.critical(parent, title, message)

def show_info_message(parent, title, message):
    QMessageBox.information(parent, title, message)

def show_confirmation_dialog(parent, title, message):
    reply = QMessageBox.question(parent, title, message, 
                                QMessageBox.Yes | QMessageBox.No, 
                                QMessageBox.No)
    return reply == QMessageBox.Yes


def resource_path(relative_path):
    try:
        # Temp folder created by PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Normal python env
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)