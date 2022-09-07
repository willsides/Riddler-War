import war
import pandas as pd
import time
from os.path import exists

saveFileName='results//sim-8K-1K-2-trial2.csv'

numSims = 8000
numStrategiesEach = 1000
numTopStrategies = 2

if exists(saveFileName):
    raise Exception('File %s already exists, enter a new name' %saveFileName)

goodStrategies = pd.DataFrame()

t0 = time.time()

for i in range(numSims):
    print('Simulating war %i' %(i+1))
    goodStrategies = pd.concat([goodStrategies, war.simulateRandomWar(numStrategiesEach, numTopStrategies)], ignore_index=True)

t1 = time.time()
print('Phase 1 wars complete in %.2f s' %(t1-t0))

battleRoyale = war.simulateWar(goodStrategies.loc[:,['one','two','three','four','five','six','seven',
    'eight','nine','ten']]).sort_values(by=['wins'], ascending=False)

t2 = time.time()
print('Battle Royale complete in %.2f s' %(t2-t1))

battleRoyale.to_csv(saveFileName, index=False)