import numpy as np
import spleeter.audio
from scipy.signal import stft, istft
import matplotlib.pyplot as plt
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from spleeter.audio import Codec
from matplotlib.pylab import mpl
import pygame
import warnings
import time

warnings.filterwarnings('ignore')
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# 采样频率
sample_rate = 44100
# 每帧采样数
fft_size = 1152
# 窗函数
window = 'hann'
# pcm数据(二进制形式)
pcm_byte = []
# pcm数据(整数形式)
pcm_num = []
# pcm数据(修改后)
pcm_out = []
# 正变换数据
pcm_stft = []
# 逆变换数据
pcm_istft = []


# 分离人声和音频
def div(input_musicfile, output_musicfile):
    separator = Separator('spleeter:2stems')
    mp3file = AudioAdapter.load(audio_descriptor=input_musicfile, duration=600.0, sample_rate=sample_rate, )
    separator.separate_to_file(
        audio_descriptor=mp3file,
        destination=output_musicfile,
        bitrate='32k',
        codec=Codec.MP3
    )


# 读取文件中的pcm数据(二进制)
def file_read_pcm(filename):
    pcm_file = open(filename, "rb")
    pcm = pcm_file.read()
    return pcm


# 将二进制pcm数据转化为整形
def transform(pcm_file):
    length = len(pcm_file)//4
    pcm = []
    for i in range(length):
        data = int.from_bytes([pcm_file[4*i], pcm_file[4*i+1], pcm_file[4*i+2], pcm_file[4*i+3]], byteorder='big', signed=True)
        pcm.append(data)
    return pcm


# 整形转二进制pcm数据
def itransform(pcm_file, size):
    t, pcm = istft(pcm_file, fs=sample_rate, window=window, nperseg=fft_size)
    pcm = pcm[:size]

    # 四舍五入到整数
    pcm = np.round(pcm)
    pcm = pcm.astype(int)
    output = bytearray()
    for each in pcm:
        data = int(each)
        add = data.to_bytes(4, byteorder='big', signed=True)
        for e in add:
            output.append(e)
    return output


# 对时域信号进行短时傅里叶变换
def analysis(signal):
    f, t, z = stft(signal, fs=sample_rate, window=window, nperseg=fft_size)
    z_abs = np.abs(z)
    z_angle = np.angle(z)
    '''plt.pcolormesh(t, f, z, vmin=0, vmax=z.mean() * 10)
    plt.show()'''
    return z


# 音乐播放器
def play(pcm):
    pygame.mixer.init(frequency=sample_rate, channels=2, buffer=4068)
    song = pygame.mixer.Sound(pcm)
    song.play()
    time.sleep(100)


if __name__ == '__main__':
    start_time = time.time()

    in_path = "Music\\test.mp3"
    out_path = "out_music"
    # 人声分离
    div(in_path, out_path)

    '''name = "pcm.txt"
    pcm_byte = file_read_pcm(name)

    pcm_num = transform(pcm_byte)
    pcm_num_length = len(pcm_num)

    # 进行短时傅里叶变换得到时频谱
    pcm_stft = analysis(pcm_num)



    # 短时傅里叶变换逆变换重新得到时域信息
    pcm_istft = itransform(pcm_stft, pcm_num_length)

    # 播放二进制音乐流
    play(pcm_istft)'''

    end_time = time.time()
    print("It cost %.6f s" % (end_time-start_time))
