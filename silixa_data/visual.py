# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:17:55 2026

@author: martin.foin
"""
"""
visual.py
------------------------
Module dedicated to Silixa Raman DTS  data visualization 

    """
        
from datetime import datetime
from glob import glob
import re
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os
import pandas as pd
import xml.etree.ElementTree as ET

    
def cmap_visu(A,
              add_ref_temp,diff_ref_temp,plot_title=''):
	"""
	2D plot of temperature over distance and time. possibility to ass ref temperatures and ref temp differentials

	Parameters
	----------
	A : dict
		DICT OBTAINED FROM process_temperature_files
	add_ref_temp : bool
		plot reference temperatures PT100 probes and internal ref   to visual 
	diff_ref_temp : bool
		plot reference temperatures PT100 probes differential   to visual 
	plot_title	: char
		Informations to display on plots
	Returns
	-------
	plots
	"""
	fig, ax1 = plt.subplots(figsize=(16, 8))

	# --- 1. Carte spatio-temporelle (à gauche) ---
	time_nums = mdates.date2num(A['time_vec'])
	im = ax1.imshow(
	    A['temperature'].T,
	    aspect='auto',
	    origin='lower',
	    extent=[
	        A['distance'][0],
	        A['distance'][-1],
	        time_nums[0],
	        time_nums[-1],
	    ],
	    cmap='inferno',
	)

	# Formatage de l'axe y pour les dates
	ax1.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

	# Ajout de la barre de couleur rattachée à ax1
	cb = fig.colorbar(im, ax=ax1) # Optionnel : met la colorbar à gauche de ax1 pour ne pas gêner
	cb.set_label('Temperature (°C)')

	ax1.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
	ax1.set_ylabel('Time', fontsize=12, fontweight='bold')
	ax1.set_title('Spatio temporal temperature map,'+plot_title, fontsize=12, fontweight='bold')

	# plt.tight_layout()
	plt.show()
	
	if add_ref_temp:
		# Création d'une figure avec 2 sous-graphiques partageant le même axe Y (le temps)
		fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), sharey=True)

		# --- 1. Carte spatio-temporelle (à gauche) ---
		time_nums = mdates.date2num(A['time_vec'])
		im = ax1.imshow(
		    A['temperature'].T,
		    aspect='auto',
		    origin='lower',
		    extent=[
		        A['distance'][0],
		        A['distance'][-1],
		        time_nums[0],
		        time_nums[-1],
		    ],
		    cmap='inferno',
		)

		# Formatage de l'axe y pour les dates
		ax1.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

		# Ajout de la barre de couleur rattachée à ax1
		# (Si vous préférez la colorbar à droite de ax1, enlevez location='left')
		cb = plt.colorbar(im)
		cb.set_label('Temperature (°C)')
		ax1.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
		ax1.set_ylabel('Time', fontsize=12, fontweight='bold')
		ax1.set_title('Spatio temporal temperature map,'+plot_title, fontsize=12, fontweight='bold')


		# --- 2. Graphique vertical (à droite) ---
		# Inversion : x = température, y = temps (A['time_vec'])
		ax2.scatter(A['probe1temp'],A['time_vec'] ,c='b',alpha=1,label='PT100 1')
		ax2.scatter( A['probe2temp'],A['time_vec'],c='r',alpha=1,label='PT100 2')
		ax2.scatter( A['internRefTemp'],A['time_vec'],c='g',alpha=1,label='intern ref')
		
		ax2.set_xlabel(' Probes temp  [°C]', fontsize=12, fontweight='bold')
		ax2.grid(True, which='both', ls='--')
		ax2.legend(fontsize=12, framealpha=1)
		ax2.set_title('Reference Temperature evolution,'+plot_title, fontsize=12, fontweight='bold')

		# plt.tight_layout()
		plt.show()


	if diff_ref_temp:
		# Création d'une figure avec 2 sous-graphiques partageant le même axe Y (le temps)
		fig, (ax1, ax2,ax3) = plt.subplots(1, 3, figsize=(18, 8), sharey=True)

		# --- 1. Carte spatio-temporelle (à gauche) ---
		time_nums = mdates.date2num(A['time_vec'])
		im = ax1.imshow(
		    A['temperature'].T,
		    aspect='auto',
		    origin='lower',
		    extent=[
		        A['distance'][0],
		        A['distance'][-1],
		        time_nums[0],
		        time_nums[-1],
		    ],
		    cmap='inferno',
		)

		# Formatage de l'axe y pour les dates
		ax1.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

		# Ajout de la barre de couleur rattachée à ax1
		cb = fig.colorbar(im, ax=ax1) # Optionnel : met la colorbar à gauche de ax1 pour ne pas gêner
		# (Si vous préférez la colorbar à droite de ax1, enlevez location='left')

		ax1.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
		ax1.set_ylabel('Time', fontsize=12, fontweight='bold')
		ax1.set_title('Spatio/temporal temperature \n'+plot_title, fontsize=12, fontweight='bold')


		# --- 2. Graphique vertical (à droite) ---
		# Inversion : x = température, y = temps (A['time_vec'])
		ax2.scatter(A['probe1temp'],A['time_vec'] ,c='b',alpha=1,label='PT100 1')
		ax2.scatter( A['probe2temp'],A['time_vec'],c='r',alpha=1,label='PT100 2')
		ax2.scatter( A['internRefTemp'],A['time_vec'],c='g',alpha=1,label='intern ref')
		ax2.set_xlabel(' Probes temp  [°C]', fontsize=12, fontweight='bold')

		
		ax2.set_xlabel(' Probes temp  [°C]', fontsize=12, fontweight='bold')
		ax2.grid(True, which='both', ls='--')
		ax2.legend(fontsize=12, framealpha=1)
		ax2.set_title('Temperature  evolution \n'+plot_title, fontsize=12, fontweight='bold')
		
		
		ax3.scatter(
		    A['probe1temp'] - A['probe2temp'],
		    A['time_vec'],
		    c='k',
		    alpha=1,s=0.5,
		    label='temp grad',
		)
		ax3.set_xlabel(' Probes temp diff [°C]', fontsize=12, fontweight='bold')
		ax3.grid(True, which='both', ls='--')
		ax3.legend(fontsize=12, framealpha=1)
		ax3.set_title('Temperature differential evolution \n'+plot_title, fontsize=12, fontweight='bold')

		# plt.tight_layout()
		plt.show()


	return

def plotovertime_fixeddist(A,Dist,mean_half,plot_title):
	"""
	Plot evolution of in temperature of a selected distance point through time.

	Parameters
	----------
	A : dict
		DICT OBTAINED FROM process_temperature_files
	Dist : int
		select the distance to plot through time
	mean_half : int
		number of samples to be mean, center is Dist, Dist+-mean_half 
	plot_title	: char
		Informations to display on plots

	Returns
	-------
	plot
	Mean_over_dist : Temperature vector over time
	
	"""
	
	dist_center = np.abs(A['distance'] - Dist).argmin()
	
	
	Mean_over_dist=np.mean(A['temperature'][Dist-mean_half:Dist+mean_half,:],axis=0)
	
	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_subplot(111)
	printdist = f"@:{dist_center:.1f} m"
	ax.plot(A['time_vec'], A['temperature'][Dist,:],c='k',alpha=0.5,label=printdist)
	ax.scatter( A['time_vec'],
	    A['probe1temp'] - A['probe2temp'],
	    c='b',
	    alpha=1,s=0.2,
	    label='temp grad',
	)
	ax.plot(A['time_vec'], Mean_over_dist,c='r',alpha=1,label='meaned')

	ax.set_xlabel('Date', fontsize=16, fontweight='bold')
	ax.set_ylabel('Temperature [°C]', fontsize=16, fontweight='bold')
	plt.title(f"temperature vs time\n; @: {dist_center} ;meaned over {mean_half*(A['distance'][1]-A['distance'][0]):.1f} m\n"+plot_title)
	plt.grid(True, which='both', ls='--')
	plt.legend(fontsize=14, framealpha=1)
	plt.tight_layout()
	plt.show()

	return Mean_over_dist
	
def plot_STD_overtime(A,plot_title):
	"""
	Plot evolution of STD in temperature time.

	Parameters
	----------
	A : dict
		DICT OBTAINED FROM process_temperature_files
	plot_title	: char
		Informations to display on plots
	Returns
	-------
	plot
	 STD_vec: Temperature STD over time
	
	"""
	
	STD_vec=np.std(A['temperature'][:,:],axis=0)

	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_subplot(111)

	ax.plot(A['time_vec'], STD_vec,c='m',alpha=1,label='STD')
	ax.scatter( A['time_vec'],
	    A['probe1temp'] - A['probe2temp'],
	    c='k',
	    alpha=1,s=0.1,
	    label='temp grad',
	)
	ax2=ax.twinx()
	ax2.scatter(A['time_vec'], A['internRefTemp'],c='g',alpha=1,label='intern ref')
	ax2.set_ylabel('Internal Temperature [°C]', fontsize=16, fontweight='bold')

	ax.set_xlabel('Date', fontsize=16, fontweight='bold')
	ax.set_ylabel('STD and Differential probes Temperature [°C]', fontsize=16, fontweight='bold')
	plt.title("STD temperature vs time \n"+plot_title)
	plt.grid(True, which='both', ls='--')
	plt.legend(fontsize=14, framealpha=1)
	plt.tight_layout()
	plt.show()

	return STD_vec


def plotoverdist_fixedtime(A,Time_center,mean_half,plot_title):
	"""
	Plot evolution of in temperature of a selected distance point through time.

	Parameters
	----------
	A : dict
		DICT OBTAINED FROM process_temperature_files
	Time : 
		select the date to plot through distance. or the measurement number over time
		
	mean_half : int
		number of samples to be mean, Time+-mean_half
	plot_title	: char
		Informations to display on plots

	Returns 
	-------
	plot
	"""
	
	if isinstance(Time_center, int)==False:
		Time_center = np.abs(A['time_vec'] - Time_center).argmin()

	
	
	print(Time_center)
	Mean_over_time=np.mean(A['temperature'][:,Time_center-mean_half:Time_center+mean_half],axis=1)
	printtime = f"@ {A['time_vec'][Time_center]:%Y-%B-%d_%H:%M}"	
	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_subplot(111)
	ax.plot(A['distance'], A['temperature'][:,Time_center],c='k',alpha=0.5,label=f"@ {A['time_vec'][Time_center]:%B-%d_%H:%M}")

	ax.plot(A['distance'], Mean_over_time,c='r',alpha=1,label='meaned')

	ax.set_xlabel('Distance [m]', fontsize=16, fontweight='bold')
	ax.set_ylabel('Temperature [°C]', fontsize=16, fontweight='bold')
	# Calculate the duration in hours
	duration_delta = mean_half * (A['time_vec'][1] - A['time_vec'][0])

	# Convert timedelta to total hours (works for datetime.timedelta, pandas Timedelta, and numpy timedelta64)
	duration_min = duration_delta.total_seconds() / 60

	# Plot with the formatted title (using a newline to keep it readable)
	plt.title(f"Temperature vs Time\n@ {printtime} (Meaned over {duration_min:.1f} min)\n"+plot_title)
	plt.grid(True, which='both', ls='--')
	plt.legend(fontsize=14, framealpha=1)
	plt.tight_layout()
	plt.show()

	return Mean_over_time
	
	
	