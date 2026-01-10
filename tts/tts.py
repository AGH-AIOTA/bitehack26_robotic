import wave
import os
import tempfile
import subprocess
from piper import PiperVoice

class VoiceSynthesizer:
    def __init__(self, model_name="pl_PL-zenski_wg_glos-medium.onnx"):
        """
        Initializes the model once.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, model_name)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}")

        print("Loading Piper model...")
        self.voice = PiperVoice.load(model_path)
        print("Model ready.")

    def say(self, text):
        """
        Generates audio to a temporary file and plays it immediately with 'paplay'.
        The file is deleted automatically after playing.
        """
        # Create a temp file that deletes itself when closed
        # delete=True ensures cleanup after the block ends
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav:
            
            # 1. Synthesize audio into the temp file
            with wave.open(temp_wav, "wb") as wav_file:
                self.voice.synthesize_wav(text, wav_file)
            
            # 2. IMPORTANT: Flush the internal buffer to ensure data is physically written to disk
            # otherwise 'paplay' might try to read an empty file.
            temp_wav.flush()

            # 3. Call 'paplay' using the temporary file path
            # This will block code execution until the audio finishes playing.
            try:
                subprocess.run(["paplay", temp_wav.name], check=True)
            except FileNotFoundError:
                print("Error: 'paplay' not found. Is PulseAudio installed?")
            except subprocess.CalledProcessError as e:
                print(f"Error playing audio: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    tts = VoiceSynthesizer()
    
    # This will generate, play, and clean up automatically
    tts.say("Halo HAlo")
    tts.say("POLSKA GUROM")