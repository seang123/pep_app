import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd

"""

Download the empatica data from empatica.com/connect/

"""


def load():
    # Open browser and visit page
    driver = webdriver.Firefox()
    driver.get('https://empatica.com/connect/')
    driver.implicitly_wait(3)  # need to wait for the page to load to follow Sessions link

    username = driver.find_element(By.ID, "username")
    username.send_keys("dertigersbrein_02@donders.ru.nl")
    password = driver.find_element(By.ID, "password")
    password.send_keys('hbs2032')
    password.send_keys(Keys.ENTER)

    #time.sleep(3)
    sessions_link = driver.find_element(By.XPATH, '//div[1]/div/div/ul[1]/li[2]/a')
    sessions_link.click()

    view_all_sessions = driver.find_element(By.XPATH, '//div[2]/a/button')
    view_all_sessions.click()


    session_list = driver.find_element(By.XPATH, '//*[@id="sessionList"]')
    print(session_list)
    print(dir(session_list))

    time.sleep(3)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    #html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.select_one("div#span12")
    table = pd.read_html(str(div))
    print(table.head())


    # Finally close driver
    #driver.close()


def main():
    load()


if __name__ == '__main__':
    main()