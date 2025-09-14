from pubsub import pub
from json import load, dump
from os import path
from platform import system

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


class Config:

    def saveConfig(self) -> None:
        
        with open(self.configFilePath, 'w') as configFile:
            dump({
                    "operatingSystem": self.system,
                    "startup": self.startup,
                    "rulesList": self.rulesList
                }, configFile)


    def loadConfig(self) -> None:

        with open(self.configFilePath, 'r') as configFile:
            dummy = load(configFile)

        self.system: str = dummy["operatingSystem"]
        self.startup: bool = dummy["startup"]
        self.rulesList: dict = dummy["rulesList"]

        del dummy
            

    def __init__(self, configFilePath: str = "./config.json") -> None:

        if not path.isfile(configFilePath):

            with open(configFilePath, 'w+') as configFile:
                dump(configTemplate, configFile)
        
        self.configFilePath = configFilePath
        self.loadConfig()


# TEST
if __name__ == "__main__":
    pass