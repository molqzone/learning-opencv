import cv2
import numpy as np
from picamera2 import Picamera2

def main():
    picam2 = Picamera2()
    
    config = picam2.create_video_configuration(main={"format": "XRGB8888", "size": (640, 480)})
    picam2.configure(config)

    picam2.start()
    print("Official camera started!")

    try:
        while True:
            frame = picam2.capture_array()

            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
 
            edges = cv2.Canny(frame_bgr, 100, 200)

            # Create colored edge overlay
            edges_colored = np.zeros_like(frame_bgr)
            edges_colored[edges != 0] = [0, 255, 0]  # Green edges
            result = cv2.addWeighted(frame_bgr, 0.7, edges_colored, 0.3, 0)

            ratio = np.mean(edges)
            color = "\033[92m" if ratio > 0.05 else "\033[93m"  # Green or Yellow
            print(f"{color}Frame capture normal - edge pixel ratio: {ratio:.2f}\033[0m", end="\r")

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()