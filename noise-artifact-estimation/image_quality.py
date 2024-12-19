# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 09:43:29 2024

@author: foellmer
"""

import os
import numpy as np
import pydicom
from scipy.ndimage import convolve
#from scipy.signal import convolve
from skimage.morphology import disk
import matplotlib.pyplot as plt

paths = [
    r'P:\cloud_data\Projects\BIOQIC\33_GUIDE-IT\image_quality\data\04-PRA-0025_CT_1',
    r'P:\cloud_data\Projects\BIOQIC\33_GUIDE-IT\image_quality\data\05-COP-0011_CT_1',
    r'P:\cloud_data\Projects\BIOQIC\33_GUIDE-IT\image_quality\data\05-COP-0326_CT_1',
    r'P:\cloud_data\Projects\BIOQIC\33_GUIDE-IT\image_quality\data\19-BAR-0134_CT_1',
]

# Threshold for artifact quantification [HU]
TH = 3000

# Kernel radius for noise quantification [pixels]
radius = 10

# Select path (use the first one in this example)
pathDefault = paths[3]

# Import data - find all files in the folder
data_files = [f for f in os.listdir(pathDefault) if f.endswith('.dcm')]
data_files.sort()  # Ensure the files are in order if necessary

# Read metadata and initialize image array
temp_path = os.path.join(pathDefault, data_files[0])
info = pydicom.dcmread(temp_path)
Im = np.zeros((info.Rows, info.Columns, len(data_files)), dtype=np.float32)

# Loop over slices and read DICOM files
for i, file_name in enumerate(data_files):
    temp_path = os.path.join(pathDefault, file_name)
    info = pydicom.dcmread(temp_path)
    Im[:, :, info.InstanceNumber - 1] = info.pixel_array

# Convert voxel values to Hounsfield Units (HU)
Im = Im * info.RescaleSlope + info.RescaleIntercept  # [HU]
Im_org = Im.copy()

# Calculate voxel volume
resolution = [float(info.PixelSpacing[0]), float(info.PixelSpacing[1]), float(info.SliceThickness)]  # [mm]
voxel_volume = np.prod(resolution)  # [mm^3]

# Exclude background
BG = np.min(Im)
Im[Im == BG] = np.nan

# Quantify artifacts by HU threshold
artefact = Im >= TH
artefact_volume = np.sum(artefact) * voxel_volume / 1e3  # Convert to cm^3
print(f'Artefact volume: {artefact_volume:.1f} cm^3')

# Noise quantification
# Create a normalized structuring element (disk shape) for convolution
SE = disk(radius).astype(np.float32)
SE /= np.sum(SE)

SE = SE[:, :, None]

# Calculate local mean and standard deviation
Im_mean = convolve(Im[:,:], SE, mode='constant', cval=np.nan)  # Local mean
temp = (Im - Im_mean) ** 2
Im_SD = np.sqrt(convolve(temp, SE, mode='constant', cval=np.nan))  # Local SD

# Calculate noise as the median of the SD within the image
temp = Im_SD[~np.isnan(Im_SD)]
noise_SD = np.median(temp)  # [HU]
noise_SD_norm = noise_SD * np.sqrt(voxel_volume)  # Normalized SD [HU * sqrt(mm^3)]
print(f'Noise: median SD = {noise_SD:.0f} HU')
print(f'Voxel volume = {voxel_volume:.3f} mm^3')
print(f'Noise: normalized median SD = {noise_SD_norm:.0f} HU * mm^(3/2)')

# # Plot intermediat results:
# plt.imshow(Im_org[:,:,30], cmap='gray')
# plt.show()
# plt.imshow(Im_mean[:,:,30], cmap='gray')
# plt.show()
# plt.imshow(Im_SD[:,:,30], cmap='gray')
# plt.show()