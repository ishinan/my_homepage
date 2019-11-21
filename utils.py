"""
File name: utils.py

Feature:
    core engine of a static site generator
    Read template html files and contents html files, and then create static html files

Requirements
    - templates directory: Jinja2 type of template files; e.g. 'base.html', 'blog_base.html'
    - content   directory: contains md files as metadata and html content for each page
    - blog      directory: contains md files as metadata and html content for each page
    - docs      directory: ssg will output final html files to this directory

Future Plan:
    - Add test_build.py and run unittest
    - Add arguements for debugging, test and feature to revert back to previous html files
"""
import os
import datetime
from shutil import copyfile
import logging
import logging.config
import inspect
import json
from jinja2 import Environment, FileSystemLoader
import markdown


# Read log.cfg file for logging congiguration
logging.config.fileConfig('log.cfg')
# Define global cache file name
dir_cache_file_name = '_dir_cache.json'
# To map html file name with title tag

# Order is importnat for nav. So we use list data type
data_nav_list = [
    {'filename': 'index.html', 'title': 'Home'},
    {'filename': 'projects.html', 'title': 'Projects'},
    {'filename': 'blog.html', 'title': 'Blog'},
    {'filename': 'contact.html', 'title': 'Contact'},
]


# Create a list of dictionaries containing page info
pages = []

# Static Blog page info
blog_posts = []

def get_current_datetime():
    '''
    Get year, month, day, hour, min from datetime module
    return:
        datetime dictionary { year, month, day, hour, minute }
    '''
    now = datetime.datetime.now()
    return { 'year': now.strftime('%Y'), 
             'month': now.strftime('%m'),
             'day': now.strftime('%d'),
             'hour': now.strftime('%H'),
             'minute': now.strftime('%M')
            }

def get_current_year():
    '''
    Get current year

    return:
        current_year as integer
    '''
    d = get_current_datetime()
    return d['year']

def ask_contents():
    '''
    Ask user input for 
        'page_title', 'main_subject', 'main_comments', 'body_paragraph',
    '''
    item_list = [ 'page_title', 'main_subject', 'main_comments', 'body_paragraph' ]
    user_input_data = {}
    print("Need inputs for some contents")
    for item in item_list:
        user_input_data[item] = input(f"-> {item}: ")
        if len(user_input_data[item]) == 0:
            user_input_data[item] = "PlaceHolder: " + item

    return user_input_data 

def read_template_html(template_dir=".", template_file_path=""):
    '''
    Read from a template html file and return a Jinja Template object
    parameter:
        template_file_path: string to path to a template html file
    return:
        A Jinja Template object 
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName)

    target_path = os.path.join(template_dir, template_file_path)
    logger.debug(f"template file path: {target_path}" )
    jinja_env = Environment(loader=FileSystemLoader(os.path.dirname(target_path)), 
                      keep_trailing_newline=True)
    return  jinja_env.get_template(os.path.basename(target_path))

def read_html_md_file(file_path):
    '''
    Read a html exntention file and return its content as string
    Read a md exntention file and return its content and meta key values
    parameter: 
        file_path
    return: 
        content [ 'html string', 
                  { 'key': [ 'value', ], 
                    'key': [ 'value' ],
                  },
                ]
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName)

    if file_path.endswith('.html'):
        with open(file_path , 'r') as f_content:
            content_of_html_file = f_content.read()
            return [ content_of_html_file ]
    elif file_path.endswith('.md'):
        with open(file_path , 'r') as f_content:
            content_of_md_file = f_content.read()
            md = markdown.Markdown(extensions=['meta', 'fenced_code', 'codehilite'])
            html_of_md_file = md.convert(content_of_md_file)
            dict_of_md_meta_data = md.Meta
            return [ html_of_md_file, 
                     dict_of_md_meta_data,
                   ]

    return [ "Could not find a content file(.html or .md)" + file_path, {}, ]

def read_json_file(file_path=dir_cache_file_name):
    '''
    Read a file which contains json formartted stings, convert(load) it and return

    parameters:
        file_path: default _dir_cache.json in the current directory

    return
        object loaded from the file content
            Python       JSON 
            ---------------------
            dict         object 
            list,tuple   array 
            str          string 
            int,float    number 
            True         true 
            False        false 
            None         null 
            ---------------------
    '''
    content = None
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f_json:
            content = json.load(f_json)
    return content

