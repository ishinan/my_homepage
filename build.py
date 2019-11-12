#!/usr/local/bin/python3
"""
Version: 
Feature:
    static site generator
    Read a template html file and contents html files, and create html files

Regquirements
    - templates directory: base html template files: 'base.html' and 'blog_base.html'
    - content dirctory: contains html files as html content for each page
    - docs directory: ssg will output final html files to this directory

Change Log:
    - N/A

Future Plan:
    - Add test_build.py and run unittest
    - Add arguements for debugging, test and feature to revert back to previous html files
"""
import os
import logging
import logging.config
import inspect
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

# blog_posts for place holders
#   <h1>${blog_title}</h1>
#   <p>${blog_summary}</p>
#   <h4>${blog_title}</h4>
#   <p>${blog_main_paragraph}</p>
blog_posts = [
    {
        "content_path": "blog/blog_post_1.html",
        "target_path": "docs/blog_post_1.html",
        "blog_date": "August 3rd, 2019",
        "blog_title": "Planning a summer vacation.",
        "blog_summary": "Planning a summer vacation.",
        "blog_main_paragraph": "Planning a summer vacation.",
    },
    {
        "content_path": "blog/blog_post_2.html",
        "target_path": "docs/blog_post_2.html",
        "blog_date": "September 3rd, 2019",
        "blog_title": "Physical Health Check.",
        "blog_summary": "Physical Health Check.",
        "blog_main_paragraph": "Physical Health Check.",
    },
    {
        "content_path": "blog/blog_post_3.html",
        "target_path": "docs/blog_post_3.html",
        "blog_date": "October 3rd, 2019",
        "blog_title": "Visiting my home town in Japan",
        "blog_summary": "Visiting my home town in Japan",
        "blog_main_paragraph": "Visiting my home town in Japan",
    },
    {
        "content_path": "blog/blog_post_4.html",
        "target_path": "docs/blog_post_4.html",
        "blog_date": "November 3rd, 2019",
        "blog_title": "Looking for peace",
        "blog_summary": "Looking for peace",
        "blog_main_paragraph": "Looking for peace",
    },
]


def read_template_html(template_file_path=""):
    '''
    Read from a template html file and return a Template object
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
    Read a html exntention file and return its content as string
    parameter: 
        file_path
    return: 
        content string
    '''
    if file_path.endswith('.html'):
        # Read a content html
        with open(file_path , 'r') as f_content:
            content = f_content.read()
            return content

    return "Could not find a content html file" + file_path


def write_html_to_file(file_path, html_content):
    '''
    Write html contents to a file 
    parameter:
        file_path: a path to html file
        html_content: html content string
    return: 
        None
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
    Read a list of content html files under a content directory
    Return a dict of content path, target path, title, html name(without html extention)
    
    Example of a dictionary:
    {
        'content_path': 'content/index.html',
        'html_name': 'index',
        'target_path': 'docs/index.html',
        'title': 'Home',
    }

    parameters:
        content_dir:
        target_dir:
    return:
        a dictionary of 'content_path', 'html_name', 'target_path', 'title' 
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


def build_full_html(template_content, html_info={}):
    '''
    Build Full conetent of html file
    Return a html content as a html string
    parameters:
        template_content: Template object 
        html_info: a dictionalry 
    return:
        a html conetent as a string
    '''
    content = read_html_file(html_info['content_path'])
    html_file = template_content.safe_substitute(
        title = html_info['title'],
        page_content = content
    )
    # Add "active" css class for nav
    full_content = html_file.replace(f"\" href=\"./{html_info['html_name']}", f" active\" href=\"./{html_info['html_name']}")

    return full_content


def build_blog_html_files(template_dir='templates', content_dir='blog', target_dir='docs'):
    '''
    Steps:
        1. Read templates/blog_base.html
        2. Create a page list 
        3. Read each content html from page list
        4. Replace the blog_base.html contents based on the page list data 
        5. Write the result to a html file as blog_post_1.html, 2, 3, and so on.
    parameter:
            template_dir: dir path to read 'base.html' template
            content_dir: dir path to read conetnt html files(Not used, place holder for future usage)
            target_dir: dir path to write final html files
    return:
        None
        Create html files under target_dir
    '''
    # Gets the name of the function from where this function is called
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName)

    # Read base.html and create a template object
    template_path = os.path.join(template_dir, 'base.html')
    logger.debug(f"template file path: {template_path}" )
    base_template = read_template_html(template_path)

    # Read blog_base.html and create a template object
    template_path = os.path.join(template_dir, 'blog_base.html')
    logger.debug(f"template file path: {template_path}" )
    blog_template = read_template_html(template_path)

    # Create contents by blog_template
    for c in blog_posts:
        html_blog_content = blog_template.safe_substitute(
            blog_title = c['blog_title'],
            blog_date = c['blog_date'],
            blog_summary = c['blog_summary'],
            blog_main_paragraph = c['blog_main_paragraph'],
        )

        html_file = base_template.safe_substitute(
                title = c['blog_title'],
                page_content = html_blog_content
        )

        # Add "active" css class for nav
        # This is always blog until the main nav include each blog page links
        html_info = { 'html_name': 'blog' }
        full_content = html_file.replace(f"\" href=\"./{html_info['html_name']}", f" active\" href=\"./{html_info['html_name']}")

        write_html_to_file(c['target_path'], full_content)
        logger.info(f"Created {c['target_path']}")


def build_html_files(template_dir='templates', content_dir='content', target_dir='docs'):
    '''
    Steps:
        1. Read base.html
        2. Create a page list 
        3. Read each content html from page list
        4. Replace base.html contents based on the page list data 
        5. Write the result to a html file
    parameter:
        template_dir: dir path to read 'base.html' template
        content_dir: dir path to read conetnt html files
        target_dir: dir path to write final html files
    return:
        None
        Create html files under target_dir
    '''
    # Gets the name of the function from where this function is called
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName)

    # Creating a template object which contains template html file
    template_path = os.path.join(template_dir, 'base.html')
    logger.debug(f"template file path: {template_path}" )
    base_template = read_template_html(template_path)

    # Create htlm page based on template html and content html files
    for html_info in create_page_list(content_dir, target_dir):
        logger.debug(f"htlm_info: {html_info}")
        full_content = build_full_html(base_template, html_info)
        write_html_to_file(html_info['target_path'], full_content)
        logger.info(f"Created {html_info['target_path']}")


def main():
    '''
    main() invokes functions
    '''
    # This create main html files
    build_html_files()

    # This create blog html files
    build_blog_html_files()


if __name__ == "__main__":
    main()