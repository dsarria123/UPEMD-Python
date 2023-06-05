"""
% **************************************************************************
%                       D R I V E R  f o r						
%        U P E M D  A N A L Y S I S  O F  B A R O R E F L E X 			
% **************************************************************************
%												
% License:										
% Copyright (C) 2019 J. R. Geddes, J. Mehlsen, and M. S. Olufsen
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
% DriverBasic ()
%
% Calls functions that (Step 1) preprocessing data and (Step 2) computes 
% metrics introduced in the study "Characterization of blood pressure and
% heart rate oscillations of POTS patients via uniform phase empirical mode
% decomposition" by J. R. Geddes, J. Mehlsen, and M. S. Olufsen. 
%
% Input: Text file with blood pressure and ECG time-series data sampled at 1000 Hz
% pkprom (scalar) defining the minimum peak prominence, needed for findpeaks (Matlab function) default value 25 
% figureson (0 = no figures, 1= figures) 

% Dependencies: Data_pre_proc.m, Osc_10s_char.m, MATLAB signal processing
% toolbox
%
% Output: 
% a_hr			Amplitude of 0.1Hz HR frequency range 
% a_sbp         Amplitude of 0.1Hz BP frequency range 
% M_h 			Quantification of Phase interaction between 0.1Hz HR and BP signals
%*********************************************************************************

% In this file, we will use 2 data sets (1 POTS 1 Control) to illustrate
% how to use our method.


"""

import Osc_10s_char

pt_cell = ['ca02a_LD','ca02a_HUT','C21af4_LD','C21af4_HUT']

    #Name of file without '.txt'

ALL_WRITE = 0; #Set to 1 if you want all parts of file to create .txt files
#to save work

"""
%% Step 1 - Preprocessing data
%Data may come from different sources, but the function "Osc_10s_char.m"
%requires a matrix containing 3 columns of data: time (s), heart rate
%(bpm), and systolic blood pressure (mmHg) 
%This function does not take in scaling for cuff measurements

%If data are in the form of time(s), ECG(V),BP(mmHg) and sampled at 1000
%Hz the following may be useful. If the data is already in deseried form 
%([t,hr,sbp]) feel free to proceed to the next section.
"""


figureson = 1
write_file = 0

pkprom = 25; #25 is default, increase or decrease in accordence to fitting
#systolic line over the top of BP (figureson)
for i in pt_cell.length:# :length(pt_cell)
    data = load(strcat(pt_cell{i},'.txt'))
    PreppedData = Data_pre_proc(data,pkprom,figureson)
    
    if write_file == 1 or ALL_WRITE == 1:
       dlmwrite(strcat(pt_cell{i},'_P.txt'),PreppedData,'precision',10)
   end
end



"""
%% Step 2 - Running UPEMD Analysis
% The function Osc_10s_char takes in patient data ([t,hr,sbp]) and 
% returns metrics: M_h (phase response),amplitude of 0.1Hz HR and 
% SBP signals using UPEMD and procedures outlined in the above paper.
"""


figureson = 1
for i in pt_cell.length: #:length(pt_cell)
     dat = load(strcat(pt_cell{i},'_P.txt')); %Load in data saved above
    [M_h,a_hr,a_sbp] = Osc_10s_char(dat,figureson); 
end