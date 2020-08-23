# imports
import StockVisualization
import pandas as pd
import seaborn as sns

def getTickerList(df):
    return list(df["Ticker"].unique())   

def stockSetup(df, ticker):
    '''the stock setup function cleans the dataframe and filters it according to a specific ticker you input'''
    
    df = df.round(2)
    
    df.drop("Return", axis=1)
    
    sector = df['GICS Sector'][0]
    df = df.drop("GICS Sector", axis=1)
    
    industry = df['GICS Sub Industry'][0]
    df = df.drop("GICS Sub Industry", axis=1)
    
    cik = df['CIK'][0]
    df = df.drop("CIK", axis=1)
    
    headLoc = df['Headquarters Location'][0]
    df = df.drop("Headquarters Location", axis=1)
    
    DateFirstAdded = df['Date first added'][0]
    df = df.drop("Date first added", axis=1)
    
    founded = df['Founded'][0]
    df = df.drop("Founded", axis=1)
    
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    
    return (df, sector, industry, cik, headLoc, DateFirstAdded, founded)

def main():
    # load in dataset
    SAndPData = pd.read_csv("database2.csv")
    
    ticker = input("Please enter a ticker: ")
    while not(ticker in getTickerList(SAndPData)):
        print("Ticker is not valid. Please try again. ")
        ticker = input("Please enter a ticker: ")

    stockData = stockSetup(SAndPData, ticker)[0]
    stockData.head(-5)
    print(stockData.dtypes)

    

    
    
if __name__ == "__main__":
    main()