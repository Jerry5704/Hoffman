import sys
import datetime
sys.path.insert(0, '..')

from DataScrapper.financeYahooScraper import financeYahooScraper
from DataHandler.dataParser import dataParser
from DataHandler.configParser import configParser
from Drawer.drawer import drawer


l = [["DJI", "1550620800", "1676851200"], ["IXIC", "1550620800", "1676851200"], ["GSPC", "1550620800", "1676851200"], ["RUT", "1550620800", "1676851200"]]

# financeYahooScraper = financeYahooScraper("DJI", "1668902400", "1676764800")
# financeYahooScraper = financeYahooScraper("IXIC", "1668902400", "1676764800")

counter = 0
for q in l:
    # financeYahooScraper_xd = financeYahooScraper(q[0], q[1], q[2])
    # dataParser_xd = dataParser(financeYahooScraper_xd.raw_data, financeYahooScraper_xd.configParser, counter)

    configParser_xd = configParser()
    with open (f"../Other/data{counter}.text", "r") as file:
        dataParser_xd = dataParser(file.read(), configParser, counter)
    
    drawer_xd = drawer(dataParser_xd)

    counter += 1
