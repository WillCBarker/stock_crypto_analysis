from coinbase.wallet.client import Client
from Historic_Crypto import Cryptocurrencies
import cbpro

import matplotlib as mp
import matplotlib.pyplot as plt

import datetime

currency_code = "ETH-USD"

import yfinance as yf

import pandas as pd
'''
Comparing stock and crypto data
    1. Plot stock/crypto historical data of past 30 days (matplotlib)
    2. Compare key differences (volume, price fluctuation, relationships)

To do:
    1. If entire plot is < 24 hours, have each interval only print hours
    2. figure out how to resize graph to acomodate more info 
        OR auto adjust spacing to ask for hours/days depending on size of request
'''
public_client = cbpro.PublicClient()


class stockAnalysis():
    def __init__ (self):
        self.s_priceList = []
        self.s_dateList = []
        self.spy = yf.Ticker("SPY")
        self.__stock_data() 

    def __stock_data(self):
        #data = yf.download("SPY", start="2022-07-01", end="2022-07-31", interval="60m")
        hist = self.spy.history(start="2022-07-01", end="2022-07-31", interval="1d")
        self.s_priceList = list(round((((hist["High"]) + (hist["Low"]))/2),2))
        print("HEY:", len(hist["Close"]))
        for i in range(1,31):
            #if saturday/sunday: insert 2 elements, both being the close price from the previous friday at index i and i+1 respectively

            #index 22 is out of bounds for axis 0 with size 20
            #iterating through a list only consisting of weekdays
            dayNum = datetime.date(2022, 7, i).weekday()
            if dayNum == 5:
                self.s_priceList.insert(i, hist["Close"][i-1])
                i += 1
            elif dayNum == 6:
                self.s_priceList.insert(i, hist["Close"][i-1])
                i += 1
    def get_Stock_Data(self):
        return (self.s_priceList)   
    
class cryptoAnalysis():
    def __init__(self):
        self.pc = cbpro.PublicClient()
        self.c_priceList = []
        self.c_dateList = []
        self.__crypto_data()
        self.__time_conversion() 
    
    def __crypto_data(self):
        data = self.pc.get_product_historic_rates("ETH-USD", "2022-07-01", "2022-07-31",86400)
        for i in data:
            self.c_dateList.append(i[0])
            self.c_priceList.append(round(((i[1] + i[2])/2), 2)) #low & high avg
        self.c_priceList = self.c_priceList[::-1]

    def __time_conversion(self):
        #converts unix time to normal
        for i in range(len(self.c_dateList)):
            date = datetime.datetime.fromtimestamp(self.c_dateList[i])
            self.c_dateList[i] = date.isoformat()
            self.c_dateList[i] = self.c_dateList[i][5:13]
        self.c_dateList = self.c_dateList[::-1]

    def get_Crypto_data(self):
        return (self.c_priceList, self.c_dateList)

'''
        graph = plot(self.c_dateList, self.c_priceList)
        ^This to go in its own class
'''
class plot():
    def __init__(self, x, y, y1):
        plt.plot(x,y)
        plt.plot(x,y1)
        plt.title('Stock & Crypto Analysis')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.xticks(rotation = 45)
        plt.show()

class driver():
    def __init__(self):                
        stock1 = stockAnalysis()
        self.s_priceList = stock1.get_Stock_Data()
        print(self.s_priceList)
        coin1 = cryptoAnalysis()
        self.c_priceList, self.c_dateList = coin1.get_Crypto_data()
        self.__call_plot()

    def __call_plot(self):
        print(len(self.s_priceList))
        pl = plot(self.c_dateList, self.c_priceList, self.s_priceList)
        '''
        NOT READY TO BE PLOTTED YET - make function to account for weekends, change [5:13] slice and just figure out how to get dates, its ugly
        '''
d1 = driver()
