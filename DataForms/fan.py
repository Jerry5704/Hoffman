class Fan():
    
    def get_a(self, x1, y1, x2, y2):
        return (y2 - y1) / (x2 - x1)

    def get_b(self, y1, x1, a):
        return y1 - a * x1

    def get_next_resistance_candlestick(self, searched_candlestick):
        try:
            for candlestick in self.candlesticks_list[searched_candlestick.number + 1:]:
                if candlestick.is_resistance:
                    return candlestick
        except AttributeError as last_candlestick_exception:
            print(last_candlestick_exception)
            pass

    def get_next_support_candlestick(self, searched_candlestick):
        try:
            for candlestick in self.candlesticks_list[searched_candlestick.number:]:
                if candlestick.is_support:
                    return candlestick
        except AttributeError as last_candlestick_exception:
            pass

    def get_fan_break_candlestick(self, first_support_candlestick, fifth_support_candlestick):
        a3 = self.get_a(first_support_candlestick.number,
                        first_support_candlestick.close,
                        fifth_support_candlestick.number,
                        fifth_support_candlestick.close)
        b3 = self.get_b(first_support_candlestick.close, fifth_support_candlestick.number, a3)
        spread_parameter = 0.03
        for candlestick in self.candlesticks_list[self.get_next_resistance_candlestick(fifth_support_candlestick).number:]:
            if (a3 * candlestick.number + b3) * (1 - spread_parameter) < candlestick.close + b3 < (a3 * candlestick.number + b3) * (1 + spread_parameter):
                return candlestick 

    def __init__(self, candlesticks_list, up_trendLine_candlesticks_list , down_trendLine_candlesticks_list):
        self.candlesticks_list = list(reversed(candlesticks_list))
        self.up_trendLine_3_candlesticks_list = [up_tradeline for up_tradeline in up_trendLine_candlesticks_list if len(up_tradeline) == 3]
        self.down_trendLine_3_candlesticks_list = [down_tradeline for down_tradeline in down_trendLine_candlesticks_list if len(down_tradeline) == 3]

        self.fans_list = []

        correction = 0.2

        # uptrend
        try:
            for trend in self.up_trendLine_3_candlesticks_list:
                first_support_candlestick = trend[-1]
                second_support_candlestick = trend[-2]
                third_support_candlestick = trend[-3]
                fourth_support_candlestick = self.get_next_support_candlestick(third_support_candlestick)
                fifth_support_candlestick = self.get_next_support_candlestick(fourth_support_candlestick)
                fan_break_candlestick = self.get_fan_break_candlestick(first_support_candlestick, fifth_support_candlestick)
                if fan_break_candlestick == None:
                    continue
                a1 = self.get_a(first_support_candlestick.number,
                                first_support_candlestick.close,
                                second_support_candlestick.number,
                                second_support_candlestick.close)
                b1 = self.get_b(second_support_candlestick.close, second_support_candlestick.number, a1)
                if fourth_support_candlestick.close > third_support_candlestick.close and fifth_support_candlestick.close < fourth_support_candlestick.close:
                    self.fans_list.append([first_support_candlestick, (third_support_candlestick.number, third_support_candlestick.close)])
                    self.fans_list.append([first_support_candlestick, (fourth_support_candlestick.number, fourth_support_candlestick.close)])
                    self.fans_list.append([first_support_candlestick, (fifth_support_candlestick.number, fifth_support_candlestick.close)])
                    self.fans_list.append([first_support_candlestick, (fan_break_candlestick.number, fan_break_candlestick.close)])
        except AttributeError as last_candlestick_exception:
            print(last_candlestick_exception)
            pass

        # # downtrend
        # for trend in self.down_trendLine_3_candlesticks_list:
        #     first_resistance_candlestick = trend[-1]
        #     second_resistance_candlestick = trend[-2]
        #     third_resistance_candlestick = trend[-3]
        #     fourth_resistance_candlestick = self.get_next_resistance_candlestick(third_resistance_candlestick)
        #     fifth_resistance_candlestick = self.get_next_resistance_candlestick(fourth_resistance_candlestick)
        #     fan_break_candlestick = self.get_fan_break_candlestick(fifth_resistance_candlestick)
        #     a1 = self.get_a(first_support_candlestick.number,
        #                     first_support_candlestick.close,
        #                     second_support_candlestick.number,
        #                     second_support_candlestick.close)
        #     b1 = self.get_b(second_support_candlestick.close, second_support_candlestick.number, a1)
            
        #     if fourth_support_candlestick.close < third_support_candlestick.close and fifth_support_candlestick.close < fourth_support_candlestick.close:
        #         # print(first_support_candlestick.number)
        #         self.fans_list.append([first_support_candlestick, (third_support_candlestick.number, third_support_candlestick.close)])
        #         self.fans_list.append([first_support_candlestick, (fourth_support_candlestick.number, fourth_support_candlestick.close)])
        #         self.fans_list.append([first_support_candlestick, (fifth_support_candlestick.number, fifth_support_candlestick.close)])
        #         # self.fans_list.append([first_support_candlestick, (fan_break_candlestick.number, fan_break_candlestick.close)])
                