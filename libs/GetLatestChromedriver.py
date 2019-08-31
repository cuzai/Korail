import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import request
import zipfile
import os

def get_path(basic_path = './webdriver') :
    down_path = os.path.join(basic_path, 'chromedriver.zip')
    driver_path = os.path.join(basic_path + '/chromedriver.exe')
    version_path = os.path.join(basic_path, 'version.txt')

    try:
        if not os.path.isdir(basic_path):
            os.mkdir(basic_path)

        chrome_option = Options()
        chrome_option.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_option)
        driver.close()
        with open(version_path, 'r') as r :
            print('chrome_version =', r.read())

        return(driver_path)
    except Exception:
        # download chrome driver
        print('chrome dirver needs to me updated. downloading driver')
        while True:
            try:
                req = requests.get('https://chromedriver.chromium.org/')
                soup = BeautifulSoup(req.content, 'html.parser')
                break
            except Exception:
                pass

        aTag = soup.select_one('.sites-layout-tile.sites-tile-name-content-1 li a')
        version = aTag.text

        version = version.split("\xa0")[1]
        print('chrome_version = ', version)

        down_url = 'https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip'.format(version)

        # extract chrome driver
        while True :
            try :
                request.urlretrieve(down_url, down_path)
                print('download complete')
                break
            except Exception as e :
                pass

        print('extracting files')
        with zipfile.ZipFile(down_path, 'r') as zf :
            zf.extractall(path = basic_path)

        # write the version
        with open(version_path, 'w') as w :
            w.write(version)

        return(os.path.join(driver_path, 'chromedriver'))

if __name__ == '__main__' :
    get_path('./../webdriver')