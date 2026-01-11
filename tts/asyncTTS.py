import wave
import os
import tempfile
import subprocess
import threading
import queue
from piper import PiperVoice

class AsyncVoiceSynthesizer:
    def __init__(self, model_name="pl_PL-zenski_wg_glos-medium.onnx"):
        """
        Inicjalizuje model oraz uruchamia wątek pracujący w tle.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, model_name)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Nie znaleziono modelu: {model_path}")

        print("Ładowanie modelu Piper...")
        self.voice = PiperVoice.load(model_path)
        print("Model gotowy.")

        # --- Konfiguracja Asynchroniczności ---
        # Kolejka FIFO (First In, First Out)
        self.queue = queue.Queue()
        
        # Flaga do zatrzymywania wątku (opcjonalnie)
        self.running = True

        # Uruchamiamy wątek, który będzie przetwarzał kolejkę
        # daemon=True oznacza, że wątek zamknie się sam, gdy główny program się zakończy
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def _worker_loop(self):
        """
        To jest funkcja działająca w osobnym wątku.
        Czeka na tekst w kolejce, a potem go przetwarza.
        """
        while self.running:
            try:
                # Pobierz tekst z kolejki (blokuje, jeśli kolejka jest pusta)
                text = self.queue.get(timeout=1) 
            except queue.Empty:
                continue

            # Jeśli otrzymamy None, to sygnał do zakończenia pracy (tzw. poison pill)
            if text is None:
                self.queue.task_done()
                break

            # Wykonaj właściwą, blokującą pracę (synteza + odtwarzanie)
            self._synthesize_and_play(text)
            
            # Oznacz zadanie jako wykonane
            self.queue.task_done()

    def _synthesize_and_play(self, text):
        """
        Prywatna metoda wykonująca "ciężką pracę".
        Jest wywoływana tylko przez wątek roboczy (worker).
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav:
                with wave.open(temp_wav, "wb") as wav_file:
                    self.voice.synthesize_wav(text, wav_file)
                
                temp_wav.flush()

                # To blokuje tylko wątek roboczy, główny program działa dalej!
                subprocess.run(["paplay", temp_wav.name], check=True)
                
        except Exception as e:
            print(f"Błąd podczas syntezy/odtwarzania: {e}")

    def say(self, text):
        """
        Dodaje tekst do kolejki i natychmiast wraca.
        Nie blokuje programu.
        """
        self.queue.put(text)

    def wait(self):
        """
        Opcjonalnie: Czeka, aż wszystkie komunikaty z kolejki zostaną wypowiedziane.
        """
        self.queue.join()

    def stop(self):
        """
        Bezpieczne zatrzymanie wątku.
        """
        self.queue.put(None) # Wysyłamy sygnał stopu
        self.worker_thread.join()

# --- Przykład użycia ---
if __name__ == "__main__":
    import time

    tts = AsyncVoiceSynthesizer()
    
    print("--- Start ---")
    
    # Te wywołania są teraz błyskawiczne (nie czekają na audio)
    tts.say("To jest pierwsza wiadomość.") 
    tts.say("A to druga, dodana do kolejki natychmiast po pierwszej.")
    tts.say("System działa asynchronicznie.")

    print("--- Komendy wydane, program może robić co innego ---")
    
    # Symulacja innej pracy programu głównego
    for i in range(5):
        print(f"Główny program liczy... {i}")
        time.sleep(0.5)

    print("--- Czekam na dokończenie mówienia (opcjonalne) ---")
    tts.wait()
    print("--- Koniec ---")