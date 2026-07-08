import os

from PySide6.QtWidgets import QWidget 
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QFontDatabase
from PySide6.QtCore import Qt, QRect, QRectF, QPointF

def load_digital_font():
    """Loads a custom digital font from local files if available.

    Returns:
        str: The name of the loaded font family, or "Consolas" if loading fails.
    """
    font_paths = ["digital-7.tff", "digital-7.ttf"]
    for path in font_paths:
        if os.path.exists(path):
            font_id = QFontDatabase.addApplicationFont(path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    return families[0]
    return "Consolas"

class VerticalAltitudeBar(QWidget):
    """A custom widget that displays a vertical altitude bar with a digital readout.

    Attributes:
        current_altitude (float): The current altitude value.
        min_altitude (float): The minimum altitude bound.
        max_altitude (float): The maximum altitude bound.
        digital_font_family (str): The font family used for the digital text display.
    """
    def __init__(self, parent=None):
        """Initializes the VerticalAltitudeBar widget.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        self.setMinimumSize(100, 220)
        self.setMaximumSize(140, 220) 
        self.current_altitude = 0.0
        self.min_altitude = 0.0
        self.max_altitude = 3000.0
        self.digital_font_family = load_digital_font()

    def set_range(self, min_val, max_val):
        """Sets the minimum and maximum altitude range for the scale.

        Args:
            min_val (float or int): The minimum altitude value.
            max_val (float or int): The maximum altitude value.
        """
        self.min_altitude = float(min_val)
        self.max_altitude = float(max_val)
        self.current_altitude = max(self.min_altitude, min(self.current_altitude, self.max_altitude))
        self.update()

    def set_altitude(self, value):
        """Updates the current altitude value and triggers a widget repaint.

        Args:
            value (float or int): The new altitude value to display.
        """
        self.current_altitude = max(self.min_altitude, min(float(value), self.max_altitude))
        self.update()

    def paintEvent(self, event):
        """Handles the paint event to draw the altitude bar, scale marks, and text.

        Args:
            event (QPaintEvent): The paint event triggered by the Qt framework.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        
        bar_width = 50
        bar_height = height - 100  
        
        
        left_space = 45 
        bar_x = left_space 
        bar_y = 20

        bar_rect = QRectF(bar_x, bar_y, bar_width, bar_height)

        
        sky_blue = QColor(135, 206, 250) 
        painter.setBrush(QBrush(sky_blue))
        painter.setPen(QPen(QColor(80, 85, 90), 2)) 
        painter.drawRect(bar_rect)

        
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        
        alt_range = self.max_altitude - self.min_altitude
        num_ticks = 3
        for i in range(num_ticks + 1):
            tick_ratio = i / num_ticks
            tick_alt = self.min_altitude + alt_range * tick_ratio
            tick_y = bar_y + bar_height - (tick_ratio * bar_height)
            
            
            painter.drawLine(int(bar_x - 8), int(tick_y), int(bar_x), int(tick_y))
            
            
            painter.drawText(0, int(tick_y - 10), int(bar_x - 12), 20, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{tick_alt:.0f}")

       
        ratio = 0.0 if alt_range == 0 else (self.current_altitude - self.min_altitude) / alt_range
        ratio = max(0.0, min(1.0, ratio))
        indicator_y = bar_y + bar_height - (ratio * bar_height)

        pointer_pen = QPen(QColor(0, 0, 0), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap)
        painter.setPen(pointer_pen)
        painter.drawLine(int(bar_x), int(indicator_y), int(bar_x + bar_width), int(indicator_y))

       
        painter.setPen(QColor(235, 235, 235))
        painter.setFont(QFont(self.digital_font_family, 20, QFont.Weight.Bold))
        
        text_val = f"{int(self.current_altitude)} m"
        text_rect_y = bar_y + bar_height + 20
        
        painter.drawText(0, int(text_rect_y), width, 20, Qt.AlignmentFlag.AlignCenter, text_val)
