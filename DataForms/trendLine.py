class TrendLine():
    
    def get_direction(self, direction):
        return direction

    def get_trends_list(self, candlesticks_list):
        
        current_candlestick_index = 0
        trends_list = []

        # ToDo: Damn, do it better -_-
        try:
            if self.direction == "up":
                for _ in range(len(candlesticks_list)):
                    current_trend_list = [candlesticks_list[current_candlestick_index]]
                    while candlesticks_list[current_candlestick_index + 1].close > candlesticks_list[current_candlestick_index].close:
                        current_trend_list.append(candlesticks_list[current_candlestick_index + 1])
                        current_candlestick_index += 1
                    if len(current_trend_list) > 1:
                        trends_list.append(current_trend_list)
                    current_candlestick_index += 1

            if self.direction == "down":
                for _ in range(len(candlesticks_list)):
                    current_trend_list = [candlesticks_list[current_candlestick_index]]
                    while candlesticks_list[current_candlestick_index + 1].close < candlesticks_list[current_candlestick_index].close:
                        current_trend_list.append(candlesticks_list[current_candlestick_index + 1])
                        current_candlestick_index += 1
                    if len(current_trend_list) > 1:
                        trends_list.append(current_trend_list)
                    current_candlestick_index += 1
        except:
            pass

        return trends_list

    def __init__(self, direction, candlesticks_list):
        self.direction = self.get_direction(direction)
        self.trends_list = self.get_trends_list(candlesticks_list)
