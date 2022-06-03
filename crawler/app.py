import requests
from lxml import html
from time import sleep
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, NoSuchTableError
# from models import init_db, AccountStat, PaymentEvent, MinerHistory
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
# TODO: first poll website to check availability before start loop


def testing():
    # 1
    address = "<address>"
    print(f"crawling {address}...")
    url = Config.BASE_URL + 'address/' + address
    host = "172.18.0.2"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor=f'http://{host}:4444/wd/hub',
        options=chrome_options
    )

    try:
        print(f"Getting {url}")
        driver.get(url)

        address = driver.find_element(By.CLASS_NAME, "address_addressText__YS_A5")
        balance = driver.find_element(By.CLASS_NAME, "address_balanceText__ds0io")
        height = driver.find_element(By.XPATH, "//div[contains(@class, 'address_statsTablesContainer___HxvE')]/div[1]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]")
        proofsinepoch = driver.find_element(By.XPATH, "//div[contains(@class, 'address_statsTablesContainer___HxvE')]/div[1]/div[2]/div/div/div/div/div/table/tbody/tr[2]/td[2]")
        lastepochmined = driver.find_element(By.XPATH, "//div[contains(@class, 'address_statsTablesContainer___HxvE')]/div[1]/div[2]/div/div/div/div/div/table/tbody/tr[3]/td[2]")

        print(f"address.text > {address.text}")
        print(f"balance.text > {balance.text}")
        print(f"height.text > {height.text}")
        print(f"proofsinepoch.text > {proofsinepoch.text}")
        print(f"lastepochmined.text > {lastepochmined.text}")

        print("Waiting for miner history...")
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//div[contains(@class, 'address_statsTablesContainer___HxvE')]/div[2]/div[2]/div/div/ul/li[@title='1']"))

        # Scraping Miner history
        disabled = False
        while not disabled:
            rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'address_statsTablesContainer___HxvE')]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr")
            for row in rows:
                epoch = row.find_elements(By.TAG_NAME, "td")[0]
                theight = row.find_elements(By.TAG_NAME, "td")[1]
                print(f"epoch > {epoch.text} - theight > {theight.text}")
            button_next = driver.find_element(By.XPATH, "//div[contains(@class, 'address_statsTablesContainer___HxvE')]/div[2]/div[2]/div/div/ul/li[@title='Next Page']/button")

            disabled = button_next.get_property('disabled')
            button_next.click()

        print("Waiting for payment events...")
        WebDriverWait(driver, timeout=60).until(lambda d: d.find_element(By.XPATH, "//div[contains(@class, 'eventsTable_inner__HsGHV')]/div[2]/div/div/ul/li[@title='Next Page']"))

        # Scraping rewards
        disabled = False
        while not disabled:
            rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'eventsTable_inner__HsGHV')]/div[2]/div/div/div/div/div/table/tbody/tr")
            for row in rows:
                if len(row.find_elements(By.TAG_NAME, "td")[0].text) == 0:
                    print("skip empty")
                    continue
                height = row.find_elements(By.TAG_NAME, "td")[0]
                type = row.find_elements(By.TAG_NAME, "td")[1]
                amount = row.find_elements(By.TAG_NAME, "td")[2]
                sender = row.find_elements(By.TAG_NAME, "td")[3]
                recipient = row.find_elements(By.TAG_NAME, "td")[4]
                print(f"{height.text} | {type.text} | {amount.text} | {sender.text} {recipient.text}")
            button_next = driver.find_element(By.XPATH, "//div[contains(@class, 'eventsTable_inner__HsGHV')]/div[2]/div/div/ul/li[@title='Next Page']/button")

            disabled = button_next.get_property('disabled')
            button_next.click()


    except Exception as e:
        print(f"{e}")
    finally:
        print(f"...and we're done!")
        driver.quit()


# def get_source(page_url):
#     """
#     A function to download the page source of the given URL.
#     """
#     r = requests.get(page_url)
#     source = html.fromstring(r.content)
#
#     return source


# def push_button_if_not_disabled():



def scrape():
    pass
    # with engine.connect() as connection:
    #     try:
    #         accounts = connection.execute(text("select address from accountstat"))
    #
    #         for account in accounts:
    #             url = Config.BASE_URL + 'address/' + account.address
    #
    #             chrome_options = webdriver.ChromeOptions()
    #             chrome_options.add_argument("start-maximized")
    #             chrome_options.add_argument("disable-infobars")
    #             chrome_options.add_argument("--disable-extensions")
    #             # chrome_options.add_argument("--headless")
    #             driver = webdriver.Remote(
    #                 command_executor='http://chrome:4444/wd/hub',
    #                 options=chrome_options
    #             )
    #             driver.get(url)
    #
    #             address = driver.find_element(By.CLASS_NAME, "address_addressText__YS_A5")
    #
    #             print(f"{address} > {datetime.now()}")
    #             driver.quit()




                # source = get_source(url)
                #
                # addr_check = source.xpath("//span[contains(@class, 'address_addressText__YS_A5')]/text()")
                # balance = source.xpath("//span[contains(@class, 'address_balanceText__ds0io')]/text()")
                # height = source.xpath(
                #     "//div[contains(@class, 'address_proofHistoryTable__oSdpQ')]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/text()")
                # proofsinepoch = source.xpath(
                #     "//div[contains(@class, 'address_proofHistoryTable__oSdpQ')]/div[2]/div/div/div/div/div/table/tbody/tr[2]/td[2]/text()")
                # lastepochmined = source.xpath(
                #     "//div[contains(@class, 'address_proofHistoryTable__oSdpQ')]/div[2]/div/div/div/div/div/table/tbody/tr[3]/td[2]/text()")
                #
                # if len(addr_check) > 0:
                #     sess_account = session.query(AccountStat).filter_by(address=account.address).first()
                #
                #     if sess_account:
                #         if len(balance) > 0:
                #             sess_account.balance = int(round(float(balance[0].replace(',', '')), 2) * 100)
                #             sess_account.updated_at = datetime.now()
                #
                #         if len(height) > 0:
                #             sess_account.towerheight = int(height[0])
                #
                #         if len(proofsinepoch) > 0:
                #             sess_account.proofsinepoch = int(proofsinepoch[0])
                #
                #         if len(lastepochmined) > 0:
                #             sess_account.lastepochmined = int(lastepochmined[0])
                #
                #         sess_account.updated_at = datetime.now()
                #
                #         if len(height) > 0 or len(balance) > 0:
                #             session.commit()

        # except ProgrammingError:
        #     print("kakapipi")


# sleep(3)
# init_db()
# sleep(1)


# while True:
#     scrape()
#     sleep(5)
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

if __name__ == '__main__':
    testing()