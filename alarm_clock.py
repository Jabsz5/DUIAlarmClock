import serial
import time
from pydub import AudioSegment
from pydub.playback import play

audio = AudioSegment.from_mp3("1 for 1, DiMaggio.mp3")
first_10_seconds = audio[:10 * 1000]

PORT = "COM5"
BAUDRATE = 9600

def main():
    try:
        # Open serial port
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        # Give Arduino a moment to reset after opening the port
        time.sleep(2)

        print(f"Connected to {PORT} at {BAUDRATE} baud. Press Ctrl+C to stop.\n")

        while True:
            line = ser.readline()  # reads until '\n' or timeout
            if line:
                try:
                    text = line.decode("utf-8", errors="ignore").strip()
                    if text == "0":
                        print("Wake up!")
                        play(first_10_seconds)

                except UnicodeDecodeError:
                    continue  # skip weird bytes

                if text:
                    print(f"Arduino: {text}")

    except serial.SerialException as e:
        print(f"Error opening serial port {PORT}: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        try:
            ser.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
