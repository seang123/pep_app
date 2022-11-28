import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd

"""

Download the empatica data from empatica.com/connect/


Delete:
dertigersbrein_02@donders.ru.nl -- A02E3E
dertigersbrein_15@donders.ru.nl -- A043AC
"""


def login(driver, username: str, password: str) -> selenium.webdriver:
    """ Return a driver to the empatica website after login """
    _username = driver.find_element(By.ID, "username")
    _username.send_keys(username)
    _password = driver.find_element(By.ID, "password")
    _password.send_keys(password)
    _password.send_keys(Keys.ENTER)
    return driver


def get_table(driver: selenium.webdriver) -> pd.DataFrame:
    """ Return table holding sessions data """
    time.sleep(0.5)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, 'html.parser')
    for body in soup('tbody'):
        body.unwrap()
    table = pd.read_html(str(soup), flavor='bs4')  # table[0] is the calendar | table[1] the session data
    return table[1]


def _download(driver: selenium.webdriver, sessions_data: pd.DataFrame, emp_id: str):
    """ Download device data """
    print(f"Downloading data for: {emp_id}")
    idx = '1'
    download_path = f'/html/body/div[3]/div[2]/div/div/table/tbody/tr[{idx}]/td[5]/div/a[3]'

    def remove_version(row):
        x = row['Device'].split(' ')[0]
        return x
    sessions_data['Device'] = sessions_data.apply(lambda row: remove_version(row), axis=1)

    emp_rows = sessions_data.query('Device == @emp_id')
    emp_rows_index = emp_rows.index.values - 1

    for i in emp_rows_index:
        download_button = f'/html/body/div[3]/div[2]/div/div/table/tbody/tr[{i}]/td[5]/div/a[3]'


def _delete_by_id(driver: selenium.webdriver, emp_id: str):
    """ Delete specific empatica sessions by device ID """
    raise NotImplementedError()

def _delete(driver: selenium.webdriver, emp_id: str = None):
    if emp_id:
        _delete_by_id(driver, emp_id)
        return

    raise NotImplementedError("Currently can only delete sessions by device ID")

def load(username: str, password: str):
    """ Load the empatica.com/connect/ website and navigate to the Sessions / view all sessions page

    Create a pandas table from the sessions data to parse

    :return: selenium.webdriver | pandas dataframe
    """
    # Open browser and visit page
    driver = webdriver.Firefox()
    driver.get('https://empatica.com/connect/')
    driver.implicitly_wait(3)  # need to wait for the page to load to follow Sessions link

    # Login
    driver = login(driver, username, password)

    # Follow link to sessions data
    sessions_link = driver.find_element(By.XPATH, '//div[1]/div/div/ul[1]/li[2]/a')
    sessions_link.click()

    # View all sessions
    view_all_sessions = driver.find_element(By.XPATH, '//div[2]/a/button')
    view_all_sessions.click()

    # Get the session list
    session_list = driver.find_element(By.XPATH, '//*[@id="sessionList"]')

    # Get the session data as a pd.DataFrame table
    table = get_table(driver)

    return driver, table

def main():
    username = "dertigersbrein_02@donders.ru.nl"
    password = 'hbs2032'
    emp_id = 'A02D01'
    driver, sessions_data = load(username, password)

    _download(driver, sessions_data, emp_id)


    # Finally close driver
    #driver.close()


if __name__ == '__main__':
    main()