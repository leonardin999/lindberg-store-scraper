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
    browser.open_available_browser(url, maximized=True)
    browser.wait_until_element_is_visible(
        "css=input.mapboxgl-ctrl-geocoder--input", timeout=10
    )


def get_infos_each_country(country, row):
    # country = country.replace(" ", "{BACKSPACE}")
    browser.click_element("css=input.mapboxgl-ctrl-geocoder--input")
    window.send_keys(country)
    time.sleep(1.5)
    browser.press_key("css=input.mapboxgl-ctrl-geocoder--input", "\ue007")
    time.sleep(1.5)
    count = browser.execute_javascript(
        "return document.querySelectorAll('div.no-results.noselect').length"
    )
    time.sleep(0.2)
    if count > 0:
        browser.reload_page()
        return
    else:
        current_row = get_list_store(row, country)
        return current_row


def get_list_store(row, country):
    browser.wait_until_element_is_visible("css=div.dealer-list-items", 30)
    count = browser.execute_javascript(
        "return document.querySelector('div.dealer-list-items').getElementsByTagName('li').length"
    )
    time.sleep(2)
    for i in range(int(count)):
        time.sleep(0.2)
        try:
            browser.execute_javascript(
                f"document.querySelector('div.dealer-list-items').getElementsByTagName('li')[{i}].click()"
            )
            time.sleep(0.5)
            name = browser.execute_javascript(
                "return document.querySelector('div.name').innerText"
            )
            time.sleep(0.2)
            worksheet.write(row, 0, name)
            address = browser.execute_javascript(
                "return document.querySelector('div.address').innerText"
            )
            add_address = re.split(r"\n", address)
            if len(add_address) == 4:
                tmp_address = add_address[0] + " " + add_address[1]
            else:
                tmp_address = add_address[0]

            worksheet.write(row, 1, tmp_address)
            time.sleep(0.2)
            try:
                zip_code = re.split(r"\n", address)[-2]
                zip_code = re.findall(r"\d+", zip_code)[-1]
            except:
                zip_code = " "
            worksheet.write(row, 3, zip_code)
            phone_number = browser.execute_javascript(
                "return document.querySelector('div.phone.dealersearch-btn').innerText"
            )
            worksheet.write(row, 2, phone_number)
            time.sleep(0.2)
            website = browser.execute_javascript(
                "return document.querySelector('div.website.dealersearch-btn').childNodes[0].href"
            )
            worksheet.write(row, 5, website)
            worksheet.write(row, 4, country)
            row += 1
        except:
            pass
    browser.reload_page()
    return row


if __name__ == "__main__":
    try:
        row = 0
        headers = [
            "Name of store",
            "street",
            "number",
            " zip code",
            "country",
            "website",
        ]
        for i, header in enumerate(headers):
            worksheet.write(row, i, header, cell_format)
        row += 1
        open_lindberg(lindberg_url)
        for country in countries:
            current_row = get_infos_each_country(country, row)
            if current_row:
                row = current_row + 1
    finally:
        browser.close_all_browsers()
        workbook.close()
        pass
