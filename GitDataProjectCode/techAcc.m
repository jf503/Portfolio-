load('Data.mat')

% Just export
%exploded_2 = string(datetime(Data(:,2),'ConvertFrom','datenum'));
%exploded_3 = string(datetime(Data(:,3),'ConvertFrom','datenum'));
%exploded_4 = string(datetime(Data(:,4),'ConvertFrom','datenum'));

%just_dts = [exploded_2 exploded_3 exploded_4];

%c = {'abc' 'def' 'ghk';[23],[24],[67];[87],[13],[999];[656],[6767],[546]};

%fid = fopen('junk.csv','w')
%fprintf(fid,'%s, %s, %s\n',just_dts{1:end,:})
%fclose(fid)

%csvwrite('datetimes.csv',just_dts)

%
%combined = [Data exploded_2 exploded_3 exploded_4];
%csvwrite('combined.csv',combined)

%PatientID | Arrival Time | Begin Time | Complete Time | TechID

%isolating rows and date time)
arrivalTime = Data(:,2)
arrivalTime2 = datetime(arrivalTime,'ConvertFrom','datenum')
beginTime = Data(:, 3)
beginTime2 = datetime(beginTime,'ConvertFrom','datenum')
begintimestr = datestr(beginTime2)

completeTime = Data(:, 4)
completeTime2 = datetime(completeTime,'ConvertFrom','datenum')


% Person who waited longest #785 waited 3:26 min

waitTime = beginTime2 - arrivalTime2
worstWait = max(waitTime)



% Find max people waiting.  

waitTimeMat = beginTime - arrivalTime

timevecWait = datevec(waitTimeMat)








%Percentile Wait Time = 92 min (1:32)

Y = prctile(waitTime, 90)




%trying to find worst tech 


% sort by tech ID and add beginTime 2

techID = sortrows(Data(:, 5))





%trying to count unique lab ID to see if more than 10 remove if less than 10 

%for unique number in col 1 






    


%  Making clean matrix for Tech and Minute data 

A = [techID beginTime];

DateVecBegin = datevec(beginTime)

minutes = DateVecBegin(:, 5)

% shows us where in tech data there are zeros for minute entries time div 10

modLogic = mod(minutes, 10)

techBias1 = [techID modLogic]



% for each tech I need to count how many total they have then find % that is zero 
%1 = techBias1[

%use logical have 1 or 0 

% two for loops to count zeros 







