import numpy as np
import wave as wave
import sys, struct

def getWindows(file_info,frames):
    windows = []
    sample = 0
    unpacked_data = struct.iter_unpack('h',frames)
    for item in unpacked_data:
        channels = item[0]
        channels += next(unpacked_data)[0] if file_info['number_of_channels'] == 2 else 0
        sample += 1
        windows.append(channels / 2)

        if sample == file_info['frame_rate']:
            yield windows
            del windows[:]
            sample = 0

def main():
    file_name = sys.argv[1]
    #file_name = 'sample_2.wav'
    file_info = {}
    lowest_peak = np.inf
    highest_peak = -np.inf

    wave_file = wave.open(file_name,'rb')
    file_info['number_of_frames'] = wave_file.getnframes()
    file_info['samp_width'] = wave_file.getsampwidth()
    file_info['number_of_channels'] = wave_file.getnchannels()
    file_info['frame_rate']= wave_file.getframerate()
    frames = wave_file.readframes(file_info['number_of_frames'])

    for window in getWindows(file_info,frames):
        am = np.abs(np.fft.rfft(window))
        avg = np.average(am)
        peaks = np.argwhere((avg * 20) <= am)
        if len(peaks) > 0:
            if lowest_peak > peaks.min():
                lowest_peak = peaks.min()
            if highest_peak < peaks.max():
                highest_peak = peaks.max()

    if lowest_peak != np.inf and highest_peak != -np.inf:
        print('low = ' + str(lowest_peak) + ', high = ' + str(highest_peak))
    else:
        print('no peaks')
    return


main()
