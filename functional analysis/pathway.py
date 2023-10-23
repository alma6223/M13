from bs4 import BeautifulSoup
from typing import List, Dict
import requests


url: str = 'https://www.genome.jp/kegg/pathway.html'

try:
    response: str = requests.get(url).text
except requests.exceptions.RequestException as error:
    print(error)


soup = BeautifulSoup(response, features='html.parser')


groups: List[str] = []

for group in soup.find_all('b')[1:8]:
    groups.append(group.text)


subgroups: List[str] = []

for subgroup in soup.find_all('b')[8:]:
    subgroups.append(subgroup.text)


codes: List[str] = []

for code in soup.find_all(attrs={'class': 'list'}):
    codes.append(code.text)


data = [] 

for group in groups:
    data.extend([group, subgroups[index], codes[index]] for index in range(len(subgroups)) if subgroups[index].startswith(group.split()[0]))

for i in data:
    print(i)
