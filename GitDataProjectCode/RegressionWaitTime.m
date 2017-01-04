Data = readtable('DataforHW4.xlsx');
Data = sortrows(Data,[2])
[r,c] = size(Data);

Data.Y = Data.dtBegin - Data.dtArrive;

test1= regress(Data.Y, Data.X)
%test1 = regress(Data.Y, ones(r,1))
Data.diff1 = abs(Data.Y - test1)


%various ways to calculate 5 min, they seem to run equally
%fivemins = minutes(5)
fivemins = 5/(24*60) 
%5 minutes in their weird date format

Data.success1 = Data.diff1 <= fivemins

%summary(Data)



%add current number of patients in line like last week (new col in_line)

Lines = []
for i = 1:r
	TaCurrent = Data.dtArrive(i);
	Ta = Data.dtArrive;
	Tb = Data.dtBegin;
	%notme = true(size(Ta));
	%notme(i) = false;
	
	total = sum(TaCurrent > Ta & TaCurrent < Tb);
	%total = sum(Ta < TaCurrent & Tb >= TaCurrent);
	%total = sum(Ta < TaCurrent & Tb >= TaCurrent & notme);
	
	Lines(i) = total;
end

% add back in later
Data.lines = Lines';

%[b, bint, rr, rrint, stats] = regress(Data.Y, [Data.X, Data.lines]);

test2 = regress(Data.Y, [Data.X, Data.lines]);

disp(test2)

prediction2 = Data.X * test2(1) + Data.lines * test2(2);

disp(prediction2)

Data.Diff2 = abs(Data.Y - prediction2);

disp(Data.Diff2)

Data.success2 = Data.Diff2 <= fivemins

%summary(Data)







% calculate number of patients in line 5 min before arrival (add new col
% five_min_before


Lines2 = []
for i = 1:r
	TaCurrent = Data.dtArrive(i);
	TaMinusFive = TaCurrent - fivemins;
	Ta = Data.dtArrive;
	Tb = Data.dtBegin;
	%notme = true(size(Ta));
	%notme(i) = false;
	
	
	total = sum(Ta < TaMinusFive & Tb >= TaMinusFive);
	%total = sum(Ta < TaCurrent & Tb >= TaCurrent & notme);
	
	Lines2(i) = total;
end


Data.lines2 = Lines2';

test3 = regress(Data.Y, [Data.X, Data.lines, Data.lines2]);

disp(test3)


prediction3 = Data.X * test3(1) + Data.lines * test3(2) + Data.lines2 * test3(3);
%prediction3 = Data.X * test3(1) + Data.lines * test3(2) + Data.lines2(3) * test3(3); % wrong 

disp(prediction3)

Data.Diff3 = abs(Data.Y - prediction3);

disp(Data.Diff3)

Data.success3 = Data.Diff3 <= fivemins

summary(Data)

Data(1:5, :)

disp(test1)

disp(test2)

disp(test3)


% end useful code























% Attempts to export to a csv 


%writetable(d, 'DataMatT.csv', 'Delimiter',',','QuoteStrings', true); % I think this one works

%DataMat.csv

%dlmwrite(dataMatTest, d,'-append', 'delimiter', ',');

% trying tests 
%d = [Data.Y, Data.X];

%plot(regress(Data.Y, Data.X));
%x2 = Data.X
%y2 = Data.Y


%[b, bint, rr, rrint, stats] = regress(y2, x2) 

%[b, bint, rr, rrint, stats] = regress(Data.Y, [Data.X, Data.lines]);


%plot(x2)
%plot(Data.X)

%testing again change r back if used above 

%[b, bint, r, rint, stats] = regress(Data.Y, [Data.X, Data.lines]);

%Again = regress(Data.Y, Data.X)
%disp(Again);

%% Same as above test for Question 6 =  1510 for the positives 
%Y3 = Data.Y
%X3 = Data.X

%Again1 = regress(Y3, X3)
%disp(Again1)

%Data.diff1Test = abs(Y3 - Again1)

%Data.success1Test = Data.diff1Test <= fivemins

%sum(Data.success1Test)




