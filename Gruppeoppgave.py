#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:01:35 2024

@author: sara
"""

#En del av oppgave g)
import datetime
import matplotlib.pyplot as plt

#Lager et funksjon for å finne et glidende gjennomsnitt for et gitt temperatur-datasett over en spesifikk tidsperiode
def glidende_gjennomsnitt(tid, temperatur, n):
    gyldige_tider = []
    gjennomsnitt =[]

    for i in range(n, len(temperatur)-n):
        temp_slice = temperatur[i - n:i + n + 1]
        gjennomsnitt_verdi = sum(temp_slice) / len(temp_slice)

        gyldige_tider.append(tid[i])
        gjennomsnitt.append(gjennomsnitt_verdi)

    return gyldige_tider, gjennomsnitt

#Oppgave e)
# Initialiser lister for hver kolonne i filene
lufttemperatur_met = []
tid_met = []
lufttrykk_met = []
lufttemperatur= []
tid= []
temperatur = []
tid_bar = []
trykk_abs = []
trykk_bar=[]

# Fyll listene for fil1
with open("temperatur_trykk_met_samme_rune_time_datasett.csv.txt", "r") as fil: #Åpner og leser av fil
    for linje in fil:
        data = linje.strip().split(";")
        if len(data)>=5:
            tiden=data[2]  
            temperaturen= data[3].replace(',', '.')
            trykk= data[4].replace(",",".")
            try:
                if "am" in tiden or "pm" in tiden:      #Tar hensyn til pm og am
                    dato_obj = datetime.datetime.strptime(tiden, "%d/%m/%Y %I:%M:%S %p") 
                else:
                    dato_obj = datetime.datetime.strptime(tiden, "%d.%m.%Y %H:%M")
                
                tid_standard = dato_obj.strftime("%Y-%m-%d %H:%M:%S")
                lufttemperatur_float= float(temperaturen)
                lufttrykk_float= float(trykk)
                tid_met.append(tid_standard)
                lufttemperatur_met.append(lufttemperatur_float)
                lufttrykk_met.append(lufttrykk_float)
            except ValueError:
                pass

# Fyll listene for fil2
with open("trykk_og_temperaturlogg_rune_time.csv.txt", "r") as fil:
    for linje in fil:
        data = linje.strip().split(";")
        if len(data) >= 5:
            # Hent dato og tid
            tiden=data[0]
            # Hent verdier og erstatt komma med punktum
            trykk_baro= data[2].replace(",", ".")
            trykk_abso= data[3].replace(",", ".")
            temperaturen= data[4].replace(",", ".")
        
        # Sjekk om barometertrykk er en tom streng
            if trykk_baro == (''):
                try:
                   if "am" in tiden or "pm" in tiden:    #Tar hensyn til pm og am
                       if " 00:" in tiden:
                           tiden = tiden.replace("00:", "12:", 1)
                       dato_obj = datetime.datetime.strptime(tiden, "%m/%d/%Y %I:%M:%S %p")
                   else:
                       dato_obj = datetime.datetime.strptime(tiden, "%m.%d.%Y %H:%M")
                   
                   tid_standard = dato_obj.strftime("%Y-%m-%d %H:%M:%S")
                   temperatur_float = float(temperaturen)
                   trykk_abs_float = float(trykk_abso) * 10
                   
                   tid.append(tid_standard)
                   temperatur.append(temperatur_float)
                   trykk_abs.append(trykk_abs_float)
                except ValueError:
                    pass
            else:
                try:
                    if "am" in tiden or "pm" in tiden:      #Tar hensyn til pm og am
                       if " 00:" in tiden:
                           tiden = tiden.replace("00:", "12:", 1)
                       dato_obj = datetime.datetime.strptime(tiden, "%m/%d/%Y %I:%M:%S %p")
                    else:
                       dato_obj = datetime.datetime.strptime(tiden, "%m.%d.%Y %H:%M")
                   
                    tid_standard = dato_obj.strftime("%Y-%m-%d %H:%M:%S")
                    temperatur_float=float(temperaturen)
                    trykk_abs_float=float(trykk_abso)*10
                    trykk_bar_float=float(trykk_baro)*10
                   
                    trykk_bar.append(trykk_bar_float)
                    tid_bar.append(tid_standard)
                    tid.append(tid_standard)
                    temperatur.append(temperatur_float)
                    trykk_abs.append(trykk_abs_float)
                except ValueError:
                # Hopp over linjer som ikke kan konverteres til float
                    pass
tider_met_dt = [datetime.datetime.strptime(tiden, "%Y-%m-%d %H:%M:%S") for tiden in tid_met]
tider_dt = [datetime.datetime.strptime(tiden, "%Y-%m-%d %H:%M:%S") for tiden in tid]
tider_baro_dt = [datetime.datetime.strptime(tiden, "%Y-%m-%d %H:%M:%S") for tiden in tid_bar]

#Bruker funksjon laget for oppgave g)
n=30
gyldige_tider, gjennomsnitt = glidende_gjennomsnitt(tider_dt, temperatur, n)

#En del av oppgave h)
start_tid = datetime.datetime(2021, 6, 11, 17, 31)
slutt_tid = datetime.datetime(2021, 6, 12, 3, 5)

temperaturer_uis_filtered = []
tider_uis_filtered = []

for tiden, temperaturen in zip(tider_dt, temperatur):
    if start_tid <= tiden <= slutt_tid:
        tider_uis_filtered.append(tiden)
        temperaturer_uis_filtered.append(temperaturen)

if temperaturer_uis_filtered:
    max_temp = max(temperaturer_uis_filtered)
    min_temp = min(temperaturer_uis_filtered)

    temperaturfall_tider = [start_tid, slutt_tid]
    temperaturfall_values = [max_temp, min_temp]
else:
    temperaturfall_tider = []
    temperaturfall_values = []

#Oppgave f), g), h) og i)
# Plotting
plt.plot(tider_met_dt, lufttemperatur_met, label="Meterologisk")
plt.plot(tider_dt, temperatur, label="UiS")
plt.plot(gyldige_tider, gjennomsnitt, label="Gjennomsnittstemperatur")
plt.plot(temperaturfall_tider, temperaturfall_values, label="Temperaturfall Maksimal til Minimal")
plt.xlabel("Tid")
plt.ylabel("Temperatur")
plt.legend()
plt.show()

plt.plot(tider_met_dt, lufttrykk_met, label = "Absoluttrykk MET")
plt.plot(tider_dt, trykk_abs, label = "Absoluttrykk")
plt.plot(tider_baro_dt, trykk_bar, label = "Barometrisk trykk")
plt.xlabel("Tid")
plt.ylabel("Trykk")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()













