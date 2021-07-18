#!/usr/bin/env python

from utc_bot import UTCBot, start_bot
import proto.utc_bot as pb
import betterproto
import math
import re

import asyncio
import random

from typing import Optional

"""Constant listed from case packet"""
DAYS_IN_YEAR = 252
LAST_RATE_ROR_USD = 0.25
LAST_RATE_HAP_USD = 0.5
LAST_RATE_HAP_ROR = 2
DaysToExp = 21

TICK_SIZES = {'6RH': 0.00001, '6RM': 0.00001, '6RU': 0.00001, '6RZ': 0.00001, '6HH': 0.00002, \
    '6HM': 0.00002, '6HU': 0.00002, '6HZ': 0.00002, 'RHH': 0.0001, 'RHM': 0.0001, 'RHU': 0.0001, 'RHZ': 0.0001, "RORUSD": 0.00001}
LOT_SIZES = {'6RH': 100000, '6RM': 100000, '6RU': 100000, '6RZ': 100000, '6HH': 100000, \
    '6HM': 100000, '6HU': 100000, '6HZ': 100000, 'RHH': 50000, 'RHM': 50000, 'RHU': 50000, 'RHZ': 50000, "RORUSD": 100000}
FUTURES = [i+j for i in ["6R", "6H", "RH"] for j in ["H", "M", "U", "Z"]]

contractVals = {}
cashVals = {}
longshort = {}
disabledAction = {}
for i in FUTURES+["RORUSD"]:
    contractVals[i] = 1
    cashVals[i] = 0.0000
    longshort[i] = 0
    disabledAction[i] = False
#inits values of each contract to 0

'''Rounds price to nearest tick_number above'''
def round_nearest(x, tick=0.0001):
    return round(round(x / tick) * tick, -int(math.floor(math.log10(tick))))

'''Finds daily interest rates from annual rate'''
def daily_rate(daily_rate):
    return math.pow(daily_rate, 1/252)

