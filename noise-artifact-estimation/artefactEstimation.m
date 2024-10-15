clear

%% import data
% pathDefault = 'E:\Projekte\GUIDE IT\Data\04-PRA-0025_CT_1\4\DICOM';
pathDefault = 'E:\Projekte\GUIDE IT\Data\05-COP-0011_CT_1\3\DICOM';
% pathDefault = 'E:\Projekte\GUIDE IT\Data\05-COP-0326_CT_1\4\DICOM';
% pathDefault = 'E:\Projekte\GUIDE IT\Data\19-BAR-0134_CT_1\7\DICOM';

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


TH = 3000;
artefact = false(size(Im));
artefact(Im >= TH) = true;
edgeColor = 'r';
contourROI(artefact, edgeColor)

artefact_volume = sum(artefact(:)) * prod(res) / 10^3;%cm^3
disp(artefact_volume)
% artefact_volume2 = squeeze(sum(artefact,[1 2]) * prod(res) / 10^3);%cm^3