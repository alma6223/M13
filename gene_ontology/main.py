import requests
import pandas as pd
import csv



def ancestors(ontologies: list, groups: list) -> pd.DataFrame:
    data: list = []
    for ontology, group in zip(ontologies, groups):
        url: str = f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{ontology.replace(':', '%3A')}/ancestors?relations=is_a%2Cpart_of%2Coccurs_in%2Cregulates"
        request: requests.Request = requests.get(url, headers={'Accept': 'application/json'})
        response: requests.Response = request.json()
        ancestors: list = response['results'][0]['ancestors']
        ancestors.remove(ontology)
        data.append([group, ancestors, ontology])
    for i in data:
        print(i)


df = pd.read_csv('dataset.csv')
df = df[df['GROUP'].isin(['oral.CU.3.meses_vs_oral.CU.debut'])].head(5)
ancestors(df['ONTOLOGY'], df['GROUP'])

