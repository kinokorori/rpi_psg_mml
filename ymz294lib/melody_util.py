# -*- coding:utf-8 -*-

__scale_freq = []

C = 0
Cs = 1
Db = 1
D = 2
Ds = 3
Eb = 3
E = 4
F = 5
Fs = 6
Gb = 6
G = 7
Gs = 8
Ab = 8
A = 9
As = 10
Bb = 10
B = 11

def get_duration(tempo = 120, note_len = 4):
    base_ms = 60.0 / tempo
    note_rate = 4.0 / note_len
    return base_ms * note_rate

def get_freq(scale=A, octave=4):
    scale_number = 12 * octave + scale
    return __scale_freq[scale_number]    


for scale in range(88):
    ex = (scale - 57) / 12.0
    f = (2 ** ex) * 440
    __scale_freq.append(f)
    