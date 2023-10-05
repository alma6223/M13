import os
import zipfile as zf


class Dataset:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.directories = os.listdir(self.origin)


    def decompress(self):
        size = len(self.directories)
        for index in range(size):
            path = f'{self.origin}/{self.directories[index]}'
            zips = os.listdir(path)
            with zf.ZipFile(zips, 'r') as zip:
                zip.extractall(self.origin)
            


ola = Dataset('D:/thetys_mariadelahoz_6_2023', 'adad')
ola.decompress()
        
        
    