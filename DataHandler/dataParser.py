import datetime
import statistics
import configparser
import pandas as pd

from DataForms.candlestick import Candlestick
from DataForms.trendLine import TrendLine
from DataForms.fan import Fan

class dataParser():

    def get_frequency(self):
        return "https://finance.yahoo.com/quote/%5EDJI/history?period1=1643334840&period2=1674856022&interval=<frequency>&filter=history&frequency=1d&includeAdjustedClose=true&guccounter=1"

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

    def get_candlesticks_list(self, average):
        list_of_candlesticks = []
        if average == 1:
            for line in self.data_lines_list[4:-1]:
                line_split = line.split(' ')
                year = int(line_split[2])
                month = self.get_month(line_split[0])
                day = line_split[1].strip(',')
                day_date = datetime.date(int(year), month, int(day))
                open = float(line_split[3].replace(",", ""))
                high = float(line_split[4].replace(",", ""))
                low = float(line_split[5].replace(",", ""))
                close = float(line_split[6].replace(",", ""))
                volume = float(line_split[8].replace(",", ""))
                list_of_candlesticks.append(Candlestick(day_date, open, high, low, close, volume))
        elif average > 1:
            list_of_average_candlesticks = []
            for i in range(0, len(self.data_lines_list[4:-1]), average):
                list_of_average_candlesticks.append(self.data_lines_list[4:-1][i:i + average])
            for average_candlesticks_list in list_of_average_candlesticks:
                average_open = 0
                average_high = 0
                average_low = 0
                average_close = 0
                average_volume = 0
                for candlestick in average_candlesticks_list:
                    candlestick_split = candlestick.split(' ')
                    year = int(candlestick_split[2])
                    month = self.get_month(candlestick_split[0])
                    day = candlestick_split[1].strip(',')
                    day_date = datetime.date(int(year), month, int(day))
                    average_open += float(candlestick_split[3].replace(",", ""))
                    average_high += float(candlestick_split[4].replace(",", ""))
                    average_low += float(candlestick_split[5].replace(",", ""))
                    average_close += float(candlestick_split[6].replace(",", ""))
                    average_volume += float(candlestick_split[8].replace(",", ""))
                average_open = average_open / average
                average_high = average_high / average
                average_low = average_low / average
                average_close = average_close / average
                average_volume = average_volume / average
                list_of_candlesticks.append(Candlestick(day_date, average_open, average_high, average_low, average_close, average_volume))
                
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

    def get_next_resistance_candlestick(self, candlestick, current_candlestick_index):
        for candlestick in self.candlesticks_list[current_candlestick_index + 1:]:
            if candlestick.is_resistance:
                return candlestick

    def get_next_support_candlestick(self, candlestick, current_candlestick_index):
        for candlestick in self.candlesticks_list[current_candlestick_index + 1:]:
            if candlestick.is_support:
                return candlestick

    def get_previous_resistance_candlestick(self, candlestick, current_candlestick_index):
        for candlestick in reversed(self.candlesticks_list[:current_candlestick_index - 1]):
            if candlestick.is_resistance:
                return candlestick
        
    def get_previous_support_candlestick(self, candlestick, current_candlestick_index):
        for candlestick in reversed(self.candlesticks_list[:current_candlestick_index - 1]):
            if candlestick.is_support:
                return candlestick

    def classify_candlestick(self, candlestick, current_candlestick_index, number_of_candlesticks):
        candlestick.number = number_of_candlesticks - current_candlestick_index
        # candlestick.number = current_candlestick_index
        candlestick.length_type = self.get_candlesticks_length_type(candlestick, current_candlestick_index)
        candlestick.pattern = self.get_pattern(candlestick)
        candlestick.is_support = self.get_is_support(candlestick, current_candlestick_index)
        candlestick.is_resistance = self.get_is_resistance(candlestick, current_candlestick_index)

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

    def classify_candlesticks_list(self):
        number_of_candlesticks = len(self.candlesticks_list)
        for current_candlestick_index, candlestick in enumerate(self.candlesticks_list):
            self.classify_candlestick(candlestick, current_candlestick_index, number_of_candlesticks)

    def get_up_trendLine_candlesticks_list(self):
        return TrendLine("up", self.support_candlesticks_list).trends_list

    def get_down_trendLine_candlesticks_list(self):
        return TrendLine("down", self.resistance_candlesticks_list).trends_list

    def get_fans_list(self):
        return Fan(self.candlesticks_list, self.up_trendLine_candlesticks_list, self.down_trendLine_candlesticks_list).fans_list
    
    def print_candlesticks(self):
        for candlestick in self.candlesticks_list:
            print("================================")
            print(f"candlestick number: {candlestick.number}")
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

    def __init__(self, raw_data, configParser, average, counter):
        self.now = datetime
        self.raw_data = raw_data
        self.configParser = configparser
        self.frequency = self.get_frequency()
        self.data_lines_list = [line for line in self.raw_data.split('\n') if line != "Download"]
        self.candlesticks_list = self.get_candlesticks_list(average)
        self.classify_candlesticks_list()


        self.resistance_candlesticks_list = [candlestick for candlestick in self.candlesticks_list if candlestick.is_resistance]
        self.support_candlesticks_list = [candlestick for candlestick in self.candlesticks_list if candlestick.is_support]
        self.up_trendLine_candlesticks_list = self.get_up_trendLine_candlesticks_list()
        self.down_trendLine_candlesticks_list = self.get_down_trendLine_candlesticks_list()


        # The Fan Principle
        self.fans_list = self.get_fans_list()

        # for candlestick in self.up_trendLine_candlesticks_list.trends_list:
        #     print(candlestick)

        # self.sideways_trendLine_list = self.get_sideways_trendLine_list()

        with open (f"data{counter}.text", "w") as file:
            file.write(self.raw_data)
        
        # self.print_candlesticks()