import gate_api
import ta
from gate_api.exceptions import ApiException, GateApiException
import pandas as pd
import time
import datetime as dt
import ccxt
import calendar
import math
from ta.momentum import RSIIndicator, WilliamsRIndicator, ROCIndicator, StochasticOscillator, StochRSIIndicator
from ta.trend import MACD,EMAIndicator, SMAIndicator
from ta.volatility import BollingerBands

import csv
from ccxt import NetworkError
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from ta import add_all_ta_features
from ta.utils import dropna
import plotly.express as px
import threading
import multiprocessing



# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(host="https://api.gateio.ws/api/v4",
                                       key = "e9734c9d33c0cfc33aa3cb2ffdcc5532",
                                       secret = "bf9660ff2d4bc08442266074ad59e4cc5a3e644d4f932c50032df66729424727"
                                       )
api_client = gate_api.ApiClient(configuration)

# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)
Wallet  = 1500
cryptowallet = 0
def add_crypto(amount):
    crypto_wallet += AfterFee(amount)
def subtract_wallet(amount, currentprice):
    Wallet-=AfterFee(amount)*currentprice
def add_wallet(amount, currentprice):
    Wallet += AfterFee(amount) * currentprice
def subtract_crypto(amount):
    crypto_wallet -= AfterFee(amount)


def Test(ticker, timeframe, status):
    data = ConstructDF(ticker, timeframe)
    if(status == "BUY"):
        subtract_wallet(1,15)
        add_crypto(15)
        print(Wallet)
    if(status == "SELL"):
        subtract_wallet(AfterFee(3))
    








