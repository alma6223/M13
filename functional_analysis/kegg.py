import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup
import requests
from requests.models import Response
from typing import List, Dict
import csv
from csv import writer


class KEGG:
    def __init__(self,  filepath_or_buffer: str, groups: List[str]):
        self.filepath_or_buffer = filepath_or_buffer
        self.groups = groups
        self.df()
        self.pathway()


    def df(self) -> DataFrame:
        df: DataFrame = pd.read_csv(filepath_or_buffer = self.filepath_or_buffer, delimiter = ',')
        df: DataFrame = df[df['GROUP'].isin(self.groups)]
        return df


    def pathway(self):
        markup: Response = requests.get(url = 'https://www.genome.jp/kegg/pathway.html').text


        soup: BeautifulSoup = BeautifulSoup(markup = markup, features = 'html.parser')        

        groups: List[str] = [group.text[0] for group in soup.find_all('b')[1:8]]
        subgroups: List[str] = [subgroup.text.split()[0] for subgroup in soup.find_all('b')[8:]]
        entries: List[str] = [entry.text for entry in soup.find_all(attrs={'class': 'list'})]


        obj: Dict[str, Dict[str, List[str]]] = {}

        for group in groups:
            obj[group] = {}
            for index in range(len(subgroups)):
                if subgroups[index][0] == group:
                    obj[group][subgroups[index]] = [f'ec{entry[:5]}' for entry in entries[index].split('\n') if entry != '']

        
        return obj


    def entries(self):
        entries: DataFrame = self.df().groupby(by = ['GROUP', 'ONTOLOGY']).size().reset_index(name = 'COUNT')
        entries.to_csv(path_or_buf = 'entries.csv')


    def subgroups(self):
        subgroups: List[List[str | int]] = [['', 'SUBGROUP', 'COUNT']]

        for groups, subgroups in self.pathway().items():
            for subgroup, entries in subgroups:
                for entry in entries:
                    if entry in [entry for entry in self.df()['ONTOLOGY']]:
                        subgroups.append([subgroup, self.df()['ONTOLOGY'].loc[self.df()['ONTOLOGY'] == entry].count()])


        with open(file = 'subgroups.csv', mode = 'w', newline = '') as csvfile:
            writer: writer = csv.writer(csvfile = csvfile)
            writer.writerows(subgroups)
        
    

    
    
    
pp = KEGG('data.csv', [], [])
pp.pathway()