class PositionTrackerBot(UTCBot):
    async def place_bids(self, asset):
        await self.emergencyReduction(asset)
        
        orders = await self.basic_mm(asset, self.fair[asset], self.params["edge"],
            1, self.params["limit"],self.max_widths[asset])
        for index, price in enumerate(orders['bid_prices']):
            if (self.pos[asset]+orders['ask_sizes'][index])<self.params["limit"] and asset!="RORUSD":
                if not disabledAction[asset]:
                    
                    resp = await self.modify_order(
                            self.askorderid[asset][index],
                            asset,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.BID,
                            orders['ask_sizes'][index],
                            round_nearest(price, TICK_SIZES[asset]),
                        )
                    self.askorderid[asset][index] = resp.order_id
            
            elif (self.pos[asset]+orders['ask_sizes'][index])<self.params["size"] and asset=="RORUSD":
                #print("BID is RORUSD")
                if not disabledAction[asset] :
                    resp = await self.modify_order(
                            self.askorderid[asset][index],
                            asset,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.BID,
                            orders['ask_sizes'][index],
                            round_nearest(price, TICK_SIZES[asset]),
                        )
                    self.askorderid[asset][index] = resp.order_id
            

        
                
      

    async def place_asks(self, asset):
        orders = await self.basic_mm(asset, self.fair[asset], self.params["edge"],
            1, self.params["limit"],self.max_widths[asset])
        for index, price in enumerate(orders['ask_prices']):


            if orders['ask_sizes'][index] != 0 and (price>0):
                if(self.pos[asset]+orders['ask_sizes'][index])<self.params["limit"] and asset!="RORUSD":
                    #print("ASK not RORUSD")
                    
                    resp = await self.modify_order(
                        self.askorderid[asset][index],
                        asset,
                        pb.OrderSpecType.LIMIT,
                        pb.OrderSpecSide.ASK,
                        orders['ask_sizes'][index],
                        round_nearest(price, TICK_SIZES[asset]),
                    )
                    self.askorderid[asset][index] = resp.order_id
                
                elif (self.pos[asset]+orders['ask_sizes'][index])<self.params["size"] and asset=="RORUSD":
                  #  print("ASK is RORUSD")
                    resp = await self.modify_order(
                        self.askorderid[asset][index],
                        asset,
                        pb.OrderSpecType.LIMIT,
                        pb.OrderSpecSide.ASK,
                        orders['ask_sizes'][index],
                        round_nearest(price, TICK_SIZES[asset]),
                    )
                    self.askorderid[asset][index] = resp.order_id
                
            await self.emergencyReduction(asset)
                

    async def evaluate_fairs(self, cashVal, pd):
        ##TO Do
        rate = 0
        s = pd[0:2]
        if (s == "6R"):
            rate = LAST_RATE_ROR_USD
        elif(s == "6H"):
            rate = LAST_RATE_HAP_USD
        else:
            rate = LAST_RATE_HAP_ROR
        fv = cashVal*(1+rate*DaysToExp/DAYS_IN_YEAR)
        return fv



    def getFair(self, cashVal, pd): #my own calculate fair 
        rate = 0
        s = pd[0:2]
        if (s == "6R"):
            rate = LAST_RATE_ROR_USD
        elif(s == "6H"):
            rate = LAST_RATE_HAP_USD
        else:
            rate = LAST_RATE_HAP_ROR
        
        fv = cashVal*(1+rate*DaysToExp/DAYS_IN_YEAR)
        self.fair[pd]=round_nearest(fv,TICK_SIZES[pd])
        #print("In Dictionary: "+str(self.fair[pd])+" FV: "+str(fv))
        #print("asset "+pd+" calculating cash: "+str(cashVal)+" rate "+str(rate)+" DTE "+str(DaysToExp)+" DIY "+str(DAYS_IN_YEAR)+" got fv "+str(fv))
        
        return 0
    
    async def checkDisable(self):
        
        for i in FUTURES+["RORUSD"]:
            if( i == "RORUSD"):
                if self.pos[i]>=9 or self.pos[i]<=-8:
                    disabledAction[i] = True
                else:
                    disabledAction[i] = False
                
            else:
                if self.pos[i]>=90 or self.pos[i]<=-90:
                    disabledAction[i] = True
                else:
                    disabledAction[i] = False
        


    async def emergencyReduction(self, asset):
      #  print("SSSSSS "+str(self.pos))
        if not disabledAction[asset]:
            if (asset == "RORUSD"):
                print("in RORUSD size  "+self.pos[asset])
                if self.pos[asset]>=8:
                    f =  self.place_order(asset,pb.OrderSpecType.MARKET, pb.OrderSpecSide.ASK, abs(self.pos[asset])+2)

                elif self.pos[asset]<=-6:
                    print("FUCK")
                    f =  self.place_order(asset,pb.OrderSpecType.MARKET, pb.OrderSpecSide.BID, abs(self.pos[asset])+2)
                    
            else:
                if self.pos[asset]>70:
                    f =  self.place_order(asset,pb.OrderSpecType.MARKET, pb.OrderSpecSide.ASK, abs(self.pos[asset])-70+20 )
                elif self.pos[asset]<=-7:
                    f =  self.place_order(asset,pb.OrderSpecType.MARKET, pb.OrderSpecSide.BID, abs(self.pos[asset])-70+20 )
        
        await self.checkDisable()


    async def basic_mm(self, asset, fair, width, clip, max_pos, max_range):
        if (asset != "RORUSD"):
            max_pos = max_pos-20
        else:
            max_pos = 5
        fade = (max_range / 2.0) / max_pos
        adjusted_fair = fair - self.pos[asset] * fade

        ##Best bid, best ask prices
        bid_p = adjusted_fair - width / 2.0
        ask_p = adjusted_fair + width / 2.0

        ##Next best bid, ask price
        bid_p2 = min(adjusted_fair - clip * fade - width / 2.0, 
            bid_p - TICK_SIZES[asset])
        ask_p2 = min(adjusted_fair + clip * fade + width / 2.0, 
            ask_p + TICK_SIZES[asset])
        
        ##Remaining ability to quote
        bids_left = max_pos - self.pos[asset]
        asks_left = max_pos + self.pos[asset]

        if bids_left <= 3:
            #reduce your position as you are violating risk limits!
            ask_p = bid_p
            ask_s = clip
            ask_p2 = bid_p + TICK_SIZES[asset]
            ask_s2 = clip
            bid_s = 0
            bid_s2 = 0
        elif asks_left <= 3:
            #reduce your position as you are violating risk limits!
            bid_p = ask_p
            bid_s = clip
            bid_p2 = ask_p - TICK_SIZES[asset]
            bid_s2 = clip
            ask_s = 0
            ask_s2 = 0
        else:
            
            #bid and ask size setting
            bid_s = min(bids_left, clip)
            bid_s2 = max(0, min(bids_left - clip, clip))
            ask_s = min(asks_left, clip)
            ask_s2 = max(0, min(asks_left - clip, clip))
        if (asset == "RORUSD"):
            ask_s  = 1
            ask_s2 = 1
        return {'asset': asset,
                'bid_prices': [bid_p, bid_p2], 
                'bid_sizes': [bid_s, bid_s2],
                'ask_prices': [ask_p, ask_p2],
                'ask_sizes': [ask_s, ask_s2],
                'adjusted_fair': adjusted_fair,
                'fade': fade}


    async def handle_exchange_update(self, update: pb.FeedMessage):
        kind, _ = betterproto.which_one_of(update, "msg")

        #Possible exchange updates: 'market_snapshot_msg','fill_msg'
        #'liquidation_msg','generic_msg', 'trade_msg', 'pnl_msg', etc.


        if kind == "pnl_msg":
            my_m2m = self.cash
            for asset in ([i+j for i in ["6R", "6H"] for j in ["H", "M", "U", "Z"]] + ["RORUSD"]):
                my_m2m += self.mid[asset] * self.pos[asset] if self.mid[asset] is not None else 0
            for asset in (["RH" + j for j in ["H", "M", "U", "Z"]]):
                my_m2m += (self.mid[asset] * self.pos[asset] * self.mid["RORUSD"] 
                    if (self.mid[asset] is not None and self.mid["RORUSD"] is not None) else 0)
            print("M2M", update.pnl_msg.m2m_pnl, my_m2m)
        #Update position upon fill messages of your trades
        elif kind == "fill_msg":
            if update.fill_msg.order_side == pb.FillMessageSide.BUY:
                self.cash -= update.fill_msg.filled_qty * float(update.fill_msg.price)
                self.pos[update.fill_msg.asset] += update.fill_msg.filled_qty
            else:
                self.cash += update.fill_msg.filled_qty * float(update.fill_msg.price)
                self.pos[update.fill_msg.asset] -= update.fill_msg.filled_qty
            for asset in FUTURES:
                if (asset == "RORUSD"):
                    print("PLAYING WITH RORUSD")
                await self.place_bids(asset)
                await self.place_asks(asset)
            await self.spot_market()
        #Identify mid price through order book updates


        elif kind == "market_snapshot_msg":
            for asset in (FUTURES + ["RORUSD"]):
                
                '''updateFairVal'''
                #self.fair[asset] = self.getFair(contractVals[asset], asset)
                #print("feeding assetVal "+str(contractVals[asset]))
                self.getFair(contractVals[asset],asset)
                #print("updated FV of "+asset+" to "+str(self.fair[asset]))
                book = update.market_snapshot_msg.books[asset]
                mid: "Optional[float]"
                if len(book.asks) > 0:
                    if len(book.bids) > 0:
                        mid = (float(book.asks[0].px) + float(book.bids[0].px)) / 2
                    else:
                        mid = float(book.asks[0].px)
                elif len(book.bids) > 0:
                    mid = float(book.bids[0].px)
                else:
                    mid = None

                self.mid[asset] = mid
        #Competition event messages

        elif kind == "generic_msg":
            print(update.generic_msg.message)
            print(self.pos)
            stringCheese = str(update.generic_msg.message)
            #we need to fix this
            if ("NEW FEDERAL" in str(update.generic_msg.message)):
                if (stringCheese[0:3] == "ROR"):
                    LAST_RATE_ROR_USD = float(stringCheese[29:])
                elif(stringCheese[0:3] == "HAP"):
                    LAST_RATE_HAP_ROR = float(stringCheese[29:])
                else:
                    LAST_RATE_HAP_USD = float(stringCheese[29:])
            for asset in FUTURES:
                await self.place_bids(asset)
                await self.place_asks(asset)
            #await self.spot_market()

        elif kind == "trade_msg":
            trade_msg = update.trade_msg
            contractVals[trade_msg.asset] = float(trade_msg.price)
            if (trade_msg.asset[0:2] =='6R' or  trade_msg.asset[0:2] =='6H'):
                cashVals[trade_msg.asset] = trade_msg.price*100000
            else:
                cashVals[trade_msg.asset] = trade_msg.price*500000
          #  print("FV of "+str(trade_msg.asset)+" is "+str(self.fair[trade_msg.asset])+" last trade: " +str(contractVals[trade_msg.asset]))

    async def spot_market(self):
        net_position = self.pos["RORUSD"]
        for month in ["H", "M", "U", "Z"]:
            net_position += 0.05 * self.pos['RH' + month]
        net_position = round(net_position)
        bids_left = self.params["spot_limit"] - self.pos["RORUSD"]
        asks_left = self.params["spot_limit"] + self.pos["RORUSD"]
        if bids_left <= 5:
            resp = await self.place_order(
                "RORUSD",
                pb.OrderSpecType.MARKET,
                pb.OrderSpecSide.ASK,
                abs(bids_left),
            )
        elif asks_left <= 5: 
            resp = await self.place_order(
                "RORUSD",
                pb.OrderSpecType.MARKET,
                pb.OrderSpecSide.BID,
                abs(asks_left),
            )
        elif (net_position > 0):
            resp = await self.place_order(
                "RORUSD",
                pb.OrderSpecType.MARKET,
                pb.OrderSpecSide.ASK,
                min(abs(net_position), asks_left),
            )
        elif (net_position < 0):
            resp = await self.place_order(
                "RORUSD",
                pb.OrderSpecType.MARKET,
                pb.OrderSpecSide.ASK,
                min(abs(net_position), bids_left),
            )

    async def handle_round_started(self):
        

        self.cash = 0.0
        self.pos = {asset:0 for asset in FUTURES + ["RORUSD"]} #still needs to be fucked

        self.fair = {asset:1.11111 for asset in FUTURES + ["RORUSD"]}

        self.mid = {asset: None for asset in FUTURES + ["RORUSD"]}

        self.max_widths = {asset:0.005 for asset in FUTURES}
        
        self.bidorderid = {asset:["",""] for asset in FUTURES}
        self.askorderid = {asset:["",""] for asset in FUTURES}


        self.params = {
            "edge": 0.005,
            "limit": 100,
            "size": 10,
            "spot_limit": 10
        }
        

if __name__ == "__main__":
    start_bot(PositionTrackerBot)



    