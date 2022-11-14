import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

"""

Download the empatica data from empatica.com/connect/

"""


def load():
    # Open browser and visit page
    driver = webdriver.Firefox()
    driver.get('https://empatica.com/connect/')

    username = driver.find_element(By.ID, "username")
    username.send_keys("dertigersbrein_02@donders.ru.nl")
    password = driver.find_element(By.ID, "password")
    password.send_keys('hbs2032')
    password.send_keys(Keys.ENTER)

    # Finally close driver
    #driver.close()


def main():
    load()


if __name__ == '__main__':
    main()