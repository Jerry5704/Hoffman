import configparser

class configParser():
    
    def __init__(self):
        self.configParser = configparser.RawConfigParser()   
        configFilePath = r'config.cfg'
        self.configParser.read(configFilePath)
        