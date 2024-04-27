from json import loads, dumps
from os import listdir

class CONFIGURATIONRULE:
    
    def __init__(self,path) -> None:
        with open(f"src/rules/{path}",'r') as f:
            self.data = f.read()
        dataDict = loads(self.data)
        self.name = dataDict["name"]
        self.mainPath = dataDict["mainPath"]
        self.rules = dataDict["rules"]

    def __repr__(self) -> str:
        return self.data
    
def getRuleSets() -> list:

    paths = [rule.split('.')[0] for rule in listdir("src/rules")]

    return paths

def saveConfig(name:str, mainPath:str, rules:list) ->None:

    conf = {"name": name,
            "mainPath": mainPath,
            "rules":rules}
    
    with open(f'src/rules/{name}.json', 'w') as f:
        f.write(dumps(conf))