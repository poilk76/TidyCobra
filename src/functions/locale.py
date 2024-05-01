import json
from src.functions.config import CONFIGURATIONMAIN

def getLocale() -> dict:
    conf = CONFIGURATIONMAIN()
    
    with open(f"src/locale/{conf.lang}.json") as f:
        data = f.read()

    return json.loads(data)