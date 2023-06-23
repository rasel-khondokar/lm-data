import json
import os
import sys

DIR_BASE = os.path.dirname(os.path.realpath(__file__)).replace('app_configs', '')
DIR_REPORT = f'{DIR_BASE}REPORT/'
DIR_RESOURCES = f'{DIR_BASE}resources/'
DIR_ERROR_LOG = 'ERROR/'
FILE_LOG = 'terminal.log'
TIME_ZONE = 'Asia/Dhaka'

APP_MODE_TEST = "test"
APP_MODE_PROD = "prod"


args = sys.argv
if len(args) > 1:
    if args[1] == 'prod':
        print('Running in prod mode!')
        APP_MODE = APP_MODE_PROD
    else:
        if 'uvicorn' in args[0]:
            print('Running in prod mode!')
            APP_MODE = APP_MODE_PROD
        else:
            print('Running in test mode!')
            APP_MODE = APP_MODE_TEST
else:
    print('Running in test mode!')
    APP_MODE = APP_MODE_TEST

FAILD_TOLERATE_POST_LIST = 10
FAILD_TOLERATE_NEW_POST = 200
FAILD_TOLERATE_RELATED_QUESTION = 100
FILE_PAGE_NOT_FOUND_TEXT = 'page_not_found.txt'