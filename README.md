# Queueing Theory and Discrete Event Simulation


## Contributors:

* Paul Hosek
* Marcel van de Lagemaat

## Program Overview
Goal of this work is to compare different Server-Client queueing models.

## Requirements
* Python 3.9+
* math
* numpy
* matplotlib
* simpy
* pandas
* csv

## Running the code

All results are aggregated into a single Jupyter Notebook named MarcelvandeLagemaat_10886699_PaulHosek_12637033_1.ipynb.
This notebook imports all relevant files and generates the plots and data found in the report.
The authors hope this will simplify review of the codebase at later points in time.

## Repository structure


| File Name           | Description                                                                                                                                                                                          |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Final Notebook | Named "MarcelvandeLagemaat_10886699_PaulHosek_12637033_1.ipynb". This notebook aggregates all the rest of the respository.|
| DES.py   | Includes both Server and Message classes as well as des_simulation to run a discrete event model simulation for a specific queue and parameters on these.                                                                    |
| Server.py     | Entails the Server class.  |
| distibutions.py     | Different distributions to use as arrival- or serving-rates distibutions. |
| Message.py     | Entails the Message class. |
| Old (directory)     | holds files not used anylonger |
| plotting.py     | Plotting functions for the distibution plots and rho by waiting time. |
| significance.py     | Functions to generate, load and plot the relation between rho and hypothesis-test significance levels. |
| gen_data.py     | Should be called in console. Simulates n means for different rhos and saves them as csv. Shows progress bar in console. |
| Images (directory)     | Images for the report. |
| signif_data (directory) | CSV files holding t-test comparison results for different models. |
