
#Author: SAM SAXON
#praying to god this works

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize

DAY_COUNT = -1

p_h = pd.read_csv("Case3HistoricalPrices.csv")
p_h = p_h.loc[:, ~p_h.columns.str.contains('^Unnamed')]

#for testing:
#train = p_h[2300:]
#p_h = p_h[:2300]

#initialize random weights
weights = np.array(np.random.random(24))
weights = weights/np.sum(weights)

def calc_sharpe(weights):
    global p_h
   
    ret = p_h.pct_change()
    m_d_r = ret.mean()
    c_m = ret.cov()

    pf_return = np.sum(m_d_r * weights) * 252
    pf_std_dev = np.sqrt(np.dot(weights.T, np.dot(c_m, weights))) * np.sqrt(252)
    sharpe = (pf_return/pf_std_dev) * (252 ** 0.5)

    #return negative value for minimze function
    return -1 * sharpe

def check_sum(weights):
    return np.sum(weights) - 1

#this is the function that matters for the competition
def allocate_portfolio(asset_prices):
    global weights
    global p_h
    global DAY_COUNT

    DAY_COUNT+=1
    #add new prices to price history
    p_h = p_h.append(asset_prices)

    if DAY_COUNT%126 != 0:
        return weights

    #optimize sharpe value
    bounds = ((0,1),(0,1))*12
    cons = ({'type':'eq','fun':check_sum})
    opt_results = minimize(calc_sharpe, weights, method='SLSQP', bounds=bounds, constraints=cons)
    weights = opt_results.x
    return opt_results.x

#function to test the solution
def test_solution():
    global p_h
    #global train
    for i in range(len(train)):
        new_data = train.loc[2300+i]
        print("Day " + str(i))
        print(allocate_portfolio(new_data))
       

#test_solution()