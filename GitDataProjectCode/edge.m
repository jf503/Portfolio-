%edge detector of lines 

%function to find lines in the edge image EdgeImg 
%function E = FindLine(EdgeImg)

load('FracturesNoisy.mat');

% Find Img Size 
[nrows, ncols] = size(Img);

[nrows, ncols] = size(Img);
%EdgeImg= Img(1:2:nrows, 1:2:ncols); % resize 2 times in x and y axes

EdgeImg = zeros(size(Img));
for x=2:nrows-1
	for y=2:ncols-1
		EdgeImg(x,y) = sqrt((Img(x+1,y)-Img(x-1,y))^2 + (Img(x,y+1)-Img(x,y-1))^2);
	end
end

%Convert the image to 1D buffer, to compute quantiles 
EdgeImg1D = reshape (EdgeImg, [nrows*ncols, 1]); 
t = max(100, quantile(EdgeImg1D, 0.99)); % select edge intensity threshold 

EdgeThresh = zeros(size(EdgeImg));
for x=2:nrows-1
	for y=2:ncols-1
		if EdgeImg(x,y) > t
			EdgeThresh(x,y) = 255.0;
		else
			EdgeThresh(x,y) = 0.0;
		end;
	end;
end;

% Set minimal and maximal line size 
r0=50; r1=2*r0;
r0sq = r0*r0;
r1sq = r1*r1;
nLine = 0; 

%Search 

tic 
for x0 = 1:nrows
	progress = 100*x0/nrows     %display current progress 
	
	%early exit for debugging
	%if progress > 25
	%	break;
	%end
	
	for y0 = 1:ncols
		if EdgeImg(x0,y0) < t continue; end;  % non edge, skip 
		
		for x1 = x0+1:min(x0+r1, nrows)
			for y1 = max(1, y0-r1): min(ncols, y0+r1)
				if (EdgeImg (x1, y1) < t), continue; end;  %GAP1
				
				if(EdgeImg(round((x0+x1)/2),round((y0+y1)/2))<t), continue, end;
				%if(round((x0+x1)/2 > round((y0+y1)/2), continue; end;
				%if(EdgeImg(round((y0+y1)/2), round((x0+x1)/2)) <t/2), continue; end:
				
				%dsq = (x1-x0)^2 + (y1-y0)^2;
				%if dsq < r0sq || dsq > r1sq
					%continue;
				%end;
				
				d = sqrt( (x1-x0)^2 + (y1-y0)^2 );
				if d<r0 || d>r1
					continue;  % too large or too small 
				end; 
				
				a = (y0-y1)/(x0-x1);  %GAP2
				b = y0-a*x0; 
				
				% Compute line cost function 
				
				C=0; dx=(x1-x0)/5;  % take sample points along each line 
				for x =x0: dx:x1
					C = C + EdgeImg(round(x), round(a*x+b));   % Edge Cost Function, gradiant image, move along line 
				
				 end; 

				% Add new detected line 
				nLine = nLine+1;
				Lines(nLine, 1) = C;   % save the ocst of this line 
				Lines(nLine, 2) = x0;  Lines(nLine, 3) = y0;  % save statr of point 
				Lines(nLine, 4) = x1;  Lines(nLine, 5) = y1;   %save end point 
			end; 
		end; 
	end; 
end; 
toc 

Lines = sortrows(Lines,-1)
nLine = max(1,round(nLine/10));

imshow(EdgeImg/255.0)
imshow(EdgeThresh/255.0)   

