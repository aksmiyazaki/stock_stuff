import requests as re
from bs4 import BeautifulSoup as sp
import pandas as pd

stock_list = ["LINX3",
              "TOTS3"]

stat_group = list()
transposed = True

def build_page_url(stock_target):
    return f"https://www.fundamentus.com.br/detalhes.php?papel={stock_target}"

for target in stock_list:
    page = re.get(build_page_url(target))
    parsed = sp(page.content, "html.parser")

    stat_dict = {"Papel": "",
                 "Cotação": "",
                 "P/L": "",
                 "P/VP": "",
                 "LPA": "",
                 "VPA":"",
                 "P/EBIT":"",
                 "Marg. EBIT": "",
                 "Marg. Líquida": "",
                 "ROIC": "",
                 "ROE": "",
                 "Div. Yield": "",
                 "EV / EBIT": "",
                 "EV / EBITDA": "",
                 "Liquidez Corr": "",
                 "Div Br/ Patrim": "",
                 "Cres. Rec (5a)": ""
                 }

    macro_table = parsed.find_all('table', class_="w728")

    get_data = False
    cur_title = ""
    for tbl in macro_table:
        for row in tbl.find_all("tr"):
            for col in row.find_all("td"):
                dt = col.select_one("span.txt")
                if dt is not None:
                    dt = dt.text.strip()

                    if get_data == True:
                        stat_dict[cur_title] = dt
                        get_data = False
                        cur_title = ""

                    if dt in stat_dict:
                        cur_title = dt
                        get_data = True

    stat_group.append(stat_dict)


df = pd.DataFrame.from_dict(stat_group)
df = df.set_index("Papel")

if transposed:
    df.T
else:
    df
