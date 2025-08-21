import serial
import struct
import time

PORT = 'COM5'
BAUD = 921600
SAVE_FILE = '1400_N_2.txt'
RECORD_DURATION = 10  # seconds
SCALE_FACTOR =  0.10197 / 32550.0


def main():
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    start_time = time.time()
    buffer = bytearray()
    data = []

    with open(SAVE_FILE, 'w') as f:
        while time.time() - start_time < RECORD_DURATION:
            # UART에서 들어온 모든 데이터 읽기
            buffer += ser.read(1024)

            # 헤더(0xAA55) + float(4바이트) 단위로 처리
            while len(buffer) >= 6:
                if buffer[0] == 0xAA and buffer[1] == 0x55:
                    float_bytes = buffer[2:6]
                    raw_val = struct.unpack('<f', float_bytes)[0]
                    scaled_val = raw_val * SCALE_FACTOR
                    data.append(scaled_val)
                    f.write(f"{scaled_val}\n")
                    buffer = buffer[6:]
                else:
                    buffer.pop(0)
    ser.close()
    print(f"✅ {RECORD_DURATION}초 동안 데이터 저장 완료 → {SAVE_FILE}")

if __name__ == "__main__":
    main()
