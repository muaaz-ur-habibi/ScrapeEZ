from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

# importing my own shit
from backend.input_data_handler import clean_url_data, clean_elements_data, input_element_data_tester, element_type_checker, clean_proxies_data

from backend.scrapers import Scraper


# literally the main function
def main_func():
    # after the scrape enable the export button
    export_logs_button.setDisabled(False)


    # create the scraping thread first

    # getting the settings
    settings = scrape_settings_processing()

    # create a scraper class of all the urls
    w_scraper = Scraper(urls=url_list,
                        elements=element_list,
                        proxies=proxies_list,
                        settings=settings)
    
    scraping_thread = QThread(parent=app)
    
    # connect the signal to the slot
    w_scraper.log_signal.connect(update_logs)

    # move the scraper to the thread
    w_scraper.moveToThread(scraping_thread)

    # start the thread
    scraping_thread.started.connect(lambda: w_scraper.scrape())
    scraping_thread.finished.connect(lambda: w_scraper.stop())
    scraping_thread.finished.connect(lambda: scraping_thread.quit())
    scraping_thread.finished.connect(lambda: scraping_thread.wait())

    scraping_thread.start()

@pyqtSlot(str)
def update_logs(msg):
    logs_text.append(msg)

# this function just deletes all the current data in the app
# like urls, elemments, proxies etc. if the user wants to do that
# but doesnt want to go into each menu and manually delete everything
def DATA_DELETE():
    url_list.clear()
    element_list.clear()
    proxies_list.clear()

    url_view_list.clear()
    element_view_list.clear()
    proxy_list.clear()

    logs_text.append("[INFO] ALL DATA HAS BEEN DELETED.")

def EXPORT_LOGS():
    logs = logs_text.toPlainText()

    with open(f"data/logs_data/logs_at_{datetime.date()}.txt", "w") as logs_file:
        logs_file.write(logs)


# displaying menu functions
def clear_display_frame():
    start_label.hide()

    url_adding_input_label.hide()
    url_adding_input.hide()
    url_request_method.hide()
    url_parameters_label.hide()
    url_parameters_input.hide()
    url_adding_button.hide()
    url_remove_button.hide()
    url_view_list.hide()

    element_input_label.hide()
    element_name_input.hide()
    element_input_type.hide()
    element_value_input_label.hide()
    element_value_input.hide()
    element_for_site_label.hide()
    element_for_site.hide()
    element_add_button.hide()
    element_remove_button.hide()
    element_test_button.hide()
    element_view_list.hide()

    http_proxy_input_label.hide()
    http_proxy_input.hide()
    https_proxy_input_label.hide()
    https_proxy_input.hide()
    proxy_for_site_label.hide()
    proxy_for_site.hide()
    proxy_add_button.hide()
    proxy_remove_button.hide()
    proxy_list.hide()

    info_presets.hide()
    preset_name_label.hide()
    preset_name_input.hide()
    current_presets_label.hide()
    presets_list.hide()
    load_presets_button.hide()
    run_presets_button.hide()

    between_url_scrape_delay_label.hide()
    between_url_scrape_delay.hide()
    between_element_scrape_delay_label.hide()
    between_element_scrape_delay.hide()
    user_agents_rotating_label.hide()
    user_agents_rotating_list.hide()
    timeout_label.hide()
    timeout_input.hide()
    http2_label.hide()
    http2.hide()
    is_dynamic_label.hide()
    is_dynamic.hide()
    redirects_label.hide()
    redirects_input.hide()

    logs_text.hide()
    start_scrape_button.hide()
    export_logs_button.hide()
    status_text.hide()



def display_url_menu():
    clear_display_frame()
    universal_title.setText("<h1>Add URL")
    
    url_adding_input_label.show()
    url_adding_input.show()
    url_request_method.show()
    url_parameters_label.show()
    url_parameters_input.show()
    url_adding_button.show()
    url_remove_button.show()
    url_view_list.show()

def display_element_menu():
    clear_display_frame()
    universal_title.setText("<h1>Add Elements")

    element_input_label.show()
    element_name_input.show()
    element_input_type.show()
    element_value_input_label.show()
    element_value_input.show()
    element_for_site_label.show()
    element_for_site.show()
    element_add_button.show()
    element_remove_button.show()
    element_test_button.show()
    element_view_list.show()

