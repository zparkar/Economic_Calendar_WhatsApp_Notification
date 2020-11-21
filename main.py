import datetime
import functools
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import sys

# Get Economic calendar from Forex Factory


@functools.lru_cache
def get_events():
    url = 'https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.json'
    events = requests.get(url).json()
    filtered_events = []
    for e in events:
        e['date'] = datetime.datetime.strptime(e['date'][:10], '%Y-%m-%d').strftime('%d/%m/%Y')
        filtered_events.append(e)
    return filtered_events


# Create a list of all events based on today's date


def event_impact(event):
    message_list = []
    today = datetime.date.today().strftime('%d/%m/%Y')
    for item in get_events():
        if item['date'] == today:
            event_name = item['title']
            country_name = item['country']
            event_date = item['date']
            impact = item['impact']
            forecast = item['forecast']
            previous = item['previous']
            message_content = f"Event name: {event_name}|Country: {country_name}|Date: {event_date}|Impact: {impact}|Forecast: {forecast}|Previous: {previous}"
            message_list.append(message_content)
    return message_list

# Store all events in a variable, if nothing is stored then stop script


string = event_impact(get_events())
if string == "":
    sys.exit()
else:

    # Replace below path with the absolute path of the chromedriver in your computer
    options = webdriver.ChromeOptions();
    options.add_argument('--user-data-dir=./User_Data')
    driver = webdriver.Chrome(chrome_options=options)
    #driver = webdriver.Chrome(r'C:\Users\User\Desktop\chromedriver')
    driver.get("https://web.whatsapp.com/")
    time.sleep(10)
    wait = WebDriverWait(driver, 30)

    # Target is the group name or whatsapp contact name
    target = 'Group or contact name'

    # Find the group name or whatsapp contact
    x_arg = f'//span[contains(@title,"{target}")]'
    group_title = wait.until(EC.presence_of_element_located((
    By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]

    # Input events and add a line break between each event and send the message
    for line in string:
        for element in line.split('|'):
            message.send_keys(element)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
    ActionChains(driver).send_keys(Keys.RETURN).perform()

    # Close the application
    driver.close()
    sys.exit()
