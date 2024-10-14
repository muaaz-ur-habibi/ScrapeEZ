import os
from datetime import datetime as dt
from urllib.parse import urlparse

import json

def file_name_generator(type:str,
                        url:str):
    url = urlparse(url=url).netloc.replace(".", "_")

    if type == 'page':
        name = f'{dt.today().strftime("%H_%M_%S")}--{str(dt.today()).split(" ")[0]}-{url.replace("/", "")}-webpage.txt'

        return name
    
    elif type == 'element':
        name = f'{dt.today().strftime("%H_%M_%S")}--{str(dt.today()).split(" ")[0]}-{url.replace("/", "")}-elements.json'

        return name

def write_webpage_content(data:str,
                          url:str):
    os.chdir('data/scraped-data')

    path = os.path.abspath(os.curdir)

    with open(f'{path}/{file_name_generator(type="page", url=url)}', 'w', errors='ignore') as file:
        file.write(data)


def write_element_content(json_data:dict,
                          url:str):
    os.chdir('data/scraped-data')

    path = os.path.abspath(os.curdir)
    file_name = file_name_generator(type='element', url=url)

    file = open(f'{path}/{file_name}', 'w', errors='ignore')

    json.dump(fp=file, obj=json_data, indent=4, sort_keys=True)

def prettify_elements_content(json_data:dict,
                              url:str):
    
    return json.dumps({
        'url': url,
        'data': json_data
    }, indent=4, skipkeys=True)