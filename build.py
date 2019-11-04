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
    - Add test_build.py and run unittest
    - Add arguements for debugging, test and revert 
"""
import os
import logging
import logging.config


# Read log.cfg file for loggeing congiguration
logging.config.fileConfig('log.cfg')


def build_html_files_01():
    '''
    This function opens the target file three times to append top.html content html and bottom.html
    '''
    # Make a list of content files
    for curr, dirs, list_content_files in os.walk('contents'):
        #print(list_content_files)
        for content_file in list_content_files:
            
            # Creating paths to contents html and target html
            content_path = os.path.join(curr, content_file)
            target_path = os.path.join('docs', content_file)

            # Read top.html and write to a target file
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


def build_html_files_02():
    '''
    This function opens the target file once
    '''

    logger = logging.getLogger(__name__)


    # Make a list of content files
    for curr, dirs, list_content_files in os.walk('contents'):
        #print(list_content_files)
        logger.info("ready a list of files: {}".format(str(list_content_files)))

        for content_file in list_content_files:
            
            # Creating paths to contents html and target html
            content_path = os.path.join(curr, content_file)
            target_path = os.path.join('docs', content_file)

            # Build the contents of html
            list_files_to_combine = ['templates/top.html', content_path, 'templates/bottom.html' ]
            full_contents = []

            for file_to_combine in list_files_to_combine:
                with open(file_to_combine , 'r') as f_content:
                    contents = f_content.readlines()
                full_contents += contents
            
            # Write to a target file once
            with open(target_path, 'w') as f_target:
                f_target.writelines(full_contents)


if __name__ == "__main__":
    build_html_files_02()
        