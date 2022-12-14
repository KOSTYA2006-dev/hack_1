import csv
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, file, period):
        self.file = file
        self.data = None
        self.period = period
        with open(self.file, encoding="utf-8") as csv_file:
            self.r = {i['tickers']: int(i['count']) for i in csv.DictReader(csv_file, delimiter=',')}

        self.data = yf.download(list(self.r.keys()), period=f'{self.period}mo')
        self.close_data = self.data.Close
        self.cost = self.close_data.tail(1).squeeze(axis=0)
        self.dCloseData = self.close_data.pct_change()
        self.dohMean = self.dCloseData.mean()
        self.year_yield = self.dohMean * 365
        self.share_price = self.cost * list(self.r.values())
        print(self.data, '------------')

    # цена акции
    def prise_stock(self):
        self.cost.name = 'cost'
        return dict(self.cost)

    # средняя годовая доходность
    def average_annual_profit(self):
        self.year_yield = self.dohMean * 365
        self.year_yield.name = 'year_yield'
        return dict(self.year_yield)

    # дивидентный доход
    def dividend_profit(self):
        self.dividend_yield = self.year_yield / self.cost * 100
        self.dividend_yield.name = 'dividend_yield'
        return dict(self.dividend_yield)

    # цена акций(цена * кол-во)
    def price_all_shares(self):
        self.share_price.name = 'share_price'
        return dict(self.share_price)

    def price_briefcase(self):
        return round(sum(self.share_price), 3)

    def grafik(self):
        self.d = '1'
        self.a = []
        for name in self.close_data:
            self.close_data[name].plot()
            plt.grid()
            plt.title(name)
            s = plt.savefig(str(self.d) + 'png')
            self.a.append(s)

            plt.show()
            self.d = int(self.d)
            self.d += 1
            print(self.a)
            

        
        self.dCloseData['F'].plot()
        plt.grid()
        plt.title('F')
        plt.savefig('Analitik001.jpg')
        plt.show()
           

    



a = Analysis('shares.csv', 12)
print(a.prise_stock())
print(a.average_annual_profit())
print(a.dividend_profit())
print(a.price_all_shares())
print(a.price_briefcase())

a.grafik()






