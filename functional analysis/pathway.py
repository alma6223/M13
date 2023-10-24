from bs4 import BeautifulSoup
from typing import List, Dict
import requests
from requests.models import Response
import json


URL: str
URL = 'https://www.genome.jp/kegg/pathway.html'


try:
    response: Response
    response = requests.get(URL)
except requests.exceptions.RequestException as error:
    print(error)


soup: BeautifulSoup
soup = BeautifulSoup(response.text, features='html.parser')


groups:  List[str]
groups: List[str] = [group.text[0] for group in soup.find_all('b')[1:8]]

subgroups: List[str]
subgroups: List[str] = [subgroup.text.split()[0] for subgroup in soup.find_all('b')[8:]]

entries: List[str]
entries: List[str] = [entry.text for entry in soup.find_all(attrs={'class': 'list'})]


data: Dict[str, Dict[str, List[str]]]
data = {}

for group in groups:
    data[group] = {}
    for index in range(len(subgroups)):
        if subgroups[index][0] == group:
            data[group][subgroups[index]] = [entry[:5] for entry in entries[index].split('\n') if entry != '']
            

FILENAME: str
FILENAME = 'pathway.json'
with open(FILENAME, 'w') as file:
    json.dump(data, file, indent=4)
