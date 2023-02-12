import sys
sys.path.insert(0, '..')

from financeYahooScraper import financeYahooScraper
from dataParser import dataParser
from configParser import configParser
from drawer.drawer import drawer

# financeYahooScraper = financeYahooScraper()

configParser = configParser()

with open ("data.text", "r") as file:
    dataParser = dataParser(file.read(), configParser.configParser)

drawer = drawer(dataParser)