gateio = ccxt.gateio()
holdings = []
def ConstructDF(ticker, timeframe):
    ohlcv = gateio.fetch_ohlcv(symbol= ticker, timeframe=timeframe, limit = 200)
    df = pd.DataFrame(ohlcv, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Time'] = [dt.datetime.fromtimestamp(float(time) / 1000) for time in df['Time']]
    # df.set_index('Time', inplace=True)
    RSIDF = RSIIndicator(df["Close"], fillna= False).rsi()
    MACDF = MACD(df["Close"], fillna= False)
    WRIDF = WilliamsRIndicator(df["High"], df['Low'], df["Close"],fillna=False)
    EMADF = EMAIndicator(df["Close"],200, fillna=False)
    STOCHDF = StochasticOscillator(df["High"], df['Low'], df["Close"],fillna=False)
    STOCHRSIDF = StochRSIIndicator(df["Close"],fillna=False)
    ROCDF = ROCIndicator(df["Close"],fillna=False)
    SMADF50= SMAIndicator(df["Close"],50,fillna = False)
    SMADF100 = SMAIndicator(df["Close"], 100, fillna=False)
    SMADF150 = SMAIndicator(df["Close"], 150, fillna=False)
    SMADF200 = SMAIndicator(df["Close"], 200, fillna=False)
    BB = BollingerBands(df["Close"], fillna=False)
    df.insert(6, "RSI", RSIDF, True)
    df.insert(7, "MACD", MACDF.macd(), True)
    df.insert(8, "MACD Signal", MACDF.macd_signal(), True)
    df.insert(9, "MACD Histo", MACDF.macd_diff(), True)
    df.insert(10, "EMA", EMADF.ema_indicator(), True)
    df.insert(11, "WRI", WRIDF.williams_r(), True)
    df.insert(12, "STOCH", STOCHDF.stoch(), True)
    df.insert(13, "STOCH Signal", STOCHDF.stoch_signal(), True)
    df.insert(14, "STOCHRSI", STOCHRSIDF.stochrsi(), True)
    df.insert(15, "ROC", ROCDF.roc(), True)
    df.insert(16, "SMA 50", SMADF50.sma_indicator(), True)
    df.insert(17, "SMA 100", SMADF100.sma_indicator(), True)
    df.insert(18, "SMA 150", SMADF150.sma_indicator(), True)
    df.insert(19, "SMA 200", SMADF200.sma_indicator(), True)
    df.insert(20, "BB UP", BB.bollinger_hband(), True)
    df.insert(21, "BB UP", BB.bollinger_lband(), True)




    return df

def GetUnits(wallet, ticker, timeframe):
    Price = float(ConstructDF(ticker,timeframe).iloc[-1,4])
    amount = 0.25*wallet
    units = amount/Price
    return units
def SellUnits(cryptowallet):
    units = holdings.pop(0)
    if(units>cryptowallet):
       units = cryptowallet
    return units




def AfterFee(amountBought):
    amountOwned = 0.0002*amountBought
    return amountBought-amountOwned

def TestStrats(ticker, timeframe, Strategy):
    Wallet = 1500
    cryptowallet = 0
    prevRSI  = 0.0000000
    prevStoch = 0.0000000
    prevStochRSI = 0.0000000
    prevROC = 0.0000000
    prevWRI = 0.0000000
    Bought = False
    Status = ""
    LeftOver = 100
    amountBought = 0
    filepath = "D:\Code\Python Projects\Cryptobot/" + ticker +"_" + Strategy + "_" + timeframe +".csv"
    outputLine = ""
    BuyPrice = 0
    ExitPoint = False
    if(timeframe == '10s'):
        timeoff=10
    elif(timeframe == '1m'):
        timeoff = 60
    elif(timeframe == '5m'):
        timeoff = 60*5
    elif(timeframe == '15m'):
        timeoff = 60*15
    elif(timeframe == '30m'):
        timeoff = 60*30
    elif(timeframe == '1h'):
        timeoff = 60*60
    with open(filepath, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Wallet Value","Wallet","Crypto Wallet","Buy Condition", "Sell Condition", "Break Even", "Exit Point","Status","Holdings"])



    while(1):
        try:
            data = ConstructDF(ticker, timeframe)
            currentprice = data.iloc[-1, 4]
            currentRSI = float(data.iloc[-1, 6])
            currentMACD = float(data.iloc[-1,7])
            currentMACDSig = float(data.iloc[-1,8])
            currentMACDHisto = float(data.iloc[-1,9])
            currentEMA = float(data.iloc[-1,10])
            currentWRI = float(data.iloc[-1,11])
            currentStoch = float(data.iloc[-1,12])
            currentStochSignal = float(data.iloc[-1,13])
            currentStochRSI = float(data.iloc[-1,14])
            currentROC = float(data.iloc[-1,15])
            ma50 = float(data.iloc[-1,16])
            ma100 = float(data.iloc[-1, 17])
            ma150 = float(data.iloc[-1, 18])
            ma200 = float(data.iloc[-1, 19])
            WalletEmpty = (Wallet<5)
            CryptoWalletEmpty = not (cryptowallet>0)
            currentBBUP = float(data.iloc[-1, 20])
            currentBBLO = float(data.iloc[-1, 21])
            ExitPoint = ((currentprice >= 1.3 * BuyPrice) or (currentprice <= 0.9 * BuyPrice)) and Bought
            BreakEven = (AfterFee(amountBought)*BuyPrice <= (AfterFee(AfterFee(amountBought))*currentprice)) and Bought
            RSIBuyCondition = (currentRSI>prevRSI and currentRSI<30) and not Bought
            RSISellCondition = ((currentRSI<prevRSI and currentRSI>70) or ExitPoint) and Bought
            StochBuyCondition = (currentStoch<20) and (currentStoch>currentStochSignal) and (currentStoch>prevStoch) and not Bought
            StochSellCondition = (((currentStoch>80) and (currentStoch<currentStochSignal) and (currentStoch<prevStoch)) or ExitPoint) and Bought
            MACDBuyCondition = (currentMACD>currentMACDSig) and (currentMACDHisto<0) and not Bought
            MACDSellCondition= (((currentMACD<currentMACDSig) and (currentMACDHisto>0))  or ExitPoint) and Bought
            StochRSIBuyCondition = (currentStochRSI>50) and (currentStochRSI<prevStochRSI) and not Bought
            StochRSISellCondition = (((currentStochRSI<50) and (currentStochRSI>prevStochRSI)) or ExitPoint ) and Bought
            ROCBuyCondition = (currentROC<0) and (currentROC>prevROC) and not Bought
            ROCSellCondition = (((currentROC>0 and currentROC<prevROC) or ExitPoint) and Bought)
            WRIBuyContition = abs(currentWRI)>80 and abs(currentWRI)<abs(prevWRI) and not Bought
            WRISellCondition = (((abs(currentWRI)<20 and abs(currentWRI)>abs(prevWRI)) or ExitPoint)  ) and Bought
            BBBuyCondition = (currentprice<currentBBLO and currentRSI<50) and not WalletEmpty
            BBSellCondition = (currentprice>currentBBUP and currentRSI>50) and not CryptoWalletEmpty and (len(holdings)>0)

            # // long
            # signal
            # if (close < lower and strength < 50 and strategy.position_size < units * 5)
            #     strategy.order("Long", strategy.long, units)
            #
            # // close
            # long
            # signal
            # if (close > upper and strength > 50 and strategy.position_size > 0)
            #     strategy.order("Close Long", strategy.short, units)
            if(Strategy == 'RSI'):
                if(RSIBuyCondition):
                    Bought = True
                    BuyPrice = float(data.iloc[-1, 4])
                    Status = "BUY at " + str(BuyPrice) + " USD"
                    amountBought = GetUnits(Wallet, ticker, timeframe)
                    Wallet =(AfterFee(amountBought)*BuyPrice)
                elif(RSISellCondition):
                    Bought = False
                    SellPrice = float(data.iloc[-1,4])
                    Status = "SELL at " + str(SellPrice) + " USD"
                    Wallet = (AfterFee(AfterFee(amountBought))*SellPrice)
                elif(not Bought):
                    Status = "Do Nothing"
                else:
                    Status = "HOLD"
                    Wallet = (AfterFee(amountBought)*currentprice)
                outputLine = [str(data.iloc[-1, 0]), str(round(Wallet, 2)), str(RSIBuyCondition), str(RSISellCondition), str(BreakEven), str(ExitPoint), str(Status), '\n']
            elif(Strategy == 'MACD'):
                if (MACDBuyCondition):
                    Bought = True
                    BuyPrice = float(data.iloc[-1, 4])
                    Status = "BUY at " + str(BuyPrice) + " USD"
                    amountBought = GetUnits(Wallet, ticker, timeframe)
                    Wallet = (AfterFee(amountBought) * BuyPrice)
                elif (MACDSellCondition):
                    Bought = False
                    SellPrice = float(data.iloc[-1, 4])
                    Status = "SELL at " + str(SellPrice) + " USD"
                    Wallet = (AfterFee(AfterFee(amountBought)) * SellPrice)
                elif (not Bought):
                    Status = "Do Nothing"
                else:
                    Status = "HOLD"
                    Wallet = (AfterFee(amountBought) * currentprice)
                outputLine = [str(data.iloc[-1, 0]), str(round(Wallet, 2)), str(MACDBuyCondition),str(MACDSellCondition), str(BreakEven), str(ExitPoint), str(Status), '\n']
            elif(Strategy == 'STOCH'):
                if (StochBuyCondition):
                    Bought = True
                    BuyPrice = float(data.iloc[-1, 4])
                    Status = "BUY at " + str(BuyPrice) + " USD"
                    amountBought = GetUnits(Wallet, ticker, timeframe)
                    Wallet = (AfterFee(amountBought) * BuyPrice)
                elif (StochSellCondition):
                    Bought = False
                    SellPrice = float(data.iloc[-1, 4])
                    Status = "SELL at " + str(SellPrice) + " USD"
                    Wallet = (AfterFee(AfterFee(amountBought)) * SellPrice)
                elif (not Bought):
                    Status = "Do Nothing"
                else:
                    Status = "HOLD"
                    Wallet = (AfterFee(amountBought) * currentprice)
                prevStoch = currentStoch
                outputLine = [str(data.iloc[-1, 0]), str(round(Wallet, 2)), str(StochBuyCondition), str(StochSellCondition),str(BreakEven), str(ExitPoint), str(Status), '\n']
            elif(Strategy == 'STOCH RSI'):
                if (StochRSIBuyCondition):
                    Bought = True
                    BuyPrice = float(data.iloc[-1, 4])
                    Status = "BUY at " + str(BuyPrice) + " USD"
                    amountBought = GetUnits(Wallet, ticker, timeframe)
                    Wallet = (AfterFee(amountBought) * BuyPrice)
                elif (StochRSISellCondition):
                    Bought = False
                    SellPrice = float(data.iloc[-1, 4])
                    Status = "SELL at " + str(SellPrice) + " USD"
                    Wallet = (AfterFee(AfterFee(amountBought)) * SellPrice)
                elif (not Bought):
                    Status = "Do Nothing"
                else:
                    Status = "HOLD"
                    Wallet = (AfterFee(amountBought) * currentprice)
                prevStochRSI = currentStochRSI
                outputLine = [str(data.iloc[-1, 0]), str(round(Wallet, 2)), str(StochRSIBuyCondition),
                              str(StochRSISellCondition), str(BreakEven), str(ExitPoint), str(Status), '\n']
            if (Strategy == 'BB'):
                if (BBBuyCondition):
                    BuyPrice = float(data.iloc[-1, 4])
                    Status = "BUY at " + str(BuyPrice) + " USD"
                    units = GetUnits(Wallet, ticker, timeframe)
                    holdings.append(AfterFee(units))
                    Wallet -= units * BuyPrice
                    cryptowallet += AfterFee(units)
                elif (BBSellCondition):
                    sellunits = SellUnits(cryptowallet)
                    SellPrice = float(data.iloc[-1, 4])
                    cryptowallet -= sellunits
                    Wallet += AfterFee(sellunits) * SellPrice
                    Status = "SELL at " + str(SellPrice) + " USD"
                else:
                    Status = "Do Nothing"
                totalValue = Wallet + (cryptowallet * currentprice)
                outputLine = [str(data.iloc[-1, 0]), str(round(totalValue, 2)), str(round(Wallet,2)),str(round(cryptowallet,2)), str(BBBuyCondition), str(BBSellCondition),
                              str(BreakEven), str(ExitPoint), str(Status),str(holdings), '\n']
                print(len(holdings))
                print("Time: : " + str(data.iloc[-1, 0]) + "     Wallet Value: $" + str(
                    round(Wallet, 2)) + "     Crypto Wallet: " + str(round(cryptowallet, 2)) + " " +str(ticker)+ "     Total Value: " + str(round(totalValue, 2))+"     Status: " + str(Status)+"     TimeFrame: " + str(timeframe)+"     Holdings: " + str(holdings))
            elif(Strategy == 'ROC'):
                if (ROCBuyCondition):
                    Bought = True
                    BuyPrice = float(data.iloc[-1, 4])
                    amountBought = GetUnits(Wallet, ticker, timeframe)
                    Status = "BUY  " + str(amountBought) + " at "  + str(BuyPrice) + " USD"
                    Wallet = (AfterFee(amountBought) * BuyPrice)
                elif (ROCSellCondition):
                    Bought = False
                    SellPrice = float(data.iloc[-1, 4])
                    Status = "SELL " + str(amountBought) + " at " + str(SellPrice) + " USD"
                    Wallet = (AfterFee(AfterFee(amountBought)) * SellPrice)
                else:
                    Status = "Do Nothing"
                    Wallet = (AfterFee(amountBought) * currentprice)
                outputLine = [str(data.iloc[-1, 0]), str(round(Wallet, 2)), str(ROCBuyCondition), str(ROCSellCondition), str(BreakEven), str(ExitPoint), str(Status), '\n']
                prevROC = currentROC
            elif(Strategy == 'WRI'):
                if (WRIBuyContition):
                    Bought = True
                    BuyPrice = float(data.iloc[-1, 4])
                    Status = "BUY at " + str(BuyPrice) + " USD"
                    amountBought = GetUnits(Wallet, ticker, timeframe)
                    Wallet = (AfterFee(amountBought) * BuyPrice)
                elif (WRISellCondition):
                    Bought = False
                    SellPrice = float(data.iloc[-1, 4])
                    Status = "SELL at " + str(SellPrice) + " USD"
                    Wallet = (AfterFee(AfterFee(amountBought)) * SellPrice)
                elif (not Bought):
                    Status = "Do Nothing"
                else:
                    Status = "HOLD"
                    Wallet = (AfterFee(amountBought) * currentprice)
                prevWRI = currentWRI
                outputLine = [str(data.iloc[-1, 0]), str(round(Wallet, 2)), str(WRIBuyContition),
                              str(WRISellCondition), str(BreakEven), str(ExitPoint), str(Status), '\n']
            with open(filepath, "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(outputLine)
            time.sleep(timeoff)
        except ConnectionError:
            print("Reconnecting...")
            time.sleep(1)
        except ApiException:
            print("Reconnecting...")
            time.sleep(1)
        except GateApiException:
            print("Reconnecting...")
            time.sleep(1)
        except NetworkError:
            print("Reconnecting...")
            time.sleep(1)



portfolio = [["AVAX_USDT","10s","BB"],["AVAX_USDT","1m","BB"],["AVAX_USDT","5m","BB"],["AVAX_USDT","15m","BB"],["AVAX_USDT","30m","BB"],["AVAX_USDT","1h","BB"]]



if __name__ == '__main__':
    # pool = multiprocessing.Pool(processes= 6)
    # P1 = pool.starmap(TestStrats, portfolio)
    TestStrats("AVAX_USDT","5m","BB")
    # detMaxBuy(1500,"BTC_USDT","10s")