def write_content_to_file(file_path, file_content, metadata={'title': "Default"}):
    '''
    Write content to a file 
        if destination_path is html, write content to it
        if destination_path is md, write metadata and content to it
        if destination_path is a json, write content to it by json format
    parameter:
        file_path: a path to html file
        file_content: html content string
        metadata: metadata dict for md file, at least 'title' is required
    return: 
        None
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName)

    content = ""
    if file_path.endswith('.html'):
        content = file_content
    elif file_path.endswith('.md'):
        for key, value in metadata.items():
            content += f"{key}: {value}\n"
        content += '\n\n' + file_content

    with open(file_path, 'w') as f_target:
        if file_path.endswith('.json'):
            json.dump(file_content, f_target)
        else:
            f_target.writelines(content)
        logger.info(f"Created {file_path}")
        return file_path

    return "Could not write to a file: " + file_path

def create_page_list(content_dir='content', content_type='md', target_dir='docs'):
    '''
    This is a generator.
    Read a list of content html files under a content directory
    Return a dict of content path, target path, title, html name(without html extention)
    
    An example of a dictionary:
    {
        'content_path': 'content/index.md',
        'file_name': 'index,
        'html_name': 'index.html',
        'target_path': 'docs/index.html',
        'title': 'Home',
    }

    parameters:
        content_dir: default: 'content'
        content_type: file exntension: .md or .html (default: md)
        target_dir: default: 'docs'
    return:
        a dictionary of 'content_path', 'file_name', 'html_name', 'target_path', 'title' 
    '''
    for curr_dir, list_dirs, list_files in os.walk(content_dir):
        # This lambda is to parse only '.html' or '.md' extention files
        for content_file in filter(lambda fname: fname.endswith(content_type), list_files):
            # This could be either, .html or .md file path
            content_path = os.path.join(curr_dir, content_file)
            # content file name and extension
            content_file_name, ext = os.path.splitext(content_file)
            # target_path is an html file path
            target_file_name = content_file_name + ".html"
            target_path = os.path.join(target_dir, target_file_name)

            yield {
                    'content_path': content_path,
                    'file_name': content_file_name,
                    'html_name': target_file_name,
                    'target_path': target_path,
                  }

def create_blog_metadata_list(blog_page_list=[]):
    '''
    Create a list which contains each blog's metadata by reading each blog page md file

    parameters:
        blog_page_list: a list of blog pages
    return:
        list of metadata of blog pages
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName)

    list_blog_metadata = []
    if len(blog_page_list) > 0:
        for blog_page in blog_page_list:
            logger.debug(f"blog_page: {blog_page}")
            _, meta_data = read_html_md_file(blog_page['content_path'])
            meta_data['html_name'] = blog_page['html_name']
            list_blog_metadata.append(meta_data)

    if  len(list_blog_metadata) > 0:
        list_blog_metadata = sorted(list_blog_metadata , key=lambda x: int(x['html_name'].replace(".html", "")), reverse=True )
    return list_blog_metadata 

def create_full_html_content(template_content, nav_list=[], html_info={}, list_blog_info=[]):
    '''
    Build a full conetent of html file
    Return a html content as a string of html content
    parameters:
        template_content: Jinja Template object 
        nav_list: a list of dictionaries of "filename" and "title" for each page
        html_info: a dictionary about a page
        list_blog_info: if page is a blog, need this to populate a blog summary page
                        This is a list of dictionaries
    return:
        a html conetent as a string
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName)

    meta_data = {}
    content, meta_data = read_html_md_file(html_info['content_path'])
    logger.debug(f"meta_data: {meta_data}" )
    content_dir = os.path.dirname(html_info['content_path'])
    logger.debug(f"content_dir: {content_dir}" )
    # page_title from either md's meta or html_info['title']
    page_title = meta_data['title'][0] if meta_data['title'] else html_info['title']  
    copyright_year = get_current_year()
    full_content = template_content.render(
                    navlinks = nav_list,
                    outputfile = html_info['html_name'],
                    source_path = content_dir,
                    title = page_title,
                    page_content = content,
                    copyright_year = copyright_year, 
                    blog_sections = list_blog_info,
                    blog_page = meta_data,
                    )
    return full_content

def build_html_files(template_dir='templates', content_dir='content', content_type='md', target_dir='docs'):
    '''
    Steps:
        1. Read jinja template files( base.html and blog_base.html )
        2. Create a page list 
        3. Read each content html from page list
        4. Render a jinja template based on the page data
        5. Write the result to a html file
    parameter:
        template_dir: dir path to read 'base.html' template
        content_dir: dir path to read conetnt html files
        content_type: 'html' or 'md'
        target_dir: dir path to write final html files
    return:
        None
        Create html files under target_dir
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName)

    base_template = read_template_html(template_dir=template_dir, template_file_path="base.html")
    blog_template = read_template_html(template_dir=template_dir, template_file_path="blog_base.html")
    each_blog_template = read_template_html(template_dir=template_dir, template_file_path="each_blog_page_base.html")

    # Create html page based on template html and content html files
    pages = [ page for page in create_page_list(content_dir=content_dir, content_type='md', target_dir=target_dir) ]
                
    # Combine template, content, meta data
    for page in pages:
        logger.debug(f"page: {page}")
        if page['file_name'] == 'blog':
            list_blog_pages = [ page for page in create_page_list(content_dir='blog', content_type='md', target_dir=target_dir) ]
            list_blog_metadata = create_blog_metadata_list(blog_page_list=list_blog_pages)
            full_content = create_full_html_content(blog_template, data_nav_list, page, list_blog_info=list_blog_metadata)
            for blog_page in list_blog_pages:
                blog_full_content = create_full_html_content(each_blog_template , data_nav_list, blog_page, list_blog_info=list_blog_metadata)
                write_content_to_file(blog_page['target_path'], blog_full_content)
        else:
            full_content = create_full_html_content(base_template, data_nav_list, page)

        write_content_to_file(page['target_path'], full_content)

