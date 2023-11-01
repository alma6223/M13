import pandas as pd
from bs4 import BeautifulSoup
import requests


class KEGG:
    def __init__(self,  filepath_or_buffer: str, groups: list) -> None:
        """
        Constructor de la clase KEGG.

        :param filepath_or_buffer: Ruta del archivo o búfer de datos.
        :param groups: Lista de grupos para filtrar los datos.
        """
        self.filepath_or_buffer = filepath_or_buffer
        self.groups = groups


    def getDataFrame(self) -> pd.DataFrame:
        """
        Carga los datos desde el archivo o búfer y filtra por grupos.

        :return: DataFrame con los datos filtrados.
        """
        delimiter: str = ','

        dataFrame: pd.DataFrame = pd.read_csv(self.filepath_or_buffer, delimiter = delimiter)
        dataFrame: pd.DataFrame = dataFrame[dataFrame['GROUP'].isin(self.groups)]


        return dataFrame


    def getPathway(self) -> list:
        """
        Obtiene información sobre las vías de KEGG desde la página web.

        :return: Lista de vías de KEGG con grupos, subgrupos y entradas.
        """
        url: str = 'https://www.genome.jp/kegg/pathway.html'

        markup: requests.models.Response = requests.get(url).text


        features: str = 'html.parser'

        soup: BeautifulSoup = BeautifulSoup(markup, features)        


        name: str = 'b'
        attrs: dict = {'class': 'list'}

        groups: list = [group.text[0] for group in soup.find_all(name)[1:8]]
        subgroups: list = [subgroup.text.split()[0] for subgroup in soup.find_all(name)[8:]]
        entries: list = [entry.text for entry in soup.find_all(attrs = attrs)]


        pathway: list = []

        for group in groups:
            for index in range(len(subgroups)):
                if subgroups[index][0] == group:
                    entry: list = [f'ec{entry[:5]}' for entry in entries[index].split('\n') if entry != '']
                    pathway.append([group, subgroups[index], entry])
        

        return pathway


    def getEntries(self, path_or_buf: str) -> pd.DataFrame:
        """
        Obtiene las entradas de datos según su entrada y las guarda en un archivo CSV.

        :param path_or_buf: Ruta donde se guarda el archivo CSV.
        :return: DataFrame con las entradas de datos.
        """
        by: list = ['GROUP', 'ONTOLOGY']
        columns: dict = {'ONTOLOGY': 'PATHWAY'}

        dataFrame: pd.DataFrame = self.getDataFrame().groupby(by).size().reset_index(name = 'COUNT')
        dataFrame: pd.DataFrame = dataFrame.rename(columns = columns)


        index: bool = False
        dataFrame.to_csv(path_or_buf, index = index)


        return dataFrame
    

    def __getData(self, process: str, path_or_buf: str) -> pd.DataFrame:
        """
        Método privado para obtener datos según el proceso especificado.

        :param process: Proceso ('subgroups' o 'groups') para el que se obtienen los datos.
        :param path_or_buf: Ruta donde se guarda el archivo CSV.
        :return: DataFrame con los datos según el proceso.
        """
        data: list = []
        entries: pd.Series = self.getDataFrame()['ONTOLOGY']

        for pathway in self.getPathway():
            for entry in pathway[2]:
                if entry in [entry for entry in entries]:
                    count: int = self.getDataFrame()[entries == entry]['ONTOLOGY'].count()
                    group: str = self.getDataFrame()[entries == entry]['GROUP'].values[0]
                    match process:
                        case 'subgroups':
                            data.append([group, pathway[1], count])
                        case 'groups':
                            data.append([group, pathway[0], count])


        columns: list = ['GROUP', 'PATHWAY', 'COUNT']
        by: list = ['GROUP', 'PATHWAY']

        dataFrame: pd.DataFrame = pd.DataFrame(data, columns = columns)
        dataFrame: pd.DataFrame = dataFrame.groupby(by)['COUNT'].sum().reset_index()


        index: bool = False
        dataFrame.to_csv(path_or_buf, index = index)


        return dataFrame


    def getSubgroups(self, path_or_buf: str) -> pd.DataFrame:
        """
        Obtiene datos de subgrupos según su entrada y los guarda en un archivo CSV.

        :param path_or_buf: Ruta donde se guarda el archivo CSV.
        :return: DataFrame con datos de subgrupos.
        """
        return self.__getData('subgroups', path_or_buf)


    def getGroups(self, path_or_buf: str) -> pd.DataFrame:
        """
        Obtiene datos de grupos según su entrada y los guarda en un archivo CSV.

        :param path_or_buf: Ruta donde se guarda el archivo CSV.
        :return: DataFrame con datos de grupos.
        """
        return self.__getData('groups', path_or_buf)

