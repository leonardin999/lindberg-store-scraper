import os
import shutil
import time
import csv
import re

from datetime import datetime
from RPA.Browser.Selenium import *

browser = Selenium(auto_close=False)
result_path = f"output\\realtor_infos_{datetime.now().strftime('%H%M%S')}.xlsx"
workbook = xlsxwriter.Workbook(report_output_path)
worksheet = workbook.add_worksheet("Denver, CO")


def minimal_task():
    print("Done.")


if __name__ == "__main__":
    try:
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
        writer.writerow(headers)
    finally:
        browser.close_all_browsers()
        f.close()
