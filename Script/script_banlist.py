import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.yugioh-card.com/en/limited/list_2025-04-07/"
headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get(url, headers=headers)
resp.encoding = resp.apparent_encoding

soup = BeautifulSoup(resp.text, 'html.parser')
pattern = re.compile(r'^cardlist_')
rows = []

tables = soup.find_all('table', class_='cardlist centertable')
for table in tables:
    for tr in table.find_all('tr', class_=pattern):
        cols = [td.get_text(strip=True) for td in tr.find_all('td')]
        if len(cols) == 5:
            row = {
                'card_type': cols[0],
                'card_name': cols[1],
                'advanced_format': cols[2],
                'remarks': cols[4]
            }
            rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("table_banlist.csv", sep=';', index=False)


