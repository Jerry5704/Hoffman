class Candlestick():

    def get_color(self):
        if self.close > self.open:
            return "green"
        return "red" 

    def get_has_upper_wick(self):
        if self.color == "green":
            if self.high / self.close < 1.002:
                return False
        else:
            if self.high / self.open < 1.002:
                return False
        return True
            

    def get_has_lower_wick(self):
        if self.color == "green":
            if self.open / self.low < 1.002:
                return False
        else:
            if self.close / self.low < 1.002:
                return False
        return True
    
    def get_wicks(self):
        self.has_upper_wick = self.get_has_upper_wick()
        self.has_lower_wick = self.get_has_lower_wick()

    def __init__(self, date, open, high, low, close, volume):
        
        # Gathered data
        self.date = date
        self.open = float(open.replace(',',''))
        self.high = float(high.replace(',',''))
        self.low = float(low.replace(',',''))
        self.close = float(close.replace(',',''))
        self.volume = float(volume.replace(',',''))

        # Known additional data
        self.color = self.get_color()
        self.get_wicks()
        self.body = abs(self.open - self.close)

        if self.color == "green":
            self.upper_shadow = self.high - self.close
            self.lower_shadow = self.open - self.low
        else:
            self.upper_shadow = self.high - self.open
            self.lower_shadow = self.close - self.low

        # Candlestick types filled only when in collection
        self.number = ""
        self.lenght_type = ""
        self.pattern = ""
        self.trend_direction = ""
        self.is_support = False
        self.is_resistance = False
        self.next_resistance_candlestick_number = "" 
        self.previous_resistance_candlestick_number = "" 
        self.next_support_candlestick_number = "" 
        self.previous_support_candlestick_number = "" 
