import json
def getConfig():
  with open('data/config.json', 'r',encoding='utf-8') as f:
    config = json.load(f)
    return config

def updateConfig(new_config):
    with open('data/config.json', 'w',encoding='utf-8') as f:
        json.dump(new_config, f,ensure_ascii=False)
        return new_config