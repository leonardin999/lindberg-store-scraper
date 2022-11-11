import re

string = f"""Potsdamer Straße 105
10785 Berlin
Germany"""

zip_code = re.split(r"\n", string)[-2]
zip_code = re.findall(r"\d+", zip_code)[-1]
print(zip_code)
