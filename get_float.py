import serial
import time

PORT = 'COM5'
BAUD = 921600
SAVE_FILE = 'data_from_float2.txt'
RECORD_DURATION = 10  # seconds

def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    start_time = time.time()

    with open(SAVE_FILE, 'w') as f:
        while time.time() - start_time < RECORD_DURATION:
            line = ser.readline().decode(errors='ignore').strip()
            if line:  # 빈 줄 무시
                f.write(line + '\n')

    ser.close()
    print(f"✅ {RECORD_DURATION}초 동안 데이터 저장 완료 → {SAVE_FILE}")

if __name__ == "__main__":
    main()
