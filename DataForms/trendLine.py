class TrendLine():
    
    def get_direction(self, direction):
        return direction

    def get_a(self, x1, y1, x2, y2):
        return (y2 - y1) / (x2 - x1)

    def get_b(self, y1, x1, a):
        return y1 - a * x1

    def check_if_trend(self, current_candlestick_index, candlesticks_list):
        if self.direction == "up":
            if candlesticks_list[current_candlestick_index].close < candlesticks_list[current_candlestick_index + 1].close:
                a = self.get_a(candlesticks_list[current_candlestick_index].number, candlesticks_list[current_candlestick_index].close, candlesticks_list[current_candlestick_index + 1].number, candlesticks_list[current_candlestick_index + 1].close)
                b = self.get_b(candlesticks_list[current_candlestick_index].close, candlesticks_list[current_candlestick_index].number, a)
                return a, b
            return None, None

        if self.direction == "down":
            if candlesticks_list[current_candlestick_index].close > candlesticks_list[current_candlestick_index + 1].close:
                a = self.get_a(candlesticks_list[current_candlestick_index].number, candlesticks_list[current_candlestick_index].close, candlesticks_list[current_candlestick_index + 1].number, candlesticks_list[current_candlestick_index + 1].close)
                b = self.get_b(candlesticks_list[current_candlestick_index].close, candlesticks_list[current_candlestick_index].number, a)
                return a, b
            return None, None

    def get_trends_list(self, candlesticks_list):
        # ToDo: Damn, do it better -_-
        try:
            current_candlestick_index = 0
            trends_list = []
            if self.direction == "up":
                for _ in range(len(candlesticks_list)):
                    current_trend_list = [candlesticks_list[current_candlestick_index]]
                    a, b = self.check_if_trend(current_candlestick_index, candlesticks_list)
                    if a != None and b != None:
                        current_trend_list.append(candlesticks_list[current_candlestick_index + 1])
                        current_candlestick_index += 1
                        while candlesticks_list[current_candlestick_index].close < candlesticks_list[current_candlestick_index + 1].close and candlesticks_list[current_candlestick_index + 1].close * 1.007 > a * candlesticks_list[current_candlestick_index + 1].number + b and candlesticks_list[current_candlestick_index + 1].close * 0.993 < a * candlesticks_list[current_candlestick_index + 1].number + b: 
                            current_trend_list.append(candlesticks_list[current_candlestick_index + 1])
                            current_candlestick_index += 1

                    else:
                        current_candlestick_index += 1
                    current_candlestick_index += 1
                    
                    if len(current_trend_list) > 2:
                        trends_list.append(current_trend_list)
            
            if self.direction == "down":
                for _ in range(len(candlesticks_list)):
                    current_trend_list = [candlesticks_list[current_candlestick_index]]
                    a, b = self.check_if_trend(current_candlestick_index, candlesticks_list)
                    if a != None and b != None:
                        current_trend_list.append(candlesticks_list[current_candlestick_index + 1])
                        current_candlestick_index += 1
                        while candlesticks_list[current_candlestick_index].close > candlesticks_list[current_candlestick_index + 1].close and candlesticks_list[current_candlestick_index + 1].close * 1.007 > a * candlesticks_list[current_candlestick_index + 1].number + b and candlesticks_list[current_candlestick_index + 1].close * 0.993 < a * candlesticks_list[current_candlestick_index + 1].number + b: 
                            current_trend_list.append(candlesticks_list[current_candlestick_index + 1])
                            current_candlestick_index += 1
                    else:
                        current_candlestick_index += 1
                    current_candlestick_index += 1
                    
                    if len(current_trend_list) > 2:
                        trends_list.append(current_trend_list)
        except:
            print("last possible trendline not available!!!!!!")
            pass

        return trends_list

    def __init__(self, direction, candlesticks_list):
        self.direction = self.get_direction(direction)
        self.trends_list = self.get_trends_list(candlesticks_list)