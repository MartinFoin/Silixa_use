# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:02:16 2026

@author: martin.foin
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import silixa_data as sd
import numpy as np
import pandas as pd
directory_i=r'G:\Utilisateurs\martin.foin\Desktop\Data\Data_silixa\TEST_bobines_1910\New_fiber'

# directory_o=r'G:\Utilisateurs\martin.foin\Desktop\Data\Data_silixa\TEST_bobines_2110\Old_fiber'
# sd.processing.xml_csv(directory_i, directory_o)

A_New_flat=sd.processing.process_temperature_files(
    directory_i,
    raw_data=True,
    file_pattern="*.csv",
    start_row=900,
    end_row=2500,
    plot_results=True,plot_title='New_fiber flat posit°'
)

sd.visual.cmap_visu(A_New_flat, plot_title='New_fiber config (1)',add_ref_temp=True, diff_ref_temp=True)




directory_i=r'G:\Utilisateurs\martin.foin\Desktop\Data\Data_silixa\TEST_bobines_2110\New_fiber'

A_New_upright=sd.processing.process_temperature_files(
    directory_i,
    raw_data=True,
    file_pattern="*.csv",
    start_row=900,
    end_row=2500,
    plot_results=True,
	plot_title='New_fiber upright posit°'
)

sd.visual.cmap_visu(A_New_upright, plot_title='New_fiber config (2)',add_ref_temp=True, diff_ref_temp=True)

directory_i=r'G:\Utilisateurs\martin.foin\Desktop\Data\Data_silixa\TEST_bobines_1910\Old_fiber'

A_old_flat19=sd.processing.process_temperature_files(
    directory_i,
    raw_data=True,
    file_pattern="*.csv",
    start_row=900,
    end_row=2500,
    plot_results=True,plot_title='Old_fiber flat posit°'
)
sd.visual.cmap_visu(A_old_flat19, plot_title='Old_fiber config (1)',add_ref_temp=True, diff_ref_temp=True)



directory_i=r'G:\Utilisateurs\martin.foin\Desktop\Data\Data_silixa\TEST_bobines_2110\Old_fiber'

A_old_flat20=sd.processing.process_temperature_files(
    directory_i,
    raw_data=True,
    file_pattern="*.csv",
    start_row=900,
    end_row=2500,
    plot_results=True,plot_title='Old_fiber flat posit°'
)
sd.visual.cmap_visu(A_old_flat20, plot_title='Old_fiber config (2)',add_ref_temp=True, diff_ref_temp=True)

#%%
import silixa_data as sd

U=sd.visual.plotovertime_fixeddist(A_New_upright,300,300)


N_1=sd.visual.plotoverdist_fixedtime(A_New_flat,800,10,plot_title='New_fiber config (1)')
O_1=sd.visual.plotoverdist_fixedtime(A_old_flat19,800,10,plot_title='old_fiber config (1)')

N_2=sd.visual.plotoverdist_fixedtime(A_New_upright,2300,10,plot_title='New_fiber config (2)')
O_2=sd.visual.plotoverdist_fixedtime(A_old_flat20,2300,10,plot_title='old_fiber config (2)')



fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
ax.plot(A_New_flat['distance'], N_1,c='b',alpha=0.5,label=f"New fiber config (1)\n Temp grad={ A_New_flat['probe1temp'][800] - A_New_flat['probe2temp'][800]:.4f}°C")
ax.plot(A_New_upright['distance'], N_2,c='r',alpha=0.8,label=f"New fiber config (2)\n Temp grad={ A_New_upright['probe1temp'][2300] - A_New_upright['probe2temp'][2300]:.4f}°C")
ax.set_xlabel('Distance [m]', fontsize=16, fontweight='bold')
ax.set_ylabel('Temperature [°C]', fontsize=16, fontweight='bold')
plt.title("Temperature vs Distance @max amplitude \n New fiber")
plt.grid(True, which='both', ls='--')
plt.legend(fontsize=14, framealpha=1)
plt.tight_layout()
plt.show()


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
ax.plot(A_old_flat19['distance'], O_1,c='b',alpha=0.5,label=f"New fiber config (1)\n Temp grad={ A_old_flat19['probe1temp'][800] - A_old_flat19['probe2temp'][800]:.4f}°C")
ax.plot(A_old_flat20['distance'], O_2,c='r',alpha=0.8,label=f"New fiber config (2)\n Temp grad={ A_old_flat20['probe1temp'][2300] - A_old_flat20['probe2temp'][2300]:.4f}°C")
ax.set_xlabel('Distance [m]', fontsize=16, fontweight='bold')
ax.set_ylabel('Temperature [°C]', fontsize=16, fontweight='bold')
plt.title("Temperature vs Distance @max amplitude \n old fiber")
plt.grid(True, which='both', ls='--')
plt.legend(fontsize=14, framealpha=1)
plt.tight_layout()
plt.show()


#%%STD



STD_new1=sd.visual.plot_STD_overtime(A_New_flat,plot_title='New_fiber config (1)')
STD_new2=sd.visual.plot_STD_overtime(A_New_upright,plot_title='New_fiber config (2)')

STD_old1=sd.visual.plot_STD_overtime(A_old_flat19,plot_title='old_fiber config (1)')
STD_old2=sd.visual.plot_STD_overtime(A_old_flat20,plot_title='old_fiber config (2)')

#%%
import pywt
wavelet = "cmor1.5-1.0"
widths = np.geomspace(1, 1000, num=1000)
date=50
print(A_New_upright['time_vec'][date])

cwtmatr, freqs = pywt.cwt(A_New_upright['temperature'].T[date]-np.mean(A_New_upright['temperature'].T[date]),widths,wavelet,sampling_period=0.255)
cwtmatr = np.abs(cwtmatr[:-1, :-1])

# plot result using matplotlib's pcolormesh (image with annoted axes)
fig, axs = plt.subplots(1, 1)
pcm = axs.pcolormesh(A_New_upright['distance'], freqs, cwtmatr)
axs.set_yscale("log")
axs.set_xlabel("Distance")
axs.set_ylabel("Spatial frequency m^-1")
axs.set_title("Continuous Wavelet Transform (Scaleogram)")


#%%
