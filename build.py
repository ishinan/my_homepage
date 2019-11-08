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


# To map html file name with title tag
title_data = {
    'index': 'Home',
    'blog': 'Blog',
    'projects': 'Projects',
    'contact':  'Contact',
}


def read_template_html(template_file_path=""):
    '''
    Read from a template html file
    parameter:
        template_file_path: string to path to a template html file
    return:
        A Template object 
    '''
    if template_file_path.endswith('.html'):
        with open(template_file_path, 'r') as f:
            template_html  = f.read()
            return Template(template_html)

    return Template("Could not find a template html file")


def read_html_file(file_path):
    '''
    Read a html exntention file and return its content
    parameter: 
        file_path
    return: 
        content list
    '''
    if file_path.endswith('.html'):
        # Read a content html
        with open(file_path , 'r') as f_content:
            content = f_content.read()
            return content

    return "Could not find a content html file" + file_path


def write_html_to_file(file_path, html_content):
    '''
    Write 
    '''
    if file_path.endswith('.html'):
        # Write to a target file once
        with open(file_path, 'w') as f_target:
            f_target.writelines(html_content)
            #logger.info(f"wrote the {html_name} to output file: {target_path}")
            return

    return "Could not find a content html file" + file_path


def create_page_list(content_dir, target_dir):
    '''
    This is a generator.
    Create a list of content html files from content directory
    Return a dict of content path, target path, html name(without html extention)
    {
       'content_path': 'contents/index.html'
       'filename': 'index.html',
       'target_path': 'docs/index.html',
       'title: 'Home', 
    }
    '''
    for curr_dir, list_dirs, list_files in os.walk(content_dir):
        for content_file in filter(lambda fname: fname.endswith('.html'), list_files):
            content_path = os.path.join(curr_dir, content_file)
            target_path = os.path.join(target_dir, content_file)
            # html file name without html extention
            html_name = content_file.replace(".html", "")

            # logger.debug(f"content path: {content_path}")
            # title_data is a dictionary mapping to tile based on html file name
            yield {
                    'content_path': content_path,
                    'html_name': html_name,
                    'target_path': target_path,
                    'title': title_data[html_name]
                  }


def build_html_files02(template_dir, content_dir, target_dir):
    '''
    parameter:
        template_dir: dir path to read a template html file
        content_dir: dir path to read a conetnt html file
        target_dir: dir path to write a final html file
    return:
        None
        Create html files under target_dir

    Following homework02 
    1. Create a page list 
    2. Read base.html
    3. Read each content html from page list
    4. Replace base.html contents based on the page list data 
    5. Write the result to a html file
    '''
    #logger = logging.getLogger(__name__)

    # Creating a template object which contains template html file
    template_path = os.path.join(template_dir, 'base.html')
    template = read_template_html(template_path)

    # Create htlm page based on template html and content html files
    for html_info in create_page_list(content_dir, target_dir):
        content = read_html_file(html_info['content_path'])
        html_file = template.safe_substitute(
            title = html_info['title'],
            html_content = content
        )

        # Add "active" css class for nav
        full_content = html_file.replace(f"\" href=\"./{html_info['html_name']}", f" active\" href=\"./{html_info['html_name']}")

        write_html_to_file(html_info['target_path'], full_content)


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

def main02(template_dir, source_content_dir, target_dir):
    build_html_files02(template_dir, source_content_dir, target_dir)

def main(source_content_dir, target_dir):
    build_html_files(source_content_dir, target_dir)


if __name__ == "__main__":
    #main("content", "docs")
    main02("templates", "content", "docs")