from bs4 import BeautifulSoup as bs
from lxml import etree

# all functions related to url input processing
def clean_url_data(url:str,
                   request_type:str,
                   parameter_para:str):
    '''Cleans the urls input data'''
    
    parameters = parameter_para.split("\n")
    parameters = parameters_processing(parameters=parameter_para)
    
    return {
        'url': url,
        'request_type': request_type,
        'parameters': parameters
    }

def parameters_processing(parameters:str):
    # just some pre-processing shit

    if parameters != "":
        parameters = parameters.replace("Headers:", "split----here").replace("Payload/Data:", "split----here").replace("Parameters:", "split----here")
        parameters = parameters.split("split----here")
        parameters = parameters[1:]

        parameters = [i.split("\n") for i in parameters]

        dictionarised_headers = {}
        dictionarised_data = {}
        dictionarised_params = {}

        # then iteration
        # splittation
        # addition
        # error handlisation
        for i in parameters[0]:
            if i != "":
                i = i.split(": ")

                try:
                    dictionarised_headers[i[0]] = i[1]
                except IndexError:
                    return "check input data"

        for i in parameters[1]:
            if i != "":
                i = i.split(": ")

                try:
                    dictionarised_data[i[0]] = i[1]
                except IndexError:
                    return "check input data"
        
        for i in parameters[2]:
            if i != "":
                i = i.split(": ")

                try:
                    dictionarised_params[i[0]] = i[1]
                except IndexError:
                    return "check input data"

        return {
            'headers': dictionarised_headers,
            'data': dictionarised_data,
            'params': dictionarised_params
        }
    
    else:
        return {
            'headers': {},
            'data': {},
            'params': {}
        }
    
# all functions related to element input processing
def clean_elements_data(element:str,
                        element_parameters:str,
                        element_type:str):
    '''Cleans the elements input data'''

    parameters = [i.strip() for i in element_parameters.split(",")]
    if parameters[0] == '' and len(parameters) == 1:
        _ = parameters.pop(0)
    
    if element_type.lower() == 'css':
        return {
            'element': css_element_cleaner(element=element),
            'element_parameter': parameters,
            'element_type': element_type
        }

    elif element_type.lower() == 'xpath':
        return {
            'element': xpath_element_cleaner(element=element),
            'element_parameter': parameters,
            'element_type': element_type
        }

def element_type_checker(element:str):
    '''Use this function to check if the user selected the correct input element type'''
    type = ''

    if element.find("/") == 0:
        type = 'xpath'

    elif element.find("<") == 0:
        type = 'css'
    
    else:
        type = 'unknown'

    return type

def css_element_cleaner(element:str):
    element_name = element.split(">")[0].replace("<", "").split(" ")[0]

    element_parts = bs(markup=element, features='lxml').find(element_name).attrs

    if dict(element_parts).get('class') != None:
        classes_stringed = " ".join(i for i in element_parts['class'])
        element_parts['class'] = classes_stringed

    element_parts['name_'] = element_name

    return element_parts

def xpath_element_cleaner(element:str):

    return {
        'xpath': element
    }

def input_element_data_tester(html:str):
    '''Allows the user to test element input data to ensure it meets with app's function standards or whatever'''
    soup = bs(html, features='html.parser')
    elements_count = len(soup.find_all('div'))

    if elements_count <= 1:
        return "meet"
    else:
        return "doesnt meet"

def input_element_data_fixer(html:str):

    return


# all functions related to proxies input data handling
def clean_proxies_data(http_proxies:list,
                       https_proxies:list):
    
    if len(http_proxies) <= 1:
        http_proxies = http_proxies[0]
    
    if len(https_proxies) <= 1:
        https_proxies = https_proxies[0]
    
    return {
        'http://': http_proxies,
        'https://': https_proxies
    }

def clean_settings_data():
    pass


def txt_to_urls_list(path:str):
    file = open(path, 'r').readlines()
    file = [i.split(":") for i in file]
    urls = [i[0] for i in file]
    req_type = [i[1] for i in file]

    return urls, req_type


# all functions related to presetting input data handling