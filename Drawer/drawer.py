import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from DataHandler.dataParser import dataParser

class drawer():          

    def draw_line_chart(self):
        self.prices = self.dataParser.get_prices(len(self.candlesticks_list), 0)

        y_axis = list(reversed(np.array(self.prices)))
        
        # ToDo: change to actual dates
        x_axis = []
        counter = 1
        for _ in y_axis:
            x_axis.append(counter)
            counter += 1

        x_axis = list(reversed(x_axis))

        plt.xlim([0, len(self.candlesticks_list)])

        plt.plot(x_axis, y_axis, color="black")

        #  draw support lines
        for candlestick in self.candlesticks_list:
            x_values = []
            y_values = []
            if candlestick.is_support:
                x_values.append(candlestick.number + 0.5)   
                x_values.append(candlestick.number + 1.5)   
                y_values.append(candlestick.close)   
                y_values.append(candlestick.close)   
                plt.plot(x_values, y_values, color="yellow")

        #  draw resistance lines
        for candlestick in self.candlesticks_list:
            x_values = []
            y_values = []
            if candlestick.is_resistance:
                x_values.append(candlestick.number + 0.5)   
                x_values.append(candlestick.number + 1.5)   
                y_values.append(candlestick.close)   
                y_values.append(candlestick.close)   
                plt.plot(x_values, y_values, color="cyan")

        # draw up_trendlines
        for candlesticks_lists in self.dataParser.up_trendLine_candlesticks_list:
            x_values = []
            y_values = []
            for candlestick in candlesticks_lists:
                x_values.append(candlestick.number + 1)
                y_values.append(candlestick.close)
            plt.plot(x_values, y_values, color="yellow")
        
        # draw down_trendlines
        for candlesticks_lists in self.dataParser.down_trendLine_candlesticks_list:
            x_values = []
            y_values = []
            for candlestick in candlesticks_lists:
                x_values.append(candlestick.number + 1)
                y_values.append(candlestick.close)
            plt.plot(x_values, y_values, color="cyan")

        # draw fans
        for fan_list in self.dataParser.fans_list:
            x_values = [fan_list[0].number + 1, fan_list[-1][0] + 1]
            y_values = [fan_list[0].close, fan_list[-1][1]]
            plt.plot(x_values, y_values, color="pink")

        plt.show()

    def draw_candlestick_chart(self):
        self.opens = list(reversed(self.dataParser.get_opens(len(self.candlesticks_list), 0)))
        self.closes = list(reversed(self.dataParser.get_prices(len(self.candlesticks_list), 0)))
        self.highs = list(reversed(self.dataParser.get_highs(len(self.candlesticks_list), 0)))
        self.lows = list(reversed(self.dataParser.get_lows(len(self.candlesticks_list), 0)))

        data_frame = pd.DataFrame({
            'open': self.opens,
            'close': self.closes,
            'high': self.highs,
            'low': self.lows,
        })

        #create figure
        plt.figure()

        #define width of candlestick elements
        width = .4
        width2 = .05

        #define up and down data_frame
        up = data_frame[data_frame.close>=data_frame.open]
        down = data_frame[data_frame.close<data_frame.open]

        #define colors to use
        col1 = 'green'
        col2 = 'red'

        #plot up data_frame
        plt.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
        plt.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
        plt.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)

        #plot down data_frame
        plt.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
        plt.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
        plt.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)

        #change to dates x-axis tick labels
        x_axis = []
        counter = 0
        for _ in self.opens:
            x_axis.append(counter)
            counter += 1
        self.dates = self.dataParser.get_dates(len(self.candlesticks_list), 0)
        plt.xticks(x_axis, self.dates, rotation=45)

        #display candlestick chart
        plt.show()

        

    def __init__(self, dataParser):
        self.dataParser = dataParser
        self.candlesticks_list = dataParser.candlesticks_list

        self.draw_line_chart()
        # self.draw_candlestick_chart()