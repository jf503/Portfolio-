%BEACON = PID
%DateTime = Time Stamp 
% X and Y are location coordinates in inches 



Data = readtable('TrackingData.xlsx')
Data = sortrows(Data, [2])
[r,c] = size(Data);
DateFix = datestr(Data.DateTime)
Data.DateRead = DateFix
format long 

%Patient 16 start at 9:53
Data16 = Data(Data.BEACON==16,:)
DateVec16 = datevec(Data16.DateTime)
%4 hour 5 min
Data16CT = Data16(DateVec16(:,4) == 9 & DateVec16(:,5) == 53,:)
Data16.hour = DateVec16(:,4)
Data16.min = DateVec16(:,5)


%Patient 18 statrt work up 
Data18 = Data(Data.BEACON == 18, :)
Procedure18 = Data18(Data18.X >= 400, :)

FirstProcedure18 = datestr(Procedure18.DateRead(1,:))


%Patient 17 Work up











%Work up Time Avg 

%make boolean vector take total min in that space and then divide by total patients


Data.WorkUpTrue = Data.X >= 150 & Data.X <=300 & Data.Y >=0 & Data.Y <=800
%summary(Data)  

unique_times = unique(Data.DateTime)
%uniqueID = unique(Data.BEACON)




%how many work up nurses, copy from recovery 

maxline = 0
for i = 1:size(unique_times);
	CurrentTime = unique_times(i);
	WorkUpTrue1 = Data.WorkUpTrue;
	DateTime1 = Data.DateTime;
	total = sum(WorkUpTrue1 & (DateTime1 == CurrentTime));
	if (total > maxline)
		maxline = total;
	end
end





% Percentage of Patients recover in ICA after Procedue and how many nurses >3 = new nurse

Data.Recover = Data.X >= 0 & Data.X < 150 & Data.Y >=0 & Data.Y <=800

maxline2 = 0
for i = 1:size(unique_times)
	CurrentTime = unique_times(i);
	RecoveryTrue = Data.Recover;
	DateTime2 = Data.DateTime;
	total = sum(RecoveryTrue & (DateTime2 == CurrentTime));
	if (total > maxline2)
		maxline2 = total;
 
 	end
 end
	
	
	
	



summary(Data)

Data(1:5,:)    

maxline
maxline2



Data16(1:5,:)
DateVec16(1:5,:)

Data16
Data16CT

%FirstDateVec18
Procedure18