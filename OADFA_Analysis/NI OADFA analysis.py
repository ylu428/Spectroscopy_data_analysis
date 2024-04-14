# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 22:50:21 2021

@author: Yi-Han

This is for plotting an analyzing the OADFA data measured by NI board (slow/fast lifetime)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog

def expo(x, A, t, y0):
    return A * np.exp(-x/t) + y0 # exponatial fitting
def biexpo(x, A1, t1, A2, t2, y0):
    return A1 * np.exp(-x/t1) + A2 * np.exp(-x/t2) + y0 # exponatial fitting

# In[] Loading data (Could load multiple files in the same diractory)
root = tk.Tk()
root.withdraw()
file_1 = filedialog.askopenfilenames(title = 'Select all VVs')
file_2 = filedialog.askopenfilenames(title = 'Select all VHs')  # filedialog.askopenfilename"s" allow tkinter to import multiple files at once

# extract filename
# file_name = os.path.basename(file_2) => this method will also give file extensions.
file_name = os.path.splitext(file_2[0])[0].split('/')[-1]

###
# read and analyze the data
timebin = pd.read_csv(file_1[0], sep="\t", header=1, names=['Time','Int'])['Time']
LifetimeVV = pd.DataFrame()
LifetimeVH = pd.DataFrame()


for i in range(len(file_1)):
    temp_name = file_1[i].split(')-')[-1]
    num = [int(m) for m in temp_name if m.isdigit()]
    num = str(num[0]*10+num[1]) if len(num) >1 else str(num[0])
    temp = pd.read_csv(file_1[i], sep="\t", header=1, names=['Time','VV'+num])['VV'+num] # read the file.csv
    LifetimeVV = pd.concat([LifetimeVV, temp], axis=1)
for i in range(len(file_2)):
    temp_name = file_2[i].split(')-')[-1]
    num = [int(m) for m in temp_name if m.isdigit()]
    num = str(num[0]*10+num[1]) if len(num) >1 else str(num[0])
    temp = pd.read_csv(file_2[i], sep="\t", header=1, names=['Time','VH'+num])['VH'+num] # read the file.csv
    LifetimeVH = pd.concat([LifetimeVH, temp], axis=1)

oadf = pd.DataFrame(data = {'Time':timebin, 
                            'VV': LifetimeVV.sum(axis=1), 
                            'HV': LifetimeVH.sum(axis=1)},dtype=float)
# In[] OADFA analysis
dye = file_name.split(' ')[0]
dye = 'RbSNP'#'RbSiO\u2082' # \u208 + number is the unicode of subscript
Gfactor = 1.16

OadFA = (oadf['VV']-Gfactor*oadf['HV'])/(oadf['VV']+Gfactor*oadf['HV'])
OadFA[np.isnan(OadFA)] = 0     # convert nan value in OadFA to zero

fitfrom = 14
fitto = 98
assum_I0 = 8 # Assumed decay starting time point
if fitto > len(OadFA):
    fitto = len(OadFA)
if assum_I0 > fitfrom:
    assum_I0 = fitfrom

popt, pcov = curve_fit(expo, oadf['Time'][fitfrom-assum_I0:fitto-assum_I0], OadFA[fitfrom:fitto], 
                        bounds = ([0.35, 1E-12, -2E-3], [0.4*1.2+0.002, 1E-2,  2E-3]))
p_sigma = np.sqrt(np.diag(pcov))
diameter = ((popt[1]*1E9)**(1/3))*1.98
dia_error = abs(1.98/3*(popt[1]*1E9)**(1/3-1)*(p_sigma[1]*1E9)) # Look up error propagation formula

plt.plot(oadf['Time']*1E6, [0 for i in range(len(oadf['Time']))], color = 'gray')
plt.scatter(oadf['Time'][fitfrom:fitto]*1E6,OadFA[fitfrom:fitto], label = dye) # label "fitfrom"
plt.plot((oadf['Time'][assum_I0:fitto])*1E6,          
          expo(oadf['Time'][0:(fitto-assum_I0)], *popt), 'r--', linewidth=3,
          label = 'Fitting OADFA (\u03B8 = '+ str(round(popt[1]*1E6, 2))+' \u03BCs)')
plt.ylim(-0.3, 0.5)
plt.xlabel('Time (\u03BCs)',fontsize=12)
plt.ylabel('Anisotropy',fontsize=12)
plt.legend(loc='upper right')
## add text to plot shows the diameter of particle
# plt.text(5.0,0.25,'Diameter = '+str(round(diameter, 1))+' \u00B1 '+str(round(dia_error,1))+' nm', 
#          fontsize=10, bbox = dict(facecolor = 'limegreen', alpha = 0.5)) # alpha control the transparency
plot1 = plt.gcf()
plt.show()