def display_proxy_menu():
    clear_display_frame()
    universal_title.setText("<h1>Add Proxies")

    http_proxy_input_label.show()
    http_proxy_input.show()
    https_proxy_input_label.show()
    https_proxy_input.show()
    proxy_for_site_label.show()
    proxy_for_site.show()
    proxy_add_button.show()
    proxy_remove_button.show()
    proxy_list.show()

def display_presets_menu():
    clear_display_frame()
    universal_title.setText("<h1>Set Presets")

    info_presets.show()
    preset_name_label.show()
    preset_name_input.show()
    current_presets_label.show()
    presets_list.show()
    load_presets_button.show()
    run_presets_button.show()

def display_settings_menu():
    clear_display_frame()
    universal_title.setText("<h1>Scrape Settings")

    between_url_scrape_delay_label.show()
    between_url_scrape_delay.show()
    between_element_scrape_delay_label.show()
    between_element_scrape_delay.show()
    user_agents_rotating_label.show()
    user_agents_rotating_list.show()
    timeout_label.show()
    timeout_input.show()
    http2_label.show()
    http2.show()
    #is_dynamic_label.show()
    #is_dynamic.show()
    redirects_label.show()
    redirects_input.show()

def display_start_menu():
    clear_display_frame()
    universal_title.setText("<h1>Start Scrape")

    logs_text.show()
    start_scrape_button.show()
    export_logs_button.show()
    status_text.show()






# gui button functions
# url button functions
def url_processing_button():
    url = url_adding_input.text()
    request_type = url_request_method.currentText()
    parameters = url_parameters_input.toPlainText()

    if url_validator(url=url) != 'valid':
        universal_alert.setWindowTitle("Error")
        universal_alert.setText("Please supply a valid URL. ScrapeEZ only supports HTTP/HTTPS protocol")
        universal_alert.exec_()

    elif url == "":
        universal_alert.setWindowTitle("Error")
        universal_alert.setText("Please enter a URL")
        universal_alert.exec_()

    elif request_type.lower() == "request type":
        universal_alert.setWindowTitle("Error")
        universal_alert.setText("Please select a request type")
        universal_alert.exec_()

    else:
        # firstly delete it from the text boxes
        url_adding_input.clear()
        url_request_method.setCurrentIndex(0)
        url_parameters_input.clear()
        url_parameters_input.setText("Headers:\n\nPayload/Data:\n\nParameters:\n")
        # do the processing shit here
        cleaned_url_data = clean_url_data(url=url, request_type=request_type, parameter_para=parameters)
        url_list.append(cleaned_url_data)

        # adding the data to the tables and other places
        curr_row_count = url_view_list.rowCount()

        request_type_item = QTableWidgetItem(request_type)
        request_type_item.setFlags(request_type_item.flags() ^ Qt.ItemIsEditable)

        urL_item = QTableWidgetItem(url)
        urL_item.setFlags(urL_item.flags() ^ Qt.ItemIsEditable)

        parameters_item = QTableWidgetItem(parameters)
        parameters_item.setFlags(parameters_item.flags() ^ Qt.ItemIsEditable)

        url_view_list.insertRow(curr_row_count)
        url_view_list.setItem(curr_row_count, 0, request_type_item)
        url_view_list.setItem(curr_row_count, 1, urL_item)
        url_view_list.setItem(curr_row_count, 2, parameters_item)

        # add url to element list as key of dict. then if user wants they can add elements, else just leave it blank
        element_list.append(
            {
                url: []
            }
        )
        # the same for proxies?
        proxies_list.append(
            {
                url: []
            }
        )

        element_for_site.addItem(url)
        proxy_for_site.addItem(url)

def remove_url_item():
    index = url_view_list.currentIndex().row()

    url_view_list.removeRow(index)
    _ = url_list.pop(index)


