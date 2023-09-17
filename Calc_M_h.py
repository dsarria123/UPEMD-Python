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
% Software. The associated published article is
% https://doi.org/10.1109/TBME.2020.2974095. 
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
% Calc_M_h(hr_10s_imf,sbp_10s_imf)
%
% Calculates value of M_h as given in the referenced paper. 
%
% Input: Targeted 0.1 Hz IMFs calculated from SetnIMF.m
%
% Dependencies:
%
% Output: M_h - Quantification of Phase interaction between 0.1Hz HR and BP signals
%*********************************************************************************

function [M_h] = Calc_M_h(hr_10s_imf,sbp_10s_imf)
h_hr = hilbert(hr_10s_imf(:,2));
phase_hr = unwrap(angle(h_hr));

h_sbp = hilbert(sbp_10s_imf(:,2));
phase_sbp = unwrap(angle(h_sbp));

M_h = trapz(abs(mod(abs(phase_hr-phase_sbp),2*pi)-pi))/(length(phase_hr)-1);

end

