# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 21:59:16 2020

@author: Yi-Han
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog

# B_state = ['disable', 'disable', 'disable', 'disable']

def select1():
    global files, input_name, Button_plot
    file_ = filedialog.askopenfilename()
    files[0].set(file_)
    Button_plot =tk.Button(root, text = "plot", command = plot_curve).place(x = 537, y = 205) # enable this function after the file is selected

def select2():
    file_ = filedialog.askopenfilename()
    files[1].set(file_)

def select3():
    file_ = filedialog.askopenfilename()
    files[2].set(file_)

def select4():
    file_ = filedialog.askopenfilename()
    files[3].set(file_)
        
def plot_curve():#xmin, xmax, ins_xmin,ins_xmax, ymin, ymax, ins_ymin, ins_ymax):
    global plot_title, xmin, xmax, ins_xmin, ins_xmax, ymin, ymax, ins_ymin, ins_ymax
    global plot1
    global cStatus
# load data    
    plot_title = input_name.get()  # get this info from string variable
    xrange = [xmin.get(), xmax.get(), ins_xmin.get(), ins_xmax.get()] # get xlim for main plot and inset plot
    yrange = [ymin.get(), ymax.get(), ins_ymin.get(), ins_ymax.get()] # get xlim for main plot and inset plot
    cStatus = [CB_vars[0].get(), CB_vars[1].get(), CB_vars[2].get(), CB_vars[3].get(), CB_vars[4].get()]
    for i in range(4):
        if cStatus[i]==1:
            tempCurve = pd.read_csv(files[i].get(), sep="\t", header=1, names=['Time','Int']) # read the file as .csv
            plt.plot(tempCurve['Time']*1E6, tempCurve['Int'], label = CurNames[i].get())

    if xrange[1] != "max":
        plt.xlim(float(xrange[0]), float(xrange[1]))
    if yrange[1] != "max":
        plt.ylim(float(yrange[0]), float(yrange[1]))    # let y axis stop at assigned value
    plt.xlabel('Time ('+ r'$\mu$' + 's)', fontsize=12)
    plt.ylabel('Photon Counts', fontsize=12)
    plt.title(plot_title, fontsize=16) # Use the file name as the title. Delete the path
    plt.legend(fontsize=8, loc='upper right')
    # add inset plot for zoomed-in curve
    if cStatus[4] ==1:
        plt.axes([.63, .25, .25, .35], facecolor='floralwhite') #add inset plot
        for i in range(4):
            if cStatus[i]==1:
                tempCurve = pd.read_csv(files[i].get(), sep="\t", header=1, names=['Time','Int']) # read the file as .csv
                plt.plot(tempCurve['Time']*1E6, tempCurve['Int'], label = CurNames[i].get())
        plt.xlim(float(xrange[2]),float(xrange[3]))
        plt.ylim(float(yrange[2]),float(yrange[3]))
        plt.tick_params(axis='both', which='major', labelsize=8)

    plot1 = plt.gcf()
    plt.show()
    
    global Button_save
    Button_save =tk.Button(root, text = "Save plot", command = saveplot).place(x = 574, y = 205) # enable this function after the data is plotted

    global Button_close
    Button_close =tk.Button(root, text = "Close", command = close).place(x = 640, y = 205) # enable this function after the data is plotted
    
    global canvas
    canvas= tk.Tk()
    bar1 = FigureCanvasTkAgg(plot1, canvas)
    bar1.get_tk_widget().pack()
    canvas.mainloop()

    

           
def saveplot():

    path1 = askdirectory()
    os.chdir(path1)
    plot1.savefig(plot_title + '.png',dpi=300,bbox_inches='tight')
    canvas.destroy()

def close():
    
#    canvas.destroy()
    root.destroy()  # close the window
    root.quit()


root = tk.Tk()
root.title('Plot timetrace from NI board')
root.geometry('700x250')

files = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
CurNames = [tk.StringVar(root, value='Pri Only'), tk.StringVar(root, value='OADF'), 
            tk.StringVar(), tk.StringVar()]
CB_vars = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]

input_name = tk.StringVar()
input_name.set('')

# Default values
xmin = tk.StringVar(root, value='0')
xmax = tk.StringVar(root, value='max')
ins_xmin = tk.StringVar(root, value='1')
ins_xmax = tk.StringVar(root, value='2')
###
ymin = tk.StringVar(root, value='0')
ymax = tk.StringVar(root, value='max')
ins_ymin = tk.StringVar(root, value='-10')
ins_ymax = tk.StringVar(root, value='150')


