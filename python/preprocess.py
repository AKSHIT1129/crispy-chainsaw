"""
Preprocessing & Signal Filtering Module for CSI Data
---------------------------------------------------
Implements:
1. High-pass Butterworth filtering (to remove static wall reflections).
2. Phase sanitization.
3. Principal Component Analysis (PCA) for noise reduction.
"""

import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.decomposition import PCA

def butter_bandpass_filter(data, lowcut=0.2, highcut=10.0, fs=50.0, order=4):
    """
    Applies a Butterworth bandpass filter to eliminate static clutter (DC offset)
    and high-frequency noise.
    
    :param data: 1D or 2D array of subcarrier amplitudes over time.
    :param lowcut: Minimum frequency in Hz (removes static clutter < 0.2 Hz).
    :param highcut: Maximum frequency in Hz (preserves human movement < 10 Hz).
    :param fs: Sampling frequency (packets per second).
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="bandpass")
    
    if data.ndim == 1:
        return filtfilt(b, a, data)
    else:
        filtered = np.zeros_like(data)
        for i in range(data.shape[1]):
            filtered[:, i] = filtfilt(b, a, data[:, i])
        return filtered

def apply_pca(csi_matrix, n_components=3):
    """
    Applies Principal Component Analysis across all OFDM subcarriers
    to extract dominant motion features and reduce noise.
    
    :param csi_matrix: 2D numpy array [time_steps, subcarriers]
    :param n_components: Number of principal components to return
    """
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(csi_matrix)
    return components, pca.explained_variance_ratio_

def sanitize_phase(phase_matrix):
    """
    Sanitizes phase linear drift caused by unsynchronized TX/RX clocks.
    """
    num_subcarriers = phase_matrix.shape[1]
    subcarrier_indices = np.arange(num_subcarriers)
    
    sanitized = np.zeros_like(phase_matrix)
    for t in range(phase_matrix.shape[0]):
        unwrapped = np.unwrap(phase_matrix[t, :])
        slope = (unwrapped[-1] - unwrapped[0]) / (num_subcarriers - 1)
        offset = np.mean(unwrapped)
        sanitized[t, :] = unwrapped - (slope * subcarrier_indices + offset)
        
    return sanitized
