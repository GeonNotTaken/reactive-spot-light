import sys

from PyQt6.QtWidgets import QApplication

from cameraFeed.cameraFeedMethods import CameraWorker
from spotLight.spotLightMethods import TransparentWindow

box_positions = [(0.125, 0.1), (0.375, 0.1), (0.625, 0.1), (0.875, 0.1)]

app = QApplication(sys.argv)


worker = CameraWorker(positions=box_positions, box_size = 400)
window = TransparentWindow(box_positions=box_positions, box_height_pct=0.2)
worker.colors_updated.connect(window.set_colors)
app.aboutToQuit.connect(worker.stop)
worker.start()
window.show()
sys.exit(app.exec())
