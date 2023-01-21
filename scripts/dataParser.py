import datetime

from candlestick import Candlestick

class dataParser():

    def get_frequency(self):
        return self.configParser.get('YAHOO', 'url')

    def get_month(self, month_name):
        if month_name == "Jan":
            return 1
        elif month_name == "Feb":
            return 2
        elif month_name == "Mar":
            return 3
        elif month_name == "Apr":
            return 4
        elif month_name == "May":
            return 5
        elif month_name == "Jun":
            return 6
        elif month_name == "Jul":
            return 7
        elif month_name == "Aug":
            return 8
        elif month_name == "Sep":
            return 9
        elif month_name == "Oct":
            return 10
        elif month_name == "Nov":
            return 11
        elif month_name == "Dec":
            return 12

    def __init__(self, raw_data, configParser):
        self.raw_data = raw_data
        self.configParser = configParser
        self.frequency = self.get_frequency()
        self.data_lines_list = [line for line in self.raw_data.text.split('\n')]
        list_of_candlesticks = []
        for line in self.data_lines_list[4:-1]:
            line_split = line.split(' ')
            year = int(line_split[2])
            month = self.get_month(line_split[0])
            day = line_split[1].strip(',')
            day_date = datetime.date(int(year), month, int(day))
            open = line_split[3]
            high = line_split[4]
            low = line_split[5]
            close = line_split[6]
            volume = line_split[8]
            list_of_candlesticks.append(Candlestick(day_date, open, high, low, close, volume))
        for candlestick in list_of_candlesticks:
            print(candlestick.date)