# element button functions
def element_processing_button():
    element = element_name_input.text()
    element_parameter = element_value_input.text()
    element_site = element_for_site.currentText()
    element_type = element_input_type.currentText()
    type_test = element_type_test()

    if element == "":
        universal_alert.setWindowTitle("Error")
        universal_alert.setText("Please enter an element")
        universal_alert.exec_()
    
    elif element_site == "Select URL":
        universal_alert.setWindowTitle("Error")
        universal_alert.setText("Please select a URL for this element")
        universal_alert.exec_()

    elif type_test == 'NOTOK':
        universal_alert.setWindowTitle("Error")
        universal_alert.setText("Selected element type does not match with computed one. Are you sure you entered the correct type?")
        universal_alert.exec_()

    else:
        # delete textbox values
        element_name_input.clear()
        element_value_input.clear()
        element_for_site.setCurrentIndex(0)

        # do the processing here
        cleaned_element_data = clean_elements_data(element=element, element_parameters=element_parameter, element_type=element_type)

        for i in element_list:
            i = dict(i)

            if element_site == list(i.keys())[0]:
                i[element_site].append(cleaned_element_data)

        # add the data to gui tables
        curr_row_count = element_view_list.rowCount()

        element_view_list.insertRow(curr_row_count)
        element_view_list.setItem(curr_row_count, 0, QTableWidgetItem(element))
        element_view_list.setItem(curr_row_count, 1, QTableWidgetItem(element_parameter))
        element_view_list.setItem(curr_row_count, 2, QTableWidgetItem(element_site))

def element_test():
    element, _ = universal_dialog.getMultiLineText(display_frame, "Test your Element", "ScrapeEZ's element parsing function can only parse one element at a time.\nIf you have a doubt whether the pasted element meets that criteria,\nyou can check it with this tool.\nSimply enter the copied element in the text box below, and hit 'Check'.\n A popup will appear telling you more info")

    if element.strip()== "":
        element_test()
    else:
        meets_or_doesnt = input_element_data_tester(html=element)

        if meets_or_doesnt == "meet":
            universal_alert.setWindowTitle("Info")
            universal_alert.setText("The element meets the criteria")
            universal_alert.exec_()
        elif meets_or_doesnt == "doesnt meet":
            universal_alert.setWindowTitle("Info")
            universal_alert.setText("The element does'nt meet the criteria")
            universal_alert.exec_()

# function that tests the type provided by the user to make sure that they 
# dont enter the wrong type by mistake!
def element_type_test():
    user_type = element_input_type.currentText().lower()
    element = element_name_input.text()

    correct_type = element_type_checker(element=element)

    if correct_type == user_type:
        return 'AOK'
    else:
        return 'NOTOK'

def remove_element_item():
    index = element_view_list.currentIndex().row()

    element_view_list.removeRow(index)
    _ = element_list.pop(index)


# proxy button functions
def proxy_processing_button():
    http_proxies = http_proxy_input.text()
    https_proxies = https_proxy_input.text()
    proxy_url = proxy_for_site.currentText()

    if proxy_url == 'Select URL':
        universal_alert.setWindowTitle("Error")
        universal_alert.setText("Please select a URL")
        universal_alert.exec_()

    elif http_proxies == "" or https_proxies == "":
        universal_alert.setWindowTitle("Error")
        universal_alert.setText("ScrapeEZ requires you to give both HTTP and HTTPS proxies")
        universal_alert.exec_()

    else:
        http_proxies = http_proxies.split(", ")
        https_proxies = https_proxies.split(", ")

        cleaned_proxies_data = clean_proxies_data(http_proxies=http_proxies,
                                               https_proxies=https_proxies)

        # add to the list that will be used for processing
        #proxies_list.append(cleaned_proxies_data)

        for i in proxies_list:
            i = dict(i)

            if list(i.keys())[0] == proxy_url:
                i[proxy_url].append(cleaned_proxies_data)
        
        # add to the gui list
        curr_row_count = proxy_list.rowCount()

        proxy_list.insertRow(curr_row_count)
        proxy_list.setItem(curr_row_count, 0, QTableWidgetItem(proxy_url))
        proxy_list.setItem(curr_row_count, 1, QTableWidgetItem(cleaned_proxies_data['http://']))
        proxy_list.setItem(curr_row_count, 2, QTableWidgetItem(cleaned_proxies_data['https://']))


