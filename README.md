README File for UPEMD analysis of Baroreflex

Code is based on the study:
Characterization of Blood Pressure and Heart Rate Oscillations in POTS Patients via Uniform Phase Empirical Mode Decomposition. 
Justen Geddes, Jesper Mehlsen, and Mette Olufsen. arXiv:1910.10332


This software calculates the three metrics presented in the above study. Namely, the amplitude of the 0.1 Hz Oscillations of Heart Rate (HR) and Systolic Blood Pressure (SBP), and the phase interaction metric (M_h). 


Usage:
The script “Driver_Osc_10s.m” has two parts:

“Step 1” outlines how to preprocess data. If your data is already processed to the desired form, skip step 1. 
Input: 
.txt file containing time, ECG, and blood pressure data sampled at 1000 Hz
pkprom (scalar) defining the minimum peak prominence, needed for findpeaks (Matlab function) default value 25 
figureson (0 = no figures, 1= figures) 


Output: .txt file containing time, Heart Rate, and systolic blood pressure data sampled at 250 Hz 

“Step 2” Describes the primary function Osc_10s_char.m
Input: .txt file containing time, Heart Rate, and systolic blood pressure data sampled at 250 Hz 
Output: The three characteristic measurements presented in the above study.




Step 1: Data Preparation

The raw data saved as .txt files sampled at 1000Hz are loaded into MATLAB generating a matrix with three columns: time (Seconds), ECG (Volts), and blood pressure data (mmHg). 
Line 18 states the sampling rate - change if data are sampled at a different rate.

Function: Data_pre_proc.m
Input: 
  .txt file containing time, ECG, and blood pressure data sampled at 1000 Hz
  pkprom (scalar) defining the minimum peak prominence, needed for findpeaks (Matlab function) default value 25 
  figureson (0 = no figures, 1= figures) 
 
Output: Array of data of the form [time, HR, SBP] sampled at 250 Hz

Dependencies: MATLAB Signal Processing Toolbox 


NOTE 1: To test the proper function of SBP and HR algorithms it is recommended to set figureson=1 previewing results. 
For some patients, pkprom may need to be raised or lowered, this is done by visual inspection. Additionally, some ECGs produce unrealistic HR readings. For these patients alternative HR calculation algorithms should be used. 

NOTE 2: Uses medfilt1 and sgolayfilt available in the signal processing tool box.





Step 2: Uniform phase empirical mode decomposition (UPEMD) analysis
Function: Osc_10s_char.m
Uses UPEMD to compute the amplitude and phase interaction of the 0.1 Hz frequency range of heart rate and systolic blood pressure, corresponding to the baroreflex.
 
Input: .txt file containing time, Heart Rate, and systolic blood pressure data sampled at 250 Hz 

Output: 
a_hr			Amplitude of 0.1Hz HR frequency range 
a_sbp 			Amplitude of 0.1Hz BP frequency range 
M_h 			Quantification of Phase interaction between 0.1Hz HR and BP signals

Dependencies: 
MATLAB Signal Processing Toolbox

-SetnIMF-
NOTE: "SetnIMF" calls "upemd" which calls "emd" 
Input: Data
Output: IMF components that are below a certain frequency, in our case below ~0.47 Hz  
Dependencies:
	upemd – Uniform Phase Emperical Mode Decomposition (UPEMD) algorithm (Courtesy of Dr. Kun Hu)
	emd – Matlab’s EMD function (signal processing toolbox)

-nFA-
Input: A matrix of IMFs 
Output: Fourier Representation of each IMF in the frequency domain. 

-target_component_IMF-
Input: Matrix of IMFs 
Output:  Index (column) and signal of the IMF, of period closest to the targeted period (10 seconds for this analysis).

-gauss_fit_mean_std-
Input: “target component” of the output of nFA
Output: mean, standard deviation, magnitude of mean, and magnitude of mean + standard deviation of a Gaussian fit curve. 

-Calc_M_h-
Input: HR and SBP 0.1 Hz IMFs and uses methods outlined in the referenced paper to
Output: M_h (For more information, see referenced paper.)





License:
Copyright (C) 2019 J. R. Geddes, J. Mehlsen, and M. S. Olufsen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, and merge the Software subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

The authors shall be cited in any work resulting from the use of the Software. The associated published article is arXiv:1910.10332.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, OR DATA, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE