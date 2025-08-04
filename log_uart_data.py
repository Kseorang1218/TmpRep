import serial
import time

PORT = 'COM5'
BAUD = 115200
SAVE_FILE = 'data1.txt'
MAX_SAMPLES = 10240

samples = []

try:
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print(f"[INFO] UART opened on {PORT}")
        while len(samples) < MAX_SAMPLES:
            line = ser.readline()
            if not line:
                print("[WARN] 읽기 타임아웃 발생, 데이터 없음")
                time.sleep(0.5)
                continue

            decoded_line = line.decode(errors='ignore').strip()
            # 수신 데이터 디버그용 출력
            # print(f"수신: {decoded_line}")

            if decoded_line == "END":
                print("\n[INFO] STM32 송신 종료")
                break

            try:
                sample = float(decoded_line)
                samples.append(sample)

                if len(samples) % 500 == 0:
                    print(f"[INFO] 수신 중... {len(samples)} / {MAX_SAMPLES} samples", flush=True)
            except ValueError:
                continue

    print(f"[INFO] 저장 완료: {SAVE_FILE} ({len(samples)} samples)")

    with open(SAVE_FILE, 'w') as f:
        for s in samples:
            f.write(f"{s}\n")

except serial.SerialException as e:
    print(f"[ERROR] 포트 열기 실패: {e}")
