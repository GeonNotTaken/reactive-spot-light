from PyQt6.QtCore import QPointF, QRect, Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen, QRadialGradient
from PyQt6.QtWidgets import QApplication, QWidget


class TransparentWindow(QWidget):
    def __init__(self, box_positions=None, box_height_pct=0.2):
        
        super().__init__()
        self.setWindowTitle("Transparent Window")
        screen = QApplication.primaryScreen().geometry()
        self.screen_width = int(screen.width())
        self.screen_height = int(screen.height())
        self.resize(self.screen_width, self.screen_height)
        
        
        self.box_positions = box_positions if box_positions else [(0.5, 0.5)]
        self.box_height_pct = box_height_pct
        self.box_height = int(self.screen_height * self.box_height_pct)
        
        self.num_boxes = len(self.box_positions)
        self.box_width = self.screen_width // self.num_boxes

        
        self.colors = [QColor("#FF5733") for _ in self.box_positions]

        # Make the background transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def set_colors(self, colors):   # ✅ one parameter — the grid
        self.colors = [QColor(int(r), int(g), int(b)) for (r, g, b) in colors]
        self.update()
        
    def _outline_path(self, rect: QRect, radius_left: int, radius_right: int):
        path = QPainterPath()
        path.moveTo(rect.left(), rect.bottom())  # bottom-left (always sharp)

        # Left edge up to top-left corner
        path.lineTo(rect.left(), rect.top() + radius_left)
        if radius_left > 0:
            path.quadTo(
                rect.left(), rect.top(),
                rect.left() + radius_left, rect.top()
            )
        else:
            path.lineTo(rect.left(), rect.top())

        # Across the top to the top-right corner
        path.lineTo(rect.right() - radius_right, rect.top())
        if radius_right > 0:
            path.quadTo(
                rect.right(), rect.top(),
                rect.right(), rect.top() + radius_right
            )
        else:
            path.lineTo(rect.right(), rect.top())

        # Down the right edge, then close (bottom-right is always sharp)
        path.lineTo(rect.right(), rect.bottom())
        path.closeSubpath()
        return path
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        radius = 50
        y_center = int(self.screen_height * self.box_positions[0][1])
        half_h = self.box_height // 2
        
        for i in range(self.num_boxes):
            x_start = i * self.box_width
            # Last box absorbs any leftover pixels from integer division
            width = self.box_width if i < self.num_boxes - 1 else (self.screen_width - x_start)

            rect = QRect(
                x_start,
                y_center - half_h,
                width,
                self.box_height,
            )
            
            radius_left = radius if i == 0 else 0
            radius_right = radius if i == self.num_boxes - 1 else 0
            
            path = self._outline_path(rect, radius_left, radius_right)
            
            color = self.colors[i] if i < len(self.colors) else QColor("#FF5733")
                    
            gradient = QRadialGradient(
                QPointF(rect.center()),
                max(rect.width(), rect.height()) / 1.5
                )
        
            color_start = QColor(color)
            color_start.setAlpha(255)
            gradient.setColorAt(0, color_start)
            
            color_end = QColor(color)
            color_end.setAlpha(0)
            gradient.setColorAt(1, color_end)

            painter.setBrush(gradient)
            painter.setPen(QPen(QColor(0, 0, 0, 200), 0))
            painter.drawPath(path)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

