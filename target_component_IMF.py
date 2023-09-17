% **************************************************************************
%                       Obtaining desired IMF 			
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
% target_component_IMF(IMF,target_freq)
%
% Give a matrix with IMFs as columns, and a target frequency, function uses
% the properties of IMFs to find the one closest in frequency to target
% frequency. 
%
% Input: Matrix of IMFs from SetnIMF.m

% Dependencies: 
%
% Output: 
% targeted_IMF - The column from IMF that is closest to target_freq in
% frequency
% target_number - The numnber of the column of targeted_IMF
%*********************************************************************************

function [targeted_IMF,target_number] = target_component_IMF(IMF,target_freq)
%Target a frequency based on average period of IMF
%%
target_length = 1/target_freq;
t = IMF(:,1)-IMF(1,1); %Just making sure t(1) = 0
imf = IMF(:,2:end);
dim_imf = size(imf);
cycle_lengths = zeros(1,dim_imf(2));

for i = 1:dim_imf(2)
   pks = findpeaks(imf(:,i));
   cycle_lengths(i) = max(t)/length(pks);  
end

target_number = find(abs(cycle_lengths-target_length)== min(abs(cycle_lengths-target_length)))+1; 
%+1 above because of adding the time column
targeted_IMF = [t,IMF(:,target_number)]; 

end


    
    
    
    