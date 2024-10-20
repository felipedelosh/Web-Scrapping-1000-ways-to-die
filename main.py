"""
This Script its create to extract 1000 ways to lie
"""
import requests
from bs4 import BeautifulSoup
import re

print("================STEP 01 of 03 - GET DATA======================")
# Extract DATA FROM URL
_url = "https://es.wikipedia.org/wiki/Anexo:Episodios_de_1000_maneras_de_morir"
response = requests.get(_url)
soup = BeautifulSoup(response.text, 'html.parser')

# SAVE ALL TABLES
tables = soup.find_all('table', {'class': 'wikitable'})

def cleanID(id):
    id = str(id).strip()
    id = re.sub(r'[a-zA-Z]', '', id)
    id = re.sub(r'\[.*?\]', '', id)
    id = re.sub(r'\(.*?\)', '', id)
    id = id.replace(" ", "")
    id = re.sub(r'\u200B', '', id)
    id = id.strip()

    try:
        id = int(id)
    except:
        print(f"Problems in ID: {id}")

    return id


def cleanData(data):
    data = str(data).lstrip().rstrip()
    data = data.replace(".", "")

    return data


def orderDATA(arrData):
    """
    Enter a information in arr of tuples [(id, info), ...(id, info)]
    return the array in ASC order
    """
    for i in range(0, len(arrData)):
        print(arrData[i])

data1000WayToLie = []
temp = ""

print("================STEP 02 of 03 - EXTACT DATA======================")
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        if len(cols) >= 8:
            _idDeath = cols[0].text
            _idDeath = cleanID(_idDeath)
            _death = cols[8].text
            _death = cleanData(_death)
            temp = temp + f"{_idDeath}|{_death}\n"
            data1000WayToLie.append((_idDeath, _death))

print("================STEP 03 of 03 - SAVE DATA======================")
with open("originalDATA.csv", "w", encoding="UTF-8") as f:
    f.write(temp)

#data1000WayToLie = orderDATA(data1000WayToLie)
