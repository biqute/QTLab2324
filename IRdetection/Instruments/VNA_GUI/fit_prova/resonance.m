%RESONANCE     Resonance profile.
%  Y0 = RESONANCE(P,X)
%  where P = [multiplicative factor, Qt, Qi, rotation, f_riso, linear bkg, quadratic bkg, cubic bkg] are variational parameters,
%  and X is a vector, returns
%  Y0 = abs(c(6)*fp + c(7)*fp.^2 + c(8)*fp.^3 + c(1)*(1 - exp(1i*c(4))*c(2)*(c(2)^-1 - (c(3))^-1) ./ (1 + i*c(5) + 2i * c(2) * (fp - fris) / (fmin+fris))));
%
% %  CHI2 = GAUSSIAN(P,[X; Y; Delta_Y])
% %  where Y and Delta_Y are experimental data and errorbar vectors,
% %  respectively, returns Chi-square:  CHI2 = sum(((Y-Y0)./Delta_Y).^);
% %
% %  CHI2 = GAUSSIAN(P,[X; Y])
% %  is the same as above, with Delta_Y = ones(size(X));


function f = resonance(par,data)
% f = abs(par(6)*data(1,:) + par(7)*data(1,:).^2 + par(8)*data(1,:).^3 + par(1)*(1 - exp(1i*par(4))*par(2)*(par(2)^-1 - (par(3))^-1) ./ (1 + 2i * par(2) * data(1,:) ./ ( data(1,:) + par(5) ) )));
fmin = data(4,1);
f = abs(par(6)*data(1,:) + par(7)*data(1,:).^2 + par(8)*data(1,:).^3 + par(1)*(1 - exp(1i*par(4))*par(2)*(par(2)^-1 - (par(3))^-1) ./ (1 + 2i * par(2) * ( data(1,:) - par(5) ) ./ fmin )));
%theoretical function
if (size(data,1)==2),    %chi-square, error = 1
    f = sum((data(2,:) - f).^2);
elseif (size(data,1)>2), %chi-square, error = 3rd row of data
    f = sum(((data(2,:) - f)./data(3,:)).^2);
end