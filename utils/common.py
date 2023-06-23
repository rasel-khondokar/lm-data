import argparse
import os

def load_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page',
                        help='start page',
                        default=1)
    parser.add_argument('--end_page',
                        help='end page',
                        default=489)
    parser.add_argument('--book_url',
                        help='book_url',
                        default='https://bdebooks.com/books/1001-motivational-quotes-for-success-by-thomas-j-vilord-by-bdebooks/')
    args = parser.parse_args()
    args.start_page = int(args.start_page)
    args.end_page = int(args.end_page)
    return args

def make_dir_if_not_exists(file_path):
    dirs = file_path.split('/')
    if dirs:
        path = ''
        for dir in dirs:
            if dir:
                path = path + dir + '/'
                if not os.path.exists(path):
                    os.mkdir(path)