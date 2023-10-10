import os
import zipfile as zf
import tarfile as tf


class Dataset:
    def __init__(self, origin: str, destination: str):
        self.origin = origin
        self.destination = destination


    def decompress(self):
        directories: list[str] = os.listdir(self.origin)
        for directory in directories:
            path: str = os.path.join(self.origin, directory)
            with zf.ZipFile(path, 'r') as zip:
                zip.extractall(self.destination)
            


ola = Dataset('D:/thetys_mariadelahoz_6_2023', 'D:/prueba')
ola.decompress()
        
        
    