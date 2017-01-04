% Bilateral Filter 


%function MySimpleImageFilter()

%filtering images with average filter 
clc; home;
close all hidden

% load some image
Img = rgb2gray(imread('LennaNoisy.png'));

%Display what we have loaded
%imshow(Img);

% Find image size
[nrows, ncols, nrgb] = size(Img);

%create noisy version 
Noisy = double(Img) + 60*rand(nrows, ncols);
Noisy = double(Img) / 255.0;

%Make copy of image 
Filtered = Noisy;


kI = 7500; lambda = .2; r = 6;

	for nr = r+1:(nrows-r-1)
		for nc = r+1:(ncols-r-1)
			%two loops for 2D pixels 
			sumV=1; sumPV=Noisy(nr, nc);
			for neighbor_r = nr-r:nr+r
				for neighbor_c = nc-r:nc+r
					% distance between pixel location
					dL = (neighbor_r-nr)^2 + (neighbor_c-nc)^2;
					if (dL< 1), continue, end;
					%distance between pixel intensities
					dI= (Noisy(nr, nc)-Noisy(neighbor_r, neighbor_c))^2;
					%weight
					%w = lambda/(1+dL) * exp( -(dI^2/kI) );
					w = lambda/( (1+dL) * exp(-dI^2/kI) );
					%w = lambda/( (1+dL) * exp(-dI/kI+1) );
					%w = lambda/( (1+dL) * exp(-dI/kI)^2 );
					w = lambda/(1+dL) * exp(-(dI/kI) );
					%w = lambda/( (1+dL) * exp(dI/kI)    );
					
					%updating the sums
					sumV = sumV + w; 
					
					%sumPV = sumPV + w*Noisy(nr, nc); % get image but grainy 
					%sumPV = Noisy(nr, nc);  % get a dark grey fileter 
					%sumPV = sumPV + Noisy(neighbor_r, neighbor_c);
					%sumPV = lambda*Noisy(nr, nc);
					%sumPV = kI*Noisy(neighbor_r, neighbor_c);
					sumPV = sumPV + w*Noisy(neighbor_r, neighbor_c);  % most clear image 
				end;
			end;
			Filtered(nr,nc) = sumPV/sumV;
		end;
		nr
	end;
					
imshow(Filtered)



