import time
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import requests
import csv


start_time = time.time()
chrome_options = Options()
chrome_options.headless = False
driver_service = Service(executable_path=r"C:\Users\Кирилл\PycharmProjects\DNS_parser\chromedriver.exe")
driver = webdriver.Chrome(service=driver_service)
driver.implicitly_wait(10)

url = "https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?p=38"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.60 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9 "
}

file = 'smartphones.csv'

def start_browser(url):
    # Открывем ссылку url
    driver.get(url=url)


def get_content():
    # Получем html данной страницы, вытаскиваем из него название и цену и сохраняем в список smartphones
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


def new_page(url):
    page = ""
    for letter in url[::-1]:
        if letter.isdigit():
            page += letter
        else:
            break
    page = str(int(page[::-1]) + 1)
    url = url[:len(url) - url[::-1].index("/")] + "?p=" + page
    start_browser(url)
    print("Перешли на следующую страницу")
    return url

def save_file(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название смартфона', 'Цена'])
        for item in items:
            writer.writerow([item['title'], item['price']])

def parser(url):
    # Пагинация сайта, вставка списка со страницы в общий список
    html = requests.get(url)
    current_url = url
    if html.status_code == 200:
        list_smartphones = []
        while True:
            if get_content():
                list_smartphones.extend(get_content())
                current_url = new_page(current_url)
                save_file(list_smartphones, file)
                time.sleep(10)
            else:
                break

    else:
        print("Сайт недоступен")

    return list_smartphones


if __name__ == "__main__":
    start_browser(url)
    result = parser(url)

    print(result)
