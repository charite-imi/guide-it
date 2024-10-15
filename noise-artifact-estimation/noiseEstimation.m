clear

%% import data
pathDefault = 'E:\Projekte\GUIDE IT\Data\1.2.392.200036.9116.2.2426555318.1479253696.3.1227800001.1';
DataName = dir(pathDefault);
DataName(1:2) = [];

iName = 1;
temp = fullfile(DataName(iName).folder, DataName(iName).name);
info = dicominfo(temp);
Im = zeros(info.Height, info.Width ,length(DataName));

for iName = 1 : length(DataName)
    temp = fullfile(DataName(iName).folder, DataName(iName).name);
    info = dicominfo(temp);
    Im(:,:,info.InstanceNumber) = dicomread(temp);
end
Im = Im * info.RescaleSlope + info.RescaleIntercept;%[HU]

res = [info.PixelSpacing' info.SliceThickness];
BG = min(Im(:));

Im = double(Im);
Im(Im == BG) = NaN;

iw(Im)

%% test the influence of kernel size
radius = 1:15;
for iRadius = 1:length(radius)
    % SE = strel('sphere', radius(iRadius));
    SE = strel('disk', radius(iRadius));
    SE = SE.Neighborhood / sum(SE.Neighborhood(:));
    Im_mean = convn(Im, SE, 'same');
    temp = (Im - Im_mean).^2;
    Im_SD = sqrt(convn(temp, SE, 'same'));

    [N,edges] = histcounts(Im_SD(:));
    ind = find(max(N) == N,1);
    Mod(iRadius) = mean(edges(ind:ind+1));
end

figure
hold on
plot(radius, Mod)


%% slice wise noise
radius = 10;
SE = strel('disk', radius);
SE = SE.Neighborhood / sum(SE.Neighborhood(:));
Im_mean = convn(Im, SE, 'same');
temp = (Im - Im_mean).^2;
Im_SD = sqrt(convn(temp, SE, 'same'));

for iSlice = 1:size(Im,3)
    temp = Im_SD(:,:,iSlice);
    [N,edges] = histcounts(temp(:));
    ind = find(max(N) == N,1);
    Mod(iSlice) = mean(edges(ind:ind+1));
end

figure
plot(Mod)


%% manual ROI
temp = Im(:,:,300);
temp = temp(BW_iw);
figure
histogram(temp)
std(double(temp))