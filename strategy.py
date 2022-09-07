from scipy.special import comb
from numpy import random
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def generate():
    
    strategy = pd.Series(index=['one','two','three','four','five','six','seven','eight','nine','ten'], dtype='float64')
    
    n = 100
    m = 10
    
    c = comb(m+n-1, m-1)
    
    r = random.randint(1,c+1,dtype='int64')
    
    for castle, num in strategy.loc[['one','two','three','four','five','six','seven','eight','nine']].iteritems():
        k = 0
        
        ck = comb(m+n-k-2, m-2)
        
        while ck < r:
            k += 1
            r -= ck
            ck = comb(m+n-k-2, m-2)
        
        strategy.loc[castle]=k
        
        n -= k
        m -= 1
        
    strategy.loc['ten'] = n
    
    return strategy

def perturb(strategy, mutations = 1):
    castles = ['one','two','three','four','five','six','seven','eight','nine','ten']
    for i in range(mutations): 
        
        pos = random.randint(0,10)
        strategy.loc[castles[pos]] += 1
        
        while True:    
            pos = random.randint(0,10)
            if strategy.loc[castles[pos]] > 0:
                strategy.loc[castles[pos]] -= 1
                break

    return strategy