# Selenium_Post_Noti
Post notifications if certain conditions are met after scraping the web


## To run on linux

1. Install python and pip
```
sudo apt update
sudo apt install python3 python3-pip -y

```

2. install selenium and WebDriver Manager
```
pip3 install selenium webdriver-manager
```

3. install google chrome
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

4. install chrome driver
```
sudo apt install chromium-chromedriver
```

5. Add in the following code below for the webdriver, this ensures compatability between the driver and the browser (i think)
```
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)