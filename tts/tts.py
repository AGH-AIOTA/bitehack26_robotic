import wave
from piper import PiperVoice

voice = PiperVoice.load("pl_PL-zenski_wg_glos-medium.onnx")
with wave.open("test.wav", "wb") as wav_file:
    voice.synthesize_wav("Co przeszkadza księdzu uprawiać seks? Plecaczek...!", wav_file)
