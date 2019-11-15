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

def main():
    '''
    Run utils with argements
    Allowed arguements
    '''

    # If argements is zero, just run simple
    # If argement is more than one, print error
    # If argement is one, and then new or build, run the task
    # This create main html files
    utils.build_html_files_from_base()
    # This create blog html files
    utils.build_blog_html_files_from_blog_base()


if __name__ == '__main__':
    #main()
    usage()
