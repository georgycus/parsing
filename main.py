import requests
from bs4 import BeautifulSoup as bf4
import re
import json


class Main:
    main_dict = {}
    second_dict = {}
    URL = "https://код-оквэд.рф"
    r = requests.get(URL)
    soup = bf4(r.text, "html.parser")
    okvad_groups = soup.find_all("h4", class_='title-bg')
    okvad_2022 = []

    for data in okvad_groups:
        if re.search(r" - .", data.text):
            okvad_2022.append(data.text)

    i = 0
    spiski = soup.find_all("table", class_="table table-striped table-hover")
    number = ""
    for data0 in spiski:
        temp = data0.find_all("tr")
        for data2 in temp:
            if re.search(r"Расшифровка", data2.text) is None:
                data3 = data2.find_all("td")
                for data4 in data3:
                    if re.search(r"\d", data4.text):
                        number = data4.text
                    else:
                        second_dict[number] = data4.text
        main_dict[okvad_2022[i]] = second_dict
        i += 1
        second_dict = {}

    with open("package.json", 'w', encoding="UTF-8") as fp:
        json.dump(main_dict, fp, sort_keys=True, indent=4, ensure_ascii=False)
