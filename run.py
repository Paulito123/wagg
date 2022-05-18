import requests
from lxml import html
import configparser


# Read local file `config.ini`.
config = configparser.ConfigParser()
config.read('config.ini')

base_url = 'https://0l.interblockcha.in/'
accounts = config["VARS"]["ACC_LIST"].split(';')

class Account:
   """
   A general class to store account info
   """

   def __init__(self, account, balance, height, proof_url):
       self.account = account
       self.balance = balance
       self.height = height
       self.proof_url = proof_url


def get_source(page_url):
   """
   A function to download the page source of the given URL.
   """
   r = requests.get(page_url)
   source = html.fromstring(r.content)

   return source


def main():

    account_collection = []

    for account in accounts:
        www_page = base_url + 'address/' + account
        vdf_proof_addr = base_url + 'api/proofs/' + account
        source = get_source(www_page)

        address = source.xpath("//span[contains(@class, 'address_addressText__YS_A5')]/text()")
        balance = source.xpath("//span[contains(@class, 'address_balanceText__ds0io')]/text()")
        height = source.xpath("//div[contains(@class, 'address_proofHistoryTable__oSdpQ')]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/text()")

        # print(f"{address}, {balance}, {height}")

        if len(address) > 0:
            acc = address[0]

            if len(balance) > 0:
                bal = float(balance[0])
            else:
                bal = 0.0

            if len(height) > 0:
                hght = height[0]
                proof_url = vdf_proof_addr
            else:
                hght = 0
                proof_url = '< no proof >'

            account = Account(acc, bal, hght, proof_url)
            account_collection.append(account)

    sum_balance = 0
    nr_accounts = 0
    for acc in account_collection:
        if acc.balance:
            nr_accounts = nr_accounts + 1
            bal = acc.balance
            sum_balance = sum_balance + bal
        else:
            bal = 0

        if acc.height:
            height = acc.height
            proof_url = acc.proof_url
        else:
            height = 0
            proof_url = '<No proof>'

        print(f"Account: {acc.account} - Balance: {bal} - Tower height: {height} - Proof url: {proof_url}")

    print(f"{nr_accounts} accounts counted with a total balance of {sum_balance}")


if __name__ == '__main__':
    main()