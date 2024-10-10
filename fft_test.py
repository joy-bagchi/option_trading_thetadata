import numpy as np
import matplotlib.pyplot as plt

# Generate a sample time series (e.g., daily closing prices)
time = np.linspace(0, 1, 500)
signal = np.sin(2 * np.pi * 50 * time) + np.sin(2 * np.pi * 120 * time)

# Apply FFT
fft_result = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(signal), time[1] - time[0])

# Plot the signal and its FFT
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time, signal)
plt.title('Time Domain Signal')

plt.subplot(2, 1, 2)
plt.plot(frequencies, np.abs(fft_result))
plt.title('Frequency Domain Signal')

plt.show()
