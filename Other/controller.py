import sys
import datetime
sys.path.insert(0, '..')

from DataScrapper.financeYahooScraper import financeYahooScraper
from DataHandler.dataParser import dataParser
from DataHandler.configParser import configParser
from Drawer.drawer import drawer


# data_list = [["DJI", "1671768778", "1677125581"], ["IXIC", "1671768778", "1677125581"], ["GSPC", "1671768778", "1677125581"], ["RUT", "1671768778", "1677125581"]]
data_list = [["GSPC", "1551228962", "1677125581"]]
average = 1

for idx, data in enumerate(data_list):
    
# Scrap data
    # financeYahooScraper_xd = financeYahooScraper(data[0], data[1], data[2])
    # dataParser_xd = dataParser(financeYahooScraper_xd.raw_data, financeYahooScraper_xd.configParser, average, idx)

# Read data from files
    configParser_xd = configParser()
    with open (f"../Other/data{idx}.text", "r") as file:
        dataParser_xd = dataParser(file.read(), configParser, average, idx)
    
    drawer_xd = drawer(dataParser_xd)

