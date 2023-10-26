import pandas as pd
from pandas import DataFrame
import json
from bs4 import BeautifulSoup
import requests
from requests.models import Response
from typing import List, Dict



class KEGG:
    def __init__(self,  filepath_or_buffer: str, groups: List[str], columns: List[str]):
        self.filepath_or_buffer = filepath_or_buffer
        self.groups = groups
        self.columns = columns


    def data_frame(self) -> DataFrame:
        data_frame: DataFrame = pd.read_csv(filepath_or_buffer = self.filepath_or_buffer, delimiter = ',')
        data_frame: DataFrame = data_frame[data_frame[self.columns[0]].isin(self.groups)]
        return data_frame


    def pathway(self) -> Dict[str, Dict[str, List[str]]]:
        url: str = 'https://www.genome.jp/kegg/pathway.html'
        markup: Response = requests.get(url = url)


        soup: BeautifulSoup = BeautifulSoup(markup = markup.text, features = 'html.parser')        
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
            json.dump(obj = obj, fp = fp, indent=4)

        
        return obj


    def entries(self, data_frame: DataFrame) -> DataFrame:
        entries: DataFrame = data_frame.groupby(by = [self.columns[0], self.columns[1]]).size().reset_index(name = 'COUNT')
        path_or_buf: str = 'entries.csv'
        entries.to_csv(path_or_buf = path_or_buf)
        return entries
    

    
    
    
pp = KEGG('data.csv', [], [])

