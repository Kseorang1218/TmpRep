import serial
import time

PORT = 'COM5'
BAUD = 115200
SAVE_FILE = '6204_B_1400_1.txt'
DURATION_SECONDS = 15  # 수집 시간 (초)

samples = []

try:
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print(f"[INFO] UART opened on {PORT}")
        start_time = time.time()
        
        while (time.time() - start_time) < DURATION_SECONDS:
            line = ser.readline()
            if not line:
                print("[WARN] 읽기 타임아웃 발생, 데이터 없음")
                continue

            decoded_line = line.decode(errors='ignore').strip()
            # print(f"수신: {decoded_line}")  # 디버깅용

            if decoded_line == "END":
                print("\n[INFO] STM32 송신 종료")
                break

            try:
                sample = float(decoded_line)
                samples.append(sample)

                if len(samples) % 500 == 0:
                    elapsed = time.time() - start_time
                    print(f"[INFO] 수신 중... {len(samples)} samples, 경과 시간: {elapsed:.1f}초", flush=True)
            except ValueError:
                continue

    print(f"[INFO] 저장 완료: {SAVE_FILE} ({len(samples)} samples)")

    with open(SAVE_FILE, 'w') as f:
        for s in samples:
            f.write(f"{s}\n")

except serial.SerialException as e:
    print(f"[ERROR] 포트 열기 실패: {e}")
