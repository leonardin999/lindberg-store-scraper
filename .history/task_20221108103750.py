import os
import shutil
import time
import csv
import re
import xlsxwriter

from datetime import datetime
from RPA.Browser.Selenium import *

browser = Selenium(auto_close=False)
# config report files
result_path = f"output\\realtor_infos_{datetime.now().strftime('%H%M%S')}.xlsx"
workbook = xlsxwriter.Workbook(result_path)
worksheet = workbook.add_worksheet("Denver, CO")
cell_format = workbook.add_format({"bold": True, "font_color": "blue"})
cell_format.set_font_size(11)
# website urls:
zillow_url = "https://www.zillow.com/professionals/real-estate-agent-reviews/denver-co/"


def open_zillow(url):
    browser.open_available_browser(url, maximized=True)
    browser.wait_until_element_is_visible("css=table.eSCkQe", timeout=30)


def get_infos_agent(agent):
    browser.execute_javascript(
        f"document.querySelectorAll('a.jMHzWg')[{agent*2}].click()"
    )
    browser.wait_until_element_is_visible("css=input#name", timeout=20)
    count = browser.execute_async_javascript(
        "return document.querySelectorAll('.kDPuVQ').length"
    )
    time.sleep(0.2)
    if count > 0:
        for i in range(count):
            get_infos_realtor(i)
    else:
        pass


def get_infos_realtor(realtor):
    browser.execute_javascript(
        f"document.querySelectorAll('.kDPuVQ')[{realtor}].getElementsByTagName('a')[1].click()"
    )
    pass


if __name__ == "__main__":
    try:
        scrapper_pages = 15
        row = 0
        headers = [
            "Name",
            "Address",
            "Phone Number",
            "Website",
            "Blog",
            "Facebook",
            "Twitter",
            "LinkedIn",
            "Company",
        ]
        for i, header in enumerate(headers):
            worksheet.write(row, i, header, cell_format)
        row += 1
        open_zillow(zillow_url)
        for page in range(scrapper_pages):
            for agent in range(10):
                get_infos_agent(agent)
            browser.execute_javascript(
                "document.querySelector(`button[rel='next']`).click()"
            )
    finally:
        browser.close_all_browsers()
        workbook.close()
