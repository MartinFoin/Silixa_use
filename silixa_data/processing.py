# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 15:54:03 2026

@author: martin.foin
"""

"""
processing.py
------------------------
Module dedicated to Silixa Raman DTS  data processing

    """
    
from datetime import datetime
from glob import glob
import re
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from silixa_data import visual

import os
import pandas as pd
import xml.etree.ElementTree as ET


def xml_csv(input_dir, output_dir):
  """convert xml silixa dts files to csv

  Parameters:
  -----------
  input_dir : path
      folder directory of data to convert
  output_dir : path
      folder directory to store converted data

  Returns:
  --------
  Converted files
  """
  # WITSML uses namespaces, which we need to strip or handle to easily find tags
  def strip_namespace(tag):
    if "}" in tag:
      return tag.split("}", 1)[1]
    return tag

  for filename in os.listdir(input_dir):
    if filename.endswith(".xml"):
      xml_path = os.path.join(input_dir, filename)
      csv_path = os.path.join(output_dir, filename.replace(".xml", ".csv"))

      try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Optional: Extract custom data or start time if present
        custom_data = {}
        for elem in root.iter():
          tag_name = strip_namespace(elem.tag)
          if tag_name in [
              "acquisitionTime",
              "referenceTemperature",
              "probe1Temperature",
              "probe2Temperature",
              "forwardMeasurementChannel",
              "startDateTimeIndex",
              "endDateTimeIndex",

          ]:
            custom_data[tag_name] = elem.text

        # Find the mnemonic (column headers) definition
        mnemonics = []
        for elem in root.iter():
          if strip_namespace(elem.tag) == "mnemonicList":
            if elem.text:
              mnemonics = [m.strip() for m in elem.text.split(",")]
          elif strip_namespace(elem.tag) == "mnemonic":
            mnemonics.append(elem.text)

        # Find the actual data rows
        data_rows = []
        for elem in root.iter():
          if strip_namespace(elem.tag) == "data":
            if elem.text:
              row_values = [val.strip() for val in elem.text.split(",")]
              data_rows.append(row_values)

        # Create a dataframe using the extracted headers and data
        if data_rows:
          # Fallback to logCurveInfo if mnemonicList wasn't found
          if not mnemonics:
            for elem in root.iter():
              if strip_namespace(elem.tag) == "logCurveInfo":
                for child in elem:
                  if strip_namespace(child.tag) == "mnemonic":
                    mnemonics.append(child.text)

          df = pd.DataFrame(
              data_rows,
              columns=(
                  mnemonics
                  if mnemonics and len(mnemonics) == len(data_rows[0])
                  else None
              ),
          )

          # Optional: Write metadata/time header at the top of the CSV if available
          # Optional: Write metadata/time header at the top of the CSV if available
          # Optional: Write metadata/time header on two lines at the top of the CSV if available
          with open(csv_path, "w", encoding="utf-8") as f:
            if custom_data:
              # Extraction sécurisée des clés (noms des variables) et des valeurs
              keys = list(custom_data.keys())
              values = list(custom_data.values())

              # Première ligne : Noms des variables
              f.write(f"#{','.join(keys)}\n")
              # Deuxième ligne : Valeurs correspondantes
              f.write(f" #{','.join(str(v) for v in values)}\n")

          # Append the dataframe rows
          df.to_csv(
              csv_path,
              mode="a" if os.path.exists(csv_path) else "w",
              index=False,
          )
          # print(f"Success: {filename}")
        else:
          print(f"Skipped {filename}: No <data> tags found.")

      except Exception as e:
        print(f"Failed {filename}: {e}")

  return


def process_temperature_files(
    directory,
    raw_data,
    file_pattern="*.csv",
    start_row=865,
    end_row=-1,
    plot_results=False,
	plot_title=''
):
  """Processes temperature CSV files, performs chronological sorting,

  extracts a specific distance range, and calculates temporal statistics.
  
  Parameters:
  -----------
  directory : path
      folder directory of csv data
      
  raw_data : bool
      Include stoke and antistoke data in the final returned dictionnary
  file pattern : char
      char pattern to select files in folder
  start_row : int
      start sample number (over distance) to crop the complete data set over distance
  end_row : int
      end of sample number (over distance) to crop the complete data set over distance, if not defined,
      default value = -1 (full distance length)
  plot_title : char 
  	  Informations to display on plots


  plot_results : bool
  
  Returns:
  --------
  A
  
  
  
  
  
  """
  search_path = os.path.join(directory, file_pattern)
  file_list = sorted(glob(search_path))
  num_files = len(file_list)

  if num_files == 0:
    raise FileNotFoundError(f"No files found matching the pattern: {search_path}")

  time_vec = []
  temperature_list = []
  probe1_list = []
  probe2_list = []
  ref_temp_list = []
  distance_data = None

  if raw_data:
    stoke_list = []
    antistoke_list = []

  for filename in file_list:
    match = re.search(r"(\d{8})_(\d{6})\.(\d{3})", filename)
    if match:
      date_str, time_str, ms_str = match.groups()
      full_date_str = f"{date_str}_{time_str}.{ms_str}"
      dt = datetime.strptime(full_date_str, "%Y%m%d_%H%M%S.%f")
      time_vec.append(dt)
    else:
      print(f"Warning: Could not extract date from file {filename}")
      time_vec.append(None)

    # Lecture des 2 lignes de métadonnées
    p1, p2, ref_t = np.nan, np.nan, np.nan
    try:
      with open(filename, "r", encoding="utf-8") as f:
        line1 = f.readline().strip()
        line2 = f.readline().strip()
        if line1.startswith("#") and line2.startswith("#"):
          keys = [k.strip() for k in line1.lstrip("# ").split(",")]
          vals = [v.strip() for v in line2.lstrip("# ").split(",")]
          meta_dict = dict(zip(keys, vals))

          ref_t = (
              float(meta_dict.get("referenceTemperature", np.nan))
              if meta_dict.get("referenceTemperature") != ""
              else np.nan
          )
          p1 = (
              float(meta_dict.get("probe1Temperature", np.nan))
              if (meta_dict.get("probe1Temperature") != "" and float(meta_dict.get("probe1Temperature"))>-900)
              else np.nan
          )
          p2 = (
              float(meta_dict.get("probe2Temperature", np.nan))
              if (meta_dict.get("probe2Temperature") != "" and float(meta_dict.get("probe2Temperature"))>-900)
              else np.nan
          )
    except Exception:
      pass

    probe1_list.append(p1)
    probe2_list.append(p2)
    ref_temp_list.append(ref_t)

    # Lecture des données en sautant les 2 lignes d'en-tête
    df = pd.read_csv(filename, delimiter=",", skiprows=2)

    if distance_data is None:
      distance_data = df.iloc[:, 0].values

    if "TMP" in df.columns:
      temperature_list.append(df["TMP"].values)
    else:
      temperature_list.append(df.iloc[:, 5].values)

    if raw_data:
      stoke_list.append(
          df["ST"].values if "ST" in df.columns else df.iloc[:, 1].values
      )
      antistoke_list.append(
          df["AST"].values if "AST" in df.columns else df.iloc[:, 2].values
      )

  time_vec = np.array(time_vec)
  sort_idx = np.argsort(time_vec)
  time_vec_sorted = time_vec[sort_idx]

  probe1temp = np.array(probe1_list)[sort_idx]
  probe2temp = np.array(probe2_list)[sort_idx]
  internRefTemp = np.array(ref_temp_list)[sort_idx]

  temperature_data = np.column_stack(temperature_list)
  if end_row==-1:
      end_row=len(temperature_data[:, sort_idx])
      
  temperature_data = temperature_data[:, sort_idx]
  temperature = temperature_data[start_row:end_row, :]
  distance_cropped = distance_data[start_row:end_row]

  if raw_data:
    stoke_data = np.column_stack(stoke_list)
    antistoke_data = np.column_stack(antistoke_list)
    stoke = stoke_data[start_row:end_row, sort_idx]
    antistoke = antistoke_data[start_row:end_row, sort_idx]

  temperature_mean = np.mean(temperature, axis=0)
  temperature_std = np.std(temperature, axis=0, ddof=1)
  uncertainty = 2 * temperature_std

  results = {
      "time_vec": time_vec_sorted,
      "distance": distance_cropped,
      "temperature": temperature,
      "temperature_mean": temperature_mean,
      "uncertainty": uncertainty,
      "probe1temp": probe1temp,
      "probe2temp": probe2temp,
      "internRefTemp": internRefTemp,
  }
  if plot_results:
	  visual.cmap_visu(results, plot_title=plot_title,add_ref_temp=True, diff_ref_temp=True)
  if raw_data:
    results["stoke"] = stoke
    results["antistoke"] = antistoke
  

  return results
