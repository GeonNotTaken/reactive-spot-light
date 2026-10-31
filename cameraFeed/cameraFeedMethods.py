import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal


class CameraWorker(QThread):
    # Signal that sends a tuple of (R, G, B) floats
    colors_updated = pyqtSignal(list)

    def __init__(self, positions=None, box_size=400, Parent=None):
        super().__init__()
        self._running = True
        self.positions = positions if positions else [(0.5, 0.5)]
        self.box_size = box_size

    def overall_avg_color(self, img):
        if img.size == 0:
            return np.array([0.0, 0.0, 0.0])
        avg_color_per_row = np.average(img, axis=0)
        return np.average(avg_color_per_row, axis=0)

    def run(self):
        cam = cv2.VideoCapture(1)

        if not cam.isOpened():
            print("Error: Could not open webcam.")
            return
        
        half = self.box_size // 2
        while self._running:
            ret, img = cam.read()
            if not ret:
                continue
            
            img = cv2.flip(img, 1)

            frame_h, frame_w = img.shape[:2]

            colors = []
            for x_pct, y_pct in self.positions:
                x_center = int(frame_w * x_pct)
                y_center = int(frame_h * y_pct)

                x_start = max(0, x_center - half)
                x_end = min(frame_w, x_center + half)
                y_start = max(0, y_center - half)
                y_end = min(frame_h, y_center + half)

                roi = img[y_start:y_end, x_start:x_end]
                avg = self.overall_avg_color(roi)
                r, g, b = avg[2], avg[1], avg[0]
                colors.append((float(r), float(g), float(b)))

                
            self.colors_updated.emit(colors)
            
        cam.release()
        cv2.destroyAllWindows()

    def stop(self):
        self._running = False
        self.quit()
        self.wait()