from GUI import viewMain
from os import path
from json import dump
from platform import system

configFilePath: str = "./config.json"
configTemplate: dict = {
    "operatingSystem": system(),
    "startup": False,
    "rulesList": [
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
        {
            "sourceFolder": "",
            "destinationFolders": []
        }
    ]
}

if __name__ == "__main__":

    if not path.isfile(configFilePath):

        with open(configFilePath, 'w+') as configFile:
            dump(configTemplate, configFile)
    
    viewMain.renderGui()