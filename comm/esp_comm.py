import serial
import struct
import time

class ESP32Communicator:
    CMD_FACE  = 48  # '0'
    CMD_GIFT =  49  # '1'
    CMD_SERVO = 50  # '2'
    
    HEADER = b'\xAA\xBB'

    def __init__(self, port: str, baudrate: int = 115200):
        """
        Inicjalizuje połączenie Serial.
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self._connect()

    def _connect(self):
        try:
            print(f"[ESP32Comm] Otwieranie portu {self.port}...")
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
            # ESP32 często resetuje się po otwarciu portu, dajmy mu chwilę
            time.sleep(2) 
            print("[ESP32Comm] Połączono.")
        except serial.SerialException as e:
            print(f"[ESP32Comm] Błąd otwarcia portu: {e}")
            raise

    def close(self):
        """Zamyka port bezpiecznie."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("[ESP32Comm] Port zamknięty.")

    def _calculate_checksum(self, payload: bytes) -> int:
        """Oblicza XOR dla payloadu."""
        xor_sum = 0
        for byte in payload:
            xor_sum ^= byte
        return xor_sum

    def _send_packet(self, cmd_type: int, data_bytes: bytes):
        """
        Metoda wewnętrzna: składa nagłówek, dane i sumę kontrolną, a następnie wysyła.
        """
        if not self.ser or not self.ser.is_open:
            print("[ESP32Comm] Błąd: Port nie jest otwarty!")
            return

        try:
            # 1. Budowa Payloadu: [Typ] + [4 bajty danych]
            # struct.pack('B') -> unsigned char (1 bajt)
            payload = struct.pack('B', cmd_type) + data_bytes

            # 2. Obliczenie sumy kontrolnej
            checksum = self._calculate_checksum(payload)

            # 3. Złożenie ramki: HEADER + PAYLOAD + CHECKSUM
            packet = self.HEADER + payload + struct.pack('B', checksum)

            # 4. Wysyłka
            self.ser.write(packet)
            
        except Exception as e:
            print(f"[ESP32Comm] Błąd wysyłania: {e}")

    # --- PUBLICZNE API ---
    def sendFace(self, value: int):
        """Wysyła pojedynczą wartość int32 do oczu."""
        # <i = Little Endian, int (4 bajty)
        data = struct.pack('<i', value)
        self._send_packet(self.CMD_FACE, data)

    def sendGift(self, value: int):
        """Wysyła pojedynczą wartość int32 do ust."""
        data = struct.pack('<i', value)
        self._send_packet(self.CMD_GIFT, data)

    def sendCoords(self, x: int, y: int):
        """Wysyła dwie współrzędne int16 (np. dla serwa)."""
        # <hh = Little Endian, short, short (2+2 bajty)
        data = struct.pack('<hh', x, y)
        self._send_packet(self.CMD_SERVO, data)

    def readLogs(self):
        """Opcjonalnie: odczytuje i wypisuje to, co ESP wysyła zwrotnie (printy)."""
        if self.ser and self.ser.in_waiting:
            try:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"[ESP -> RPi]: {line}")
            except Exception:
                pass