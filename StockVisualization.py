# note this is a modifed version of the jupyter notebook version to be able to use the functions with a gui
# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as style
import matplotlib.dates as mdates
import plotly.graph_objs as go
import seaborn as sns
sns.set_style("darkgrid")
from ta.momentum import RSIIndicator
from ta.trend import MACD
from datetime import datetime, timedelta

def stockSetup(df, ticker):
    '''the stock setup function cleans the dataframe and filters it according to a specific ticker you input'''
    tickers = list(df["Ticker"].unique())
    if ticker in tickers:
        stockData = df[df["Ticker"]==ticker]
    else:
        raise Exception("Ticker is not valid")
  
    stockData = stockData.drop('Ticker', axis=1)
    stockData = stockData.drop("File", axis=1)
    stockData = stockData.round(2)
    stockData['Date'] = pd.to_datetime(stockData['Date'])
    stockData.dropna(axis=0, inplace=True)
    stockData = stockData.set_index('Date')
    return stockData


# these functions below convert the object oriented version of the TA library into functions that are easy to call
def generateRSI(df, period=14):
  return RSIIndicator(df["Adj Close"], period).rsi()

def generateMACD(df, periodShort=12, periodLong=26):
  return MACD(df["Adj Close"], n_slow=periodShort, n_fast=periodLong).macd()

def generateMACDSignal(df, period=9):
  return MACD(df["Adj Close"], n_sign=period).macd_signal()

def generateMACDDiff(df, periodShort=12, periodLong=26, periodSign=9):
  return MACD(df["Adj Close"], n_slow=periodShort, n_fast=periodLong, n_sign=periodSign).macd_diff()

def generatePercentageChange(df):
  return df["Adj Close"].pct_change()*100

figures = []
def plotAdjClose(df, size=(15,6)):
  figures.append(plt.figure(figsize=size))
  sns.lineplot(x = df.index, y=df['Adj Close'])
  plt.show()

def plotRSI(df, overBought=70, overSold=30, period=14):
  df["RSI"] = generateRSI(df, period)
  figures.append(plt.figure(figsize=(15,3)))
  sns.lineplot(x = df.index, y=df['RSI'])
  plt.plot([df.index.min(),df.index.max()],[overBought, overBought])
  plt.plot([df.index.min(),df.index.max()],[overSold, overSold])
  plt.show()

def plotMACD(df, periodShort=12, periodLong=26, periodSignal=9):
  df['MACD'] = generateMACD(df, periodShort, periodLong)
  df["MACD Signal"] = generateMACDSignal(df, periodSignal)
  df['MACD Difference'] = generateMACDDiff(df, periodShort, periodLong, periodSignal)
  figures.append(plt.figure(figsize=(15,3)))
  sns.lineplot(x = df.index, y=df['MACD'])
  sns.lineplot(x = df.index, y=df['MACD Signal'])
  plt.show()

def plotPercentageChange(df):
  df['Percentage Change'] = generatePercentageChange(df)
  figures.append(plt.figure(figsize=(15,3)))
  sns.lineplot(x = df.index, y=df['Percentage Change'])
  plt.show()

def plotVolume(df):
  figures.append(plt.figure(figsize=(15,3)))
  sns.lineplot(x=df.index, y=df['Volume'])
  
# plotting the difference graphs above
'''
plotAdjClose(filteredDf)
plotVolume(filteredDf)
#plotPercentageChange(filteredDf)
plotRSI(filteredDf, overBought=70, overSold=30)
plotMACD(filteredDf)
'''

# to filter

'''
#years = generatedData.index.year.unique() # Change this to be specific years you want to filter out
years = [2019]
filteredDf = generatedData[generatedData.index.year.isin(years)]

months = filteredDf.index.month.unique() # Change this to be specific months you want to filter out
#months = [#put your months here]
filteredDf = filteredDf[filteredDf.index.month.isin(months)]

days = filteredDf.index.day.unique() # Change this to be specific days you want to filter out
#days = [#put your days here]
filteredDf = filteredDf[filteredDf.index.day.isin(days)]
'''

# candlestick chart using plotly
def createCandlestck(df): 
    data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])]
    return go.Figure(data=data)

#createCandlestck(df).show()

def findFallingKnives(df, ticker):
  # allows you to find fallingKnives based on a stock ticker and a condition of RSI, MACD and a SMA
  # you have to change the conditions within this function
  SmaWindow=7
  newDf = stockSetup(df, ticker)
  newDf["RSI"] = generateRSI(newDf)
  newDf["MACD"] = generateMACD(newDf)
  newDf["SMA"] = newDf['Adj Close'].rolling(window=SmaWindow).mean()

  #plt.figure(figsize=(15,8))
  #sns.lineplot(x = df.index, y=df['Adj Close'])
  #sns.lineplot(x = df.index, y=df["SMA"])
  # plt.show()

  # these are the condition statements below: I couldnt figure out how to keep them in one line so..
  fallingKniveDf = newDf[newDf["MACD"] <= -.5]
  fallingKniveDf = newDf[newDf['Adj Close'] < newDf['SMA']]
  fallingKniveDf = newDf[newDf['RSI'] <40]


  # takes the filtered df from above and graphs a specific interval around that date
  aroundIndex = []
  for date in fallingKniveDf.index:
      aroundIndex.append(pd.date_range(start=date - timedelta(weeks=2), end=date+ timedelta(weeks=2)))

  FallingKnifeSubset = []
  for dates in aroundIndex:
      FallingKnifeSubset.append(newDf[newDf.index.isin(dates)])

  return FallingKnifeSubset

def main():
  df = pd.read_csv("Official_Dataset.csv")
  AAPLFallingKnives = findFallingKnives(df, "AAPL")
  plotAdjClose(AAPLFallingKnives[0])
    
  
if __name__ == "__main__":
  main()
