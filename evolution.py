import war
import pandas as pd
import time
from os.path import exists
import strategy

saveFileName='results//evolved-vs-extended-data-300-10-728-30-3.csv'
numOffspringPerParent = 300
mutations = 10
numSurvivors = 728
rounds = 30

controlStrats = pd.read_csv('extended_training_data.csv')
parentStrats = pd.read_csv('results\\real-evolved-all-duplicated-removed.csv')

if exists(saveFileName):
    raise Exception('File %s already exists, enter a new name' %saveFileName)

currentGeneration = parentStrats.copy()

starttime = time.time()

for round in range(rounds):
    t0=time.time()
    print('Starting round %i' %(round+1)) 
    survivors = pd.DataFrame()
    
    offspring = []
    
    for index, strat in currentGeneration.loc[:,['one','two','three','four','five','six','seven','eight','nine','ten']].iterrows():
        for i in range(numOffspringPerParent):
            offspring.append(strategy.perturb(strat.copy(), mutations))    
    
    offspring = pd.DataFrame(offspring).reset_index(drop=True)
    offspring.drop_duplicates(inplace=True, ignore_index=True)
    
    t1=time.time()
    print('Offspring created in %i s' %(t1-t0))
    
    offspring = war.battleAgainstControl(offspring, controlStrats)
    
    t2=time.time()
    print('Battles complete in %i s' %(t2-t1))
    
    offspring['WinRatio'] = offspring['wins']/(offspring['wins'] + offspring['losses'] + offspring['draws'])
    offspring = offspring.sort_values(['WinRatio'], ascending=False, ignore_index=True)        
    
    currentGeneration = offspring.head(numSurvivors)
    print('Round took %i s total' %(time.time()-t0))

print('Evolved through %i generations in %i s' %(rounds, time.time()-starttime))
currentGeneration.to_csv(saveFileName, index=False)