# scrape settings processing functions
def scrape_settings_processing():
    url_delay = int(between_url_scrape_delay.text()) if between_url_scrape_delay.text() != "" else 0
    element_delay = int(between_element_scrape_delay.text()) if between_element_scrape_delay.text() != "" else 0
    user_agents_list = user_agents_rotating_list.toPlainText().split("\n")
    timeout = int(timeout_input.text()) if timeout_input.text() != "" else None
    dynamism = True if is_dynamic.text() == '✅' else False
    is_http2 = True if http2.text() == '✅' else False
    redirects_to_follow = redirects_input.text()
    
    if redirects_to_follow.lower() == "true":
        redirects_to_follow = True

    elif redirects_to_follow == "":
        redirects_to_follow = False

    else:
        redirects_to_follow = int(redirects_to_follow)

    return {
        "url_delay": url_delay,
        "element_delay": element_delay,
        "user_agents_list": user_agents_list,
        "timeout": timeout,
        "http2": is_http2,
        "dynamism": dynamism,
        "redirects_to_follow": redirects_to_follow
    }

# scrape settings functions
def set_dynamism():
    if is_dynamic.isChecked():
        is_dynamic.setStyleSheet("background: red")
        is_dynamic.setText("❌")
    else:
        is_dynamic.setStyleSheet("background: green")
        is_dynamic.setText("✅")

def set_http():
    if http2.isChecked():
        http2.setStyleSheet("background: red")
        http2.setText("❌")
    else:
        http2.setStyleSheet("background: green")
        http2.setText("✅")

def url_validator(url:str):
    '''Simple function to validate the url provided'''

    if 'http' in url and '.' in url and ':' in url and '//' in url:
        return 'valid'
    else:
        return 'invalid'




# variables that will be used to store the inputted data
url_list = []
element_list = []
proxies_list = []
output_list = []




# main gui program
app = QApplication([])

root = QMainWindow()
root.setFixedSize(800, 550)
root.setWindowTitle("ScrapeEZ")
root.setWindowIcon(QIcon("assets/scrapeez_icon.ico"))

# the two main frames:
# a control which will hold all the nav buttons 
# and a display which will show the actual things

control_frame = QFrame(root)
display_frame = QFrame(root)

control_frame.setFixedSize(200, 525)
control_frame.move(5, 10)
control_frame.setStyleSheet("""
QPushButton:hover {
background: pink;
font-weight: bold;
color: white;
}
""")

display_frame.setFixedSize(585, 525)
display_frame.move(210, 10)


# adding the title
main_heading = QLabel(control_frame)
main_heading.setText("<h2><u>ScrapeEZ</u></h2>")
main_heading.setStyleSheet("border: none;")
main_heading.move(60, 5)

# different menu buttons
url_menu_button = QPushButton(control_frame)
url_menu_button.setFixedSize(160, 40)
url_menu_button.setText("Add URLs")
url_menu_button.move(20, 50)
url_menu_button.clicked.connect(display_url_menu)

elements_menu_button = QPushButton(control_frame)
elements_menu_button.setFixedSize(160, 40)
elements_menu_button.setText("Add Elements")
elements_menu_button.move(20, 100)
elements_menu_button.clicked.connect(display_element_menu)

proxy_menu_button = QPushButton(control_frame)
proxy_menu_button.setFixedSize(160, 40)
proxy_menu_button.setText("Add Proxies")
proxy_menu_button.move(20, 150)
proxy_menu_button.clicked.connect(display_proxy_menu)

presets_menu_button = QPushButton(control_frame)
presets_menu_button.setFixedSize(160, 40)
presets_menu_button.setText("Set/Run Presets")
presets_menu_button.move(20, 200)
presets_menu_button.clicked.connect(display_presets_menu)
presets_menu_button.hide()

settings_menu_button = QPushButton(control_frame)
settings_menu_button.setFixedSize(160, 40)
settings_menu_button.setText("Scrape Settings")
settings_menu_button.move(20, 200)
settings_menu_button.clicked.connect(display_settings_menu)

start_button = QPushButton(control_frame)
start_button.setFixedSize(160, 40)
start_button.setText("Start Scrape")
start_button.move(20, 250)
start_button.clicked.connect(display_start_menu)

