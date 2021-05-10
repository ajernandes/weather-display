from datetime import datetime
import json
from PIL import ImageTk,Image,ImageEnhance
import requests
import sys
import time
import tkinter as tk
from tkinter.ttk import *
import tkinter.font as font




#Spotsylvania
lat = 38.1979
long = -77.5878


#Purdue
#lat = 40.4237
#long = -86.9212


try:
    infodata = json.loads(requests.get('https://api.weather.gov/points/' + str(lat) + ',' + str(long)).text)
    furl = infodata['properties']['forecast']
    ourl = infodata['properties']['observationStations']
    ourl = json.loads(requests.get(ourl).text)['features'][0]['id'] + '/observations/latest'
except:
    print("Cannot get weather data... Check your connection")
    sys.exit()
    
def reload():
    dtime()
    update()

def close():
    sys.exit()
    
def dtime():
    try:
        ctime = time.strftime('%-I:%M', time.localtime(time.time()))
    except:
        ctime = time.strftime('%I:%M', time.localtime(time.time()))
    cday = time.strftime('%A', time.localtime(time.time()))
    try:
        cdate = time.strftime('%B %-d', time.localtime(time.time()))
    except:
        cdate = time.strftime('%B %d', time.localtime(time.time()))
    
    disptime.config(text = ctime)
    dispday.config(text = cday)
    dispdate.config(text = cdate)
    disptime.after(500, dtime)  

