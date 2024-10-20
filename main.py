"""
This Script its create to extract 1000 ways to die
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
    data = data.replace("\n", "")
    data = re.sub(r'\u200B', '', data)

    return data


def orderDATA(arrData):
    """
    Enter a information in arr of tuples [(id, info), ...(id, info)]
    return the array in ASC order
    """
    n = len(arrData)
    for i in range(0, n):
        for j in range(0, n - i - 1):
            if int(arrData[j][0]) > int(arrData[j+1][0]):
                temp = arrData[j]
                arrData[j] = arrData[j+1]
                arrData[j+1] = temp


data1000WayToDie = []
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
            data1000WayToDie.append((_idDeath, _death))

print("================STEP 03 of 03 - SAVE DATA======================")
with open("originalDATA.csv", "w", encoding="UTF-8") as f:
    f.write(temp)


_dataOrder100waysToDie = "ID|DEATH\n"
orderDATA(data1000WayToDie)
for i in data1000WayToDie:
    _dataOrder100waysToDie = _dataOrder100waysToDie + f"{i[0]}|{i[1]}\n"

with open("1000WaysToDie.csv", "w", encoding="UTF-8") as f:
    f.write(_dataOrder100waysToDie)