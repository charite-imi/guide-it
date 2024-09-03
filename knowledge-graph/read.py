import pydicom
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

dicom_file_path = 'dataset/1.2.392.200036.9116.2.2426555318.1479253696.86031.1.260.dcm'

ds = pydicom.dcmread(dicom_file_path)

hu_values = ds.pixel_array.flatten()


hist, bin_edges = np.histogram(hu_values, bins=50)

X = hist.reshape(-1, 1)


n_components = 2
gmm = GaussianMixture(n_components=n_components, random_state=0).fit(X)

labels = gmm.predict(X)

plt.figure(figsize=(10, 6))
plt.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), edgecolor='black', align="edge")
plt.title('HU Histogram with GMM Components')
plt.xlabel('Hounsfield Units (HU)')
plt.ylabel('Frequency')

for i in range(n_components):
    plt.axvline(x=bin_edges[np.argmax(gmm.means_[i])], color='r', linestyle='--')

plt.show()

