import re

string = (
    f"235 Springvale Road\nShop G-122, The Glen\nGlen Waverley Victoria 3150\nAustralia"
)

zip_code = re.split(r"\n", string)[-2]
# zip_code = re.match(r"\d+", zip_code)
print(zip_code)
