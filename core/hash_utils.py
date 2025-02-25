#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

def calculate_sha1(file_path):
    sha1 = hashlib.sha1()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
            
    return sha1.hexdigest()

def calculate_md5(file_path):
    md5 = hashlib.md5()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            md5.update(chunk)
            
    return md5.hexdigest()
