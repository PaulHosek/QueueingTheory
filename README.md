# Queueing Theory and Discrete Event Simulation


## Contributors:

* Paul Hosek (2753446)
* Marcel van de Lagemaat (10886699)

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
| old (directory)     | holds files not used anylonger |
| plotting.py     | Plotting functions for the distibution plots and rho by waiting time. |
| segnificance.py     | Functions to generate, load and plot the relation between rho and hypothesis-test significance levels. |
| gen_data.py     | Should be called in console. Simulates n means for different rhos and saves them as csv. Shows progress bar in console. |
| Images (directory)     | Images for the report. |
| segnif_data | CSV files holding t-test comparison results for different models. |
| lorem | lorem |
| lorem | lorem |
| lorem | lorem |
