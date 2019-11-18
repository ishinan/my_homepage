import sys
import os
import utils

def usage():
    '''
    print usage if arguments is not proper
    '''
    utility_name = os.path.basename(sys.argv[0])
    print(f"""Usage:
    {utility_name} new   : To create a new content html file
    {utility_name} build : To create static html files based on templates and contents
    """)

def build_static_site():
    '''
    build static site from the current content
    '''
    # This create main html files
    utils.build_html_files()


def build_new_blog_post():
    '''
    build a new blog post md file under blog dirctory by asking user inputs, 
    and populate a blog_post_{number}.html file under docs directory
    '''
    utils.build_new_blog_post()

def build_blog_pages_hw3():
    '''
    build each blog pages (homework03)
    '''
    # This create blog html files
    utils.build_blog_html_files_from_blog_base()

def create_new_content_file():
    '''
    create a new content file in 'content' directory
    '''
    content_dict_user_input = utils.ask_contents()
    utils.create_new_content_file(content_dict=content_dict_user_input)

def main():
    '''
    Run utils with argements(new or build). 
    '''
    func_list = {
        'new': create_new_content_file,
        'build': build_static_site,
        'bpages':build_blog_pages_hw3,
        'new-blog-post':build_new_blog_post,
    }
    # Removing python command if this utility is called with a python command
    python_cmd_list = [ 'python', 'python2', 'python3', 'py2', 'py3' ]
    if sys.argv[0] in python_cmd_list:
        sys.argv = sys.argv[1:]

    # Note sys.argv includes the command itself;e.g. 'manage.py new' is two elements
    if len(sys.argv) == 2 and sys.argv[1] in func_list.keys():
           func_list[sys.argv[1]]()
    else:
        options = '|'.join([ x for x in func_list.keys() ])
        print(f"Must have one argument [{options}]")
        usage()


if __name__ == '__main__':
    main()
