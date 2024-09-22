import time
import csv

from seleniumwire import webdriver  # Selenium Wire allows to use HTTP Basic Auth with proxy
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

def wait_for_element(parent, *args, **kwargs):
    start_time = time.time()
    while True:
        try:
            element = parent.find_element(*args, **kwargs)
            if not element.get_attribute('innerText'):
                raise WebDriverException("The element didn't load!")
            return element
        except WebDriverException as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)


def parse_pre_open_market(browser):
    browser.get('https://www.nseindia.com')

    marked_data_link = wait_for_element(browser, By.LINK_TEXT, 'MARKET DATA')

    actions = ActionChains(browser)
    actions.move_to_element(marked_data_link).click().perform()

    pre_open_market_link = wait_for_element(browser, By.LINK_TEXT, 'Pre-Open Market')
    pre_open_market_link.click()

    tbody = wait_for_element(browser, By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')

    with open('pre_open_market_data.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Имя', 'Цена'])
        for row in rows[:-1]:    # The last row isn't need because it is a summary line of the table
            data = row.text.split()
            writer.writerow([data[0], data[5]])     # Only columns 'Symbol' and 'Final' are needed


def emulate_user_story(browser):
    browser.get('https://www.nseindia.com')

    nifty_bank_link = wait_for_element(browser, By.ID, 'tabList_NIFTYBANK')
    nifty_bank_link.click()

    view_all_link = wait_for_element(browser, By.XPATH, '//div[@id="tab4_gainers_loosers"]/div[3]/a')
    # Another element wraps the view_all_link, so using actions.scroll_to_element() or view_all_link.click()
    # results in JavascriptException. Instead, use execute_script()
    browser.execute_script('arguments[0].scrollIntoView();', view_all_link)
    browser.execute_script('arguments[0].click();', view_all_link)

    selector = wait_for_element(browser, By.ID, 'equitieStockSelect')
    selector.click()

    nifty_alpha_50_option = wait_for_element(selector, By.XPATH, '//option[@value="NIFTY ALPHA 50"]')
    nifty_alpha_50_option.click()

    nifty_alpha_50_tbody = wait_for_element(browser, By.TAG_NAME, 'tbody')
    nifty_alpha_50_tbody.click()
    nifty_alpha_50_tbody_offsetHeight = nifty_alpha_50_tbody.get_attribute('offsetHeight')
    browser.execute_script(f'window.scrollTo(0, {nifty_alpha_50_tbody_offsetHeight});')


if __name__ == '__main__':
    sw_options = {
            'proxy': {
                'https': 'https://8MMGjo:xp70BL@91.216.186.190:8000',
            },
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    browser = webdriver.Chrome(service=Service(executable_path='chromedriver'),
                               options=chrome_options,
                               seleniumwire_options=sw_options)

    parse_pre_open_market(browser)
    emulate_user_story(browser)

    browser.quit()
