#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave

CHUNK = 1024


def play(wavfile):
    print 'Im trying...'
    wf = wave.open(wavfile, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
