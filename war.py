import strategy
import pandas as pd
import time
import numpy as np

# Functions that carry out the game itself

# Point values for the castles
castles = pd.Series([1,2,3,4,5,6,7,8,9,10],
                index=['one','two','three','four','five','six','seven','eight','nine','ten'])

# Simulate all the one-on-one match-ups betweeen a set of strategies
# Plans is a DataFrame with the the castle numbers as column names, and one row per strategy
# Returns the DataFrame joined with columns for the number of wins, losses, and draws of each row
def simulateWar(plans):
    plans=plans.join(plans.loc[:,['one','two','three','four','five','six','seven',
        'eight','nine','ten']].apply(battle, axis=1, args=(plans,)).rename({-1:'losses',
        0:'draws',1:'wins'}, axis=1))
    return plans

# Simulate a set of strategies against a separate set of strategies
def battleAgainstControl(testPlans, enemyPlans):
    testPlans=testPlans.join(testPlans.loc[:,['one','two','three','four','five','six','seven',
        'eight','nine','ten']].apply(battle, axis=1, args=(enemyPlans,)).rename({-1:'losses',
        0:'draws',1:'wins'}, axis=1))
    return testPlans

# Create completely random strategies, simulate them against each other, and return the top performers
# numStrategies is an int for how many strategies to create
# numResults is an int for how many of the best strategies to return
# Returns a DataFrame containing the best strategies                                                            
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

# Battles one strategy againt a set of strategies
# Plans is a Pandas Series with the the castle numbers as index labels
# plans is a DataFrame with the the castle numbers as column names, and one row per strategy
# Returns the number of losses, draws, and wins as a Pandas Series with respective indexes of -1, 0, and 1.
def battle(plan, plans):
    results = np.sign(plan - plans) * castles
    results['outcome'] = np.sign(results.sum(axis=1))
    tally = results['outcome'].value_counts()
    return tally