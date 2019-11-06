#!/usr/local/bin/python3
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
from string import Template



# Read log.cfg file for loggeing congiguration
logging.config.fileConfig('log.cfg')

def build_html_files_one_template(content_dir, target_dir):
    '''
    This function read one template html
    Relapace the contents and title and nav's active by tempalate module
    This function opens the target file once
    '''
    title_data = {
        'index': 'Home',
        'blog': 'Blog',
        'projects': 'Projects',
        'contact':  'Contact',
    }

    # Read from one_template.html
    with open('templates/one_template.html', 'r') as f:
        template_html  = f.read()
    template = Template(template_html)

    # Make a list of content files
    for curr, dirs, list_content_files in os.walk(content_dir):
        #print(list_content_files)
        for content_file in list_content_files:
            # Creating paths to contents html and target html
            content_path = os.path.join(curr, content_file)
            target_path = os.path.join(target_dir, content_file)
            html_name = content_file.replace(".html", "")

            # Build the contents of html
            with open(content_path , 'r') as f_content:
                content = f_content.read()

            # print(type(content))
            # print(title_data[html_name])
            # print(template)

            full_contents = template.safe_substitute(
                   title = title_data[html_name],
                   html_content = content
                )

            full_contents = full_contents.replace(f"\" href=\"./{html_name}", f" active\" href=\"./{html_name}")

            # Write to a target file once
            with open(target_path, 'w') as f_target:
                f_target.writelines(full_contents)


def build_html_files(content_dir, target_dir):
    '''
    This function read the top and bottom files once
    This function write the target file once
    '''
    part_top = [] 
    part_bottom = []
    # Read from top.html
    with open('templates/top.html', 'r') as f:
        part_top = f.readlines()
    # Read from bottom.html
    with open('templates/bottom.html', 'r') as f:
        part_bottom = f.readlines()

    # Make a list of content files
    for curr, dirs, list_content_files in os.walk(content_dir):
        #print(list_content_files)
        for content_file in list_content_files:
            
            # Creating paths to contents html and target html
            content_path = os.path.join(curr, content_file)
            target_path = os.path.join(target_dir, content_file)

            # Build the contents of html
            with open(content_path , 'r') as f_content:
                contents = f_content.readlines()
            full_contents = part_top + contents + part_bottom

            # Write to a target file once
            with open(target_path, 'w') as f_target:
                f_target.writelines(full_contents)


if __name__ == "__main__":
    #build_html_files("contents", "docs")
    build_html_files_one_template("contents02", "docs")