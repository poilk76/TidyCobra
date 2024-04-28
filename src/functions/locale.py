import json

def getLocale(lang:str) -> dict:
    
    with open(f"src/locale/{lang}.json") as f:
        data = f.read()

    return json.loads(data)