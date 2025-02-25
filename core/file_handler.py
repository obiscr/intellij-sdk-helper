#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import re
from core.hash_utils import calculate_sha1

class FileProcessor:
    def __init__(self):
        self.home_dir = os.path.expanduser("~")
        
    def process_zip(self, source_directory, zip_file, log_callback):
        try:
            zip_path = os.path.join(source_directory, zip_file)
            log_callback(f"[Processing file]: {zip_path}")
            
            log_callback(f"[Calculating SHA1]...")
            sha1_hash = calculate_sha1(zip_path)
            log_callback(f"[SHA1]: {sha1_hash}")
            
            if self._is_intellij_file(zip_file):
                self._process_intellij_file(source_directory, zip_file, sha1_hash, log_callback)
            else:
                log_callback(f"[WARNING]: File {zip_file} does not appear to be an IntelliJ file. Skipping.")
                
        except Exception as e:
            log_callback(f"[ERROR]: {str(e)}")
            raise
            
    def _is_intellij_file(self, filename):
        lower_name = filename.lower()
        return ('idea' in lower_name) and (lower_name.endswith('.zip') or lower_name.endswith('.jar'))
            
    def _process_intellij_file(self, source_directory, zip_file, sha1_hash, log_callback):
        platform_type = ""
        version = ""
        
        # File name: ideaXX-VERSION[-sources].zip/jar
        match = re.match(r'idea([A-Z]+)-([0-9\.]+)(?:-sources)?(?:\.zip|\.jar)', zip_file)
        if match:
            platform_type = match.group(1)  # IC, IU
            version = match.group(2)        # 2022.2.5, 2024.2.1
            
            log_callback(f"[INFO]: Detected platform type: {platform_type}, version: {version}")
        else:
            log_callback(f"[WARNING]: Could not parse platform type and version from filename: {zip_file}")
            return
        
        target_base_dir = os.path.join(self.home_dir, ".gradle", "caches", "modules-2", "files-2.1", 
                                     "com.jetbrains.intellij.idea", f"idea{platform_type}", version)
        
        target_hash_dir = os.path.join(target_base_dir, sha1_hash)
        
        log_callback(f"[Creating directory]: {target_hash_dir}")
        os.makedirs(target_hash_dir, exist_ok=True)
        
        source_file = os.path.join(source_directory, zip_file)
        target_file = os.path.join(target_hash_dir, zip_file)
        
        log_callback(f"[Copying file to]: {target_file}")
        shutil.copy2(source_file, target_file)
        
        log_callback(f"[SUCCESS]: File processed and copied to Gradle cache structure.")