clear_everything_button = QPushButton(control_frame)
clear_everything_button.setFixedSize(160, 40)
clear_everything_button.setText("Clear all fields")
clear_everything_button.move(20, 300)


# actual different menu items

# universal GUI elements
# the universal title for all menus
universal_title = QLabel(display_frame)
universal_title.move(10, 10)
universal_title.setFixedWidth(300)
universal_title.setFixedHeight(30)

# universal alert box
universal_alert = QMessageBox()

# universal dialog box
universal_dialog = QInputDialog



# starting menu-ish type display.
universal_title.setText("<h1>ScrapeEZ - scrape easily")

start_label = QLabel(display_frame)
start_label.move(10, 40)
start_label.setFont(QFont("Helvetica", 10))
start_label.setText("""
Welcome to ScrapeEZ, a tool to help you scrape the web easily
To get started, you can view the documentation/manual over @ <insert future webpage link>
                    
Or, alternatively, you can just follow this quick and brief guide.

HOW TO USE:
        STEP 1: URL adding
            Pretty straightforward, just add the URLs to scrape in the box. DO NOT ADD THE
            ENTIRE LIST AT ONCE. Add them one by one. You can also specify any request
            parameters to send with the request.
                    
        STEP 2: Element adding (Optional)
            If you would like to scrape specific elements, or specific parameters of the
            elements from the webpage, you can add them here
                    
        STEP 4: Proxies (Also Optional)
            Got some proxies? Add them here and you can scrape through them
                    
        STEP 4: Request Settings (Also Optional)
            Highly recommended to tweak some of these settings so as to not get blocked
            by anti-bot filters like captchas
                    
        STEP 5: Running
            Finally just go through the data and start the scrape
""")







# actual menu GUIs
# url adding menu
url_adding_input_label = QLabel(display_frame)
url_adding_input_label.setText("URL:")
url_adding_input_label.setFont(QFont("Arial", 10))
url_adding_input_label.move(10, 60)

url_adding_input = QLineEdit(display_frame)
url_adding_input.move(50, 58)
url_adding_input.setFont(QFont("Arial", 10))
url_adding_input.setFixedWidth(300)
url_adding_input.setPlaceholderText("http://example.com")

url_request_method = QComboBox(display_frame)
url_request_method.move(360, 59)
url_request_method.addItems(["Request Type", "GET", "POST"])

# and the parameters as well
url_parameters_label = QLabel(display_frame)
url_parameters_label.setText("URL parameters (if none, just delete all text in here). One per line")
url_parameters_label.setFont(QFont("Arial", 10))
url_parameters_label.move(10, 100)

url_parameters_input = QTextEdit(display_frame)
url_parameters_input.setLineWrapColumnOrWidth(2000)
url_parameters_input.setLineWrapMode(QTextEdit.FixedPixelWidth)
url_parameters_input.setAcceptRichText(False)
url_parameters_input.setFixedSize(440, 130)
url_parameters_input.move(10, 120)
url_parameters_input.setText("Headers:\n\nPayload/Data:\n\nParameters:\n")
url_parameters_input.setStyleSheet("""
background: white;
color: black;
""")

url_adding_button = QPushButton(display_frame)
url_adding_button.setText("Add")
url_adding_button.move(10, 260)
url_adding_button.setFixedSize(80, 40)
url_adding_button.clicked.connect(url_processing_button)

url_remove_button = QPushButton(display_frame)
url_remove_button.setText("Remove")
url_remove_button.move(100, 260)
url_remove_button.setFixedSize(80, 40)
url_remove_button.clicked.connect(remove_url_item)

url_view_list = QTableWidget(display_frame)
url_view_list.setColumnCount(3)
url_view_list.setHorizontalHeaderLabels(["Type", "URL", "Parameters"])
url_view_list.setColumnWidth(0, 50)
url_view_list.setColumnWidth(1, 250)
url_view_list.setColumnWidth(2, 240)
url_view_list.move(10, 310)
url_view_list.setFixedWidth(560)


url_adding_input_label.hide()
url_adding_input.hide()
url_request_method.hide()
url_parameters_label.hide()
url_parameters_input.hide()
url_adding_button.hide()
url_remove_button.hide()
url_view_list.hide()

