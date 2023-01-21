from financeYahooScraper import financeYahooScraper
from dataParser import dataParser

financeYahooScraper = financeYahooScraper()

dataParser = dataParser(financeYahooScraper.raw_data, financeYahooScraper.configParser)