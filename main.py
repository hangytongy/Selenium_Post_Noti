from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import requests
import json

def chrome_(url):
    #set up chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the webpage
    driver.get(url)

    # Wait for the page to load (you might need to adjust the sleep time or use WebDriverWait for more complex scenarios)
    time.sleep(10)

    # Find elements with the specified class
    elements = driver.find_elements(By.CLASS_NAME, 'FeedListItem_uid__oE5G0')
    timings = driver.find_elements(By.CLASS_NAME, 'FeedListItem_createdAt__ZFSGG')

    # Extract the text from the elements
    elements = [element.text for element in elements]
    timings = [timing.text for timing in timings ]
    
    # Close the browser
    driver.quit()
    
    return elements, timings

def get_projects(telegram_bot_api,telegram_chat_id):
    
    projects = []
    urls = ["https://debank.com/quest?status=hot","https://debank.com/quest?status=all"]
    
    while True:

        for url in urls:

            elements,timings = chrome_(url)
                    
            for i,element in enumerate(elements):
                if element not in projects:
                    projects.append(element)
                    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {element} added in project list, posted {timings[i]} ago')
                    
                    #send notification
                    message = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {element} added in project list, posted {timings[i]} ago'
                    payload = {'chat_id' : telegram_chat_id,'text' : message}
                    
                elif 'min' in timings[i]:
                    time_ = timings[i]
                    time_ = int(time_[0:time_.index('min')].split()[1])
                    if time_ < 5:
                        #send notification
                        message = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {elements[i]} added in project list, posted {timings[i]} ago'
                        payload = {'chat_id' : telegram_chat_id,'text' : message}
    
                elif 's' in timings[i]:
                    #send notification
                    message = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {elements[i]} added in project list, posted {timings[i]} ago'
                    payload = {'chat_id' : telegram_chat_id,'text' : message}
    
                else:
                    message = None
    
            if message != None:
    
                try: 
                    tele_response = requests.post(telegram_bot_api, json=payload)
    
                    if tele_response.status_code == 200:
                        print("posted successfully")
                    else:
                        print(f"failed to post : {tele_response.status_code}, Response : {tele_response.text}")
    
                except Exception as e:
                    print(f"error posting message {e}")
                    
            time.sleep(300)

if __name__ == '__main__':   
    
    telegram_bot_token = ""
    telegram_bot_api = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    telegram_chat_id = "" #input slack channel ID here
    
    payload = {'chat_id' : telegram_chat_id, 'text' : 'init bot, ignore first notifications'}
    init = requests.post(telegram_bot_api, json=payload)
    
    get_projects(telegram_bot_api,telegram_chat_id)
