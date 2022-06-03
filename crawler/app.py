import requests
from lxml import html
from time import sleep
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, NoSuchTableError
from models import init_db, AccountStat, PaymentEvent, MinerHistory
from database import session, engine
from config import Config
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


def get_source(page_url):
    """
    A function to download the page source of the given URL.
    """
    r = requests.get(page_url)
    source = html.fromstring(r.content)

    return source


# def push_button_if_not_disabled():



def scrape():
    # with engine.connect() as connection:
    #     try:
    #         accounts = connection.execute(text("select address from accountstat"))
    #
    #         for account in accounts:
    #             www_page = Config.BASE_URL + 'address/' + account.address
    #             source = get_source(www_page)
    #
    #             addr_check = source.xpath("//span[contains(@class, 'address_addressText__YS_A5')]/text()")
    #             balance = source.xpath("//span[contains(@class, 'address_balanceText__ds0io')]/text()")
    #             height = source.xpath(
    #                 "//div[contains(@class, 'address_proofHistoryTable__oSdpQ')]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/text()")
    #             proofsinepoch = source.xpath(
    #                 "//div[contains(@class, 'address_proofHistoryTable__oSdpQ')]/div[2]/div/div/div/div/div/table/tbody/tr[2]/td[2]/text()")
    #             lastepochmined = source.xpath(
    #                 "//div[contains(@class, 'address_proofHistoryTable__oSdpQ')]/div[2]/div/div/div/div/div/table/tbody/tr[3]/td[2]/text()")
    #
    #             if len(addr_check) > 0:
    #                 sess_account = session.query(AccountStat).filter_by(address=account.address).first()
    #
    #                 if sess_account:
    #                     if len(balance) > 0:
    #                         sess_account.balance = int(round(float(balance[0].replace(',', '')), 2) * 100)
    #                         sess_account.updated_at = datetime.now()
    #
    #                     if len(height) > 0:
    #                         sess_account.towerheight = int(height[0])
    #
    #                     if len(proofsinepoch) > 0:
    #                         sess_account.proofsinepoch = int(proofsinepoch[0])
    #
    #                     if len(lastepochmined) > 0:
    #                         sess_account.lastepochmined = int(lastepochmined[0])
    #
    #                     sess_account.updated_at = datetime.now()
    #
    #                     if len(height) > 0 or len(balance) > 0:
    #                         session.commit()
    #
    #     except ProgrammingError:
    #         print("kakapipi")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor='http://chrome:4444/wd/hub',
        options=chrome_options
    )


    # driver = webdriver.Chrome(chrome_options=options,
    #                           executable_path=r'C:\WebDrivers\ChromeDriver\chromedriver_win32\chromedriver.exe')
    # driver.get('http://www.boston.gov.uk/index.aspx?articleid=6207&ShowAdvancedSearch=true')
    # mySelectElement = Select(WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "select#DatePresets[name='DatePresets']"))))
    # mySelectElement.select_by_visible_text('Last month')
    # # driver.find_element_by_css_selector("input.button[name='searchFilter']").click()
    # numLinks = len(WebDriverWait(driver, 20).until(
    #     EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "input.pageNumberButton"))))
    # print(numLinks)
    # for i in range(numLinks):
    #     print("Perform your scrapping here on page {}".format(str(i + 1)))
    #     WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    #         (By.XPATH, "//input[@class='pageNumberButton selected']//following::input[1]"))).click()
    # driver.quit()

    driver.get('http://google.com')
    print(f"{driver.title} > {datetime.now()}")
    driver.quit()



sleep(3)
init_db()
sleep(1)


while True:
    scrape()
    sleep(5)
    # with engine.connect() as connection:
    #     try:
    #         accounts = connection.execute(text("select * from accountstat"))
    #         for row in accounts:
    #             print(f"address={row.address} with balance={row.balance}")
    #             print(f"proofsinepoch={row.proofsinepoch} | lastepochmined={row.lastepochmined}")
    #     except NoSuchTableError:
    #         print("Shizzlemanizzle no table")
    #     except ProgrammingError:
    #         print("Shizzlemanizzle programming error")
    # sleep(5)
    # sleep(60 * Config.SLEEP_MINS)