# elements adding menu
element_input_label = QLabel(display_frame)
element_input_label.setText("Add specific elements to scrape")
element_input_label.move(10, 60)
element_input_label.setFont(QFont("Arial", 10))

element_name_input = QLineEdit(display_frame)
element_name_input.setFont(QFont("Arial", 10))
element_name_input.move(10, 80)
element_name_input.setPlaceholderText("Element")
element_name_input.setFixedWidth(380)

element_input_type = QComboBox(display_frame)
element_input_type.addItems(['CSS', 'XPath'])
element_input_type.setFont(QFont("Arial", 9))
element_input_type.move(400, 80)

element_value_input_label = QLabel(display_frame)
element_value_input_label.setText("Specific parameter(s)(seperated by comma) of this\nelement that you would like to scrape:")
element_value_input_label.setFont(QFont("Arial", 10))
element_value_input_label.move(10, 110)

element_value_input = QLineEdit(display_frame)
element_value_input.setFont(QFont("Arial", 10))
element_value_input.move(235, 124)
element_value_input.setFixedWidth(154)
element_value_input.setPlaceholderText("Element Parameter")

element_for_site_label = QLabel(display_frame)
element_for_site_label.setText("Select the site this element belongs to: ")
element_for_site_label.setFont(QFont("Arial", 10))
element_for_site_label.move(10, 160)

element_for_site = QComboBox(display_frame)
element_for_site.setFixedWidth(270)
element_for_site.move(240, 159)
element_for_site.addItem("Select URL")

element_add_button = QPushButton(display_frame)
element_add_button.setFixedSize(80, 40)
element_add_button.setText("Add")
element_add_button.move(10, 190)
element_add_button.clicked.connect(element_processing_button)

element_remove_button = QPushButton(display_frame)
element_remove_button.setFixedSize(80, 40)
element_remove_button.setText("Remove")
element_remove_button.move(100, 190)
element_remove_button.clicked.connect(remove_element_item)

element_test_button = QPushButton(display_frame)
element_test_button.setFixedSize(80, 40)
element_test_button.setText("Test my\nElement")
element_test_button.move(190, 190)
element_test_button.clicked.connect(element_test)

element_view_list = QTableWidget(display_frame)
element_view_list.setFixedSize(500, 270)
element_view_list.move(10, 240)
element_view_list.setColumnCount(3)
element_view_list.setColumnWidth(0, 220)
element_view_list.setColumnWidth(1, 90)
element_view_list.setColumnWidth(2, 180)
element_view_list.setHorizontalHeaderLabels(["Element", "Parameter", "URL"])



element_input_label.hide()
element_name_input.hide()
element_input_type.hide()
element_value_input_label.hide()
element_value_input.hide()
element_for_site_label.hide()
element_for_site.hide()
element_add_button.hide()
element_remove_button.hide()
element_test_button.hide()
element_view_list.hide()

# proxies adding menu
http_proxy_input_label = QLabel(display_frame)
http_proxy_input_label.setText("HTTP Proxies (seperated by ', '): ")
http_proxy_input_label.setFont(QFont("Arial", 10))
http_proxy_input_label.move(10, 60)

http_proxy_input = QLineEdit(display_frame)
http_proxy_input.setFixedWidth(300)
http_proxy_input.setPlaceholderText("http://proxy.com:port_number")
http_proxy_input.move(200, 58)
http_proxy_input.setFont(QFont("Arial", 10))

https_proxy_input_label = QLabel(display_frame)
https_proxy_input_label.setText("HTTPS Proxies (seperated by ', '): ")
https_proxy_input_label.setFont(QFont("Arial", 10))
https_proxy_input_label.move(10, 90)

https_proxy_input = QLineEdit(display_frame)
https_proxy_input.setFixedWidth(300)
https_proxy_input.setPlaceholderText("https://proxy.com:port_number")
https_proxy_input.move(210, 88)
https_proxy_input.setFont(QFont("Arial", 10))

