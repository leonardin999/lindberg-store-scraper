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
workbook = xlsxwriter.Workbook(report_output_path)
worksheet = workbook.add_worksheet("Denver, CO")
cell_format = workbook.add_format({"bold": True, "font_color": "blue"})
cell_format.set_font_size(11)
# website urls:
zillow_url = "https://www.zillow.com/professionals/real-estate-agent-reviews/denver-co/"


def open_zillow(url):
    browser.open_available_browser(url, maximized=True)
    browser.wait_until_element_is_visible("css=table.eSCkQe", timeout=30)


if __name__ == "__main__":
    try:
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
        browser.click_button("Next page")
    finally:
        browser.close_all_browsers()
        workbook.close()
