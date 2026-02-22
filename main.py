import numpy as np
import matplotlib.pyplot as plt

# 1. Parameter Determination
# Student numbers: 31, 26, 17
f0 = 31 + 26 + 17  # f0 = 74 Hz
f1 = f0            # 74 Hz
f2 = f0 / 2        # 37 Hz
f3 = 10 * f0       # 740 Hz

# 2. Sampling Frequency Selection
# f_max is f3 (740 Hz). Nyquist criterion: fs > 2 * f_max (1480 Hz).
# Choosing fs = 10000 Hz for high resolution.
fs = 10000 

# 3. Time Window
# Need to display at least 3 full periods. 
# The longest period is for the lowest frequency f2 (37 Hz).
T2 = 1 / f2
duration = 3 * T2 # 3 periods of the slowest signal
t = np.arange(0, duration, 1/fs)

# 4. Signal Generation
s1 = np.sin(2 * np.pi * f1 * t)
s2 = np.sin(2 * np.pi * f2 * t)
s3 = np.sin(2 * np.pi * f3 * t)
s_total = s1 + s2 + s3

# 5. Visualization - Three separate subplots
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(t, s1)
plt.title(f'f1 = {f1} Hz (f0)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t, s2)
plt.title(f'f2 = {f2} Hz (f0/2)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t, s3)
plt.title(f'f3 = {f3} Hz (10*f0)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.savefig('task1_subplots.png')

# 6. Visualization - Sum of signals
plt.figure(figsize=(10, 4))
plt.plot(t, s_total)
plt.title(f'Sum of Signals (f1 + f2 + f3)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.savefig('task1_sum.png')

print(f"f0: {f0}, f1: {f1}, f2: {f2}, f3: {f3}")