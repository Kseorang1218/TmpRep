import serial
import time

PORT = 'COM5'
BAUD = 921600
SAVE_FILE = 'data_bin2.txt'
RECORD_DURATION = 10  # 초 단위

SCALE_FACTOR = 0.10197 / 32550.0

samples = []

try:
    with serial.Serial(PORT, BAUD, timeout=0) as ser:
        print(f"[INFO] UART opened on {PORT}")
        start_time = time.time()
        leftover = b''

        while time.time() - start_time < RECORD_DURATION:
            data = ser.read(ser.in_waiting or 4096)
            if not data:
                continue

            data = leftover + data
            n_bytes = len(data) - (len(data) % 3)
            chunk = data[:n_bytes]
            leftover = data[n_bytes:]

            # 여기서 바로 chunk 처리
            for i in range(0, len(chunk), 3):
                b0, b1, b2 = chunk[i:i+3]

                # 24bit signed integer 계산
                sample_int32 = b0 | (b1 << 8) | (b2 << 16)
                if sample_int32 & 0x800000:  # 음수 체크
                    sample_int32 -= 1 << 24

                # -1 ~ 1 범위로 정규화
                sample_normalized = sample_int32 / 8388608.0  # 2^23

                # 필요하면 스케일링 적용
                sample_float = sample_normalized * SCALE_FACTOR
                samples.append(sample_float)



        print(f"[INFO] 저장 완료: {SAVE_FILE} ({len(samples)} samples)")

    # 텍스트 파일로 저장
    with open(SAVE_FILE, 'w') as f:
        for s in samples:
            f.write(f"{s}\n")

except serial.SerialException as e:
    print(f"[ERROR] 포트 열기 실패: {e}")
