#!/usr/bin/env python

from dataclasses import astuple
from utc_bot import UTCBot, start_bot
import proto.utc_bot as pb
import betterproto
import numpy as np
import asyncio
import random
import scipy
from scipy.stats import norm

option_strikes = [90, 95, 100, 105, 110]


class optionBot(UTCBot):

    async def handle_round_started(self):
        """
        This function is called when the round is started. You should do your setup here, and
        start any tasks that should be running for the rest of the round.
        """

        # This variable will be a map from asset names to positions. We start out by initializing it
        # to zero for every asset.
        self.positions = {}
        
        self.rfr = 0.0174 #might need to check this, it's the risk free rate as of March 21

        self.positions["UC"] = 0
        for strike in option_strikes:
            for flag in ["C", "P"]:
                self.positions[f"UC{strike}{flag}"] = 0

        # Stores the current day (starting from 0 and ending at 5). This is a floating point number,
        # meaning that it includes information about partial days
        self.current_day = 0

        # Stores the current value of the underlying asset
        self.underlying_price = 100

    def compute_vol_estimate(self) -> float:
        """
        This function is used to provide an estimate of underlying's volatility. Because this is
        an example bot, we just use a placeholder value here. We recommend that you look into
        different ways of finding what the true volatility of the underlying is.
        """
        return 0.35
    def getNormal(self, value):
        return norm.cdf(value, 0, 1)

    def getD1(self, underlying_px, k, stdv, rfr, time):
        a = np.log(underlying_px/k) + (rfr+(stdv**2)/2)*time
        return a/(stdv*(time**(1/2)))

    def getD2(self, d1, stdv, time):
        return d1-stdv*(time**(1/2))

    def compute_options_price(
        self,
        flag: str,
        underlying_px: float,
        strike_px: float,
        time_to_expiry: float,
        volatility: float,
    ) -> float:
        value = 0
        standardDev = 1
        """
        You may want to look into the py_vollib library, which is installed by default in your
        virtual environment.
        """
        if (flag == "C"):
            d1 = getD1(underlying_px,strike_px,standardDev,self.rfr,time_to_expiry)
            d2 = getD2(d1,standardDev,time_to_expiry)
            value = underlying_px*getNormal(d1)-strike_px*np.exp(-1*self.rfr*time_to_expiry)*getNormal(d2)
        else:
            pass

        return value

    async def update_options_quotes(self):
        """
        This function will update the quotes that the bot has currently put into the market.

        In this example bot, the bot won't bother pulling old quotes, and will instead just set new
        quotes at the new theoretical price every time a price update happens. We don't recommend
        that you do this in the actual competition
        """
        # What should this value actually be?
        time_to_expiry = 21 / 252
        vol = self.compute_vol_estimate()

        for strike in option_strikes:
            for flag in ["C", "P"]:
                asset_name = f"UC{strike}{flag}"
                theo = self.compute_options_price(
                    flag, self.underlying_price, strike, time_to_expiry, vol
                )

                bid_response = await self.place_order(
                    asset_name,
                    pb.OrderSpecType.LIMIT,
                    pb.OrderSpecSide.BID,
                    1,  # How should this quantity be chosen?
                    theo - 0.30,  # How should this price be chosen?
                )
                assert bid_response.ok

                ask_response = await self.place_order(
                    asset_name,
                    pb.OrderSpecType.LIMIT,
                    pb.OrderSpecSide.ASK,
                    1,
                    theo + 0.30,
                )
                assert ask_response.ok

    async def handle_exchange_update(self, update: pb.FeedMessage):
        kind, _ = betterproto.which_one_of(update, "msg")

        if kind == "pnl_msg":
            # When you hear from the exchange about your PnL, print it out
            print("My PnL:", update.pnl_msg.m2m_pnl)

        elif kind == "fill_msg":
            # When you hear about a fill you had, update your positions
            fill_msg = update.fill_msg

            if fill_msg.order_side == pb.FillMessageSide.BUY:
                self.positions[fill_msg.asset] += update.fill_msg.filled_qty
            else:
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

        elif kind == "trade_msg":
            # There are other pieces of information the exchange provides feeds for. See if you can
            # find ways to use them to your advantage (especially when more than one competitor is
            # in the market)
            pass


if __name__ == "__main__":
    start_bot(optionBot)