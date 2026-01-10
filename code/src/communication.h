#include <Arduino.h>

enum Type {
    DISPLAY_EYES = 48,  // ascii '0'
    DISPLAY_MOUTH = 49, // ascii '1'
    SERVO = 50          // ascii '2'
};

struct Packet
{
    Type messageType;
    
    union Data {
        int32_t rawValue;

        int32_t eyes;
        int32_t mouth;
        struct {
            int16_t x;
            int16_t y;
        } servo;
    } data;
};

using PacketCallback = void(*)(Packet);

const uint8_t HEADER_1 = 0xAA;
const uint8_t HEADER_2 = 0xBB;
const uint8_t PACKET_SIZE = 6; // 1 (Type) + 4 (Data) + 1 (Checksum)

class RPIComm {
private:
    bool _sendLogs = false;
    uint8_t _buffer[PACKET_SIZE];
    PacketCallback _callback = nullptr;
    
    // Stany maszyny stanów do odbioru
    enum State { WAITING_FOR_H1, WAITING_FOR_H2, READING_DATA };
    State state = WAITING_FOR_H1;
    uint8_t bytesRead = 0;

public:
    void begin() {
        Serial.begin(115200);
    }

    void sendLogs(bool doSend) {
        _sendLogs = doSend;
    }

    void handle() {
        while (Serial.available()) {
            uint8_t b = Serial.read();

            switch (state) {
                case WAITING_FOR_H1:
                    if (b == HEADER_1) state = WAITING_FOR_H2;
                    break;

                case WAITING_FOR_H2:
                    if (b == HEADER_2) {
                        state = READING_DATA;
                        bytesRead = 0; // Reset licznika danych
                    } else {
                        state = WAITING_FOR_H1; // Fałszywy alarm, wracamy
                    }
                    break;

                case READING_DATA:
                    _buffer[bytesRead++] = b;
                    
                    if (bytesRead >= PACKET_SIZE) {
                        // 1. Sprawdźmy sumę kontrolną (XOR)
                        uint8_t calcChecksum = 0;
                        for(int i=0; i<PACKET_SIZE-1; i++) {
                            calcChecksum ^= _buffer[i];
                        }

                        if (calcChecksum == _buffer[PACKET_SIZE-1]) {
                            // 2. Parsowanie
                            Packet p;
                            p.messageType = (Type)_buffer[0];
                            memcpy(&p.data.rawValue, &_buffer[1], 4);
                            if(_sendLogs) {
                                Serial.printf("Type: %d, data: %d\n", p.messageType, p.data.rawValue);
                            }

                            if (_callback) _callback(p);
                        } else {
                        }
                        
                        state = WAITING_FOR_H1; 
                    }
                    break;
            }
        }
    }
    
    void setPacketCallback(PacketCallback callback) {
        _callback = callback;
    }
};