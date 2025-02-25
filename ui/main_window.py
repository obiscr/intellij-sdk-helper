#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QPushButton, QListWidget, QTextEdit, 
                            QLabel, QFileDialog, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal

from core.file_handler import FileProcessor

class WorkerThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, source_directory, zip_file):
        super().__init__()
        self.source_directory = source_directory
        self.zip_file = zip_file
        self.processor = FileProcessor()
        
    def run(self):
        try:
            self.processor.process_zip(self.source_directory, self.zip_file, self.log_signal.emit)
            self.finished_signal.emit()
        except Exception as e:
            self.log_signal.emit(f"[ERROR]: {str(e)}")
            self.finished_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.zip_files = []
        self.current_worker = None
        self.home_dir = os.path.expanduser("~")
        
    def init_ui(self):
        self.setWindowTitle("IntelliJ SDK Helper")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Source Directory (with ZIP/JAR files):")
        self.dir_input = QLineEdit()
        self.dir_input.setReadOnly(True)
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.browse_btn)
        main_layout.addLayout(dir_layout)
        
        self.file_list = QListWidget()
        main_layout.addWidget(QLabel("ZIP/JAR Files:"))
        main_layout.addWidget(self.file_list)
        
        self.process_btn = QPushButton("Process Selected File")
        self.process_btn.clicked.connect(self.process_file)
        self.process_btn.setEnabled(False)
        main_layout.addWidget(self.process_btn)
        
        main_layout.addWidget(QLabel("Processing Log:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)
        
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Source Directory with ZIP/JAR Files")
        if directory:
            self.dir_input.setText(directory)
            self.scan_for_zip_files(directory)
            
    def scan_for_zip_files(self, directory):
        self.zip_files = []
        self.file_list.clear()
        
        try:
            all_files = os.listdir(directory)
            for file in all_files:
                if file.endswith('.zip') or file.endswith('.jar'):
                    self.zip_files.append(file)
                    self.file_list.addItem(file)
            
            if self.zip_files:
                self.process_btn.setEnabled(True)
                self.log_output.append(f"[INFO]: Found {len(self.zip_files)} ZIP/JAR files in the directory.")
            else:
                self.process_btn.setEnabled(False)
                self.log_output.append("[INFO]: No ZIP/JAR files found in the selected directory.")
        except Exception as e:
            self.log_output.append(f"[ERROR]: Could not scan directory: {str(e)}")
            
    def process_file(self):
        if not self.file_list.currentItem():
            QMessageBox.warning(self, "Warning", "Please select a file to process first.")
            return
            
        selected_file = self.file_list.currentItem().text()
        source_directory = self.dir_input.text()
        
        self.log_output.append(f"[START PROCESSING]: {selected_file}")
        
        self.process_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        
        self.current_worker = WorkerThread(source_directory, selected_file)
        self.current_worker.log_signal.connect(self.append_log)
        self.current_worker.finished_signal.connect(self.on_process_finished)
        self.current_worker.start()
        
    def append_log(self, message):
        self.log_output.append(message)
        
    def on_process_finished(self):
        self.process_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.log_output.append("[FINISHED]")
