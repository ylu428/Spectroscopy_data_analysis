# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:05:03 2020

@author: asus
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog

def selectEX():
    file_ = filedialog.askopenfilename()
    fileEx.set(file_)
    global Button3
    Button3 =tk.Button(root, text = "plot", command = plot_curve).grid(row = 3, column = 1) # enable this function after the file is selected

def selectEM():
    file_ = filedialog.askopenfilename()
    fileEm.set(file_)
    global Button3
    Button3 =tk.Button(root, text = "plot", command = plot_curve).grid(row = 3, column = 1) # enable this function after the file is selected

def plot_curve():
    global file_name
    dataEx = fileEx.get()  # get this info from string variable
    dfEx = pd.read_csv(dataEx, sep="\t", header=None, names=['Wavelength','Emission']) #read file with tab-delimited, assign column names
    dfEx = dfEx.iloc[ dfEx.index[dfEx['Wavelength']>0] ]
    #Delete negative wavelength data produced by the fluorometer software.
    dataEm = fileEm.get()  # get this info from string variable
    dfEm = pd.read_csv(dataEm, sep="\t", header=None, names=['Wavelength','Emission']) #read file with tab-delimited, assign column names
    dfEm = dfEm.iloc[ dfEm.index[dfEm['Wavelength']>0] ]
    #Delete negative wavelength data produced by the fluorometer software.
    
    global Dye_name
    Dye_name = input_name.get()
    # plot main plot
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    line1, = ax1.plot(dfEx['Wavelength'][:], dfEx['Emission'][:],'r')
    line2, = ax2.plot(dfEm['Wavelength'][:], dfEm['Emission'][:],'g')
    ax1.set_xlabel('Wavelength (nm)', fontsize=14)
    ax1.set_ylabel('Count', fontsize=14)
    y_lim = max(max(dfEx['Emission']), max(dfEm['Emission']))*1.1
    ax1.set_ylim(0,y_lim)
    ax2.set_ylim(0,y_lim)
    plt.title(Dye_name, fontsize=18)
    plt.legend(handles=[line1, line2], labels=['Excitation', 'Emission'], loc = 0, fontsize=10)
    plt.tight_layout()

    global plot1
    plot1 = plt.gcf()
    
    global Button3
    Button3 =tk.Button(root, text = "Save plot", command = saveplot).grid(row = 3, column = 2) # enable this function after the data is plotted
    
    global canvas
    canvas= tk.Tk()
    bar1 = FigureCanvasTkAgg(plot1, canvas)
    bar1.get_tk_widget().pack()
    canvas.mainloop()
           
def saveplot():

    path1 = askdirectory()
    os.chdir(path1)
    plot1.savefig(Dye_name + '.png',dpi=600,bbox_inches='tight')
    root.destroy()  # close the window
    canvas.destroy()
    root.quit()

root = tk.Tk()
root.title('Plot Spectrum from PTI Fluorometer')
#root.geometry('500x300')
fileEx = tk.StringVar()
fileEm = tk.StringVar()
input_name = tk.StringVar()

Label0 = tk.Label(root,text = "Dye:").grid(row = 0, column = 0)
Entry0 = tk.Entry(root, textvariable = input_name, width =60).grid(row = 0, column = 1)

Label1 = tk.Label(root,text = "Excitation:").grid(row = 1, column = 0)
Entry1 = tk.Entry(root, textvariable = fileEx, width =60).grid(row = 1, column = 1)
Button1 =tk.Button(root, text = "select", command = selectEX).grid(row = 1, column = 2)

Label2 = tk.Label(root,text = "Emission:").grid(row = 2, column = 0)
Entry2 = tk.Entry(root, textvariable = fileEm, width =60).grid(row = 2, column = 1)
Button2 =tk.Button(root, text = "select", command = selectEM).grid(row = 2, column = 2)

Button3 =tk.Button(root, text = "plot", command = plot_curve, state= "disabled").grid(row = 3, column = 1)
Button4 =tk.Button(root, text = "Save plot", state= "disabled", command = saveplot).grid(row = 3, column = 2)
#Button5 =tk.Button(root, text = "Plot & Save", state= "disabled", command = saveplot).grid(row = 2, column = 3)

root.mainloop()
del fileEx, fileEm, input_name

# In[] future work: add a selection list to perform absorbance spectrum plotting

'''material for selection list'''
import tkinter as tk

OptionList = [
"Aries",
"Taurus",
"Gemini",
"Cancer"
] 

app = tk.Tk()

app.geometry('400x70')

variable = tk.StringVar(app)
variable.set(OptionList[0])

opt = tk.OptionMenu(app, variable, *OptionList)
opt.config(width=90, font=('Helvetica', 12))
opt.pack(side="top")

labelTest = tk.Label(text="", font=('Helvetica', 12), fg='red')
labelTest.pack(side="top")

def callback(*args):
    labelTest.configure(text="The selected item is {}".format(variable.get()))

variable.trace("w", callback)

app.mainloop()

'''material for absorbance spectrium'''
root = tk.Tk()
root.withdraw()
absfile = filedialog.askopenfilename()
Abs_c = pd.read_csv(absfile, sep=",", header=1)

NorAbs_c = (Abs_c['Abs.']-Abs_c['Abs.'].min())/(Abs_c['Abs.'].max()-Abs_c['Abs.'].min()) #normalization of absorption
plt.plot(Abs_c['Wavelength nm.'], Abs_c['Abs.'], label = 'absorbance')
plt.xlabel('Wavelength (nm)', fontsize=14)
plt.ylabel('Intensity', fontsize=14)
plt.title('AgNC absorbance', fontsize=18)
#dplt.legend()
fig=plt.gcf()

root = tk.Tk()
root.withdraw()

file_path = askdirectory()
os.chdir(file_path)

fig.savefig('New AgNC Sample absorbance.png',dpi=600, bbox_inches='tight')  


