#!/usr/local/bin/python
"""
Version: 
Feature:
    Read Templates/top.html and bottom.html and Contents html files, and create html files

Regquirements
    - templates/top.html, templates/bottom.html and contents/*.html
    - docs directory

Change Log:
    - N/A

Plan:
    - Check Directories
    - Read files 
    - Write contets to a html file in docs directory
    - Add test_build.py and run unittest
    - Use function style
    - Add arguements for debugging, test and revert 
"""
import os


# Make a list of content files
for curr, dirs, list_content_files in os.walk('contents'):
    #print(list_content_files)
    for content_file in list_content_files:
        # Read top.html and write to a target file
        content_path = os.path.join(curr, content_file)
        target_path = os.path.join('docs', content_file)

        with open('templates/top.html', 'r') as f_content, open(target_path, 'w') as f_target:
            contents = f_content.readlines()
            f_target.writelines(contents)

        # Read a content html and write to a target file
        with open(content_path, 'r') as f_content, open(target_path, 'a') as f_target:
            contents = f_content.readlines()
            f_target.writelines(contents)

        # Read bottom html and write to a target file
        with open('templates/bottom.html', 'r') as f_content, open(target_path, 'a') as f_target:
            contents = f_content.readlines()
            f_target.writelines(contents)

        