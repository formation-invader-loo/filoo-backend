""" Nessecary setup to run the Backend
"""
import os
from utils.configuration import get_config

def setup_data_dir() -> None:
    """Sets up essential directories for the program to run.

    Returns:
        None:
    """
    data_path = get_config('paths', 'data')
    if not os.path.isdir(data_path):
        os.makedirs(data_path)

    html_path = get_config('paths', 'html')
    if not os.path.isdir(html_path):
        os.makedirs(html_path)

    uploads_path = get_config('paths', 'uploads')
    if not os.path.isdir(uploads_path):
        os.makedirs(uploads_path)
    
    if not os.path.isdir(os.path.join(os.path.dirname(__file__), data_path + '/library')):
        os.makedirs(data_path + '/library')
    
    if not os.path.isdir(os.path.join(os.path.dirname(__file__), data_path + '/collections')):
        os.makedirs(data_path + '/collections')


def main():
    setup_data_dir()


if __name__ == '__main__':
    main()