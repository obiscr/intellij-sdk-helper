#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from ui.utils import resource_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    default_font = QApplication.font()

    font = QFont("微软雅黑", 8)
    app.setFont(font)

    resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    os.makedirs(resources_dir, exist_ok=True)
    
    window = MainWindow()
    icon_path = resource_path('logo.png')
    window.setWindowIcon(QIcon(icon_path))
    window.show()
    
    sys.exit(app.exec_())
