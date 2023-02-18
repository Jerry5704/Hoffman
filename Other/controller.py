import sys
sys.path.insert(0, '..')

from DataScrapper.financeYahooScraper import financeYahooScraper
from DataHandler.dataParser import dataParser
from DataHandler.configParser import configParser
from Drawer.drawer import drawer

# financeYahooScraper = financeYahooScraper()

# dataParser = dataParser(financeYahooScraper.raw_data, financeYahooScraper.configParser)

configParser = configParser()

with open ("../DataForms/data.text", "r") as file:
    dataParser = dataParser(file.read(), configParser)

drawer = drawer(dataParser)