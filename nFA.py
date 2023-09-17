% **************************************************************************
%                       Calculation of Fourier Spectrum		
% **************************************************************************

%********************************************************************************
% Code adapted from MATLAB's FFT example on Mathworks
%
% Input: IMF calculated from SetnIMF.m
%
% Dependencies: 
%
% Output: Matrix with Frequency vector and Power vector
%*********************************************************************************



function [FA] = nFA(IMF)


Fs = 250; %Sampling rate 250Hz
numdatapoints = 200; %Frequencys are small enough where we only need first 200 data points
dimf = size(IMF);
FA = [];
% Adapted from MATLAB's FFT page
for i = 2:dimf(2)
    imf = IMF(:,i);
    F = fft(imf);
    xF = F(1:floor(length(imf)/2)+1);
    DF = Fs/length(imf);
    freqvec = 0:DF:Fs/2;
    A = abs(xF); %Getting amplitudes
    An = 2.*A/length(imf); %Normalzing amplitudes, 2* since looking at half of the spectrum
    sfreqvec = freqvec(1:numdatapoints)';
    Astar = An(1:length(sfreqvec));
    if i ==2
        FA = [FA,sfreqvec];
    end
    FA = [FA,Astar];
end


end