## Standard deviation of fitting value
# print('r0 =', round(popt[0], 3),'\u00B1',round(p_sigma[0],3))  
# print('\u03B8 =', round(popt[1]*1E6, 3),'\u00B1',round(p_sigma[1]*1E6,3), '\u03BCs')
# print('diameter = ', round(diameter, 2) ,'\u00B1',round(dia_error,2) ,'nm')  
# print('No rebinning')
# print('OADFA tail matching:', round(sum(OadFA[fitto-20:fitto])/20, 6), '(G=', Gfactor, ')')


plt.plot(oadf['Time']*1E6, oadf['VV'], label = 'I$_\parallel$')
plt.plot(oadf['Time']*1E6, Gfactor*oadf['HV'], label = 'I$_\perp$')
plt.xlabel('Time (\u03BCs)',fontsize=12)
plt.ylabel('Counts',fontsize=12)
plt.ylim(-5, max(oadf['VV'])/100)
plt.legend()
plot2 = plt.gcf()
plt.show()
# In[] save plots
file_path = askdirectory()
os.chdir(file_path)


plot1.savefig(file_name.split('VH')[0] +' (OADFA).png',dpi=600, bbox_inches='tight')
plot2.savefig(file_name.split('VH')[0] +' (FL decay).png',dpi=600, bbox_inches='tight')


# In[] Rebinning by 2



oadf2 = pd.DataFrame(data = {'Time':np.zeros(int(len(timebin)/2)), 
                            'VV': np.zeros(int(len(timebin)/2)), 
                            'VH': np.zeros(int(len(timebin)/2))},dtype=float)

for i in range(int(len(timebin)/2)):
    oadf2['Time'][i] = oadf['Time'][2*i]
    oadf2['VV'][i] = (oadf['VV'][2*i]+oadf['VV'][2*i+1])
    oadf2['VH'][i] = (oadf['HV'][2*i]+oadf['HV'][2*i+1])

dye = file_name.split(' ')[0]
dye = 'RbSNP'#'RbSiO\u2082' # \u208 + number is the unicode of subscript
Gfactor = 1.16

OadFA = (oadf2['VV']-Gfactor*oadf2['VH'])/(oadf2['VV']+Gfactor*oadf2['VH'])
OadFA[np.isnan(OadFA)] = 0     # convert nan value in OadFA to zero

fitfrom = 7
fitto = 48
assum_I0 = 4 # Assumed decay starting time point
if fitto > len(OadFA):
    fitto = len(OadFA)
if assum_I0 > fitfrom:
    assum_I0 = fitfrom

popt, pcov = curve_fit(expo, oadf2['Time'][fitfrom-assum_I0:fitto-assum_I0], OadFA[fitfrom:fitto], 
                        bounds = ([0.35, 1E-12, -2E-3], [0.4*1.2+0.002, 1E-2,  2E-3]))
p_sigma = np.sqrt(np.diag(pcov))
diameter = ((popt[1]*1E9)**(1/3))*1.98
dia_error = abs(1.98/3*(popt[1]*1E9)**(1/3-1)*(p_sigma[1]*1E9)) # Look up error propagation formula

residuals = pd.DataFrame(data = {'y_data':OadFA[fitfrom:fitto].reset_index(drop=True),
                                 'y_pred':expo(oadf2['Time'][fitfrom-assum_I0:fitto-assum_I0], *popt).reset_index(drop=True)})


'''######  Plotting OADFA and fitting curve ######'''
fig, axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
axs[0].plot(oadf2['Time']*2E6-2, [0 for i in range(len(oadf2['Time']))], color = 'gray')
axs[0].scatter(oadf2['Time'][fitfrom:fitto]*1E6-0.7,OadFA[fitfrom:fitto], label = dye) 
axs[0].plot((oadf2['Time'][assum_I0:fitto])*1E6-0.7,          
          expo(oadf2['Time'][0:(fitto-assum_I0)], *popt), 'r--', linewidth=3,
          label = 'Fitting OADFA')# (\u03B8 = '+ str(round(popt[1]*1E6, 2))+' \u03BCs)')
axs[0].set_xlim(-0.40, 9.2)
axs[0].set_ylim(-0.2, 0.4)
axs[0].set_ylabel('Anisotropy',fontsize=12)
axs[0].legend(loc='upper right')
## add text to plot shows the diameter of particle
# plt.text(4.9,0.25,'Diameter = '+str(round(diameter, 1))+' \u00B1 '+str(round(dia_error,1))+' nm', 
#          fontsize=10, bbox = dict(facecolor = 'limegreen', alpha = 0.5)) # alpha control the transparency
# plot1 = plt.gcf()
# plt.show()

