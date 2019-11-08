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

def read_template(template_file_path):
    '''
    Read from template html file
    Return content of template html
    '''
    with open(template_file_path, 'r') as f:
        template_html  = f.read()
        return Template(template_html)


def create_page_lists(content_dir):
    '''
    Read html files from content directory and create a page list
    Return a list of content path, target path, html name(without html extention)
    pages = [ {
                'content_path': 'contents/index.html'
                'filename': 'index.html',
                'target_path': 'docs/index.html',
              }
            ]
    '''
    pass


def build_html_files02(content_dir, target_dir):
    '''
    Following homework02 
    1. Create a page list 
    2. Read base.html
    3. Read each content html from page list
    4. Replace base.html contents based on the page list data 
    5. Write the result to a html file
    '''
    #logger = logging.getLogger(__name__)
    logger = logging.getLogger('dev')

    pages = [
        {
            "filename": "index.html",
            "title": "Home"
        },
        {
            "filename": "blog.html",
            "title": "Blog"
        },
        {
            "filename": "projects.html",
            "title": "Projects"
        },
        {
            "filename": "contact.html",
            "title": "Contact"
        },
    ]


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


def main(source_content_dir, target_dir):
    build_html_files(source_content_dir, target_dir)


if __name__ == "__main__":
    main("content", "docs")