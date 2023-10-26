import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import json
from bs4 import BeautifulSoup
import requests
from requests.models import Response
from typing import List, Dict



class KEGG:
    def __init__(self,  filepath_or_buffer: str):
        self.data_frame: DataFrame = pd.read_csv(filepath_or_buffer = filepath_or_buffer, delimiter = ',')


    def pathway(self):
        url: str = 'https://www.genome.jp/kegg/pathway.html'
        response: Response = requests.get(url = url)


        soup: BeautifulSoup = BeautifulSoup(markup = response.text, features = 'html.parser')        
        groups: List[str] = [group.text[0] for group in soup.find_all('b')[1:8]]
        subgroups: List[str] = [subgroup.text.split()[0] for subgroup in soup.find_all('b')[8:]]
        entries: List[str] = [entry.text for entry in soup.find_all(attrs={'class': 'list'})]


        obj: Dict[str, Dict[str, List[str]]] = {}
        for group in groups:
            obj[group] = {}
            for index in range(len(subgroups)):
                if subgroups[index][0] == group:
                    obj[group][subgroups[index]] = [entry[:5] for entry in entries[index].split('\n') if entry != '']


        file: str = 'pathway.json'
        with open(file = file, mode = 'w') as fp:
            json.dump(obj = obj, fp = fp)


    def entries(self, groups: List[str], columns: List[str]) -> DataFrame:
        """
        
        """
        entries: DataFrame = pd.concat([self.data_frame[self.data_frame[columns[0]].isin(groups)]])
        entries: DataFrame = entries.groupby(by = [columns[0], columns[1]]).size().reset_index(name = 'COUNT')
        path_or_buf: str = 'entries.csv'
        entries.to_csv(path_or_buf = path_or_buf)
        return entries
