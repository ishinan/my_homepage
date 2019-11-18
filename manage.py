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
    utils.build_html_files_from_base()
    # This create blog html files
    #utils.build_blog_html_files_from_blog_base()

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

def create_new_content_file():
    '''
    create a new content file in 'content' directory
    '''
    content_dict_user_input = ask_contents()
    utils.create_new_content_file(content_dict=content_dict_user_input)

def build_blog_page():
    '''
    Testing to build a blog page 
    '''
    utils.build_blog_html_files_from_blog_base02()

def main():
    '''
    Run utils with argements(new or build). 
    '''
    func_list = {
        'new': create_new_content_file,
        'build': build_static_site,
        'bblog': build_blog_page,
    }
    # Removing python command if this utility is called with a python command
    python_cmd_list = [ 'python', 'python2', 'python3', 'py2', 'py3' ]
    if sys.argv[0] in python_cmd_list:
        sys.argv = sys.argv[1:]

    # Note sys.argv includes the command itself;e.g. 'manage.py new' is two elements
    if len(sys.argv) == 2 and sys.argv[1] in func_list.keys():
           func_list[sys.argv[1]]()
    else:
        print("Must have one argument [new|build]")
        usage()

def main_old():
    '''
    Run utils with argements(new or build). 
    '''
    # This create main html files
    utils.build_html_files_from_base()
    # This create blog html files
    utils.build_blog_html_files_from_blog_base()


if __name__ == '__main__':
    main()
