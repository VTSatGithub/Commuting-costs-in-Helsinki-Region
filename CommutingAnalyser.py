
# coding: utf-8

# # Commuting Cost Analysis in Helsinki Region
# 
# As a resident of the Helsinki area I was interested which mode of transportation is more cost-efficient for commuting within Helsinki region (including municipalities of Helsinki, Espoo, and Vantaa). Means of transportation considered are: private car, DriveNow car sharing service, public transport, and Taxi service. Approximate distance of 50 km is assumed to be the width of the region from east to west as well as North to South. In the following I discuss each mode of transport, followed by graphs depicting cost of commuting as a function of distance. Three different average speeds assumed simulating different traffic conditions. Finally, results are discussed around three user cases derived from my own experience. 
# Valeri Tsatsishvili
# 

import numpy as np
import matplotlib.pyplot as plt

# Initialize: input all necessary information here

FuelCons = [7 ,12]                         # fuel consumption highway(min)  and town(max) L per 100km
FuelPrice = 1.45                         # how much 1L fuel costs
TotalExpCar = 1200                      #'how much do you spend on a car annually including regular bills and repairs/services 
InsTaxCar = 700                         #'only fixed tax+insurance
PubTrCostInt = 2.20                     # Internal single ticket
PubTrCostReg = 4.20                     # single 2zone regional ticket
PubTrCostPer = 106.5/30                 # 30 day 2 zone regional ticket
DrvNowCostMin = 0.46                     # 'DriveNow price per min'
dist=list(range(1,51))                  # range of distances in km



# First, lets define couple of functions 
FuelConsRange = max(FuelCons) - min(FuelCons)
Scaling = np.round(FuelConsRange/60,3)   #here I assume that average speed in Helsinki region can range between 10km/h up to 70km/h.  

def EstFC(FuelCons,AvgSpeed,Scaling):
    # rough estimate of fuel consumption based on average speed
    FuelConsEst = max(FuelCons) - AvgSpeed*Scaling 
    return FuelConsEst

def CostAnalysis(dist, AvgSpeed,FuelConsEst,FuelPrice,InsTaxCar,TotalExpCar, DrvNowCostMin):
    # estimate costs as a function of distance
    TrCostCar = []
    TrCostTaxi = []
    TrCostDrvNow =[]
    DrvNowCostHr= DrvNowCostMin*60
    for d in range(1,max(dist)+1):
        TrCostCar.append(TotalExpCar/365 + (FuelConsEst/100 * d)*FuelPrice)
        TrCostTaxi.append(5.90 + d*1.60 + InsTaxCar/365)
        TrCostDrvNow.append(d/AvgSpeed*DrvNowCostHr+InsTaxCar/365) 
    return TrCostCar, TrCostTaxi,TrCostDrvNow


# In[] Visualization

get_ipython().magic('matplotlib notebook')
from IPython.core.pylabtools import figsize
figsize(10, 15) 
plt.figure()
count = 0

# The script below iteratively estimates costs for disserent transports at different average speed and plot the results

for AvgSpeed in [20, 30, 40]:
    
    FuelConsEst = EstFC(FuelCons,AvgSpeed,Scaling)
    [TrCostCar, TrCostTaxi,TrCostDrvNow] = CostAnalysis(dist, AvgSpeed,FuelConsEst,FuelPrice,InsTaxCar,TotalExpCar, DrvNowCostMin)
    
    count = count + 1
    index = 310 + count
    plt.subplot(index)
    
    plt.plot(dist,TrCostCar,'b.-')
    plt.plot(dist,TrCostDrvNow,'g.-')
    plt.plot(dist,TrCostTaxi,'r.-')

    plt.plot(dist,InsTaxCar/365 + PubTrCostInt*np.ones(max(dist)),'c-.')
    plt.plot(dist,InsTaxCar/365 + PubTrCostReg*np.ones(max(dist)),'y-.')
    plt.plot(dist,InsTaxCar/365 + PubTrCostPer*np.ones(max(dist)),'k-.')

    # some formatting
    plt.title(('Aerage speed in km/h:', AvgSpeed))
    plt.xlabel('Distance km')
    plt.ylabel('Cost Eur')
    plt.legend(['Car','DrvNow','Taxi','PubTrInt','PubTrReg','PubTrPer'])
    plt.xticks(np.arange(0,51,5))
    plt.xlim(0,55)
    plt.ylim(0,30)
    plt.grid()


    