# Type title for plot and name 
Label_title = tk.Label(root,text = "Plot title:").place(x = 20, y = 20)
Entry_title = tk.Entry(root, textvariable = input_name, width =40).place(x = 80, y = 20)

# Select a file for first curve
c1 = tk.Checkbutton(root, text='Data1',variable=CB_vars[0], onvalue=1, offvalue=0)
c1.place(x = 20, y = 45)
Entry_sel1 = tk.Entry(root, textvariable = files[0], width =60).place(x = 80, y = 45)
Button_sel1 =tk.Button(root, text = "select", command = select1).place(x = 450, y = 40)
Label_sel1a = tk.Label(root,text = "Curve name 1:").place(x = 500, y = 45)
Entry_sel1a = tk.Entry(root, textvariable = CurNames[0], width =15).place(x = 600, y = 45)

# Select a file for second curve
c2 = tk.Checkbutton(root, text='Data2',variable=CB_vars[1], onvalue=1, offvalue=0)
c2.place(x = 20, y = 70)
Entry_sel2 = tk.Entry(root, textvariable = files[1], width =60).place(x = 80, y = 70)
Button_sel2 =tk.Button(root, text = "select", command = select2).place(x = 450, y = 65)
Label_sel2a = tk.Label(root,text = "Curve name 2:").place(x = 500, y = 70)
Entry_sel2a = tk.Entry(root, textvariable = CurNames[1], width =15).place(x = 600, y = 70)

# Select a file for third curve
c3 = tk.Checkbutton(root, text='Data3',variable=CB_vars[2], onvalue=1, offvalue=0)
c3.place(x = 20, y = 95)
Entry_sel3 = tk.Entry(root, textvariable = files[2], width =60).place(x = 80, y = 95)
Button_sel3 =tk.Button(root, text = "select", command = select3).place(x = 450, y = 90)
Label_sel3a = tk.Label(root,text = "Curve name 3:").place(x = 500, y = 95)
Entry_sel3a = tk.Entry(root, textvariable = CurNames[2], width =15).place(x = 600, y = 95)

# Select a file for forth curve
c4 = tk.Checkbutton(root, text='Data4',variable=CB_vars[3], onvalue=1, offvalue=0)
c4.place(x = 20, y = 120)
Entry_sel4 = tk.Entry(root, textvariable = files[3], width =60).place(x = 80, y = 120)
Button_sel4 =tk.Button(root, text = "select", command = select4).place(x = 450, y = 115)
Label_sel4a = tk.Label(root,text = "Curve name 4:").place(x = 500, y = 120)
Entry_sel4a = tk.Entry(root, textvariable = CurNames[3], width =15).place(x = 600, y = 120)

# Enter X/Y axis range
Label_plotpara = tk.Label(root,text = "Plot parameters:").place(x = 20, y = 160)
cInset = tk.Checkbutton(root, text='Inset',variable=CB_vars[4], onvalue=1, offvalue=0)
cInset.place(x = 250, y = 160)
    # X range for main plot    
Label_x_min = tk.Label(root,text = "X-axis from:").place(x = 30, y = 185)
Entry_x_min = tk.Entry(root, textvariable = xmin, width =5).place(x = 105, y = 185)
Label_x_max = tk.Label(root,text = "to:").place(x = 145, y = 185)
Entry_x_min = tk.Entry(root, textvariable = xmax, width =5).place(x = 165, y = 185)
    # X range for inset plot
Label_ins_xmin = tk.Label(root,text = "Inset X-axis from:").place(x = 250, y = 185)
Entry_ins_xmin = tk.Entry(root, textvariable = ins_xmin, width =5).place(x = 350, y = 185)
Label_ins_xmax = tk.Label(root,text = "to:").place(x = 390, y = 185)
Entry_ins_xmax = tk.Entry(root, textvariable = ins_xmax, width =5).place(x = 410, y = 185)
    # Y range for main plot    
Label_x_min = tk.Label(root,text = "Y-axis from:").place(x = 30, y = 210)
Entry_x_min = tk.Entry(root, textvariable = ymin, width =5).place(x = 105, y = 210)
Label_x_max = tk.Label(root,text = "to:").place(x = 145, y = 210)
Entry_x_min = tk.Entry(root, textvariable = ymax, width =5).place(x = 165, y = 210)
    # Y range for inset plot
