import strategy
import pandas as pd
import time
import numpy as np

castles = pd.Series([1,2,3,4,5,6,7,8,9,10],
                index=['one','two','three','four','five','six','seven','eight','nine','ten'])

def simulateWar(plans):
    plans=plans.join(plans.loc[:,['one','two','three','four','five','six','seven',
        'eight','nine','ten']].apply(battle, axis=1, args=(plans,)).rename({-1:'losses',
        0:'draws',1:'wins'}, axis=1))
    return plans

def battleAgainstControl(testPlans, enemyPlans):
    testPlans=testPlans.join(testPlans.loc[:,['one','two','three','four','five','six','seven',
        'eight','nine','ten']].apply(battle, axis=1, args=(enemyPlans,)).rename({-1:'losses',
        0:'draws',1:'wins'}, axis=1))
    return testPlans
                                                                               
def simulateRandomWar(numStrategies, numResults):
    plans=[]
    
    t0=time.time()
    for i in range(numStrategies):
        plans.append(strategy.generate())
    plans = pd.DataFrame(plans)
    t1=time.time()
    print('Generated strategies in %0.2f s' %(t1-t0))
    
    plans=simulateWar(plans)
    
    t2=time.time()
    print('Completed battles in %0.2f s' %(t2-t1))
    
    return plans.sort_values(by=['wins'], ascending=False).head(numResults)

def battle(plan, plans):
    results = np.sign(plan - plans) * castles
    results['outcome'] = np.sign(results.sum(axis=1))
    tally = results['outcome'].value_counts()
    return tally