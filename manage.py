import sys
import os
import utils


def usage():
    '''
    Print usage of this CLI tool 
    '''
    utility_name = os.path.basename(sys.argv[0])
    print(f"""Usage:
    {utility_name} new           : To create a new content html file
    {utility_name} build         : To create static html files based on templates and contents
    {utility_name} new-blog-post : To create a new blog page
    """)

def build_static_site():
    '''
    Build static site from the files in "content" directory 
    '''
    utils.build_html_files()

def build_new_blog_post():
    '''
    Build a new blog post md file under blog dirctory by asking user inputs, 
    and populate a {number}.html file under docs directory
    '''
    f_path = utils.build_new_blog_post()
    print(f"Created: {f_path}")

def cache_update():
    cache_path = utils.create_file_list_cache('blog')
    print(f"Cache updated: {cache_path}")

def create_new_content_file():
    '''
    Create a new content file in 'content' directory
    '''
    content_dict_user_input = utils.ask_contents()
    utils.create_new_content_file(content_dict=content_dict_user_input)

def main():
    '''
    Run utils with argements, or pring this tool's usage
    '''
    func_list = {
        'new': create_new_content_file,
        'build': build_static_site,
        'new-blog-post': build_new_blog_post,
        'cache': cache_update,
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
