from src.functions.config import CONFIGURATIONRULE
import os
import shutil
from datetime import datetime

class SORTER:

    def move(self,src:str, dst:str) -> None:

        shutil.move(os.path.join(src, self.src_file), os.path.join(dst, self.dst_file))

    def sort(self) -> None:
        
        for pool in self.configurations:
            if os.path.isdir(pool["path"]):
                filebase = os.listdir(pool["path"])
                for file in filebase:
                    if '.' in file:
                        ext = file.split('.')[1]
                        for rule in pool["rules"]:
                            if ext in rule[1]:
                                self.src_file = file
                                self.dst_file = f'{rule[0]}/{file}'
                                if os.path.isfile(self.dst_file):
                                    self.dst_file = self.src_file.replace(self.src_file.split("/")[-1],"") + \
                                    self.src_file.split("/")[-1].split(".")[0] + \
                                    f'_{str(int(datetime.timestamp(datetime.now()))%1000000)}'+\
                                    '.'+self.src_file.split("/")[-1].split(".")[1]
                            
                                self.move(pool["path"], pool["path"])
                

    def getConfigurations(self) -> None:

        result = []

        for file in os.listdir("src/rules/"):
            conf = CONFIGURATIONRULE(file)
            result.append({"path":conf.mainPath, "rules":conf.rules})

        self.configurations = result

    def __init__(self) -> None:

        self.getConfigurations()
