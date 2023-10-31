import pandas as pd
from bs4 import BeautifulSoup
import csv


class KEGG:
    def __init__(self,  filepath_or_buffer, groups):
        self.filepath_or_buffer = filepath_or_buffer
        self.groups = groups
        self.df()
        self.pathway()


    def df(self):
        df = pd.read_csv(self.filepath_or_buffer, delimiter = ',')
        df = df[df['GROUP'].isin(self.groups)]
        return df


    def pathway(self):
        with open('KEGG PATHWAY Database.html') as markup:
            soup = BeautifulSoup(markup, 'html.parser')        


        groups = [group.text[0] for group in soup.find_all('b')[1:8]]
        subgroups = [subgroup.text.split()[0] for subgroup in soup.find_all('b')[8:]]
        entries = [entry.text for entry in soup.find_all(attrs={'class': 'list'})]


        pathway = []

        for group in groups:
            for index in range(len(subgroups)):
                if subgroups[index][0] == group:
                    pathway.append([group, subgroups[index], [f'ec{entry[:5]}' for entry in entries[index].split('\n') if entry != '']])

        
        return pathway


    def entries(self):
        entries = self.df().groupby(['GROUP', 'ONTOLOGY']).size().reset_index(name = 'COUNT')
        entries.to_csv('entries.csv')


    def subgroups(self):
        subgroups = []


        for index in range(len(self.pathway())):
            for entry in self.pathway()[index][2]:
                if entry in [entry for entry in self.df()['ONTOLOGY']]:
                    count = self.df()['ONTOLOGY'].loc[self.df()['ONTOLOGY'] == entry].count()
                    group = self.df()['GROUP'].loc[self.df()['ONTOLOGY'] == entry]
                    subgroups.append([group, self.pathway()[index][1], count])


        with open('subgroups.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(subgroups)
    

    
    
    
data = KEGG('data.csv', [
    'fecal.Control.control_vs_fecal.CU.3.meses',
    'fecal.Control.control_vs_fecal.CU.6.meses',
    'fecal.Control.control_vs_fecal.CU.debut',
    'fecal.CU.6.meses_vs_fecal.CU.debut'
])


