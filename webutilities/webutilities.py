# Class used to stock all the methods used for web exploration

#############
#  Imports  #
#############
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
import time

#############
# Constants #
#############
readme_url = 'https://github.com/que-ro/quest_of_lab_graal/edit/main/README.md'
waiting_time_for_dynamic_loading_content = 2

class WebUtilities:

    # return a chrome webdriver
    @staticmethod
    def get_chrome_driver():
        try:
            # Init chrome driver options
            chrome_options = Options()
            
            # Add headless browser mode
            chrome_options.add_argument("--headless")
            
            # Get driver
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='../webdrivers/chromedriver.exe')
            
        except SessionNotCreatedException as e:
            raise Exception('Error code 0001. Check ' + readme_url + ' to resolve it.')
            
        return driver
        
    # scroll to the bottom of a dynamic loading page
    @staticmethod
    def scroll_bottom_of_dynamic_page(driver):
    
        # Get scroll height.
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:

            # Scroll down to the bottom.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(waiting_time_for_dynamic_loading_content)

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
        
    # return scrapy html response from driver
    @staticmethod
    def get_driver_html_response(driver, request):
    
        # Send request through the browser
        driver.get(request.url)

        # Wait in case of web page download through ajax
        time.sleep(waiting_time_for_dynamic_loading_content)
        
        # Scroll down the bottom of the page
        WebUtilities.scroll_bottom_of_dynamic_page(driver)
        
        # Get the body response
        body = driver.page_source
        
        # Return the body as a scrapy html response
        return  HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        
    

    
        
        