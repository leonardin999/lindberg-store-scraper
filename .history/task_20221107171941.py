import os
import shutil
import time
import csv
import re

from datetime import datetime
from RPA.Browser.Selenium import *

browser = Selenium(auto_close=False)
result_path = f"output\\realtor_infos_{datetime.now().strftime('%H%M%S')}.csv"
if os.path.isfile(result_path):
    os.remove(result_path)
f = open(result_path, "w")
writer = csv.writer(f)


def minimal_task():
    print("Done.")


if __name__ == "__main__":
    minimal_task()
