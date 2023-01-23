class Candlestick():

    def __init__(self, date, open, high, low, close, volume):
        self.date = date
        self.open = float(open.replace(',',''))
        self.high = float(high.replace(',',''))
        self.low = float(low.replace(',',''))
        self.close = float(close.replace(',',''))
        self.volume = float(volume.replace(',',''))

        # Calculations
        self.upper_shadow = self.high - self.close
        self.body = abs(self.open - self.close)
        self.type = ""
        print(f"body lenght = {self.body}")