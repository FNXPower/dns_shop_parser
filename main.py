import time
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import csv

# csv = smartphone_from_dns-shop
start_time = time.time()
chrome_options = Options()
chrome_options.headless = False
driver_service = Service(executable_path=r"C:\Users\Кирилл\PycharmProjects\DNS_parser\chromedriver.exe")
driver = webdriver.Chrome(service=driver_service)

url = "https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?p=1"
city_list = ['Оренбург']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.60 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9 "
}


def start_browser(url):
    driver.get(url=url)

def get_content():
    soup = BS(driver.page_source, "lxml")
    time.sleep(1)
    products = soup.find_all(class_="catalog-product__name ui-link ui-link_black")
    prices = soup.find_all("div", class_="product-buy__price")
    smartphones = []
    for i in range(0, len(products)):
        smartphones.append(
            {
                'title': products[i].text,
                'price': prices[i].text,
            }
        )

    return smartphones


def parser():
    pagination = int(input('Количество страниц для парсинга:'))
    html = requests.get(url)

    if html.status_code == 200:
        list_smartphones = []
        for page in range(1, pagination+1):
            list_smartphones.extend(get_content())

    else:
        print("Страницы нет или сайт недоступень")

    return list_smartphones


def main():
    start_browser(url)
    result = parser()
    print('ya tut')
    print(result)



if __name__ == "__main__":
    main()
