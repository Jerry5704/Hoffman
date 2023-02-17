import datetime
import statistics
import pandas as pd

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

    def get_candlesticks_list(self):
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
        return list_of_candlesticks

    def get_avreage_candlestick_body(self):
        self.candlestick_body_list = []
        for candlestick in self.candlesticks_list:
            self.candlestick_body_list.append(candlestick.body)
        return statistics.fmean(self.candlestick_body_list)

    # long body means that current candlestick body is at least twice as long as regular* candlestick body
    # * by regular I mean avreage for every candlestick body in the list
    def get_is_long_body(self, candlestick, current_candlestick_index):
        if self.candlesticks_list[current_candlestick_index].body > 2 * self.get_avreage_candlestick_body():
            return True
        return False 

    def get_candlesticks_length_type(self, candlestick, current_candlestick_index):
        if self.get_is_long_body(candlestick, current_candlestick_index):
            return "long"
        else:
            return "short" 

    def get_pattern(self, candlestick):
        if candlestick.length_type == "long" and candlestick.has_lower_wick == False and candlestick.has_upper_wick == False:
            return "marubozu"
        return "no pattern found"

    def get_trend_direction(self, candlestick, current_candlestick_index):
        pass

    def get_is_support(self, candlestick, current_candlestick_index):
        try:
            if self.candlesticks_list[current_candlestick_index - 1].close > self.candlesticks_list[current_candlestick_index].close and  self.candlesticks_list[current_candlestick_index + 1].close > self.candlesticks_list[current_candlestick_index].close:
                return True
        except:
            return False
        return False

    def get_is_resistance(self, candlestick, current_candlestick_index):
        try:
            if self.candlesticks_list[current_candlestick_index - 1].close < self.candlesticks_list[current_candlestick_index].close and  self.candlesticks_list[current_candlestick_index + 1].close < self.candlesticks_list[current_candlestick_index].close:
                return True
        except:
            return False
        return False

    def classify_candlestick(self, candlestick, current_candlestick_index):
        candlestick.number = current_candlestick_index
        candlestick.length_type = self.get_candlesticks_length_type(candlestick, current_candlestick_index)
        candlestick.pattern = self.get_pattern(candlestick)
        candlestick.is_support = self.get_is_support(candlestick, current_candlestick_index)
        candlestick.is_resistance = self.get_is_resistance(candlestick, current_candlestick_index)
        # candlestick.trend_direction = self.get_trend_direction(candlestick, current_candlestick_index)

        current_candlestick_index += 1
        return candlestick

    def get_prices(self, days, current_candlestick_index):
        return [candlestick.close for candlestick in self.candlesticks_list[current_candlestick_index : current_candlestick_index + 1 + days]]

    def get_opens(self, days, current_candlestick_index):
        return [candlestick.open for candlestick in self.candlesticks_list[current_candlestick_index : current_candlestick_index + 1 + days]]

    def get_highs(self, days, current_candlestick_index):
        return [candlestick.high for candlestick in self.candlesticks_list[current_candlestick_index : current_candlestick_index + 1 + days]]

    def get_lows(self, days, current_candlestick_index):
        return [candlestick.low for candlestick in self.candlesticks_list[current_candlestick_index : current_candlestick_index + 1 + days]]
    
    def get_dates(self, days, current_candlestick_index):
        return [candlestick.date for candlestick in self.candlesticks_list[current_candlestick_index: current_candlestick_index + 1 + days]]

    def get_ema(self, days, current_candlestick_index):
        self.prices = pd.DataFrame(
            {'Stock_Values': self.get_prices(days, current_candlestick_index)})
        return self.prices.ewm(com=0.4).mean()

    def classify_candlesticks_list(self):
        current_candlestick_index = 0
        for candlestick in self.candlesticks_list:
            self.classify_candlestick(candlestick, current_candlestick_index)
            current_candlestick_index += 1
    
    def print_candlesticks(self):
        candlestick_number = 0
        for candlestick in self.candlesticks_list:
            candlestick_number += 1
            # if candlestick.is_support is True:
            print("================================")
            print(f"candlestick number: {candlestick_number}")
            print(f"date: {candlestick.date}")
            print(f"open: {candlestick.open}")
            print(f"close: {candlestick.close}")
            print(f"high: {candlestick.high}")
            print(f"low: {candlestick.low}")
            print(f"volume: {candlestick.volume}")
            print(f"color: {candlestick.color}")
            print(f"body: {candlestick.body}")
            print(f"has upper wick?: {candlestick.has_upper_wick}")
            print(f"has lower wick?: {candlestick.has_lower_wick}")
            print(f"upper shadow: {candlestick.upper_shadow}")
            print(f"lower shadow: {candlestick.lower_shadow}")
            print(f"length type: {candlestick.length_type}")
            print(f"pattern: {candlestick.pattern}")
            print(f"is support: {candlestick.is_support}")
            print(f"is resistance: {candlestick.is_resistance}")
            print("================================")

    def __init__(self, raw_data, configParser):
        self.raw_data = raw_data
        self.configParser = configParser
        self.frequency = self.get_frequency()
        self.data_lines_list = [line for line in self.raw_data.split('\n')]
        # self.data_lines_list = [line for line in self.raw_data.text.split('\n')]
        self.candlesticks_list = self.get_candlesticks_list()
        self.classify_candlesticks_list()

        # with open ("data.text", "w") as file:
        #     file.write(self.raw_data.text)
        # print(self.raw_data.text)
        self.print_candlesticks()
        