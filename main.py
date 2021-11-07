import numpy as np
from scipy.signal import stft, istft
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
import warnings

warnings.filterwarnings('ignore')
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号


def read_pcm():

    return


# sampling frequency
fs = 100
# 窗函数
window = 'hann'
# frame长度
n = 256

# 构建signal
# 前一段频率为2，后一段频率为10
signal = np.cos(2*np.pi*200*np.arange(10000)/10000)
signal = np.append(signal, np.cos(2*np.pi*1000*np.arange(10000)/10000))

# STFT
f, t, Z = stft(signal, fs=fs, window=window, nperseg=n)

# 求幅值
Z = np.abs(Z)

#print(f)

# 如下图所示
plt.pcolormesh(t, f, Z, vmin=0, vmax=Z.mean()*10)
plt.show()
