import numpy as np 
import scipy.signal
import matplotlib.pyplot as plt


NUM_SAMPLES_BUFFER = 400
FILTER_AFTER_N = 100
BP_LOW_CUTOFF = 20
BP_HIGH_CUTOFF = 500
ORDER = 2
LP_HIGH_CUTOFF = 10
samplingRate = 4000


########### LOW PASS 
b, a = scipy.signal.butter(ORDER, LP_HIGH_CUTOFF, 'lowpass',fs=samplingRate) 

# Show the frequency response of the filter
# w, h = signal.sosfreqz(sos, worN=fft.next_fast_len(self.sample_rate*10))
w, h = scipy.signal.freqz(b, a)
plt.figure()
plt.subplot(2, 1, 1)
db = 20*np.log10(np.maximum(np.abs(h), 1e-5))
plt.plot((samplingRate/2)*(w/np.pi), db)
plt.ylim(-105, 5)
plt.grid(True)
plt.yticks([0, -20, -40, -60, -80, -100])
plt.ylabel('Gain [dB]')
plt.title('Lowpass Filter Frequency Response')
plt.subplot(2, 1, 2)
plt.plot((samplingRate/2)*(w/np.pi), np.angle(h))
plt.grid(True)
plt.yticks([-np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi],
            [r'$-\pi$', r'$-\pi/2$', '0', r'$\pi/2$', r'$\pi$'])
plt.ylabel('Phase [rad]')
plt.xlabel('Frequency [Hz]')
plt.show()


####### BANDPASS

sos = scipy.signal.butter(ORDER, [BP_LOW_CUTOFF, BP_HIGH_CUTOFF], 'bandpass', output='sos',fs=samplingRate)
        
b, a = scipy.signal.butter(ORDER, [BP_LOW_CUTOFF, BP_HIGH_CUTOFF], 'bandpass',fs=samplingRate)
# Show the frequency response of the filter
# w, h = signal.sosfreqz(sos, worN=fft.next_fast_len(self.sample_rate*10))
# w, h = scipy.signal.freqz(b, a)
w, h = scipy.signal.sosfreqz(sos)
plt.figure()
plt.subplot(2, 1, 1)
db = 20*np.log10(np.maximum(np.abs(h), 1e-5))
plt.plot((samplingRate/2)*(w/np.pi), db)
plt.ylim(-105, 5)
plt.grid(True)
plt.yticks([0, -20, -40, -60, -80, -100])
plt.ylabel('Gain [dB]')
plt.title("Bandpass Filter Frequency Response")
plt.subplot(2, 1, 2)
plt.plot((samplingRate/2)*(w/np.pi), np.angle(h))
plt.grid(True)
plt.yticks([-np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi],
            [r'$-\pi$', r'$-\pi/2$', '0', r'$\pi/2$', r'$\pi$'])
plt.ylabel('Phase [rad]')
plt.xlabel('Frequency [Hz]')
plt.show()