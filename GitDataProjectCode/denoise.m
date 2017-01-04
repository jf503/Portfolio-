% average denoising 

function MySimpleImageFilter()
%filtering images with average filter 
clc; home;
close all hidden

% load some image
Img = rgb2gray(imread('LennaNoisy.png'));

%Display what we have loaded
imshow(Img);

% Find image size
[nrows, ncols] = size(Img);

%create noisy version 
Noisy = double(Img) + 60*rand(nrows, ncols);
Noisy = double(Img) / 255;


%Make copy of image 
Filtered = Noisy;

%set filter radius 
r = 7; 

%filter pixel by pixel 
bCodingApproach = 0;
if (bCodingApproach == 0)
	for nr = r + 1:nrows-r-1 
		for nc = r+1:ncols-r-1
			Filtered(nr, nc) = mean2(Noisy(nr-r:nr+r, nc-r:nc+r));
		end;
	end;
end;

imshow(Filtered)
whos