proxy_for_site_label = QLabel(display_frame)
proxy_for_site_label.setText("Select the URL which will be scraped from this proxy")
proxy_for_site_label.setFont(QFont("Arial", 10))
proxy_for_site_label.move(10, 120)

proxy_for_site = QComboBox(display_frame)
proxy_for_site.setFixedWidth(200)
proxy_for_site.move(10, 140)
proxy_for_site.addItem("Select URL")

proxy_add_button = QPushButton(display_frame)
proxy_add_button.setFixedSize(60, 25)
proxy_add_button.move(230, 137)
proxy_add_button.setText("Add")
proxy_add_button.clicked.connect(proxy_processing_button)

proxy_remove_button = QPushButton(display_frame)
proxy_remove_button.setFixedSize(60, 25)
proxy_remove_button.move(300, 137)
proxy_remove_button.setText("Remove")

proxy_list = QTableWidget(display_frame)
proxy_list.setColumnCount(3)
proxy_list.setColumnWidth(2, 150)
proxy_list.setColumnWidth(1, 150)
proxy_list.setColumnWidth(0, 100)
proxy_list.setHorizontalHeaderLabels(["URL", "HTTP Proxy", "HTTPS Proxy"])
proxy_list.setFixedSize(410, 300)
proxy_list.move(10, 170)


http_proxy_input_label.hide()
http_proxy_input.hide()
https_proxy_input_label.hide()
https_proxy_input.hide()
proxy_for_site_label.hide()
proxy_for_site.hide()
proxy_add_button.hide()
proxy_remove_button.hide()
proxy_list.hide()

# presets menu
info_presets = QLabel(display_frame)
info_presets.setFont(QFont("Arial", 10))
info_presets.move(10, 40)
info_presets.setText(
"""
This menu is for setting/running presets.
Presets essentially allow you to reuse your most common scrapes
See the documentation for more
""")

preset_name_label = QLabel(display_frame)
preset_name_label.setText("Set a name for your preset:")
preset_name_label.move(10, 120)
preset_name_label.setFont(QFont("Arial", 10))

preset_name_input = QLineEdit(display_frame)
preset_name_input.setFont(QFont("Arial", 10))
preset_name_input.setPlaceholderText("Name (case sensitive)")
preset_name_input.move(170, 118)

current_presets_label = QLabel(display_frame)
current_presets_label.setText("Presets you currently have saved: ")
current_presets_label.setFont(QFont("Arial", 10))
current_presets_label.move(10, 160)

presets_list = QListWidget(display_frame)
presets_list.setFixedSize(450, 320)
presets_list.move(10, 190)

load_presets_button = QPushButton(display_frame)
load_presets_button.setText("Load Presets\nfrom Database")
load_presets_button.setFixedSize(90, 40)
load_presets_button.move(475, 190)

run_presets_button = QPushButton(display_frame)
run_presets_button.setText("Run selected\npreset")
run_presets_button.setFixedSize(90, 40)
run_presets_button.move(475, 240)


info_presets.hide()
preset_name_label.hide()
preset_name_input.hide()
current_presets_label.hide()
presets_list.hide()
load_presets_button.hide()
run_presets_button.hide()

# request settings menu
between_url_scrape_delay_label = QLabel(display_frame)
between_url_scrape_delay_label.setText("Delay between scraping each URL: ")
between_url_scrape_delay_label.setFont(QFont("Arial", 10))
between_url_scrape_delay_label.move(10, 60)

between_url_scrape_delay = QLineEdit(display_frame)
between_url_scrape_delay.setFont(QFont("Arial", 10))
between_url_scrape_delay.setPlaceholderText("Delay (in seconds)")
between_url_scrape_delay.move(220, 58)

between_element_scrape_delay_label = QLabel(display_frame)
between_element_scrape_delay_label.setText("Delay between scraping elements in a URL: ")
between_element_scrape_delay_label.setFont(QFont("Arial", 10))
between_element_scrape_delay_label.move(10, 90)

between_element_scrape_delay = QLineEdit(display_frame)
between_element_scrape_delay.setFont(QFont("Arial", 10))
between_element_scrape_delay.setPlaceholderText("Delay (in seconds)")
between_element_scrape_delay.move(270, 88)

