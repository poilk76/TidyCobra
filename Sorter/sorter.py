from Sorter.config import Config
from glob import glob
from shutil import move
from os import path

def sortFolderByExtensions(rule: dict) -> None:

    #  rule format:
    #  {
    #      "sourceFolder": "<path to source folder>",
    #      "destinationFolders": [
    #           {
    #               "extensions": [<file extensions like pdf, png, ...>],
    #               "destinationPath": "<path where file should go>"
    #           },
    #           ...
    #      ]
    #  }, ...

    sourceFolder:str = rule["sourceFolder"]
    if not sourceFolder or not path.isdir(sourceFolder):
        return
    
    extensionsMapping:dict = {}
    for folder in rule["destinationFolders"]:
        for extension in folder["extensions"]:

            if extension in extensionsMapping.keys():
                continue

            if not path.isdir(folder["destinationPath"]):
                continue

            extensionsMapping[extension] = folder["destinationPath"]

    files:list = glob(f'{sourceFolder}/*')
    for file in files:
        fileExtension:str = "."+file.split('.')[-1]

        if not fileExtension in extensionsMapping.keys():
            continue
        
        fileName:str = path.basename(file)
        newFilePath:str = f'{extensionsMapping[fileExtension]}/{fileName}'

        i:int = 1
        while path.isfile(newFilePath):
            newFilePath = f'{extensionsMapping[fileExtension]}/d{i}_{fileName}'
            i += 1

        move(file,newFilePath)

class Sorter:

    def sortAll(self) -> None:
        for rule in self.ruleList:
            sortFolderByExtensions(rule)

    def __init__(self, config: Config) -> None:
        self.ruleList: list = config.rulesList


# TEST
if __name__ == "__main__":
    pass