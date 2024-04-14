# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 14:01:37 2022

@author: apm41

Read the FIFO data from BH photon counting board,
convert it to TCSPC, make the lifetime plot, and do OADFA analysis.

To get clear OADFA result, high enough OADF photon counts are required. 
This data analysis program provide a function that can add up multiple files from the same sample,
which enhance the OADFA data quality
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog
import time 


root = tk.Tk()
root.withdraw()
data_vv = filedialog.askopenfilename()
file_name_vv = os.path.splitext(data_vv)[0].split('/')[-1]

data_vh = filedialog.askopenfilename()
file_name_vh = os.path.splitext(data_vh)[0].split('/')[-1]
# In[] From 

### VV binning
start_t1 = time.time()# Stopwatch start


vv_Info = pd.read_csv(data_vv, names=['a']).loc[:16].reset_index(drop=True)
vv = pd.read_csv(data_vv, names=['a']).loc[17:].reset_index(drop=True) # read the file as .csv, read only first section (vertical emission)
vv = pd.DataFrame(vv.a.str.split(' ',-1).tolist()).apply(pd.to_numeric) # split the column named "a" and rename the column
vv = pd.DataFrame({'Macro': vv[0], 'Micro': vv[1]})

Macro_t= float(vv_Info.iloc[5].str.split(':').tolist()[0][1])*1E-9 # read the macro time info from data_vv
Micro_t= float(vv_Info.iloc[6].str.split(':').tolist()[0][1])*1E-12 # read the micro time info from data_vv


vv_time = pd.DataFrame(columns=['time(s)'])
vv_time['time(s)'] = vv['Macro']*Macro_t + vv['Micro']*Micro_t

