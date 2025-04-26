from pydub import AudioSegment
import numpy as np
import io

def convert_audio_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    wav_io = io.BytesIO()
    audio.export(wav_io, format='wav')
    wav_io.seek(0)
    return wav_io

def normalize_audio(audio_segment):
    return audio_segment.apply_gain(-audio_segment.dBFS)

def get_audio_array(audio_segment):
    return np.array(audio_segment.get_array_of_samples())

def save_audio_file(audio_segment, file_path):
    audio_segment.export(file_path, format='wav')