user_agents_rotating_label = QLabel(display_frame)
user_agents_rotating_label.setText("User-Agent rotation list:\n(If you are entering user\nagents here be sure to\nnot enter them in the\nweb parameters section\nin URL adding menu)")
user_agents_rotating_label.setFont(QFont("Arial", 10))
user_agents_rotating_label.move(10, 120)

user_agents_rotating_list = QPlainTextEdit(display_frame)
user_agents_rotating_list.setFont(QFont("Arial", 10))
user_agents_rotating_list.move(150, 120)
user_agents_rotating_list.setMaximumHeight(80)
user_agents_rotating_list.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

http2_label = QLabel(display_frame)
http2_label.setText("Use HTTP/2?")
http2_label.setFont(QFont("Arial", 10))
http2_label.move(10, 230)

http2 = QPushButton(display_frame)
http2.setText("✅")
http2.move(95, 226)
http2.setFixedSize(30, 27)
http2.setStyleSheet("background: green;")
http2.setCheckable(True)
http2.clicked.connect(set_http)

timeout_label = QLabel(display_frame)
timeout_label.setFont(QFont("Arial", 10))
timeout_label.setText("Set the timeout value for connection to be established: ")
timeout_label.move(10, 260)

timeout_input = QLineEdit(display_frame)
timeout_input.setPlaceholderText("Timeout (in seconds)")
timeout_input.setFont(QFont("Arial", 10))
timeout_input.move(330, 257)

is_dynamic_label = QLabel(display_frame)
is_dynamic_label.setFont(QFont("Arial", 10))
is_dynamic_label.move(10, 290)
is_dynamic_label.setText("Enable Dynamism:")

is_dynamic = QPushButton(display_frame)
is_dynamic.setCheckable(True)
is_dynamic.setFixedSize(30, 27)
is_dynamic.move(122, 286)
is_dynamic.setText("✅")
is_dynamic.setStyleSheet("background: green;")
is_dynamic.clicked.connect(set_dynamism)

redirects_label = QLabel(display_frame)
redirects_label.setText("Enter the maximum redirects to follow\n(leave blank to disable this following\nredirects or enter TRUE for unlimited\nfollowing)")
redirects_label.setFont(QFont("Arial", 10))
redirects_label.move(10, 290)

redirects_input = QLineEdit(display_frame)
redirects_input.move(235, 291)
redirects_input.setFont(QFont("Arial", 10))
redirects_input.setPlaceholderText("No. of redirects to follow")


between_url_scrape_delay_label.hide()
between_url_scrape_delay.hide()
between_element_scrape_delay_label.hide()
between_element_scrape_delay.hide()
user_agents_rotating_label.hide()
user_agents_rotating_list.hide()
timeout_label.hide()
timeout_input.hide()
http2_label.hide()
http2.hide()
is_dynamic_label.hide()
is_dynamic.hide()
redirects_label.hide()
redirects_input.hide()

# scrape starting widgets
logs_text = QTextEdit(display_frame)
logs_text.setFixedSize(570, 300)
logs_text.move(10, 50)
logs_text.setFont(QFont("Arial", 9))
logs_text.setText("--------------------------------------------------------LOGS START HERE--------------------------------------------------------")
logs_text.setLineWrapColumnOrWidth(5000)
logs_text.setLineWrapMode(QTextEdit.FixedPixelWidth)

start_scrape_button = QPushButton(display_frame)
start_scrape_button.setText("Start")
start_scrape_button.setFixedSize(70, 40)
start_scrape_button.setFont(QFont("Arial", 9))
start_scrape_button.move(10, 360)
start_scrape_button.clicked.connect(main_func)

export_logs_button = QPushButton(display_frame)
export_logs_button.setText("Export\nLogs")
export_logs_button.setFixedSize(70, 40)
export_logs_button.setFont(QFont("Arial", 9))
export_logs_button.setDisabled(True)
export_logs_button.move(90, 360)



status_text = QLabel(display_frame)
status_text.setText("Current Status: NOT STARTED")
status_text.setFont(QFont("Arial", 11))
status_text.move(180, 360)


logs_text.hide()
start_scrape_button.hide()
export_logs_button.hide()
status_text.hide()




root.show()
app.exec_()