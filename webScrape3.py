from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from bs4 import BeautifulSoup as bs
import re as re
import time
import csv
import re
import pickle
import pandas


# USERNAME = "votoy69387@datakop.com"
# PASSWORD = "WatermelonHigh123"

# print(PATH)
# print(USERNAME)
# print(PASSWORD)

PATH = "/Applications/chromedriver"
s = Service(PATH)
driver = webdriver.Chrome(service=s)

# driver.get("https://www.google.com")

# email=driver.find_element_by_id("username")
# email.send_keys(USERNAME)
# password=driver.find_element_by_id("password")
# password.send_keys(PASSWORD)

# password.send_keys(Keys.RETURN)

links = []

# search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
# search_query.send_keys('site:linkedin.com/in/ AND "investor" AND "stroke"')

# .send_keys() to simulate the return key
# search_query.send_keys(Keys.ENTER)

# results = driver.find_elements_by_xpath("//div[@class='g']//div[@class='r']//a[not(@class)]");
# for result in results:
#    print(result.get_attribute("href"))

f = open('data.csv', 'a', newline='')
writer = csv.writer(f)
# writer.writerow(["Group", "Title", "LinkedIn URL", "Description"])


regex = re.compile('[^a-zA-Z] ')


def getKeywords():
    k = []
    keywordsFile = open('keywords.txt', 'r')
    for line in keywordsFile:
        k.append(line)
    return k


def getUnscraped():
    """Gets unscraped hospital groups"""
    scraped = pandas.read_csv("data.csv")

    groups = []
    with open('hospital_groups.txt', 'r') as hg:
        for line in hg:
            if line not in scraped['Group'].values.tolist():
                groups.append(line)

    return groups


hospital_groups = getUnscraped()
keywords = getKeywords()

driver.get(
    "http://www.google.com/search?q=site:linkedin.com/in/ AND CFO AND Hospital")
# Add cookies to avoid recaptcha
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

try:
    for group in hospital_groups:
        print(group)
        for keyword in keywords:
            # The keywords in double quotes is what the linkedIn files are searched by
            for page in range(1):
                url = "http://www.google.com/search?q=" + \
                    'site:linkedin.com/in/ AND "{}" AND "{}"'.format(
                        keyword, group) + "&start=0&num=2"
                cookies = pickle.load(open("cookies.pkl", "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.get(url)

                # search_query.send_keys('site:linkedin.com/in/ AND "investor" AND "stroke"')

                soup = bs(driver.page_source, 'html.parser')
                # soup = BeautifulSoup(r.text, 'html.parser')

                # div classname for search in google search
                search = soup.find_all('div', class_="tF2Cxc")
                for div in search:
                    url = div.a.get('href')
                    description = ""
                    try:
                        for item in div.contents[1].contents[0].contents[1:]:
                            description = description + \
                                regex.sub("", item.contents[0])
                    except:
                        print("no description")
                    row = [group, keyword, url, description]
                    print(row)
                    writer.writerow(row)
                time.sleep(20)
        hospital_groups.remove(group)

except Exception as error:
    print(error)

finally:
    # Write back to file unscraped groups
    with open('hospital_groups.txt', 'w') as hg:
        for h in hospital_groups:
            hg.write(h)
    f.close()
