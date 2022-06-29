
from filtering_functions import *
import matplotlib.pyplot as plt


test_data = np.random.normal(0, 1, 19341)
print(np.shape(test_data))

print(np.shape(test_data)[0])
# print(test_data.shape(1))

test_data_transpose = np.transpose(test_data)

b, a = scipy.signal.butter(5, [5, 500], 'bandpass',fs=4000) #analog=True
bandpass_filtered_data = scipy.signal.filtfilt(b, a, test_data)
    
bandpass_filtered_data_transpose = scipy.signal.filtfilt(b, a, test_data_transpose)
    
filtered_data = bandpass_filter(test_data, 5, 500, 5, 4000)

print(np.all(bandpass_filtered_data == bandpass_filtered_data_transpose))
plt.plot(test_data)
plt.plot(bandpass_filtered_data)
plt.plot(bandpass_filtered_data_transpose)
plt.plot(filtered_data)
plt.legend(['Raw','Filtered', 'Transpose', 'Filtered with func'])
plt.show()
