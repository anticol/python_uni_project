import math
import numpy as np
import wave as wave
import sys
from struct import unpack

PITCHES = ['C', 'Cis', 'D', 'Es', 'E', 'F', 'Fis', 'G', 'Gis', 'A', 'Bes', 'B']


def get_tone(_freq, freq):
    pitches_len = len(PITCHES)
    log_distance = pitches_len * (math.log2(freq) - math.log2(_freq * pow(2, -(pitches_len + 9) / pitches_len)))

    tones_difference = int(log_distance % pitches_len)
    octaves_difference = int(log_distance // pitches_len)
    cents = int(round(float(100 * (log_distance % 1)),0))

    if cents >= 50:
        tones_difference += 1
        cents = - (100 - cents)

    if tones_difference >= pitches_len:
        tones_difference -= pitches_len
        octaves_difference += 1

    tone = PITCHES[tones_difference]
    if octaves_difference >= 0:
        additional_chars = ("'" * octaves_difference)
        tone = tone.lower()
    else:
        additional_chars = (',' * (-1 * octaves_difference - 1))

    tone = tone + additional_chars
    mark = '+' if cents >= 0 else ''

    return str(tone) + mark + str(cents)


def ch_avg(bytes, num_channels):
    i = 0

    newBytes = []
    while i <= (len(bytes) - num_channels):
        averaged_frame_byte = 0
        for channel_idx in range(num_channels):
            averaged_frame_byte += bytes[i + channel_idx]
        averaged_frame_byte /= num_channels
        newBytes += [averaged_frame_byte]
        i += num_channels

    return newBytes


def cluster_peaks(peaks):
    if len(peaks) == 0:
        return []

    all_cls = []
    current = []

    for p in peaks:
        freq, ampl = p

        if (current[-1][0] if len(current) > 0 else None) == freq - 1:
            current.append((freq, ampl))
        else:
            if len(current) > 0:
                all_cls.append(max(current, key=lambda tuple: tuple[1]))

            current = [(freq, ampl)]

    if len(current) > 0:
        all_cls.append(max(current, key=lambda tuple: tuple[1]))

    clusters = list(filter(lambda tuple: tuple[0] != 0, all_cls))
    return clusters


def parse_frames(music_file, frames_per_sec, num_of_sec, num_of_channels):
    total_frames = int(frames_per_sec * num_of_sec)
    parsed_bytes = unpack("%ih" % (int(num_of_channels * frames_per_sec * num_of_sec)), music_file.readframes(total_frames))
    parsed_bytes = ch_avg(parsed_bytes, int(num_of_channels))

    return parsed_bytes


def get_peaks(music_file, given_freq):
    from_window_time = 0
    to_window_time = 0.1
    frames_per_second = music_file.getframerate()
    number_of_frames = music_file.getnframes()
    seconds = number_of_frames / frames_per_second

    number_of_windows = number_of_frames // (0.1 * frames_per_second)
    number_of_windows = number_of_windows - (number_of_windows % 10)
    all_peaks = []

    if seconds >= 1:
        last_ten_windows_frames_bytes = parse_frames(music_file, frames_per_second, num_of_sec=1.0,
                                                     num_of_channels= music_file.getnchannels())

    #for _ in range(int(number_of_windows - 1)):
    while from_window_time + 1 < seconds:
        if from_window_time + 1 > seconds:
            continue

        frequency_information = np.fft.rfft(last_ten_windows_frames_bytes)
        amplitudes = list(map(lambda frequency_information: np.abs(frequency_information), frequency_information))
        avg_amplitude = sum(amplitudes) / len(amplitudes)

        window_peaks = [(frequency, amplitude) for frequency, amplitude in enumerate(amplitudes) if
                        amplitude >= 20 * avg_amplitude and amplitude != 0]

        clustered_peaks = cluster_peaks(window_peaks)
        #top 3 peaks
        top_peaks = sorted(clustered_peaks, key=lambda tuple: tuple[1])[-3:]

        if len(top_peaks) > 0:
            sorted_peaks_by_freq = sorted(top_peaks, key=lambda tuple: tuple[0])
            tones_str = ' '.join([get_tone(given_freq, freq) for freq, ampl in sorted_peaks_by_freq])

            if len(all_peaks) > 0 and all_peaks[-1]['to_time'] == from_window_time and all_peaks[-1]['result'] == tones_str:
                all_peaks[-1]['to_time'] = to_window_time
            else:
                new_peak = {'from_time': from_window_time, 'to_time': to_window_time, 'result': tones_str}
                all_peaks.append(new_peak)

        from_window_time += 0.1
        to_window_time += 0.1

        if from_window_time + 1 < seconds:
            last_window_frames_bytes = parse_frames(music_file, frames_per_second, num_of_sec=0.1,
                                                        num_of_channels= music_file.getnchannels())

            del last_ten_windows_frames_bytes[:(int(0.1 * frames_per_second))]
            last_ten_windows_frames_bytes += last_window_frames_bytes

    return all_peaks


def main():
    file_name = sys.argv[2]
    freq = int(sys.argv[1])
    #file_name = 'sample_1.wav'
    #freq = 440
    music_file = wave.open(file_name, 'rb')
    for p in get_peaks(music_file,freq):
        print('%.1f-%.1f' %(p['from_time'], p['to_time']), p['result'])


main()
