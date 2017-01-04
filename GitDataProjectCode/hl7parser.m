olddir = cd('\\Mac\Home\Documents\MATLAB\Clinical_HL7_Samples-20160912T235316Z\Clinical_HL7_Samples');

earliest_dob = 9999999999999;

%Names = strings;

files = dir('*.out');
for file = files'
	fid = fopen(file.name);
	
	tline = fgetl(fid);
	while ischar(tline)
	    %disp(tline)
		C = strsplit(tline,'|','CollapseDelimiters',false);
		
		tag = C{1,1};
		
		if tag == 'PID'
			name = string(C{1,6});
			dob = str2num(C{1,8});
			%disp(name)
			%disp(dob)
            if dob < earliest_dob
                earliest_dob = dob;
            end
            Names = [Names name];
		end	
	
	    % read the next line
	    tline = fgetl(fid);
	end

	fclose(fid);
end

disp('Earliest dob:')
disp(earliest_dob)

disp(size(unique(Names)))
disp(unique(Names))

cd(olddir)
