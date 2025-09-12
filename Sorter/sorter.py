from Sorter.config import CONFIG
from glob import glob
from shutil import move
from os import path, mkdir
from datetime import datetime

def fixDuplicate(filePath) -> str:
    newName: str = filePath.split(".")
    newName[0] += "_" + str(int(datetime.timestamp(datetime.now())) % 1000000)
    return ".".join(newName)

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

    for destinationFolder in rule["destinationFolders"]:
        for extension in destinationFolder["extensions"]:
            for fileName in glob(f'*{extension}'):
                currentFilePath: str = rule["sourceFolder"] + "/" + fileName
                newFilePath: str = destinationFolder["destinationPath"] + "/" + fileName
                print(currentFilePath)
                print(newFilePath)

                if not path.isdir(destinationFolder["destinationPath"]):
                    mkdir(destinationFolder["destinationPath"])

                while path.isfile(newFilePath):
                    newFilePath = destinationFolder["destinationPath"] + "/" + fixDuplicate(fileName)

                move(currentFilePath, newFilePath)

class SORTER:

    def sortAll(self) -> None:
        for rule in self.ruleList:
            sortFolderByExtensions(rule)

    def __init__(self, config: CONFIG) -> None:
        self.ruleList: list = config.rulesList


# TEST
if __name__ == "__main__":
    pass