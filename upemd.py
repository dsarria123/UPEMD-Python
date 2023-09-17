
%********************************************************************************
% Code courtesy of Dr. Kun Hu, Harvard
%********************************************************************************


function [IMF] = upemd(s,sampf,fd)
% s: input signal
% sampf: sampling rate
% fd: desired frequency
maskifL=floor(log2((sampf/2)/(fd*2.18)));
jj=0:maskifL;
rmf=fd*2.18*2.^(maskifL-jj);
ii=find(rmf>2*fd);
rmf=rmf(ii);
rmf=[rmf,fd];
len=length(s);
maxn=length(rmf);

allmodex=zeros(4,length(s));
maskinamp=nanstd(s);   % Peng Li changed here: std-->nanstd in case of nan, Jul 10, 2018
IMF=[];outIMFn=0;
toModifyBC = 1;
typeSpline = 2;
numImf = 4;
maxSift = 10;
for jj=1:maxn
    if jj>1
        s=s-allmodex(1,:);
    end
    allmodex=zeros(4,len); 
    for ii=1:16
        maskinf=cos(2*pi*(rmf(jj))*(0:length(s)-1)/sampf+(ii-1)*2*pi/16);
        z=s+maskinamp*maskinf;
        allmodey= emd(z, toModifyBC, typeSpline, numImf, maxSift); 
        allmodey = allmodey';
        if size(allmodey,1)>3
            allmodey(4,:)=sum(allmodey(4:end,:));
        end
        allmodex(1:4,:)=allmodex(1:4,:)+allmodey(1:4,:);
        clear allmodey;
    end
    allmodex=allmodex./16;
    if jj>=maxn-4
       IMF(outIMFn+1,:)=allmodex(1,:); 
       outIMFn=outIMFn+1;
    end
end

end