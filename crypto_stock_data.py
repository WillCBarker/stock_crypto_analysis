#from coinbase.wallet.client import Client
#from Historic_Crypto import Cryptocurrencies
import cbpro

import matplotlib as mp
import matplotlib.pyplot as plt

import datetime

currency_code = "ETH-USD"

import yfinance as yf

import pandas as pd

from pandas.tseries.holiday import USFederalHolidayCalendar
UScal = USFederalHolidayCalendar()
'''
Comparing stock and crypto data
    1. Plot stock/crypto historical data of past 30 days (matplotlib)
    2. Compare key differences (volume, price fluctuation, relationships)

To do:
    1. If entire plot is < 24 hours, have each interval only print hours
    2. figure out how to resize graph to acomodate more info 
        OR auto adjust spacing to ask for hours/days depending on size of request
    3. have start and end date be variables, potentially inputs?
    4. change [5:13] slice and just figure out how to get dates, its ugly
'''
public_client = cbpro.PublicClient()


class stockAnalysis():
    def __init__ (self):
        self.s_priceList = []
        self.s_dateList = []
        self.spy = yf.Ticker("SPY")
        self.__stock_data() 

    def __stock_data(self):
        hist = self.spy.history(start="2022-06-01", end="2022-07-01", interval="1d")
        self.s_priceList = list(round((((hist["High"]) + (hist["Low"]))/2),2))
        self.__missing_day_handler(hist)
        #self.__holiday_check()
    
    def __holiday_check(self, date):
        #Takes date object as paremeter, converting it into a datetime object to check if it's present in the list of holidays for the given time period
        converted_date = datetime.datetime.combine(date, datetime.time(0,0))
        holidays = UScal.holidays(start="2022-06-01", end="2022-07-01").to_pydatetime()
        if converted_date in holidays:
            print("PRESENT IN HOLIDAYS: ", date)
            return True

    def __missing_day_handler(self, hist):
        #Fills in days missing from s_priceList due to markets being closed, catches weekdays and holidays
        x = 0
        for i in range(1,31): #days in month, should be dynamic
            #if saturday/sunday: insert 2 elements, both being the close price from the previous friday at index i and i+1 respectively
            #iterating through a list only consisting of weekdays
            '''
            Goal: For every day the markets closed, insert the closing price of the last time the market was open into the correct position
            Problem: hist["Close"] (the dataframe I'm pulling data from) only has weekdays information, so counting up by i (the amount of days in the month)
                     eventually goes out of bounds, we need a serparate counter to access the correct elements in hist
            '''
            date = datetime.date(2022, 6, i)
            dayNum = date.weekday()

            if (self.__holiday_check(date)) == True or dayNum == 5 or dayNum == 6:
                self.s_priceList.insert(i, hist["Close"][i-x])
                i += 1
                x += 1

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
        data = self.pc.get_product_historic_rates("ETH-USD", "2022-06-01", "2022-06-30",86400)
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
d1 = driver()
