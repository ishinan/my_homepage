#!/usr/local/bin/python3
"""
Version: 
Feature:
    static site generator
    Read template html files and contents html files, and create html files

Regquirements
    - base template html and content html files
    - docs directory as destination

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

def build_html_files(content_dir, target_dir):
    '''
    This function reads one template html
    Relapace the contents and title by tempalate module
    Add "active" css class for nav by string.replace()
    Write the content to the target file
    '''
    #logger = logging.getLogger(__name__)
    logger = logging.getLogger('dev')

    # Dict key is html file name, value is string for title tag
    title_data = {
        'index': 'Home',
        'blog': 'Blog',
        'projects': 'Projects',
        'contact':  'Contact',
    }
    logger.debug(f"title_data: {title_data}")

    # Read from one_template.html
    with open('templates/base.html', 'r') as f:
        template_html  = f.read()
    template = Template(template_html)

    # Make a list of content files
    for curr, dirs, list_content_files in os.walk(content_dir):
        for content_file in list_content_files:
            # Creating paths to contents html and target html
            content_path = os.path.join(curr, content_file)
            target_path = os.path.join(target_dir, content_file)
            html_name = content_file.replace(".html", "")

            logger.debug(f"content path: {content_path}")

            # Read a content html
            with open(content_path , 'r') as f_content:
                content = f_content.read()

            # Build the full content by template 
            full_contents = template.safe_substitute(
                   title = title_data[html_name],
                   html_content = content
                )

            # Add "active" css class for nav
            full_contents = full_contents.replace(f"\" href=\"./{html_name}", f" active\" href=\"./{html_name}")

            # Write to a target file once
            with open(target_path, 'w') as f_target:
                f_target.writelines(full_contents)
                logger.info(f"wrote the {html_name} to output file: {target_path}")


if __name__ == "__main__":
    build_html_files("content", "docs")