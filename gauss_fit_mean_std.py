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
%  gauss_fit_mean_std(x_and_y_data_cols)
%
% Computes a Gaussian fit of data given in x_and_y_data_cols.
%
% Input: n-by-2 matrix with data
%
% Dependencies: 
% 
% Output: 
% mean - "Center" of Gaussian
% standard_deviation - standard deviation of Gaussian
% magnitude_of_mean - function value of the mean
% magnitude_of_plus_std - function value of mean+standard_deviation
%*********************************************************************************


function [mean, standard_deviation,magnitude_of_mean, magnitude_of_plus_std]...
    = gauss_fit_mean_std(x_and_y_data_cols)
%Takes x and y data, fits with Gaussian, and outputs mean and Standard
%deviation

f = fit(x_and_y_data_cols(:,1),x_and_y_data_cols(:,2),'gauss1');

mean = f.b1;

standard_deviation =f.c1;

magnitude_of_mean = f.a1;

magnitude_of_plus_std = f(mean + standard_deviation);




end