def update():
    def getficon(index):
        if fdata['properties']['periods'][index]['icon'][35:-12].count('/') > 1:
            return(fdata['properties']['periods'][index]['icon'][35:-12].replace('/','               ')[:-15].replace(' ', '').replace(',', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '') + '.png')
        else:
            return(fdata['properties']['periods'][index]['icon'][35:-12].replace('/','').replace(',', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '') + '.png')

    hadProblem = False
    print("Updating")
    try:
        odata = json.loads(requests.get(ourl).text)
    except:
        print("Failed to load current weather data")
        hadProblem = True
    try:
        fdata = json.loads(requests.get(furl).text)
    except:
        print("Failed to load current forecast")
        hadProblem = True
    try:
        ctemp = str(round(odata['properties']['temperature']['value']*1.8+32)) + '°'
        disptemp.configure(text = ctemp)
    except:
        print("Could not update temperature")
        hadProblem = True
    try:
        cwindd = odata['properties']['windDirection']['value']*1
        windd = ImageTk.PhotoImage(Image.open('icons/arrow.png').rotate(-cwindd).resize((100, 100), Image.ANTIALIAS))
        dispcwindd.image = windd  
        dispcwindd.config(image = windd)
    except:
        print("Count not update wind direction")
        hadProblem = True
    try:
        cwinds = str(round(odata['properties']['windSpeed']['value']/1.609,1)) + ' mph'
        dispcwinds.config(text = cwinds)
    except:
        print("Could not update wind speed")
        hadProblem = True
    try:
        cdisc = odata['properties']['textDescription'].title()
        dispcdisc.config(text = cdisc)
    except:
        print("Could not update description")
        hadProblem = True
    try:
        cicon = odata['properties']['icon']
        cicon = ("icons/" + cicon[35:-12] + '.png').replace('/','')
        ico = ImageTk.PhotoImage(Image.open(cicon).resize((200, 200), Image.ANTIALIAS))  
        dispcicon.image = ico
        dispcicon.configure(image = ico)
    except:
        print("Could not update icon")
        hadProblem = True

    try:
        if fdata['properties']['periods'][0]['isDaytime']:
            tmax = str(round(fdata['properties']['periods'][0]['temperature'])) + '°  '
            tmin = str(round(fdata['properties']['periods'][1]['temperature'])) + '°  '
            dispmin.configure(text = tmin)
            dispmax.configure(text = tmax)
            tomorrowStart = 2
        else:
            tmin = str(round(fdata['properties']['periods'][0]['temperature'])) + '°  '
            tmax = 'N/A'
            dispmin.configure(text = tmin)
            tomorrowStart = 1
    except:
        tomorrowStart = 1
        print("Could not update min/max temperature")
        hadProblem = True
    try:
        ficon = [getficon(0),
                 getficon(tomorrowStart),
                 getficon(tomorrowStart + 2),
                 getficon(tomorrowStart + 4),
                 getficon(tomorrowStart + 6),
                 getficon(tomorrowStart + 8),
                 getficon(tomorrowStart + 10)]

        fico0 = ImageTk.PhotoImage(Image.open(ficon[0]).resize((50, 50), Image.ANTIALIAS))
        fico1 = ImageTk.PhotoImage(Image.open(ficon[1]).resize((50, 50), Image.ANTIALIAS))
        fico2 = ImageTk.PhotoImage(Image.open(ficon[2]).resize((50, 50), Image.ANTIALIAS))
        fico3 = ImageTk.PhotoImage(Image.open(ficon[3]).resize((50, 50), Image.ANTIALIAS))
        fico4 = ImageTk.PhotoImage(Image.open(ficon[4]).resize((50, 50), Image.ANTIALIAS))
        fico5 = ImageTk.PhotoImage(Image.open(ficon[5]).resize((50, 50), Image.ANTIALIAS))
        fico6 = ImageTk.PhotoImage(Image.open(ficon[6]).resize((50, 50), Image.ANTIALIAS))

        ficon0.image = fico0
        ficon1.image = fico1
        ficon2.image = fico2
        ficon3.image = fico3
        ficon4.image = fico4
        ficon5.image = fico5
        ficon6.image = fico6

        ficon0.config(image = fico0)
        ficon1.config(image = fico1)
        ficon2.config(image = fico2)
        ficon3.config(image = fico3)
        ficon4.config(image = fico4)
        ficon5.config(image = fico5)
        ficon6.config(image = fico6)
    except:
        print("Could not update forecast icons")
        hadProblem = True

    try:
        fmin = [tmin, 
                str(round(fdata['properties']['periods'][tomorrowStart + 1]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 3]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 5]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 7]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 9]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 11]['temperature'])) + '°']

        fmax = [tmax, 
                str(round(fdata['properties']['periods'][tomorrowStart]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 2]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 4]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 6]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 8]['temperature'])) + '°', 
                str(round(fdata['properties']['periods'][tomorrowStart + 10]['temperature'])) + '°']
                
        ftemp0.config(text = fmax[0] + ', ' + fmin[0])
        ftemp1.config(text = fmax[1] + ', ' + fmin[1])
        ftemp2.config(text = fmax[2] + ', ' + fmin[2])
        ftemp3.config(text = fmax[3] + ', ' + fmin[3])
        ftemp4.config(text = fmax[4] + ', ' + fmin[4])
        ftemp5.config(text = fmax[5] + ', ' + fmin[5])
        ftemp6.config(text = fmax[6] + ', ' + fmin[6])
    except:
        print("Could not update weekly high/low")
        hadProblem = True
    try:
        fday = ['Today',
                'Tomorrow',
                datetime.strftime(datetime.strptime(fdata['properties']['periods'][tomorrowStart + 2]['startTime'], '%Y-%m-%dT%H:%M:%S%z'), '%a'),
                datetime.strftime(datetime.strptime(fdata['properties']['periods'][tomorrowStart + 4]['startTime'], '%Y-%m-%dT%H:%M:%S%z'), '%a'),
                datetime.strftime(datetime.strptime(fdata['properties']['periods'][tomorrowStart + 6]['startTime'], '%Y-%m-%dT%H:%M:%S%z'), '%a'),
                datetime.strftime(datetime.strptime(fdata['properties']['periods'][tomorrowStart + 8]['startTime'], '%Y-%m-%dT%H:%M:%S%z'), '%a'),
                datetime.strftime(datetime.strptime(fdata['properties']['periods'][tomorrowStart + 10]['startTime'], '%Y-%m-%dT%H:%M:%S%z'), '%a')]
        fday0.config(text = fday[0])
        fday1.config(text = fday[1])
        fday2.config(text = fday[2])
        fday3.config(text = fday[3])
        fday4.config(text = fday[4])
        fday5.config(text = fday[5])
        fday6.config(text = fday[6])
    except:
        print("Could not update forecast day of week")
        hadProblem = True

    if hadProblem:
        disptemp.after(10000, update)
    else:
        disptemp.after(600000, update)

window = tk.Tk()
window.attributes('-fullscreen', True)
frameMain = tk.Frame(window, background='black')
frameFC = tk.Frame(window, background = 'black')

frameMain.columnconfigure(0, weight = 1)
frameMain.columnconfigure(1, weight = 1)
frameMain.columnconfigure(2, weight = 1)
frameMain.columnconfigure(3, weight = 1)
frameMain.columnconfigure(4, weight = 1)
frameMain.columnconfigure(5, weight = 1)
frameMain.columnconfigure(6, weight = 1)
frameMain.columnconfigure(7, weight = 1)

frameMain.rowconfigure(0, weight = 1)
frameMain.rowconfigure(1, weight = 1)
frameMain.rowconfigure(2, weight = 1)
frameMain.rowconfigure(3, weight = 1)
frameMain.rowconfigure(4, weight = 1)
frameMain.rowconfigure(5, weight = 1)
frameMain.rowconfigure(6, weight = 1)
frameMain.rowconfigure(7, weight = 1)

frameFC.columnconfigure(0, weight = 1)
frameFC.columnconfigure(1, weight = 1)
frameFC.columnconfigure(2, weight = 1)
frameFC.columnconfigure(3, weight = 1)
frameFC.columnconfigure(4, weight = 1)
frameFC.columnconfigure(5, weight = 1)
frameFC.columnconfigure(6, weight = 1)

