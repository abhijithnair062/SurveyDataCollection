# Make sure there is no current instance of Tor Browser running before executing this code
import csv
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

binary = '/Applications/Tor Browser.app/Contents/MacOS/firefox'
# the location of

if os.path.exists(binary) is False:
    raise ValueError("The binary path to Tor Firefox does not exist")
firefox_binary = FirefoxBinary(binary)

# following makes the browser invisible
options = Options()
options.add_argument("--headless")

def startup(binary = None, options = None):
    browser = None
    if not browser:
        browser = webdriver.Firefox(firefox_binary=binary,options=options)
    time.sleep(5)
    browser.find_element("xpath",'//*[@id="connectButton"]').click()
    time.sleep(5)
    return browser

# Download each web page locally
def downloadPage(url,filename,driver):
    # driver = get_browser(binary= firefox_binary)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
    currentPage = driver.page_source
    with open(filename,'w') as f:
        f.write(currentPage)
    driver.quit()

def setup():
    imageidcsv = set()
    with open('/Users/abhijithnair/Desktop/RA/TechPro_Robot_Gadget_Wearable.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            column_value = row[2]
            imageidcsv.add(column_value)

        dir = '/Users/abhijithnair/Desktop/RA/MTurkIntegration/robots_wearables_gadgets'
        imageidDir = set()
        for f in os.listdir(dir):
            if os.path.isfile(os.path.join(dir,f)):
                imageidDir.add(str(f).replace(".jpg",""))


        newset = imageidcsv.difference(imageidDir)
        return newset

# Download image in a webpage
def downloadImage(html_path,outputFilePath):
    with open(html_path, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
    image_tags = soup.find_all('img', class_ = 'js-feature-image')
    if len(image_tags) == 0:
        image_tags = soup.find_all('img', class_ = 'aspect-ratio--object bg-black z3')
    img_urls = [tag["src"] for tag in image_tags]
    for url in img_urls:
        response = requests.get(url)
        with open(outputFilePath,"wb") as f:
            f.write(response.content)


index = 9440
html_dir = "temp/"
if not os.path.exists(html_dir):
    os.makedirs(html_dir)
img_dir = "robots_wearables_gadgets_v2/"
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

#     Get the IDs of images which are not processed yet
notProcessed = setup()

with open('/Users/abhijithnair/Desktop/RA/TechPro_V3.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        column_value = row[5]
        imageid = row[2]
        if imageid in notProcessed:
            try:
                filename = os.path.join(html_dir, "{0}.html".format(imageid))
                browser = startup(binary = firefox_binary,options=options)
                downloadPage(column_value,filename,browser)
                imageOutputFilename = os.path.join(img_dir,"{0}.jpg".format(imageid))
                downloadImage(filename,imageOutputFilename)
                os.remove(filename)
            except:
                print("Processing failed for link : {0}".format(imageid))
            finally:
                index +=1
