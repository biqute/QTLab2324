function [ out ] = fit_res( name_file , guess_param, start, stop )
%Funzione per fittare risonanze con MINUIT; la variabile di ingresso
%guess_param deve contenere, in ordine: fattore moltiplicativo (in genere
%1), Qt, Qi, rotazione, f di risonanza, termine fondo lineare, fondo
%quadratico, fondo cubico. La variabile start stabilisce l'indice di 
%partenza per considerare una sottofinestra delle frequenze.
%Es: fit_res('gap75.txt',[1 1e3 6e4 -0.5 0 -1e-9 -1e-19 0], 1,1601)

close all
a = (load(name_file))';
%a = (load(name_file));
f=a(1,start:stop);y=(sqrt(a(2,start:stop).^2+a(3,start:stop).^2));

Y = max(y);
y = y/Y;
% y = y / mean(y(1:10));

%determino il minimo di s21
[~, I] = min(y);
fmin = f(I);
x = f - fmin;
fmin = fmin * ones(1,length(x));

range = [1, 0.5, 1.5; 2, 1, 1e7; 3, 1, 1e8];
%6, -1e-8, 1e-8; 7, -1e-17, 1e17; 8, -1e-22, 1e22

out = fminuit('resonance','mnplot',guess_param,[x;y;y;fmin],'-s',range);
mnplot_res(out,[x;y;y;fmin],'resonance')
hold on
plot(out(5),20*log10(y(I)),'ro')
out(5) = out(5) + fmin(1);

end