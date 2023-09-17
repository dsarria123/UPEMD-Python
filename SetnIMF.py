% **************************************************************************					
%                                  SetnIMF 			
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
% -SetnIMF-
% NOTE: "SetnIMF" calls "upemd" which calls "emd" 
% Input: Data from Osc_10s_char.m
% Output: IMF components that are below a certain frequency, in our case below ~0.47 Hz  
% Dependencies:
% 	upemd ? Uniform Phase Emperical Mode Decomposition (UPEMD) algorithm (Courtesy of Dr. Kun Hu)
% 	emd ? Matlab?s EMD function (signal processing toolbox)
%%********************************************************************************

function [IMFr] = SetnIMF(t,data,CycleEst)
%Calculates all IMFs under 0.46666 Hz (Max Resp Freq)

IMFt = [];
SamHz = 1/mean(diff(t)); %Usually 250 Hz
Data_Epoch = (1/60)*(1/SamHz); %Data_Epoch needs to be in terms of hours

CycleEstimate = 1/(3600)*CycleEst; %CycleEstimate needs to be in terms of hours

[m,n]=size(data);
if m<n
    data=data';
    [m,n]=size(data);
end

data = [data(:); data(:); data(:); data(:); data(:)];

sampf=60/Data_Epoch;fc=1/CycleEstimate;
[IMF] = upemd(data',sampf,fc);
len=length(data);
tc=[0:len-1]*Data_Epoch/60;

data = data(m*2+1:m*3);
tc = tc(1:m);
tc=tc*3600;  % Adjust for hours to seconds
IMF = IMF(:, m*2+1:m*3);
IMF = [tc;IMF];

disp('---------------------------------------------------------------------');

disp(['Targeted cycle length (seconds): ',num2str(round(CycleEstimate*3600))]);

IMF = IMF';

for j = min(size(IMF)):-1:2
        pks = findpeaks(IMF(:,j)); %This works well by defintion of IMF
        cycLength = (max(t)-min(t))/length(pks);
        if cycLength > (60/28) %~.46666 Hz, 28 breaths/min, Very generous, loose bound (looking for 0.1 Hz)
            IMFt = [IMFt,IMF(:,j)];
        else
            break
        end
end
IMFr = [t,IMFt];



end