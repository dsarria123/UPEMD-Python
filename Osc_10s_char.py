"""

% **************************************************************************					
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
% Osc_10s_char(Matrix_of_t_hr_sbp)
%
% Computes metrics introduced in the study "Characterization of blood pressure 
% and heart rate oscillations of POTS patients via uniform phase empirical mode
% decomposition" by J. R. Geddes, J. Mehlsen, and M. S. Olufsen. 
%
% Input: Matrix of time, heart rate, and systolic blood pressure data
% sampled at 250 Hz. 
%
%
% Dependencies:
% -SetnIMF-
% NOTE: "SetnIMF" calls "upemd" which calls "emd" 
% Input: Data
% Output: IMF components that are below a certain frequency, in our case below ~0.47 Hz  
% Dependencies:
% 	upemd ? Uniform Phase Emperical Mode Decomposition (UPEMD) algorithm (Courtesy of Dr. Kun Hu)
% 	emd ? Matlab?s EMD function (signal processing toolbox)
% 
% -nFA-
% Input: A matrix of IMFs 
% Output: Fourier Representation of each IMF in the frequency domain. 
% 
% -target_component_IMF-
% Input: Matrix of IMFs 
% Output:  Index (column) and signal of the IMF, of period closest to the targeted period (10 seconds for this analysis).
% 
% -gauss_fit_mean_std-
% Input: ?target component? of the output of nFA
% Output: mean, standard deviation, magnitude of mean, and magnitude of mean + standard deviation of a Gaussian fit curve. 
%
% MATLAB signal processing toolbox
%
%
% Output: 
% a_hr			Amplitude of 0.1Hz HR frequency range 
% a_sbp         Amplitude of 0.1Hz BP frequency range 
% M_h 			Quantification of Phase interaction between 0.1Hz HR and BP signals
%*********************************************************************************


"""



function [M_h,a_hr,a_sbp] = Osc_10s_char(Matrix_of_t_hr_sbp,figureson)
%This function takes in patient data and returns metrics: M_h (phase
%response), amplitude of 0.1Hz HR and SBP signals

t = Matrix_of_t_hr_sbp(:,1);
hr = Matrix_of_t_hr_sbp(:,2);
sbp = Matrix_of_t_hr_sbp(:,3);

dt = mean(diff(t));

[IMF_hr] = SetnIMF(t,hr,10); 
[IMF_sbp] = SetnIMF(t,sbp,10);
FA_sbp=nFA(IMF_sbp);
FA_hr =nFA(IMF_hr);


% a_hr
[t_imf_hr,tnum_set_hr] = target_component_IMF(IMF_hr,0.1); %Find 0.1 Hz HR IMF
fa_set_hr = FA_hr(:,[1,tnum_set_hr]);
[~,~,a_hr,~]= gauss_fit_mean_std(fa_set_hr);

% a_sbp
[t_imf_sbp,tnum_set_sbp] = target_component_IMF(IMF_sbp,0.1); %Find 0.1 Hz SBP IMF 
fa_set_sbp = FA_sbp(:,[1,tnum_set_sbp]);
[~,~,a_sbp,~] = gauss_fit_mean_std(fa_set_sbp);

M_h = Calc_M_h(t_imf_hr,t_imf_sbp);
%%
if figureson == 1
    figure
    subplot(2,2,1)
    hold on
    for i = 2:size(FA_hr,2)
        bar(FA_hr(:,1),FA_hr(:,i))
    end
    ylabel('Amplitude of HR IMF')
    title('All IMFs below 0.47 Hz')
    
    subplot(2,2,3)
    hold on
    for i = 2:size(FA_sbp,2)
        bar(FA_sbp(:,1),FA_sbp(:,i))
    end
    hold off
    ylabel('Amplitude of SBP IMF')
    xlabel('Frequency (Hz)')
    
    subplot(2,2,2)
    f = fit(FA_hr(:,1),FA_hr(:,tnum_set_hr),'gauss1');
    hold on
    bar(FA_hr(:,1),FA_hr(:,tnum_set_hr))
    plot(FA_hr(:,1),f(FA_hr(:,1)),'linewidth',4,'col','r')
    title('0.1 Hz IMF')
    xlim([0,.2])
    
    subplot(2,2,4)
    f = fit(FA_sbp(:,1),FA_sbp(:,tnum_set_hr),'gauss1');
    hold on
    bar(FA_sbp(:,1),FA_sbp(:,tnum_set_sbp))
    plot(FA_sbp(:,1),f(FA_sbp(:,1)),'linewidth',4,'col','r')
    xlabel('Frequency (Hz)')
    xlim([0,.2])

    
    
end
end