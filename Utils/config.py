from json import load, dump
from os import path

configTemplate: dict = {
    "startup": False,
    "isIntervalRunning": False,
    "interval": 15000,
    "rulesList": [
        #  {
        #      "sourceFolder": "<path to source folder>",
        #      "destinationFolders": [
        #           {
        #               "extensions": [<file extensions like .pdf, .png, ...>],
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
                    "isIntervalRunning": self.isIntervalRunning,
                    "interval":self.interval,
                    "startup": self.startup,
                    "rulesList": self.rulesList
                }, configFile)


    def loadConfig(self,configFilePath:str) -> None:

        with open(configFilePath, 'r') as configFile:
            dummy:dict = load(configFile)

        if "rules" in dummy.keys():
            # old config format support
            self.isIntervalRunning: bool = False
            self.interval: int = 15000
            self.startup: bool = False
            self.rulesList: list = [
                {
                    "sourceFolder": dummy["path_downloads"],
                    "destinationFolders": [
                        {
                            "destinationPath": rule[0],
                            "extensions": rule[1].split(" ")
                        }
                        for rule in dummy["rules"]
                    ]
                }
            ]
        else:
            self.isIntervalRunning: bool = dummy["isIntervalRunning"]
            self.interval: int = dummy["interval"]
            self.startup: bool = dummy["startup"]
            self.rulesList: list = dummy["rulesList"]
            

    def __init__(self, configFilePath: str = "./config.json") -> None:

        if not path.isfile(configFilePath):

            with open(configFilePath, 'w+') as configFile:
                dump(configTemplate, configFile)
        self.configFilePath = configFilePath
        self.loadConfig(self.configFilePath)