## residuals plot
# fig, axs = plt.subplots(2, 2, figsize=(15, 15))
axs[1].plot(oadf2['Time']*2E6-2, [0 for i in range(len(oadf2['Time']))], color = 'gray')
axs[1].scatter(oadf2['Time'][fitfrom:fitto]*1E6-0.7, 
               residuals['y_data']-residuals['y_pred'], label = 'Residuals')
axs[1].set_xlim(-0.40, 9.2)
axs[1].set_ylim(-0.2, 0.2)
axs[1].set_xlabel('Time (\u03BCs)',fontsize=12)
axs[1].set_ylabel('Residuals')
plt.show()


## Standard deviation of fitting value
print('r0 =', round(popt[0], 3),'\u00B1',round(p_sigma[0],3))  
print('\u03B8 =', round(popt[1]*1E6, 3),'\u00B1',round(p_sigma[1]*1E6,3), '\u03BCs')
print('diameter = ', round(diameter, 2) ,'\u00B1',round(dia_error,2) ,'nm')  
print('Rebinning by two')
print('OADFA tail matching:', round(sum(OadFA[fitto-10:fitto])/10,6), '(G=', Gfactor, ')')

plt.plot(oadf2['Time'][:510]*1E6-0.7, oadf2['VV'][:510], label = 'I$_\parallel$')
plt.plot(oadf2['Time'][:510]*1E6-0.7, Gfactor*oadf2['VH'][:510], label = 'I$_\perp$')
plt.xlabel('Time (\u03BCs)',fontsize=12)
plt.ylabel('Counts',fontsize=12)
plt.xlim(-0.40, 9.2)
plt.ylim(-5, max(oadf2['VV'])/50)
plt.legend()
# plt.yscale("log",base = 10)
plot2 = plt.gcf()
plt.show()


# In[] Save raw data in one csv file
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import xlsxwriter

root = tk.Tk()
root.withdraw()
file_path = askdirectory()
os.chdir(file_path)

writer_VV = pd.concat([timebin, LifetimeVV], axis=1).set_index("Time")
writer_VH = pd.concat([timebin, LifetimeVH], axis=1).set_index("Time")
writer_OADFA = pd.DataFrame({'Time': timebin*1E6, 'VV': 0, 
                             'VH': 0, 'VH*G': 0, 'OADFA': 0}).set_index("Time")


## Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(file_name.split('VH')[0]+'all).xlsx', engine='xlsxwriter')

## Convert the dataframe to an XlsxWriter Excel object.
writer_OADFA.to_excel(writer, sheet_name='OADFA')
writer_VV.to_excel(writer, sheet_name='VV')
writer_VH.to_excel(writer, sheet_name='VH')

## Data analysis in Sheet "OADFA"
writer.sheets['OADFA'].write(0, 6, 'G factor')
writer.sheets['OADFA'].write(1, 6, '=OADFA!$G4')
writer.sheets['OADFA'].write(2, 6, 'Auto G')
writer.sheets['OADFA'].write(3, 6, '=Sum(B'+str(len(timebin)-15)+':B'+str(len(timebin)-1)
                             +')/Sum(C'+str(len(timebin)-15)+':C'+str(len(timebin)-1)+')')
for i in range(len(timebin)):
    num = str(i+2)
    writer.sheets['OADFA'].write(i+1, 1, '=SUM(VV!B'+ num +':K'+ num +')')
    writer.sheets['OADFA'].write(i+1, 2, '=SUM(VH!B'+ num +':K'+ num +')')
    writer.sheets['OADFA'].write(i+1, 3, '=C'+ num +'*$G$2')
    writer.sheets['OADFA'].write(i+1, 4, '=(B'+ num +'-D'+ num +')/(B' + num +'+D'+ num +')')
## Plot of VV and VH
chart1 = writer.book.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
chart1.add_series({
    'name':       '=OADFA!$B1',
    'categories': '=OADFA!$A2:$A'+str(len(timebin)+1),
    'values':     '=OADFA!$B2:$B'+str(len(timebin)+1)})
chart1.add_series({
    'name':       '=OADFA!$D1',
    'categories': '=OADFA!$A2:$A'+str(len(timebin)+1),
    'values':     '=OADFA!$D2:$D'+str(len(timebin)+1)})
chart1.set_y_axis({'min': 0, 'max': 1000})
writer.sheets['OADFA'].insert_chart('H1', chart1)
## Plot of OADFA
chart2 = writer.book.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
chart2.add_series({
    'name':       '=OADFA!$E1',
    'categories': '=OADFA!$A2:$A'+str(len(timebin)+1),
    'values':     '=OADFA!$E2:$E'+str(len(timebin)+1)})
chart2.set_y_axis({'min': -0.4, 'max': 0.6})
writer.sheets['OADFA'].insert_chart('H16', chart2)

## writer.save()
writer.close() # Save and close the xlsx file