import os
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QBrush, QFontDatabase
from PySide6.QtCore import Qt, QRectF, QPointF


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


class ProfessionalSpeedometer(QWidget):
    """A custom widget that displays a professional circular speedometer gauge.

    Features a metallic frame, dynamic arc coloring based on warning thresholds, 
    scale ticks, an animated needle, and a central digital readout.

    Attributes:
        current_value (float): The current numeric value displayed by the speedometer.
        min_value (float): The minimum allowable value.
        max_value (float): The maximum allowable value.
        warn_ratio (float): The threshold ratio (0.0 to 1.0) at which the arc begins 
            transitioning to warning colors.
        digital_font_family (str): The font family used for the central digital text.
    """
    def __init__(self, parent=None):
        """Initializes the ProfessionalSpeedometer widget.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.setMinimumSize(180, 180)
        self.setMaximumSize(240, 240)
        self.current_value = 0.0
        self.min_value = 0.0
        self.max_value = 50.0
        
        self.warn_ratio = 0.6
        self.digital_font_family = load_digital_font()

    def set_range(self, min_val, max_val):
        """Sets the minimum and maximum boundary limits for the gauge.

        Args:
            min_val (float or int): The minimum boundary value.
            max_val (float or int): The maximum boundary value.
        """
         
        self.min_value = float(min_val)
        self.max_value = float(max_val)
        self.current_value = max(self.min_value, min(self.current_value, self.max_value))
        self.update()

    def set_value(self, value):
        """Updates the current value of the speedometer and triggers a repaint.

        Args:
            value (float or int): The new value to be displayed.
        """
        self.current_value = max(self.min_value, min(float(value), self.max_value))
        self.update()

    def paintEvent(self, event):
        """Handles the paint event to render the speedometer components.

        Draws the metallic frame, background track, dynamic color arc, 
        scale ticks, needle, and the central digital readout.

        Args:
            event (QPaintEvent): The paint event triggered by the Qt framework.
        """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height) - 40
        cx = width / 2
        cy = height / 2
        radius = size / 2

        rect_x = cx - radius
        rect_y = cy - radius
        arc_rect = QRectF(rect_x, rect_y, size, size)
        arc_start = 225

        value_range = self.max_value - self.min_value
        ratio = 0.0 if value_range == 0 else (self.current_value - self.min_value) / value_range
        ratio = max(0.0, min(1.0, ratio))

        
        painter.save()
        frame_pen = QPen(QColor(80, 85, 90), 2)
        painter.setPen(frame_pen)
        painter.drawEllipse(arc_rect)
        painter.restore()

        
        base_pen = QPen(QColor(45, 48, 50), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(base_pen)
        painter.drawArc(int(rect_x), int(rect_y), int(size), int(size), arc_start * 16, -270 * 16)

        
        current_span = -(ratio * 270)

        if ratio > 0:
            if ratio <= self.warn_ratio:
                active_pen = QPen(QColor(220, 225, 230), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(active_pen)
                painter.drawArc(arc_rect, arc_start * 16, int(current_span * 16))
            else:
                active_pen = QPen(QColor(220, 225, 230), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(active_pen)
                warn_span = -(self.warn_ratio * 270)
                painter.drawArc(arc_rect, arc_start * 16, int(warn_span * 16))

                factor = (ratio - self.warn_ratio) / (1.0 - self.warn_ratio)
                r = int(211 + (192 - 211) * factor)
                g = int(84 + (41 - 84) * factor)
                b = int(0 + (43 - 0) * factor)

                high_pen = QPen(QColor(r, g, b), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(high_pen)
                start_angle_warn = arc_start + warn_span
                span_remaining = current_span - warn_span
                painter.drawArc(arc_rect, int(start_angle_warn * 16), int(span_remaining * 16))

        # 4. ÇENTİKLER VE RAKAMLAR
        painter.save()
        font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        painter.setFont(font)
        start_rot = 135

        # Ara Çentikler
        sub_ticks = 50
        for s in range(sub_ticks + 1):
            rot_angle = start_rot + (s / sub_ticks) * 270
            painter.save()
            painter.translate(cx, cy)
            painter.rotate(rot_angle)
            painter.setPen(QPen(QColor(140, 145, 150), 1))
            painter.drawLine(int(radius - 15), 0, int(radius - 8), 0)
            painter.restore()

        # Ana Çentikler (aralığı 5 eşit parçaya böl)
        num_main_ticks = 5
        for i in range(num_main_ticks + 1):
            tick_ratio = i / num_main_ticks
            tick_val = self.min_value + value_range * tick_ratio
            rot_angle = start_rot + tick_ratio * 270

            painter.save()
            painter.translate(cx, cy)
            painter.rotate(rot_angle)
            painter.setPen(QPen(QColor(240, 240, 240), 2))
            painter.drawLine(int(radius - 20), 0, int(radius - 8), 0)

            painter.translate(radius - 35, 0)
            painter.rotate(-rot_angle)
            painter.setPen(QColor(240, 240, 240))
            painter.drawText(QRectF(-20, -15, 40, 30), Qt.AlignmentFlag.AlignCenter, f"{tick_val:.0f}")
            painter.restore()

        painter.restore()

        # 5. MAVİ İBRE
        needle_angle = 135 + (ratio * 270)

        painter.save()
        painter.translate(cx, cy)
        painter.rotate(needle_angle)

        blue_color = QColor(0, 130, 255)
        needle_pen = QPen(blue_color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, int(radius - 22), 0)

        painter.setBrush(QBrush(blue_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(0, 0), 6, 6)
        painter.restore()

        # 6. DİJİTAL MERKEZ DEĞERİ
        if ratio <= self.warn_ratio:
            digi_color = QColor(235, 235, 235)
        else:
            factor = (ratio - self.warn_ratio) / (1.0 - self.warn_ratio)
            r = int(211 + (192 - 211) * factor)
            g = int(84 + (41 - 84) * factor)
            b = int(0 + (43 - 0) * factor)
            digi_color = QColor(r, g, b)

        painter.setPen(digi_color)
        painter.setFont(QFont(self.digital_font_family, 14, QFont.Weight.Bold))
        painter.drawText(int(cx - 50), int(cy + 10), 100, 40, Qt.AlignmentFlag.AlignCenter, f"{self.current_value:.1f}")
