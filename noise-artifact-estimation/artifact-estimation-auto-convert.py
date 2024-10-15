# caution: generated using OpenAPI, to be tested


import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from skimage import measure

# %% Import data
# Change to your desired path
path_default = r'E:\Projekte\GUIDE IT\Data\05-COP-0011_CT_1\3\DICOM'

# Get list of all files in the directory
data_names = [f for f in os.listdir(path_default) if os.path.isfile(os.path.join(path_default, f))]

# Read first DICOM file to get info about image dimensions
temp = os.path.join(path_default, data_names[0])
info = pydicom.dcmread(temp)
im_shape = (info.Rows, info.Columns, len(data_names))

# Initialize empty 3D array
im = np.zeros(im_shape)

# Read all DICOM files and insert them into the 3D array
for i_name, file_name in enumerate(data_names):
    temp = os.path.join(path_default, file_name)
    info = pydicom.dcmread(temp)
    im[:, :, info.InstanceNumber - 1] = info.pixel_array

# Apply rescale slope and intercept for Hounsfield Units (HU)
im = im * info.RescaleSlope + info.RescaleIntercept

# Get resolution and background intensity
res = np.array([info.PixelSpacing[0], info.PixelSpacing[1], info.SliceThickness])
bg = np.min(im)

# Replace background intensity with NaN
im = np.where(im == bg, np.nan, im)

# Plotting the image using matplotlib (equivalent to `iw(Im)` in MATLAB)
plt.imshow(im[:, :, im.shape[2]//2], cmap='gray')  # Show middle slice as an example
plt.colorbar()
plt.show()

# Thresholding to find artefacts
th = 3000
artefact = im >= th

# Plotting artefact contours
edge_color = 'r'
contours = measure.find_contours(artefact[:, :, im.shape[2]//2], 0.5)  # Middle slice as example
plt.imshow(im[:, :, im.shape[2]//2], cmap='gray')
for contour in contours:
    plt.plot(contour[:, 1], contour[:, 0], edge_color, linewidth=2)
plt.show()

# Calculate artefact volume (in cm^3)
artefact_volume = np.sum(artefact) * np.prod(res) / 10**3
print(f'Artefact volume: {artefact_volume:.2f} cm^3')

# Uncomment below if you want to calculate volume per slice
# artefact_volume_per_slice = np.sum(artefact, axis=(0, 1)) * np.prod(res) / 10**3
```

### Key points in the Python code:
# 1. **DICOM Handling**: `pydicom` is used to read DICOM files and retrieve necessary metadata such as pixel spacing, slice thickness, rescale slope, and intercept.
# 2. **Numpy Arrays**: The DICOM images are stored in a 3D numpy array.
# 3. **Contour Detection**: The `skimage.measure.find_contours` function is used to detect artefact contours, similar to MATLAB's `contourROI`.
# 4. **Image Display**: `matplotlib` is used for image display and contour plotting, similar to `iw` and `contourROI` functions in MATLAB.