end_t1 = time.time() # Stopwatch stop
print('processing time (VV) =', 
      int((end_t1-start_t1)//3600), ':', int((end_t1-start_t1)%3600//60), ':', int((end_t1-start_t1)%60)) # print stopwatch result

#### VH binning
start_t1 = time.time()# Stopwatch start


vh_Info = pd.read_csv(data_vh, names=['a']).loc[:16].reset_index(drop=True)
vh = pd.read_csv(data_vh, names=['a']).loc[17:].reset_index(drop=True) # read the file as .csv, read only first section (vertical emission)
vh = pd.DataFrame(vh.a.str.split(' ',-1).tolist()).apply(pd.to_numeric) # split the column named "a" and rename the column
vh = pd.DataFrame({'Macro': vh[0], 'Micro': vh[1]})

Macro_t= float(vh_Info.iloc[5].str.split(':').tolist()[0][1])*1E-9 # read the macro time info from data_vh
Micro_t= float(vh_Info.iloc[6].str.split(':').tolist()[0][1])*1E-12 # read the micro time info from data_vh


vh_time = pd.DataFrame(columns=['time(s)'])
vh_time['time(s)'] = vh['Macro']*Macro_t + vh['Micro']*Micro_t

end_t1 = time.time() # Stopwatch stop
print('processing time (VH) =', 
      int((end_t1-start_t1)//3600), ':', int((end_t1-start_t1)%3600//60), ':', int((end_t1-start_t1)%60)) # print stopwatch result


# In[] plot VV OADF
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000 
# without this, the number of data point might be too large for matplotlib
# or you can choose to plot only a small region when number of data point is very large

repRate = 2E3
BinNum = 2500
print('Bin size =', 1E6/repRate/BinNum, '\u03BCs')
num1 = str(1)

# Initinal binning; find the maximum peak location.
new_vv_time1=(vv_time)%(1/repRate)*1E6
vv_time1vv = pd.DataFrame({'Time':np.histogram(new_vv_time1['time(s)'],bins = BinNum)[1][1:],
                         'Counts'+num1: np.histogram(new_vv_time1['time(s)'],bins = BinNum)[0]})

# Move the peak to the desired position by delaying
targ_peak_t = 20 # us
WdelayVV = targ_peak_t*1E-6-vv_time1vv['Counts'+num1].idxmax()/repRate/BinNum
new_vv_time2=(vv_time+WdelayVV)%(1/repRate)*1E6
vv_time2vv = pd.DataFrame({'Time':np.histogram(new_vv_time2['time(s)'],bins = BinNum)[1][1:],
                         'Counts'+num1: np.histogram(new_vv_time2['time(s)'],bins = BinNum)[0]})


plt.plot(vv_time2vv['Time'],vv_time2vv['Counts'+num1])
plt.yscale('log', base = 10)
plt.title('OADF(VV)')
print(file_name_vv)
print('Max value', max(vv_time2vv['Counts'+num1]), 'at bin', vv_time2vv['Counts'+num1].idxmax())
# In[] plot VH OADF
repRate = 2E3
BinNum = 2500
print('Bin size =', 1E6/repRate/BinNum, '\u03BCs')
num1 = str(1)
# Initinal binning; find the maximum peak location.
new_vh_time1=(vh_time)%(1/repRate)*1E6
vh_time1vh = pd.DataFrame({'Time':np.histogram(new_vh_time1['time(s)'],bins = BinNum)[1][1:],
                         'Counts'+num1: np.histogram(new_vh_time1['time(s)'],bins = BinNum)[0]})

# Move the peak to the desired position by delaying
targ_peak_t = 20 # us
WdelayVH = targ_peak_t*1E-6-vh_time1vh['Counts'+num1].idxmax()/repRate/BinNum
new_vh_time2=(vh_time+WdelayVH)%(1/repRate)*1E6
vh_time2vh = pd.DataFrame({'Time':np.histogram(new_vh_time2['time(s)'],bins = BinNum)[1][1:],
                         'Counts'+num1: np.histogram(new_vh_time2['time(s)'],bins = BinNum)[0]})


plt.plot(vh_time2vh['Time'],vh_time2vh['Counts'+num1])
plt.yscale('log', base = 10)
plt.title('OADF(VH)')
print(file_name_vh)
print('Max value', max(vh_time2vh['Counts'+num1]), 'at bin', vh_time2vh['Counts'+num1].idxmax())
# In[] Plot both
lifetime_sumVV = pd.DataFrame({'Time': vv_time2vv['Time'],'Counts':vv_time2vv['Counts'+num1]})
lifetime_sumVH = pd.DataFrame({'Time': vv_time2vv['Time'],'Counts':vh_time2vh['Counts'+num1]})

plt.plot(vv_time2vv['Time'],vv_time2vv['Counts'+num1], label = 'VV')
plt.plot(vh_time2vh['Time'],vh_time2vh['Counts'+num1]*1.00, label = 'VH')
plt.yscale('log', base = 10)
plt.xlabel('Time (\u03BCs)',fontsize=12)
plt.ylabel('Photon counts', fontsize=12)
plt.title('OADF(Both)')
plt.legend()
plt.show()

# Zoomed-in plot

plt.plot(lifetime_sumVV['Time'],lifetime_sumVV['Counts'], label = 'I$_\parallel$')
plt.plot(lifetime_sumVH['Time'],lifetime_sumVH['Counts']*1.07, label = 'I$_\perp$')
plt.xlim(12,79)
plt.ylim(0,1000)
plt.xlabel('Time (\u03BCs)',fontsize=12)
plt.ylabel('Photon counts', fontsize=12)
plt.title('OADF(Both)')
plt.legend()
plt.show()

print('VV max:', max(lifetime_sumVV['Counts']),', VH max:', max(lifetime_sumVH['Counts']))
# In[] Adding up counts
# del goodVLPdatacsv 

# define goodVLPdatacsv if it doesn't exist
try:
    goodVLPdatacsv['vvall'] = lifetime_sumVV['Counts']+goodVLPdatacsv['vvall']
    goodVLPdatacsv['vhall'] = lifetime_sumVH['Counts']+goodVLPdatacsv['vhall']
except:
    goodVLPdatacsv = pd.DataFrame({'Time': lifetime_sumVH['Time'],
                                   'vvall': lifetime_sumVV['Counts'], 
                                   'vhall': lifetime_sumVH['Counts']})
# In[] plot goodVLPdatacsv
plt.plot(goodVLPdatacsv['Time'],goodVLPdatacsv['vvall'], label = 'I$_\parallel$')
plt.plot(goodVLPdatacsv['Time'],goodVLPdatacsv['vhall']*1.07, label = 'I$_\perp$')
plt.xlim(18,100)
plt.ylim(0,1500)
plt.xlabel('Time (\u03BCs)',fontsize=12)
plt.ylabel('Photon counts', fontsize=12)
plt.title('OADF(Both)')
plt.legend()
plot_OADFA = plt.gcf()
plt.show()

print('VV max:', max(goodVLPdatacsv['vvall']),', VH max:', max(goodVLPdatacsv['vhall']))

# In[]
def expo(x, A, t, y0):
    return A * np.exp(-x/t) + y0 # exponatial fitting

Gfactor = 1.45
OadfA = (goodVLPdatacsv['vvall']-Gfactor*goodVLPdatacsv['vhall'])/(goodVLPdatacsv['vvall']+(Gfactor*goodVLPdatacsv['vhall']))
OadfA[np.isnan(OadfA)] = 0

fitfrom = goodVLPdatacsv['vhall'].idxmax() +9
fitto = goodVLPdatacsv['vhall'].idxmax()+ 60
assum_I0 = goodVLPdatacsv['vhall'].idxmax()+8 # Assumed decay starting time point
if fitto > len(OadfA):
    fitto = len(OadfA)
if assum_I0 > fitfrom:
    assum_I0 = fitfrom

popt, pcov = curve_fit(expo, goodVLPdatacsv['Time'][fitfrom-assum_I0:fitto-assum_I0], OadfA[fitfrom:fitto], 
                       bounds = ([0.10, 1E-12, -2E-3], [0.45, 50,  2E-3]))
p_sigma = np.sqrt(np.diag(pcov))
diameter = ((popt[1]*1E3)**(1/3))*1.98 # unit: nm
dia_error = abs(1.98/3*(popt[1]*1E3)**(1/3-1)*(p_sigma[1]*1E3)) # Look up error propagation formula
residuals = pd.DataFrame(data = {'y_data':OadfA[fitfrom:fitto].reset_index(drop=True),
                                 'y_pred':expo(goodVLPdatacsv['Time'][fitfrom-assum_I0:fitto-assum_I0], *popt).reset_index(drop=True)})


'''######  Plotting OADFA and fitting curve ######'''

fig, axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

axs[0].plot(goodVLPdatacsv['Time']-2, [0 for i in range(len(goodVLPdatacsv['Time']))], color = 'gray')
axs[0].scatter(goodVLPdatacsv['Time'][fitfrom:fitto]-21.2,OadfA[fitfrom:fitto], label = 'mVenus')#, color = 'green')

axs[0].plot((goodVLPdatacsv['Time'][assum_I0:fitto]-21.2),          
          expo(goodVLPdatacsv['Time'][0:(fitto-assum_I0)]-goodVLPdatacsv['Time'][0], *popt), 'r--', linewidth=3,
          label = 'Fitting OADFA')# (\u03B8 = '+ str(round(popt[1], 2))+' \u03BCs)')

axs[0].set_xlim(-0.1,11)
axs[0].set_ylim(-0.2, 0.4)
axs[0].set_ylabel('Anisotropy',fontsize=12)
axs[0].legend()

axs[1].plot(goodVLPdatacsv['Time']-2, [0 for i in range(len(goodVLPdatacsv['Time']))], color = 'gray')
axs[1].scatter((goodVLPdatacsv['Time'][fitfrom:fitto]-21.2), 
               residuals['y_data']-residuals['y_pred'], label = 'Residuals') # label "fitfrom"
axs[1].set_xlim(-0.1,11)
axs[1].set_ylim(-0.2, 0.2)
axs[1].set_xlabel('Time (\u03BCs)',fontsize=12)
axs[1].set_ylabel('Residuals')


plot_OADFA = plt.gcf()
plt.show()


print('r0 =', round(popt[0], 3),'\u00B1',round(p_sigma[0],3))  
print('\u03B8 =', round(popt[1], 3),'\u00B1',round(p_sigma[1],3), '\u03BCs')
print('diameter = ', round(diameter, 2) ,'\u00B1',round(dia_error,2) ,'nm')  
print('OADFA tail matching:', round(sum(OadfA[fitto-10:fitto])/10,6), '(G=', Gfactor, ')')
# In[] Save plot OADFA
path2 = askdirectory()
os.chdir(path2)
file_name = file_name_vv.split('_VV)')[0]+')'
plot_OADFA.savefig(file_name + '(OADFA_'+str(round(1E9/repRate/BinNum))+' bin_G='+str(Gfactor)+').png',dpi=600,bbox_inches='tight')