frameFC.rowconfigure(0, weight = 1)
frameFC.rowconfigure(1, weight = 1)
frameFC.rowconfigure(2, weight = 1)

disptime = tk.Label(frameMain, font=("Ariel", 60), background = 'black', foreground = "darkgrey")
dispday = tk.Label(frameMain, font=("Ariel", 25), background = 'black', foreground = "darkgrey")
dispdate = tk.Label(frameMain, font=("Ariel", 25), background = 'black', foreground = "darkgrey")
updateData = tk.Button(frameMain, text = 'Update', command = update, background = 'black', foreground = 'darkgrey')

disptemp = tk.Label(frameMain, font=("Ariel",60), background = 'black', foreground = "darkgrey", text = 'N/A')
dispmin = tk.Label(frameMain, font=("Ariel", 20), background = 'black', foreground = "darkgrey", text = 'N/A')
dispmax = tk.Label(frameMain, font=("Ariel", 20), background = 'black', foreground = "darkgrey", text = 'N/A')

dispcicon = tk.Label(frameMain, background = 'black', foreground = "darkgrey")
dispcdisc = tk.Label(frameMain, font=("Ariel", 20), background = 'black', foreground = "darkgrey")

dispcwindd = tk.Label(frameMain, background = 'black', foreground = "darkgrey")
dispcwinds = tk.Label(frameMain, font=("Ariel", 20), background = 'black', foreground = "darkgrey", text = 'Unavaliable')


ficon0 = tk.Label(frameFC, background = 'black', foreground = "darkgrey")
ficon1 = tk.Label(frameFC, background = 'black', foreground = "darkgrey")
ficon2 = tk.Label(frameFC, background = 'black', foreground = "darkgrey")
ficon3 = tk.Label(frameFC, background = 'black', foreground = "darkgrey")
ficon4 = tk.Label(frameFC, background = 'black', foreground = "darkgrey")
ficon5 = tk.Label(frameFC, background = 'black', foreground = "darkgrey")
ficon6 = tk.Label(frameFC, background = 'black', foreground = "darkgrey")

ftemp0 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A, N/A')
ftemp1 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A, N/A')
ftemp2 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A, N/A')
ftemp3 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A, N/A')
ftemp4 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A, N/A')
ftemp5 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A, N/A')
ftemp6 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A, N/A')

fday0 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A')
fday1 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A')
fday2 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A')
fday3 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A')
fday4 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A')
fday5 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A')
fday6 = tk.Label(frameFC, font=("Ariel", 10), background = 'black', foreground = "darkgrey", text = 'N/A')


disptime.grid(row = 0, column = 0, rowspan = 4, columnspan = 4)
dispday.grid(row = 3, column = 0, rowspan = 2, columnspan = 4)
dispdate.grid(row = 4, column = 0, rowspan = 2, columnspan = 4)
updateData.grid(row = 5, column = 0, rowspan = 2, columnspan = 4)

disptemp.grid(row = 0, column = 5, rowspan = 4, columnspan = 2)
dispmax.grid(row = 0, column = 7, rowspan = 1, columnspan = 1)
dispmin.grid(row = 2, column = 7, rowspan = 1, columnspan = 1)

dispcicon.grid(row = 4, column = 4, rowspan = 2, columnspan = 3)
dispcdisc.grid(row = 6, column = 4, rowspan = 1, columnspan = 2)

dispcwindd.grid(row = 4, column = 7, rowspan = 2, columnspan = 1)
dispcwinds.grid(row = 6, column = 7, rowspan = 2, columnspan = 1)

ficon0.grid(row = 0, column = 0)
ficon1.grid(row = 0, column = 1)
ficon2.grid(row = 0, column = 2)
ficon3.grid(row = 0, column = 3)
ficon4.grid(row = 0, column = 4)
ficon5.grid(row = 0, column = 5)
ficon6.grid(row = 0, column = 6)

ftemp0.grid(row = 1, column = 0)
ftemp1.grid(row = 1, column = 1)
ftemp2.grid(row = 1, column = 2)
ftemp3.grid(row = 1, column = 3)
ftemp4.grid(row = 1, column = 4)
ftemp5.grid(row = 1, column = 5)
ftemp6.grid(row = 1, column = 6)

fday0.grid(row = 2, column = 0)
fday1.grid(row = 2, column = 1)
fday2.grid(row = 2, column = 2)
fday3.grid(row = 2, column = 3)
fday4.grid(row = 2, column = 4)
fday5.grid(row = 2, column = 5)
fday6.grid(row = 2, column = 6)

window.config(cursor='none')
#close = tk.Button(window, text = close, command = close).pack()
frameMain.pack(fill = tk.BOTH, side = tk.TOP, expand = True)
frameFC.pack(fill = tk.BOTH, side = tk.BOTTOM, expand = True)

dtime()
update() 
window.mainloop()
