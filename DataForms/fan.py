class Fan():
    
    def get_a(self, x1, y1, x2, y2):
        return (y2 - y1) / (x2 - x1)

    def get_b(self, y1, x1, a):
        return y1 - a * x1

    def get_next_resistance_candlestick_number(self, searched_candlestick):
        for candlestick in self.candlesticks_list[searched_candlestick.number + 1:]:
            if candlestick.is_resistance:
                return candlestick.number

    def get_next_support_candlestick_number(self, searched_candlestick):
        for candlestick in self.candlesticks_list[searched_candlestick.number + 1:]:
            if candlestick.is_support:
                return candlestick.number
        
    def get_fan_break_point(self, second_projected_resistance_candlestick):
        after_second_projected_resistance_candlestick_close = self.candlesticks_list[second_projected_resistance_candlestick.number + 1].close 
        for candlestick in self.candlesticks_list[second_projected_resistance_candlestick.number:]:
            if candlestick.close > after_second_projected_resistance_candlestick_close * 0.9993 and \
               candlestick.close < after_second_projected_resistance_candlestick_close * 1.0007:
                return (candlestick.number, candlestick.close)
        return False
            
    def __init__(self, candlesticks_list, up_trendLine_candlesticks_list , down_trendLine_candlesticks_list):
        self.candlesticks_list = candlesticks_list
        self.up_trendLine_3_candlesticks_list = [up_tradeline for up_tradeline in up_trendLine_candlesticks_list if len(up_tradeline) == 3]
        self.down_trendLine_3_candlesticks_list = [down_tradeline for down_tradeline in down_trendLine_candlesticks_list if len(down_tradeline) == 3]

        self.fans_list = []

        # uptrend
        for trend in self.up_trendLine_3_candlesticks_list:
            self.starting_support_candlestick = trend[0]
            self.first_known_support_candlestick = trend[1]
            self.a1 = self.get_a(self.starting_support_candlestick.number,
                                 self.starting_support_candlestick.close,
                                 self.first_known_support_candlestick.number,
                                 self.first_known_support_candlestick.close)
            self.b1 = self.get_b(self.starting_support_candlestick.close, self.starting_support_candlestick.number, self.a1)
            try:
                first_projected_resistance_candlestick_number = self.get_next_resistance_candlestick_number(trend[-1])
                first_projected_resistance_candlestick = self.candlesticks_list[first_projected_resistance_candlestick_number]
                if first_projected_resistance_candlestick.close * 1.007 > self.a1 * first_projected_resistance_candlestick_number + self.b1 and \
                   first_projected_resistance_candlestick.close * 0.993 < self.a1 * first_projected_resistance_candlestick_number + self.b1:
                    second_projected_resistance_candlestick_number = self.get_next_resistance_candlestick_number(first_projected_resistance_candlestick)    
                    second_projected_resistance_candlestick = self.candlesticks_list[second_projected_resistance_candlestick_number]
                    if second_projected_resistance_candlestick.close * 1.007 > self.a1 * second_projected_resistance_candlestick_number + self.b1 and \
                       second_projected_resistance_candlestick.close * 0.993 < self.a1 * second_projected_resistance_candlestick_number + self.b1:
                        # Changed way of implementation xD
                        self.line3_a =  self.get_a(self.starting_support_candlestick.number,
                                                   first_projected_resistance_candlestick_number + 1,
                                                   self.starting_support_candlestick.close,
                                                   self.candlesticks_list[first_projected_resistance_candlestick_number + 1].close)
                        self.line3_b = self.get_b(self.starting_support_candlestick.close, self.starting_support_candlestick.close, self.line3_a)
                        self.fan_break_point = self.get_fan_break_point(second_projected_resistance_candlestick)
                        if self.fan_break_point:
                            self.fans_list.append([self.starting_support_candlestick, (first_projected_resistance_candlestick_number,
                                                                                        first_projected_resistance_candlestick.close)])
                            self.fans_list.append([self.starting_support_candlestick, (second_projected_resistance_candlestick_number,
                                                                                        second_projected_resistance_candlestick.close)])
                            self.fans_list.append([self.starting_support_candlestick, (self.fan_break_point[0], self.fan_break_point[1])])
            except Exception as e:
                print(e)
        
        # downtrend
        for trend in self.down_trendLine_3_candlesticks_list:
            self.starting_resistance_candlestick = trend[0]
            self.first_known_resistance_candlestick = trend[1]
            self.a1 = self.get_a(self.starting_resistance_candlestick.number,
                                 self.starting_resistance_candlestick.close,
                                 self.first_known_resistance_candlestick.number,
                                 self.first_known_resistance_candlestick.close)
            self.b1 = self.get_b(self.starting_resistance_candlestick.close, self.starting_resistance_candlestick.number, self.a1)
            try:
                first_projected_support_candlestick_number = self.get_next_support_candlestick_number(trend[-1])
                first_projected_support_candlestick = self.candlesticks_list[first_projected_support_candlestick_number]
                if first_projected_support_candlestick.close * 1.007 > self.a1 * first_projected_support_candlestick_number + self.b1 and \
                   first_projected_support_candlestick.close * 0.993 < self.a1 * first_projected_support_candlestick_number + self.b1:
                    second_projected_support_candlestick_number = self.get_next_support_candlestick_number(first_projected_support_candlestick)
                    second_projected_support_candlestick = self.candlesticks_list[second_projected_support_candlestick_number]
                    if second_projected_support_candlestick.close * 1.007 > self.a1 * second_projected_support_candlestick_number + self.b1 and \
                       second_projected_support_candlestick.close * 0.993 < self.a1 * second_projected_support_candlestick_number + self.b1: 
                        # Changed way of implementation xD
                        self.line3_a =  self.get_a(self.starting_resistance_candlestick.number,
                                                   first_projected_support_candlestick_number + 1,
                                                   self.starting_resistance_candlestick.close,
                                                   self.candlesticks_list[first_projected_support_candlestick_number + 1].close)
                        self.line3_b = self.get_b(self.starting_resistance_candlestick.close, self.starting_resistance_candlestick.close, self.line3_a)
                        self.fan_break_point = self.get_fan_break_point(second_projected_support_candlestick)
                        if self.fan_break_point:
                            self.fans_list.append([self.starting_resistance_candlestick, (first_projected_support_candlestick_number,
                                                                                          first_projected_support_candlestick.close)])
                            self.fans_list.append([self.starting_resistance_candlestick, (second_projected_support_candlestick_number,
                                                                                          second_projected_support_candlestick.close)])
                            self.fans_list.append([self.starting_resistance_candlestick, (self.fan_break_point[0], self.fan_break_point[1])])
            except Exception as e:
                print(e)

