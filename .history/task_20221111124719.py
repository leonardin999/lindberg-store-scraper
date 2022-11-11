import os
import shutil
import time
import csv
import re
import xlsxwriter

# from RPA.Browser.Playwright import *
from datetime import datetime

from RPA.Browser.Selenium import *
from RPA.Desktop.Windows import Windows

window = Windows()
browser = Selenium()
# config report files
result_path = f"output\\store_infos_{datetime.now().strftime('%H%M%S')}.xlsx"
workbook = xlsxwriter.Workbook(result_path)
worksheet = workbook.add_worksheet("lindberg")
cell_format = workbook.add_format({"bold": True, "font_color": "blue"})
cell_format.set_font_size(11)
countries = list()
# List of countries:
with open("countries.txt", "r") as f:
    for line in f.readlines():
        if line != "":
            countries.append(line)

# website urls:
lindberg_url = "https://lindberg.com/en/find-a-store#/country"


def open_lindberg(url):
    browser.open_available_browser(url)
    browser.wait_until_element_is_visible(
        "css=input.mapboxgl-ctrl-geocoder--input", timeout=10
    )


def get_infos_each_country(country):
    browser.input_text("css=input.mapboxgl-ctrl-geocoder--input", country)
    window.send_keys("Enter")
    time.sleep(1.5)
    count = browser.execute_javascript(
        "return document.querySelectorAll('div.no-results.noselect').length"
    )
    time.sleep(0.2)
    if count > 0:
        browser.reload_page()
        return
    else:
        get_list_store()


def get_list_store():
    browser.wait_until_element_is_visible("div.dealer-list-items")
    count = browser.execute_javascript(
        "return document.querySelector('div.dealer-list-items').getElementsByTagName('li').length"
    )
    time.sleep(0.2)
    for i in range(int(count)):
        browser.execute_javascript(
            f"document.querySelector('div.dealer-list-items').getElementsByTagName('li')[{i}].click()"
        )
        time.sleep(1)
        name = browser.execute_javascript(
            "return document.querySelector('div.name').innerText"
        )
        time.sleep(0.2)
        address = browser.execute_javascript(
            "return document.querySelector('div.address').innerText"
        )
        time.sleep(0.2)
        try:
            zip_code = re.split(r"\n", address)[-2]
            zip_code = re.match(r"\d+", zip_code)
        except:
            zip_code = ""
        phone_number = browser.execute_javascript(
            "return document.querySelector('div.phone.dealersearch-btn').innerText"
        )
        time.sleep(0.2)
        website = browser.execute_javascript(
            "return document.querySelector('div.website.dealersearch-btn').childNodes[0].href"
        )


if __name__ == "__main__":
    try:
        scrapper_pages = 15
        row = 0
        headers = ["Name of store", "street", "number", " zip code", "country"]
        for i, header in enumerate(headers):
            worksheet.write(row, i, header, cell_format)
        row += 1
        open_lindberg(lindberg_url)
        for country in countries:
            get_infos_each_country(country)
    finally:
        # browser.close_all_browsers()
        # workbook.close()
        pass