def create_new_content_file(content_base_template='templates/new_content_base.html', 
                            content_dict={}, content_dir='content', target_name='new_content.md'):
    '''
    Create a new content file
    parameters:
        content_base_template: default "templates/new_content_base.html"
        content_dict: { 'page_title': "value", 
                        'main_subject': "value",
                        'main_comments': "value",
                       }
        content_dir: default "content"
        target_name: 
    return:
        None
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName) 

    # Set content_dict if no parameter is passed
    if len(content_dict) == 0:
        content_dict = { 'page_title': "Placeholder", 
                    'main_subject': "Placeholder",
                    'main_comments': "Placeholder",
                    'body_paragraph': "Placeholder"
                    }
    logger.debug(f"content_dict: {content_dict}")

    new_content_template = read_template_html(content_base_template)
    new_content = new_content_template.render(
                  page_title = content_dict['page_title'],
                  main_subject = content_dict['main_subject'],
                  main_comments = content_dict['main_comments'],
                  body_paragraph = content_dict['body_paragraph'],
                )

    target_path = os.path.join(content_dir, target_name)
    # if os.path.isfile(target_path):
    #     target_path = target_path + datetime.datetime.now()       
    write_content_to_file(target_path, new_content)
    logger.info(f"Created a new content file: {target_path}")

def get_new_blog_file_path(target_dir='blog'):
    '''
    Check 'blog/_dir_cache.json, and find the next file name.
    Return a new file path

    return
        a string file path; e.g. 5.md
    '''
    cache_file_path = os.path.join(target_dir, dir_cache_file_name)
    if not os.path.isfile(cache_file_path):
        create_file_list_cache(target_dir=target_dir)
    cache_content = read_json_file(cache_file_path)

    print(type(cache_content))
    new_file_number = len(cache_content['list_files']) + 1
    new_file_name = str(new_file_number) + ".md"
    os.path.join(target_dir, new_file_name)

    return os.path.join(target_dir, new_file_name)

def create_new_blog_content(target_dir='blog', source_path=''):
    '''
    Read a md file, check metadata, and create a new blog md file in 'blog' dir.
    then, return created blog content in target_dir('blog')

    parameters:
        source_path: user created markdown file containing a blog content and blog metadata
                     required metadata:
                        title, subject, created_date, image, image_alt, short_summary
    return:
        a string name of a path to blog md file (example, 'blog/5.md')
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName) 

    new_file_path = get_new_blog_file_path(target_dir=target_dir)
    if source_path.endswith('.md') and os.path.isfile(source_path):
        copyfile(source_path, new_file_path)

    # Update the cache 
    create_file_list_cache(target_dir=target_dir)
    return new_file_path


def create_file_list_cache(target_dir='.', file_ext='.md'):
    '''
    Create a cache file to keep file list in the directory
         cache file name: _dir_cache.json
         It contains, the diretory name and list of files 
         It is a json format
            {"dir_name": "blog", "list_files": ["5.md", "1.md", "4.md", "3.md", "2.md"], "created_time": "20191120_946"}

    parameter:
        target_dir
    return:
        created file path './blog/_dir.cache'
    '''
    t = get_current_datetime()
    created_time = str(t['year']) + str(t['month']) + str(t['day']) + "_" + str(t['hour']) + str(t['minute'])

    for curr, list_dirs, list_files in os.walk(target_dir):
        if dir_cache_file_name in list_files:
            list_files.remove(dir_cache_file_name)

    cache_content =  { 'dir_name': target_dir,
                       'list_files': list_files, 
                       'created_time': created_time,
                     }
    target_path = os.path.join(target_dir, dir_cache_file_name)
    write_content_to_file(target_path, cache_content)
    return target_path 

def build_new_blog_post():
    '''
    build a new blog post md file under blog dirctory by asking user inputs
        Currently only a markdown file(.md) is accepted
        A provided md file must contain required metadata such as title, subject, image

    return:
        blog_file_path e.g. 'blog/5.md'
    '''
    loggerName = inspect.stack()[0][3]
    logger = logging.getLogger(loggerName) 
    
    user_input_blog_file_path = ''
    while True: 
        file_path = input('Provide a file path to a blog post markdown(.md) file: ')
        if file_path.endswith('.md') and os.path.isfile(file_path):
            user_input_blog_file_path = file_path
            break
        print("Cannot find the markdown(.md) file")

    logger.debug(f"Accepted user input: {user_input_blog_file_path}")
    blog_file_path = create_new_blog_content(source_path=user_input_blog_file_path)

    return blog_file_path


def main():
    build_html_files()
