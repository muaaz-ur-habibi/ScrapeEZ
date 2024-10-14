# for scraping with default i.e css
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
# for scraping with xpath
from lxml import html
# for scraping with regex
import re

from PyQt5.QtCore import pyqtSignal, QObject

import random

import httpx
from http import HTTPStatus

import time

from .data_writer import write_webpage_content, write_element_content, prettify_elements_content

# the webpage scraper class
# takes urls: must
# other things are meh
class Scraper(QObject):
    # log signal that can emit log messages
    log_signal = pyqtSignal(str)

    def __init__(self,
                 urls:list,
                 elements:list=None,
                 proxies:list=None,
                 settings:dict={},
                 html_lxml='html'):
        QObject.__init__(self)
        
        super().__init__()
        
        self.urls=urls
        self.elements=elements
        self.proxies=proxies
        self.settings=settings
        self.html_or_lxml=html_lxml

        # setting scrape parameters
        self.log_signal.emit("[INFO] SETTING SCRAPE PARAMETERS")

        self.url_delay = self.settings.get('url_delay', 0)
        self.element_delay = self.settings.get('element_delay', 0)
        self.user_agent_rota_list = self.settings.get('user_agents_list', [])
        self.timeout:float = self.settings.get('timeout', None)
        self.http2 = self.settings.get('http2', False)
        http1 = True if self.http2 == False else True
        self.dynamism = self.settings.get('dynamism', False)

        self.following = False

        self.redirects_to_follow = self.settings.get('redirects_to_follow', 0)
        if self.redirects_to_follow != False:
            self.following = True
        else:
            self.following = False


        self.session = httpx.Client(
            timeout=self.timeout,
            http1=http1,
            http2=self.http2,
            follow_redirects=self.following,
            max_redirects=self.redirects_to_follow
        )

    def scrape(self):
        urls_scraped = 0
        total_urls = len(self.urls)

        for i in range(len(self.urls)):
            i = self.urls[i]

            elements = []
            for x in self.elements:
                if list(dict(x).keys())[0] == i['url']:
                    elements.append(x[i['url']])

            self.parameters = i['parameters']

            self.log_signal.emit(f"[INFO] NOW SCRAPING: {i['url']}")
            self.log_signal.emit(f"[INFO] REQUESTS TYPE: {i['request_type']}")

            time.sleep(self.url_delay)

            url = i['url']
            req_type = i['request_type']

            proxy = {}

            for x in self.proxies:
                if list(dict(x).keys())[0] == url:
                    proxy = x[url]

            if proxy != []:
                proxy = proxy[0]

            # setting random user agents if the list isnt empty
            if self.user_agent_rota_list[0] != '':
                self.log_signal.emit("[INFO] SETTING A RANDOM USER AGENT")

                self.parameters['headers']['User-Agent'] = random.choice(self.user_agent_rota_list)
            
            else:
                self.log_signal.emit("[INFO] NO USER AGENT LIST PROVIDED")

            if proxy == []:
                if req_type.upper() == "GET":
                    try:
                        request = self.session.get(url=url,
                                                    headers=self.parameters['headers'],
                                                    #params=self.parameters['params'],
                                                    )

                        if request.status_code == 200:
                            self.log_signal.emit(f"[INFO] REQUEST STATUS: {request.status_code} {HTTPStatus(request.status_code).phrase}")

                            if elements == [[]]:
                                self.log_signal.emit("[INFO] NO ELEMENTS FOUND. PROCEEDING TO PROCESS WEBPAGE")

                                if self.html_or_lxml == 'html':

                                    urls_scraped+=1
                                    self.log_signal.emit("[INFO] SAVING SCRAPED WEBPAGE TO scraped-data FOLDER")
                                    self.scrape_webpage(html_=request.content, url=url)

                                elif self.html_or_lxml == 'lxml':
                                    urls_scraped+=1
                                    pass

                            else:
                                self.log_signal.emit("[INFO] ELEMENTS FOUND. SCRAPING ELEMENTS")

                                urls_scraped+=1

                                self.scrape_elements(html_=request.content, elements=elements, url=url)

                        else:
                            self.log_signal.emit(f"[WARN] REQUEST STATUS: {request.status_code} {HTTPStatus(request.status_code).phrase}")
                            self.log_signal.emit(f"[WARN] REQUEST FOR {url} UNSUCCESSFUL")

                    except httpx.NetworkError as net_err:
                        self.log_signal.emit(f"[ERRR] NETWORK ERROR OCCURED WITH {url}. PLEASE CHECK THE STATUS OF YOUR CONNECTION. ERROR MESSAGE: {net_err}")

                    except httpx.TimeoutException as timeout:
                        self.log_signal.emit(f"[ERRR] CONNECTION TO {url} TIMED OUT. ERROR MESSAGE: {timeout}")
                    
                    except httpx.ProtocolError as proto:
                        self.log_signal.emit(f"[ERRR] PROTOCOL VIOLATION OCCURED WHILE CONNECTING TO {url}. ERROR MESSAGE: {proto}")

                    except httpx.ProxyError as prox:
                        self.log_signal.emit(f"[ERRR] PROXY ERROR OCCURED. ENSURE THE RELIABILITY OF YOUR PROXY. ERROR MESSAGE {prox}")

                    except httpx.RequestError as req_err:
                        self.log_signal.emit(f"[ERRR] REQUEST ERROR. TRY AGAIN IN A BIT. ERROR MESSAGE: {req_err}")
                    
                    except httpx.InvalidURL as wtf:
                        self.log_signal.emit(f"[ERRR] INVALID URL SUPPLIED. ERROR MESSAGE: {wtf}")
            


                elif req_type.upper() == "POST":
                    try:
                        request = self.session.post(url=url,
                                            data=self.parameters['data'],
                                            headers=self.parameters['headers'],
                                            params=self.parameters['params'])
                        
                        
                        if request.status_code == 200:
                            self.log_signal.emit(f"[INFO] REQUEST STATUS: {request.status_code} {HTTPStatus(request.status_code).phrase}")

                            if elements == [[]]:
                                self.log_signal.emit("[INFO] NO ELEMENTS FOUND. PROCEEDING TO PROCESS WEBPAGE")

                                if self.html_or_lxml == 'html':

                                    urls_scraped+=1

                                    self.log_signal.emit("[INFO] SAVING SCRAPED WEBPAGE TO scraped-data FOLDER")
                                    self.scrape_webpage(html_=request.content.decode(), url=url)

                                elif self.html_or_lxml == 'lxml':
                                    
                                    urls_scraped+=1
                                    
                            else:
                                self.log_signal.emit("[INFO] ELEMENTS FOUND. SCRAPING ELEMENTS")

                                urls_scraped+=1

                                self.scrape_elements(html_=request.content, elements=elements, url=url)

                        else:
                            self.log_signal.emit(f"[WARN] REQUEST STATUS: {request.status_code} {HTTPStatus(request.status_code).phrase}")
                            self.log_signal.emit(f"[WARN] REQUEST FOR {url} UNSUCCESSFUL")
                    
                    except httpx.NetworkError as net_err:
                        self.log_signal.emit(f"[ERRR] NETWORK ERROR OCCURED WITH {url}. PLEASE CHECK THE STATUS OF YOUR CONNECTION. ERROR MESSAGE: {net_err}")

                    except httpx.TimeoutException as timeout:
                        self.log_signal.emit(f"[ERRR] CONNECTION TO {url} TIMED OUT. ERROR MESSAGE: {timeout}")
                    
                    except httpx.ProtocolError as proto:
                        self.log_signal.emit(f"[ERRR] PROTOCOL VIOLATION OCCURED WHILE CONNECTING TO {url}. ERROR MESSAGE: {proto}")

                    except httpx.ProxyError as prox:
                        self.log_signal.emit(f"[ERRR] PROXY ERROR OCCURED. ENSURE THE RELIABILITY OF YOUR PROXY. ERROR MESSAGE {prox}")

                    except httpx.RequestError as req_err:
                        self.log_signal.emit(f"[ERRR] REQUEST ERROR. TRY AGAIN IN A BIT. ERROR MESSAGE: {req_err}")
                    
                    except httpx.InvalidURL as wtf:
                        self.log_signal.emit(f"[ERRR] INVALID URL SUPPLIED. ERROR MESSAGE: {wtf}")

                self.log_signal.emit(f"[INFO] URLS SCRAPED SUCCESSFULLY: {urls_scraped}/{total_urls}")
        
            else:
                self.log_signal.emit("[INFO] PROXIES DETECTED. SWITCHING TO PROXY MODE")

                if req_type.upper() == "GET":
                    try:
                        request = httpx.get(url=url,
                                            headers=self.parameters['headers'],
                                            params=self.parameters['params'],
                                            proxies=proxy)

                        if request.status_code == 200:
                            self.log_signal.emit(f"[INFO] REQUEST STATUS: {request.status_code} {HTTPStatus(request.status_code).phrase}")

                            if elements == [[]]:
                                self.log_signal.emit("[INFO] NO ELEMENTS FOUND. PROCEEDING TO PROCESS WEBPAGE")

                                if self.html_or_lxml == 'html':

                                    urls_scraped+=1

                                    self.log_signal.emit("[INFO] SAVING SCRAPED WEBPAGE TO scraped-data FOLDER")
                                    self.scrape_webpage(html_=request.content, url=url)

                                elif self.html_or_lxml == 'lxml':
                                    urls_scraped+=1
                                    pass

                            else:
                                self.log_signal.emit("[INFO] ELEMENTS FOUND. SCRAPING ELEMENTS")

                                urls_scraped+=1

                                self.scrape_elements(html_=request.content, elements=elements, url=url)

                        else:
                            self.log_signal.emit(f"[WARN] REQUEST STATUS: {request.status_code} {HTTPStatus(request.status_code).phrase}")
                            self.log_signal.emit(f"[WARN] REQUEST FOR {url} UNSUCCESSFUL")

                    except httpx.NetworkError as net_err:
                        self.log_signal.emit(f"[ERRR] NETWORK ERROR OCCURED WITH {url}. PLEASE CHECK THE STATUS OF YOUR CONNECTION. ERROR MESSAGE: {net_err}")

                    except httpx.TimeoutException as timeout:
                        self.log_signal.emit(f"[ERRR] CONNECTION TO {url} TIMED OUT. ERROR MESSAGE: {timeout}")
                    
                    except httpx.ProtocolError as proto:
                        self.log_signal.emit(f"[ERRR] PROTOCOL VIOLATION OCCURED WHILE CONNECTING TO {url}. ERROR MESSAGE: {proto}")

                    except httpx.ProxyError as prox:
                        self.log_signal.emit(f"[ERRR] PROXY ERROR OCCURED. ENSURE THE RELIABILITY OF YOUR PROXY. ERROR MESSAGE {prox}")

                    except httpx.RequestError as req_err:
                        self.log_signal.emit(f"[ERRR] REQUEST ERROR. TRY AGAIN IN A BIT. ERROR MESSAGE: {req_err}")
                    
                    except httpx.InvalidURL as wtf:
                        self.log_signal.emit(f"[ERRR] INVALID URL SUPPLIED. ERROR MESSAGE: {wtf}")


                elif req_type.upper() == "POST":
                    try:
                        request = httpx.post(url=url,
                                            data=self.parameters['data'],
                                            headers=self.parameters['headers'],
                                            params=self.parameters['params'],
                                            proxies=self.proxies)
                        
                        if request.status_code == 200:
                            self.log_signal.emit(f"[INFO] REQUEST STATUS: {request.status_code} {HTTPStatus(request.status_code).phrase}")

                            if elements == [[]]:
                                self.log_signal.emit("[INFO] NO ELEMENTS FOUND. PROCEEDING TO PROCESS WEBPAGE")

                                if self.html_or_lxml == 'html':

                                    urls_scraped+=1

                                    self.log_signal.emit("[INFO] SAVING SCRAPED WEBPAGE TO scraped-data FOLDER")
                                    self.scrape_webpage(html_=request.content, url=url)

                                elif self.html_or_lxml == 'lxml':
                                    
                                    urls_scraped+=1
                            
                            else:
                                self.log_signal.emit("[INFO] ELEMENTS FOUND. SCRAPING ELEMENTS")

                                urls_scraped+=1

                                self.scrape_elements(html_=request.content, elements=elements, url=url)

                        else:
                            self.log_signal.emit(f"[WARN] REQUEST STATUS: {request.status_code} {HTTPStatus(request.status_code).phrase}")
                            self.log_signal.emit(f"[WARN] REQUEST FOR {url} UNSUCCESSFUL")
                    
                    except httpx.NetworkError as net_err:
                        self.log_signal.emit(f"[ERRR] NETWORK ERROR OCCURED WITH {url}. CHECK THE STATUS OF THE CONNECTION. ERROR MESSAGE: {net_err}")

                    except httpx.TimeoutException as timeout:
                        self.log_signal.emit(f"[ERRR] CONNECTION TO {url} TIMED OUT. ERROR MESSAGE: {timeout}")
                    
                    except httpx.ProtocolError as proto:
                        self.log_signal.emit(f"[ERRR] PROTOCOL VIOLATION OCCURED WHILE CONNECTING TO {url}. ERROR MESSAGE: {proto}")

                    except httpx.ProxyError as prox:
                        self.log_signal.emit(f"[ERRR] PROXY ERROR OCCURED. ENSURE THE RELIABILITY OF YOUR PROXY. ERROR MESSAGE {prox}")

                    except httpx.RequestError as req_err:
                        self.log_signal.emit(f"[ERRR] REQUEST ERROR. TRY AGAIN IN A BIT. ERROR MESSAGE: {req_err}")
                    
                    except httpx.InvalidURL as wtf:
                        self.log_signal.emit(f"[ERRR] INVALID URL SUPPLIED. ERROR MESSAGE: {wtf}")

                self.log_signal.emit(f"[INFO] URLS SCRAPED SUCCESSFULLY: {urls_scraped}/{total_urls}")
                

    
    def scrape_webpage(self,
                       html_:str,
                       url:str):
        
        soup = bs(html_, features='html5lib')
        soup = soup.prettify()

        write_webpage_content(data=soup, url=url)

    def scrape_elements(self,
                        html_:str,
                        elements:list,
                        url:str):
        elements = elements[0]
        elements_scraped = {
            'css': [],
            'xpath': [],
        }

        num_elems_scrped = 0

        self.log_signal.emit("[INFO] LOADING ELEMENTS FOR SCRAPE")

        soup = bs(html_, features='lxml')
        dom = html.fromstring(html=str(soup).replace("&", "&amp;"))
        
        for element in elements:
            # delaying based on the delay provided
            time.sleep(self.element_delay)
            # different processing based on the different scraping methods
            if element['element_type'].lower() == 'css':
                self.log_signal.emit("[INFO] PARSING ELEMENTS WITH CSS SELECTORS")
                # get all the attributes of the css element
                attributes = dict(element['element'])
                # since we really dont need this. why is this even in here? hmmmm
                to_waste = attributes.pop('name_')

                elem = soup.find_all(element['element']['name_'], attrs=attributes)

                #elem = [self.extract_element_info(i) for i in elem]
                elem = [self.extract_element_info(i) for i in elem]

                elements_scraped['css'].append(elem)

                num_elems_scrped+=1
                
                # ALHAMDULILLAH this works, now just write it all to the logs
            
            elif element['element_type'].lower() == 'xpath':
                self.log_signal.emit("[INFO] PARSING ELEMENTS WITH XPATH PATHS")
                # get the xpath of the xpath (lol)
                xpath = element['element']['xpath']

                # scrape the xpath from the dom
                elem = dom.xpath(xpath)[0]

                text = str(elem.text).strip()
                name = elem.tag
                elem = elem.attrib

                elem['tag'] = name
                elem['text'] = text

                elements_scraped['xpath'].append(elem)

                num_elems_scrped+=1

            elif element['element_type'].lower() == 'regex':
                self.log_signal.emit("[INFO] PARSING WITH REGEX EXPRESSIONS")
                print("Did you implement regex?")
        
        self.log_signal.emit(f"[INFO] {num_elems_scrped}/{len(elements)} ELEMENTS OF {url} SCRAPED SUCCESSFULLY")
        self.log_signal.emit("[INFO] NOW SAVING ELEMENTS TO FILE")


        try:
            write_element_content(elements_scraped, url)
        except Exception as e:
            self.log_signal.emit(f"[ERRR] SAVING FAILED. PRINTING OUTPUT TO CONSOLE INSTEAD. ERROR MESSAGE: {e}")
            self.log_signal.emit
            elements_scraped = prettify_elements_content(elements_scraped, url=url)

            self.log_signal.emit(elements_scraped)

    # for extracting element and element's children info 
    def extract_element_info(self, element):

        element_info = {
            'tag': element.name,
            'attributes': dict(element.attrs),
            'content': element.text,
            'children': []  # Initialize an empty list for children
        }

        # Recursively process children
        for child in element.children:
            if child.name is not None:  # Check if child is a Tag object
                element_info['children'].append(self.extract_element_info(child))

        return element_info