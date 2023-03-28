from NSEDownload import stocks
import pandas as pd
import numpy as np
#import mysql.connector
import os
#from sqlalchemy import create_engine, text
from datetime import date



def main():
    final_verdict=""

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    stock_list = []
    with open(os.path.join(fileDir, 'stocklist.txt')) as f:
        stock_list = f.readlines()
        stock_list = [x.strip() for x in stock_list]
    for _symbol in stock_list:
        
        print("Checking: Stock: "+_symbol)
        
        df=stocks.get_data(symbol=_symbol, start_date='3-3-2023', end_date='27-3-2023')

        df2 = df[["Last Price", "Average Price"]].copy()
        df3=df2.reset_index()

        df3.rename(columns = {'Last Price':'Close_Price', 'Average Price':'VWAP'}, inplace = True)

        df3["Notional_Bprice"]=df3["VWAP"]

           
        li=df3.index.values.tolist()
        
        l1=[x+1 for x in li]
        l2=[x%20 if x>20 else x for x in l1]
        l3=[20 if x%20==0 else x for x in l2]
        
        df3["Total_Notional_Shares"]=l3
        df3["Total_Notional_Invest"]=df3["Notional_Bprice"].cumsum()

        df3["AVG_BPrice"]=df3["Total_Notional_Invest"]/df3["Total_Notional_Shares"]

        df3["Val_at_Close"]=df3["Close_Price"]*df3["Total_Notional_Shares"]

        df3["PnL"]=((df3["Val_at_Close"]-df3["Total_Notional_Invest"])*100)/df3["Total_Notional_Invest"]
        
        #result_df = df3[df3['PnL']<= -3]
        arr=df3["PnL"].to_numpy()
        
        if arr[-1]<=-3:
            price=df3["Close_Price"].to_numpy()[-1]
            PNL=df3["PnL"].to_numpy()[-1].round(2)
            final_verdict+=_symbol+(' ' * (30-len(_symbol)))+"price: "+str(price)+(' ' * (30-len(str(price))))+"pnl: "+str(PNL)+"\n"
    if(final_verdict!=""):
        print("\n")
        print(final_verdict)
    else:
        print("\n")
        print("NO STOCKS TO BUY") 
main()



