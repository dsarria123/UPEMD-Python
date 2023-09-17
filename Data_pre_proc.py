"""

 **************************************************************************
%                       D R I V E R  f o r						
%        U P E M D  A N A L Y S I S  O F  B A R O R E F L E X 			
% **************************************************************************
%												
% License:										
% Copyright (C) 2019 J. R. Geddes, J. Mehlsen, and M. S. Olufsen
%
% Code, in part, adapted from code supplied by Dr. Ben Randall, University
% of Michigan 
%
% Contact information:									
% Mette Olufsen (msolufse@ncsu.edu)
% North Carolina State University
% Raleigh, NC
% 
% Permission is hereby granted, free of charge, to any person obtaining a
% copy of this software and associated documentation files (the "Software"),
% to deal in the Software without restriction, including without limitation
% the rights to use, copy, modify, and merge the Software subject to the 
% following conditions:
% 
% The above copyright notice and this permission notice shall be included
% in all copies or substantial portions of the Software.
% 
% The authors shall be cited in any work resulting from the use of the 
% Software. The associated published article is arXiv:1910.10332. 
% 
% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES 
% WHATSOEVER RESULTING FROM LOSS OF USE, OR DATA, WHETHER IN AN ACTION OF 
% CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN 
% CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE
%
%%********************************************************************************

%%********************************************************************************
% Data_pre_proc(data,pkprom,figureson)
%
% Preprocesses given data to extract Heart Rate and Systolic Blood Pressure
% 
%
% Input: 
% .csv file containing time, ECG, and blood pressure data sampled at 1000 Hz
% pkprom 
% pkprom (scalar) defining the minimum peak prominence, needed for findpeaks (Matlab function) default value 25 
% figureson (0 = no figures, 1= figures) 

%
% Dependencies: MATLAB signal processing toolbox

% Output: .csv file containing time, Heart Rate, and systolic blood pressure
% data sampled at 250 Hz 
%*********************************************************************************
**/
"""

import numpy as np
from scipy.signal import find_peaks, medfilt, sgolayfilt
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d




"""

%This function turns a matrix with time, ECG, and BP to a matrix with
%Time, ECG, HR, and Systolic Blood Pressure
%Code adapted from code supplied by Dr. Ben Randall

"""

## ECG to HR function

def ECG_to_HR(Tdata,ECG,figureson):

   # %{
    #Makes continuous respiration signal. Loads in 
    #    Tdata - Time points in seconds (sec)
     #   ECG   - ECG data must be in millivolts (mV)
      #  figureson - If 1, it plots a bunch of figures 
    #%}
   # otherfigureson = 0; %Turn on and off all graphs except hr vs time

    dt = np.mean(np.diff(Tdata)); 

    #%Correct baseline of ECG signal with medfilt1

    smoothECG = medfilt(ECG, kernel_size=int(0.2 / dt))

    #Filter out P waves and QRS complex with a window of 200 ms
    smoothECG2 = medfilt(smoothECG, kernel_size=int(0.6 / dt))

    #Filter out T waves with a window of 600 ms 
    smoothECG3 = medfilt(ECG, kernel_size=int(0.6 / dt))

    #Baseline corrected ECG signal
    BaselineCorrectedECG = ECG - smoothECG2; 

    #Savitsky-Golay Filter 

    #Savitsky-Golay Filter filters out VERY low frequency signals. The window
    #ust be odd and within .15 sec 
    SVGwindow = int (0.15/dt); 
    if SVGwindow % 2 == 0:
        SVGwindow = SVGwindow + 1
     
    #Check to ensure order is less than window size 
    if SVGwindow > 5:
        SVGorder = 5; 
    else:
        SVGorder = 3; 
    
    smoothECG4 = sgolayfilt(BaselineCorrectedECG,SVGorder,SVGwindow); 

    # Accentuate peaks to easily find them 

    # Can now extract Q and R peaks 
    accentuatedpeaks = BaselineCorrectedECG - smoothECG4; 

    #Finds Q and R points with minimum peak distance of 200 ms 
    z, _ = find_peaks(accentuatedpeaks,distance = int(0.2 / dt))
    zz = np.mean(accentuatedpeaks(z)); 
    iR, _ = find_peaks(accentuatedpeaks, height=zz, distance=int(0.2 / dt)) 

    RRint = np.diff(Tdata(iR)) #make this a step function with nodes at T_RRint  
    T_RRint = Tdata[iR[: -1]]; 

    HRi = 60.0 / RRint; 
    #interpolate over step function and evaluate at Tdata 
    E_HR_Func = interp1d(T_RRint, HRi, kind='cubic', fill_value='extrapolate')
    E_HR = E_HR_Func(Tdata)

    if figureson == 1:
        plt.figure()
        plt.scatter(Tdata, E_HR, s=2)
        plt.title('Estimated HR')
        plt.xlabel('Time')
        plt.ylabel('Beats per minute')

    return E_HR

# BP to SBP Function

def SBPcalc(Tdata,Pdata, pkprom, graphsYoN):
    #Determine SBP signal NOTE FOR CREDIT: CODE ADAPTED FROM BEN RANDELL 
    #Pkprm := MinPeakProminence, usually 25 is good but may need to go lower
    #Run code with output graphs first to eyeball, then comment out. 
    graphs = graphsYoN; #0= no graphs, 1=with graphs

    dt = np.mean(np.diff(Tdata))

    sbploc, _ = find_peaks(Pdata, distance=int(0.25 / dt), prominence=pkprom)

    T = np.concatenate(([Tdata[0]], Tdata[sbploc], [Tdata[-1]]))
    P = np.concatenate(([Pdata[sbploc[0]]], Pdata[sbploc], [Pdata[sbploc[-1]]]))
    SP = interp1d(T, P, kind='cubic', fill_value='extrapolate')
    SPdata = SP(Tdata)

    if graphsYoN == 1:
        plt.figure()
        plt.plot(Tdata, Pdata)
        plt.plot(Tdata, SPdata, 'r')

    return SPdata

def Data_pre_proc(data, pkprom, figureson):

    sub_figs_on = 0


    t = data[:, 0] - data[0,0] #Make initial time 0
    ECG = data[:, 1] * 1000 #Needs to be in mV
    BP = data[:, 2]

    HR = ECG_to_HR(t,ECG,sub_figs_on);
    SPdata = SBPcalc(t,BP,pkprom,sub_figs_on);


    data2 = np.column_stack((t, HR, SPdata))



    #Sample the data: CHANGE FOR DIFFERENT Hz CONVERSION
    sample = np.arange(0,len(data), 4)

    Prepped_data = data2[sample, :]

    # Plotting data 

    if figureson == 1:
        plt.figure()
        plt.subplot(3, 1, 1)
        plt.plot(t, ECG)
        plt.ylabel('ECG mV')
        plt.title('Data to be analyzed')
        plt.subplot(3, 1, 2)
        plt.plot(t, HR)
        plt.ylabel('HR (bpm)')
        plt.subplot(3, 1, 3)
        plt.plot(t, BP)
        plt.plot(t, SPdata, 'r', linewidth=2)
        plt.legend(['BP', 'SBP'], loc='southeast')
        plt.ylabel('Pressure (mmHg)')
        plt.xlabel('Time (s)')
       
    return Prepped_data
  