Label_ins_xmin = tk.Label(root,text = "Inset Y-axis from:").place(x = 250, y = 210)
Entry_ins_xmin = tk.Entry(root, textvariable = ins_ymin, width =5).place(x = 350, y = 210)
Label_insx_max = tk.Label(root,text = "to:").place(x = 390, y = 210)
Entry_insx_max = tk.Entry(root, textvariable = ins_ymax, width =5).place(x = 410, y = 210)

Button_plot =tk.Button(root, text = "plot", command = plot_curve, state= "disabled").place(x = 537, y = 205)
Button_save =tk.Button(root, text = "Save plot", command = saveplot, state= "disabled").place(x = 574, y = 205)
Button_close =tk.Button(root, text = "Close", command = close, state= "disabled").place(x = 640, y = 205)

c1.select()
c2.select()
cInset.select()

root.mainloop()

del files, input_name, xmin, xmax, ins_xmin, ins_xmax, ymin, ymax, ins_ymin, ins_ymax

# In[] Lifetime fitting

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog
from scipy.optimize import curve_fit

root = tk.Tk()
root.withdraw()
file_name = filedialog.askopenfilename()
###
# read and analize the data 
Lifetime1 = pd.read_csv(file_name, sep="\t", header=1, names=['Time','Int']) # read the file as .csv
Count = Lifetime1['Int'] #adjust the value to microsecond scale

fit_from = 50
fit_to = 1000

oadf = pd.DataFrame(data = {'Time':Lifetime1['Time'][fit_from:fit_to]-Lifetime1['Time'][fit_from], 'decay': Count[fit_from:fit_to]},dtype=float)


## In[] define function BIC and BIC analysis

def BIC(y, yhat, k, weight = 1):    # y = raw data; yhat = fitting model;k = number of parameters; n = number of data points; sigma= standard deviation of the error
    err = y - yhat
    sigma = np.std(np.real(err))
    n = len(y)
    BI = n*np.log(sigma**2) + weight*k*np.log(n)
    return BI


'''=====================================================
============= Multi-exponential equation ===============
====================================================='''

def expo1(x, A, k, y0):
    return A * np.exp(-x/k) + y0 # exponatial fitting

def expo2(x, A, k, A2, k2, y0):
    return A * np.exp(-x/k) + A2 * np.exp(-x/k2)+ y0 # exponatial fitting

def expo3(x, A, k, A2, k2, A3, k3, y0):
    return A * np.exp(-x/k) + A2 * np.exp(-x/k2) + A3 * np.exp(-x/k3)+ y0 # exponatial fitting

def expo4(x, A, k, A2, k2, A3, k3, A4, k4, y0):
    return A * np.exp(-x/k) + A2 * np.exp(-x/k2) + A3 * np.exp(-x/k3)+ y0 # exponatial fitting


popt1, pcov1 = curve_fit(expo1, oadf['Time'], oadf['decay'], 
                         bounds=(0,[max(oadf['decay'])*2,100,50]))
popt2, pcov2 = curve_fit(expo2, oadf['Time'], oadf['decay'], 
                         bounds=([max(oadf['decay'])/3,0,max(oadf['decay'])/5,0,0],[max(oadf['decay'])*2,1,max(oadf['decay'])*2,1,50]))
popt3, pcov3 = curve_fit(expo3, oadf['Time'], oadf['decay'], 
                         bounds=([max(oadf['decay'])/3,0,max(oadf['decay'])/5,0,0,0,0],[max(oadf['decay'])*2,1,max(oadf['decay'])*2,1,max(oadf['decay'])*2,1,50]))
popt4, pcov4 = curve_fit(expo4, oadf['Time'], oadf['decay'], 
                         bounds=([max(oadf['decay'])/3,0,max(oadf['decay'])/5,0,0,0,0,0,0],[max(oadf['decay'])*2,1,max(oadf['decay'])*2,1,max(oadf['decay'])*2,1,max(oadf['decay'])*2,1,50]))
expofit = [expo1(oadf['Time'], *popt1), expo2(oadf['Time'], *popt2), 
           expo3(oadf['Time'], *popt3), expo4(oadf['Time'], *popt4)]
popt = [popt1, popt2, popt3, popt4]
pcov = [pcov1, pcov2, pcov3, pcov4]

BIC_result = []
plt.plot(oadf['Time']*10**6, oadf['decay'], label='raw data')
for i in range(4):
    BI = BIC(oadf['decay'], expofit[i], 2*i+3)
    BIC_result.append(BI)
    plt.plot(oadf['Time']*10**6, expofit[i], label ='expo '+str(i+1))
plt.legend()
plt.xlabel('Time ('+ r'$\mu$' + 's)', fontsize=14)
plt.ylabel('Photon Counts', fontsize=14)
plt.title('AgNC 630 emitter: OADF',fontsize=18)
plot1 = plt.Figure()
plot1.set_canvas(plt.gcf().canvas)
plt.show()

# BIC analysis
plt.plot(range(1,5),BIC_result,'o-')
plt.title('BIC analysis',fontsize=18)
plt.xlabel('expoential')
plt.ylabel('BIC value')
plot2 = plt.Figure()
plot2.set_canvas(plt.gcf().canvas)

paras = pd.DataFrame()
for i in range(4):
    temp = pd.DataFrame({'popt'+str(i+1):popt[i]})
    paras=pd.concat((paras,temp), axis=1)
    
print(paras)

# In[] Save OADF decay and BIC result
intensity = 47904
file_path = askdirectory()
os.chdir(file_path)
plot1.savefig('OADF of '+ str(intensity) +'W sec_laser.png',dpi=600, bbox_inches='tight')
plot2.savefig('BIC analysis of '+ str(intensity) +'W sec_laser.png',dpi=600, bbox_inches='tight')

paras.to_csv('Fitting paras of '+ str(intensity) +'W sec_laser.csv')

# In[] Collect all of the lifetime data and put into one file

root = tk.Tk()
root.withdraw()

file_path = askdirectory()
inten = []
All_files=pd.DataFrame({'component': ['A1', 'exp1', 'A2', 'exp2', 'y0', 'intensity(W)', 'k1', 'k2']})
for file in os.listdir(file_path):
    if file.endswith(".csv"):
        path = file_path+"/"+file
        name = str(file)
        temp_inten = ''.join([n for n in name if n.isdigit()]) #extract digit
        inten.append(int(temp_inten))
#        file_element = os.path.splitext(file)[0].split('-')[-1]
        a = pd.read_csv(path, header=0, names=["component", temp_inten +" W-1", temp_inten +" W-2", temp_inten +" W-3", temp_inten +" W-4"])#.apply(pd.to_numeric)
        All_files = pd.concat([All_files,a[temp_inten +" W-2"]],axis=1).iloc[0:8]
        print(os.path.join(file))

All_files = All_files.set_index('component')
All_files.loc['intensity(W)',:] = inten
All_files.loc['k1',:] = 1/All_files.loc['exp1',:]
All_files.loc['k2',:] = 1/All_files.loc['exp2',:]

All_files = All_files.T
All_files= All_files.set_index('intensity(W)')
os.chdir(file_path)
All_files.to_excel('Biexpo lifetime data_110W(20200814).xlsx', index=True)
#os.path.basename(file_path)

# In[] Collect all of the OADF ratio data and put into one file

root = tk.Tk()
root.withdraw()

file_path = askdirectory()
priinten = []
secinten = []
All_files=pd.DataFrame()
for file in os.listdir(file_path):
    if file.startswith('OADF') & file.endswith(".txt"):
        path = file_path+"/"+file
        name = str(file)
        # find primary intensity from file name
        pri = os.path.splitext(file)[0].split('_')[2] #split text for file names
        pri = ''.join([n for n in pri if n.isdigit()]) #extract digit
        priinten.append(int(pri))
        # find secondary intensity from file name
        sec = os.path.splitext(file)[0].split('_')[-1] #split text for file names
        sec = ''.join([n for n in sec if n.isdigit()]) #extract digit
        secinten.append(int(sec))
        temp_inten = str(pri) + ' W pri + ' + str(sec)  + ' W sec'
        a = pd.read_csv(path, sep="\t", header=0, names=["time", temp_inten +" counts"])#.apply(pd.to_numeric)
        All_files = pd.concat([All_files,a[temp_inten +" counts"]],axis=1).iloc[395:795]
        print(os.path.join(file))

All_files = All_files.reset_index(drop=True)
All_files.loc[400,:] = ' '
All_files.loc['priI',:] = priinten
All_files.loc['secI',:] = secinten
All_files.loc['prompt',:] = All_files.iloc[0:2,:].sum(axis=0)
All_files.loc['OADF',:] = All_files.iloc[3:399,:].sum(axis=0)
All_files.loc['ratio',:] = All_files.iloc[404,:]/All_files.iloc[403,:]
All_files = All_files.sort_values(by=['priI', 'secI'], axis = 1)

os.chdir(file_path)
All_files.to_excel('OADF ratio(20200814).xlsx', index=True)