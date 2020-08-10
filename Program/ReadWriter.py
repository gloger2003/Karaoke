import json
import os
import sys


def get_description():
    try:
        with open('descs.json', 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        with open('descs.json', 'w', encoding='utf-8') as f:
            data = {}
            for filename in files:
                data[filename] = {
                    'Creator' : '',
                    'Name'    : '',
                    'Genre'   : '',
                    'Date'    : '',
                    'Image'   : '',
                }
            json.dump(data, f, indent=2, ensure_ascii=False)
    return data


def get_media_from_dir():
    path       = sys.path[0] + '/Songs'
    list_dir   = os.listdir(path)
    files      = [file for file in list_dir if file.find('.mp4') != -1]
    path_files = [path + '/' + k for k in files]
    return files, path_files
