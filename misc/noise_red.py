from scipy.io import wavfile
import noisereduce as nr
rate, data = wavfile.read("Audio-20220905-182709.wav")
print(rate, data, data.shape)
reduced_noise = nr.reduce_noise(y=data, sr=rate)
# wavfile.write("Audio-20220905-182709-Reduced.wav", rate, reduced_noise)