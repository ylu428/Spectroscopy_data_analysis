# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 23:38:56 2019

@author: Yi-Han

Analyze and plot the steady state FA spectrum measured by fluorometer 
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
# In[]
''' load emmision spectrum'''
root = tk.Tk()
root.withdraw()
file_name_em = filedialog.askopenfilename()
Exat630em_c = pd.read_csv(file_name_em, sep=",", header=0) #read file with tab-delimited, assign column names

Exat630em_c = Exat630em_c.loc[ Exat630em_c.index[Exat630em_c['Wavelength(nm)']>0] ]

root = tk.Tk()
root.withdraw()
file_name_em = filedialog.askopenfilename()
Emat565ex_c = pd.read_csv(file_name_em, sep=",", header=0) #read file with tab-delimited, assign column names

Emat565ex_c = Emat565ex_c.loc[ Emat565ex_c.index[Emat565ex_c['Wavelength(nm)']>0] ]
# In[]
name="AgNC fluorometer FA spectrum"

VVex, = plt.plot(Exat630em_c['Wavelength(nm)'], Exat630em_c['Intensity'],'limegreen')
VHex, = plt.plot(Exat630em_c['Wavelength(nm).3'], Exat630em_c['Intensity.3'],'r')

VVem, = plt.plot(Emat565ex_c['Wavelength(nm)'][11:], Emat565ex_c['Intensity'][11:], 'g--')
VHem, = plt.plot(Emat565ex_c['Wavelength(nm).3'][11:], Emat565ex_c['Intensity.3'][11:],'--', color='firebrick')

plt.title(name, fontsize=18)
plt.xlabel('Wavelength (nm)', fontsize=15)
plt.ylabel('Intensity', fontsize=15)
plt.ylim(150, 730)
plt.legend(handles=[VVex, VHex], labels=['Ipara', 'Iperp'])

plt.tight_layout()
temp = plt.gcf()

# In[]
'''Save figure'''
root = tk.Tk()
root.withdraw()

file_path = askdirectory()
os.chdir(file_path)
temp.savefig(name+ '-2.jpg',dpi=600)

# In[]

rex = (Exat630em_c['Intensity']-Exat630em_c['Intensity.1']/Exat630em_c['Intensity.2']*Exat630em_c['Intensity.3'])/(Exat630em_c['Intensity']+2*Exat630em_c['Intensity.1']/Exat630em_c['Intensity.2']*Exat630em_c['Intensity.3'])
rem = (Emat565ex_c['Intensity']-Emat565ex_c['Intensity.1']/Emat565ex_c['Intensity.2']*Emat565ex_c['Intensity.3'])/(Emat565ex_c['Intensity']+2*Emat565ex_c['Intensity.1']/Emat565ex_c['Intensity.2']*Emat565ex_c['Intensity.3'])

Excitation = plt.scatter(Exat630em_c['Wavelength(nm)'], rex)
Emission = plt.scatter(Emat565ex_c['Wavelength(nm)'][11:], rem[11:])

plt.title("Steady State Anisotropy", fontsize=18)
plt.xlabel('Wavelength (nm)', fontsize=15)
plt.ylabel('Anisotropy', fontsize=15)
plt.ylim(-0.0, 0.4)
plt.legend(labels=['Excitation', 'Emission'])
plt.tight_layout()
temp = plt.gcf()

'''Save figure'''
root = tk.Tk()
root.withdraw()

file_path = askdirectory()
os.chdir(file_path)
temp.savefig("Steady state anisotropy-2.jpg",dpi=600)

# In[] Loading data (Could load multiple files in the same diractory)
root = tk.Tk()
root.withdraw()
file_1 = filedialog.askopenfilenames(title = 'Select all Exs')
file_2 = filedialog.askopenfilenames(title = 'Select all Ems')  # filedialog.askopenfilename"s" allow tkinter to import multiple files at once

# extract filename
# file_name = os.path.basename(file_2) => this method will also give file extensions.
file_name = os.path.splitext(file_2[0])[0].split('/')[-1]

###
# read the file and remove non-data part
Wavelength_ex = pd.read_csv(file_1[0], sep="\t", header=None, names=['nm','Int'])
Wavelength_ex = Wavelength_ex['nm'].loc[ Wavelength_ex.index[Wavelength_ex['nm']>0] ]  #remove non-data part

Wavelength_em = pd.read_csv(file_2[0], sep="\t", header=None, names=['nm','Int'])
Wavelength_em = Wavelength_em['nm'].loc[ Wavelength_em.index[Wavelength_em['nm']>0] ]  #remove non-data part


Int_ex = pd.DataFrame()
Int_em = pd.DataFrame()


for i in range(len(file_1)):
    temp_name = file_1[i].split('(')[-1].split(')')[0]
    temp = pd.read_csv(file_1[i], sep="\t", header=None, names=['nm',temp_name+'ex'])[temp_name+'ex'] # read the file.csv
    temp = temp.loc[temp.index[temp>0] ]
    Int_ex = pd.concat([Int_ex, temp], axis=1)
for i in range(len(file_2)):
    temp_name = file_2[i].split('(')[-1].split(')')[0]
    temp = pd.read_csv(file_2[i], sep="\t", header=None, names=['nm',temp_name+'em'])[temp_name+'em'] # read the file.csv
    temp = temp.loc[temp.index[temp>0] ]
    Int_em = pd.concat([Int_em, temp], axis=1)

r_ex = (Int_ex['VVex']-Int_ex['VHex']*Int_ex['HVex']/Int_ex['HHex'])/(Int_ex['VVex']+2*Int_ex['VHex']*Int_ex['HVex']/Int_ex['HHex']) 
r_em = (Int_em['VVem']-Int_em['VHem']*Int_em['HVem']/Int_em['HHem'])/(Int_em['VVem']+2*Int_em['VHem']*Int_em['HVem']/Int_em['HHem'])

Excitation = plt.scatter(Wavelength_ex, r_ex)
Emission = plt.scatter(Wavelength_em, r_em)

plt.title("Steady State Anisotropy", fontsize=18)
plt.xlabel('Wavelength (nm)', fontsize=15)
plt.ylabel('Anisotropy', fontsize=15)
plt.ylim(-0.0, 0.4)
plt.legend(labels=['Excitation', 'Emission'])
plt.tight_layout()
temp = plt.gcf()

'''Save figure'''
root = tk.Tk()
root.withdraw()

file_path = askdirectory()
os.chdir(file_path)
temp.savefig("Steady state anisotropy-2.jpg",dpi=600)