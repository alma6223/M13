import os
import zipfile
import shutil


class Dataset:
    def __init__(self, origin: str, destination: str) -> None:
        self.origin = origin
        self.destination = destination

    def decompress(self) -> None:
        directories: list[str] = os.listdir(self.origin)
        for directory in directories:
            path: str = os.path.join(self.origin, directory)
            with zipfile.ZipFile(path, 'r') as zip:
                zip.extractall(self.destination)

    def copy(self):
        sequence: int = 1
        directories: list[str] = os.listdir(self.destination)
        for directory in directories:
            path: str = os.path.join(self.destination, directory)
            files: list[str] = os.listdir(path)
            
            for file in files:
                extension: str = os.path.splitext(file)[1]
                filename: str = f'frame_{sequence:04d}{extension}'
                origin: str = os.path.join(self.destination, directory, file)
                destination: str = os.path.join(self.destination, filename)

                shutil.copy(origin, destination)
                sequence += 1
            
        
    