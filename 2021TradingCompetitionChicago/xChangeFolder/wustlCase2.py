#!/usr/bin/env python
from dataclasses import astuple
from utc_bot import UTCBot, start_bot
import proto.utc_bot as pb
import betterproto
import numpy as np
import asyncio
import random
import scipy
import py_vollib.black_scholes.greeks.analytical as gk
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.implied_volatility import implied_volatility


#list containing orders that haven't been filled yet
unfilledOrder= {} #contains the limit order values 

option_strikes = [90, 95, 100, 105, 110]
underlyingPosit = {}
for strike in option_strikes:
    for flag in ["C", "P"]:
        underlyingPosit[f"UC{strike}{flag}"] = 0
        unfilledOrder[f"UC{strike}{flag}"]=0

class optionBot(UTCBot):

    async def handle_round_started(self):
        """
        This function is called when the round is started. You should do your setup here, and
        start any tasks that should be running for the rest of the round.
        """
        self.positions = {}
        self.rfr = 0.0172
        #risk management below here->
        self.gamma = 0
        self.theta = 0
        self.vega = 0
        self.delta = 0
        #remember that it's ABS value of the limits we can't hit
        self.deltaLimit = 1850
        self.gammaLimit = 18
        self.vegaLimit = 30
        self.thetaLimit = 25

        self.positions["UC"] = 0
        for strike in option_strikes:
            for flag in ["C", "P"]:
                self.positions[f"UC{strike}{flag}"] = 0
        self.current_day = 0

        # Stores the current value of the underlying asset
        self.underlying_price = 100
        self.defaultSize = 5
        self.baseSize = 5
        self.bigSize = 8

    def compute_vol_estimate(self, price, strike, time, flag) -> float:
        #reverse IV if there isn't enough data, come up with HV 
        flag = flag.lower()
        try:
            iv = implied_volatility(price,self.underlying_price,strike,time,self.rfr,flag)
            return iv
        except:
            return -9
        

    def compute_options_price(
        self,
        flag: str,
        underlying_px: float,
        strike_px: float,
        time_to_expiry: float,
        volatility: float,
    ) -> float:
        
        value = black_scholes(flag, underlying_px, strike_px, time_to_expiry ,self.rfr, volatility)

        return value
    

    async def handle_exchange_update(self, update: pb.FeedMessage):
        kind, _ = betterproto.which_one_of(update, "msg")

        if kind == "pnl_msg":
            # When you hear from the exchange about your PnL, print it out
            print("My PnL:", update.pnl_msg.m2m_pnl)

        elif kind == "fill_msg":
            # When you hear about a fill you had, update your positions
            fill_msg = update.fill_msg
            if (len(fill_msg.asset)==5):
                fillStrike = int(fill_msg.asset[2:4])
                fillFlag = fill_msg.asset[4:].lower()
            else:
                fillStrike = int(fill_msg.asset[2:5])
                fillFlag = fill_msg.asset[5:].lower()
            
            fillQty = fill_msg.filled_qty
            if fill_msg.order_side == pb.FillMessageSide.BUY:
                
                time_to_expiry = (21 +5-self.current_day)/ 252
                vol = self.compute_vol_estimate(self.underlying_price,fillStrike,time_to_expiry,fillFlag)
                if (vol!=-9):
                    
                    self.delta = self.defaultSize*fillQty*gk.delta(fillFlag,fillStrike, self.underlying_price,time_to_expiry, self.rfr,vol)+self.delta
                    
                    self.gamma += fillQty*gk.gamma(fillFlag,fillStrike, self.underlying_price,time_to_expiry, self.rfr,vol)*self.defaultSize
                    self.theta += fillQty*gk.theta(fillFlag,fillStrike, self.underlying_price,time_to_expiry, self.rfr,vol)*self.defaultSize
                    self.vega += fillQty*gk.vega(fillFlag,fillStrike, self.underlying_price,time_to_expiry, self.rfr,vol)*self.defaultSize

                    
                    self.positions[fill_msg.asset] += update.fill_msg.filled_qty
                    ask = await self.place_order(
                        fill_msg.asset,
                        pb.OrderSpecSide.LIMIT,
                        pb.OrderSpecSide.ask,
                        self.defaultSize,
                        unfilledOrder[fill_msg.asset]
                    )
                    assert ask.ok
                    unfilledOrder[fill_msg.asset] = unfilledOrder[fill_msg.asset]-fillQty

            else:
                self.delta = self.delta-self.defaultSize*fillQty*gk.delta(fillFlag,fillStrike, self.underlying_price,time_to_expiry, self.rfr,vol)
                self.gamma -= fillQty*gk.gamma(fillFlag,fillStrike, self.underlying_price,time_to_expiry, self.rfr,vol)*self.defaultSize
                self.theta -= fillQty*gk.theta(fillFlag,fillStrike, self.underlying_price,time_to_expiry, self.rfr,vol)*self.defaultSize
                self.vega -= fillQty*gk.vega(fillFlag,fillStrike, self.underlying_price,time_to_expiry, self.rfr,vol)*self.defaultSize

                self.positions[fill_msg.asset] -= update.fill_msg.filled_qty

        elif kind == "market_snapshot_msg":
            # When we receive a snapshot of what's going on in the market, update our information
            # about the underlying price.
            book = update.market_snapshot_msg.books["UC"]

            # Compute the mid price of the market and store it
            self.underlying_price = (
                float(book.bids[0].px) + float(book.asks[0].px)
            ) / 2

            await self.update_options_quotes()

        elif (
            kind == "generic_msg"
            and update.generic_msg.event_type == pb.GenericMessageType.MESSAGE
        ):
            # The platform will regularly send out what day it currently is (starting from day 0 at
            # the start of the case)
            self.current_day = float(update.generic_msg.message)
            #genMsg = update.generic_msg
            
           # print("GENERIC MESSAGE "+str(genMsg.event_type))


        elif kind == "trade_msg":
            #finds what the last trade price was:
            trade_msg = update.trade_msg
            underlyingPosit[trade_msg.asset]=float(trade_msg.price)
            #print("tradeAsset: "+trade_msg.asset+" latest price: "+trade_msg.price+" recorded: "+str(underlyingPosit[trade_msg.asset]))
            

  
    def getSpread(self):
        return .1
        #we have to determine how wide!

    async def update_options_quotes(self):
        #only trading the 100strike, will upgrade later
        strk = 100
        time_to_expiry = (21 +5-self.current_day)/ 252
        for strk in option_strikes:
            for flag in ["C","P"]:
                product = f"UC{strk}{flag}"
                flag = flag.lower()
                vol = self.compute_vol_estimate(underlyingPosit[product], strk, time_to_expiry, flag)
                if(self.delta>0):
                    print("Delta "+str(self.delta))
                if (vol!=9):
                    theoPrice = self.compute_options_price(flag,self.underlying_price,strk,time_to_expiry,vol)
                    theoPrice = round(theoPrice,1)
                    thisTheta = self.defaultSize*100*gk.theta(flag,strk,self.underlying_price,time_to_expiry,self.rfr,vol)
                    thisDelta = self.defaultSize*100*gk.delta(flag,strk,self.underlying_price,time_to_expiry,self.rfr,vol)
                    thisGamma  = self.defaultSize * 100* gk.gamma(flag,strk,self.underlying_price,time_to_expiry,self.rfr,vol)
                    thisVega = self.defaultSize * 100* gk.vega(flag,strk,self.underlying_price,time_to_expiry,self.rfr,vol)
                    print("MEAPP "+product+" Actualprice: "+str(underlyingPosit[product])+" Theoretical price: "+str(theoPrice))
                    if theoPrice>=underlyingPosit[product]: #this means its theoretically undervalued
                        if(theoPrice>underlyingPosit[product]):
                            self.defaultSize = self.bigSize #it buys more when the option is dirt cheap
                        if(abs(thisTheta+self.theta)<self.thetaLimit and abs(thisDelta+self.delta)<self.deltaLimit):
                            if(abs(thisGamma+self.gamma)<self.gammaLimit and abs(thisVega+self.vega)<self.vegaLimit):
                                bid = await self.place_order(
                                    product,
                                    pb.OrderSpecType.LIMIT,
                                    pb.OrderSpecSide.BID,
                                    self.defaultSize,  # How should this quantity be chosen?
                                    round(theoPrice-self.getSpread(),1)  # How should this price be chosen?
                                )
                                #print("asked for "+str(theoPrice+self.getSpread())+" trading at "+str(underlyingPosit[product]))
                                #print("ASSET CLASS "+product+" price: "+str(underlyingPosit[product]))
                                assert bid.ok
                                unfilledOrder[product] = unfilledOrder[product]+self.defaultSize
                        self.defaultSize = self.baseSize
                

 
            

if __name__ == "__main__":
    start_bot(optionBot)