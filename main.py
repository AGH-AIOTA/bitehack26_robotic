import time
from esp_comm import ESP32Communicator
from tts import VoiceSynthesizer

PORT = '/dev/ttyUSB0'
tts = VoiceSynthesizer()

def main():
    try:
        esp = ESP32Communicator(PORT)

        tts.say("Rozpoczynam sterowanie!")
        print("Rozpoczynam sterowanie...")
        
        licznik = 0
        
        while True:
            esp.sendEyes(100 + licznik)
            
            #esp.sendMouth(-500) 

            x = licznik % 100
            y = (licznik * 2) % 200
            #esp.sendCoords(x, y)

            print(f"Wysłano pętlę nr {licznik}")

            esp.readLogs()

            licznik += 1
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nZatrzymano przez użytkownika.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    main()