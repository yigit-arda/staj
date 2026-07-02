import os
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QBrush, QFontDatabase
from PySide6.QtCore import Qt, QRectF, QPointF

def load_digital_font():
    font_paths = ["digital-7.tff", "digital-7.ttf"]
    for path in font_paths:
        if os.path.exists(path):
            font_id = QFontDatabase.addApplicationFont(path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    return families[0]
    return "Consolas"

class VerticalThermometer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 220) 
        self.setMaximumSize(140, 280)
        self.current_temp = 32.0  
        self.min_temp = -10.0
        self.max_temp = 40.0
        self.digital_font_family = load_digital_font()

    def set_range(self, min_val, max_val):
        self.min_temp = float(min_val)
        self.max_temp = float(max_val)
        self.current_temp = max(self.min_temp, min(self.current_temp, self.max_temp))
        self.update()

    def set_temperature(self, value):
        self.current_temp = max(self.min_temp, min(float(value), self.max_temp))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # --- TÜP VE ÖLÇEK BOYUTLARI ---
        tube_w = 16
        tube_h = height - 120 # Metin için biraz yer açtık
        tube_x = (width - tube_w) / 2 # Ortaya aldık
        tube_y = 20
        
        bulb_radius = 16
        bulb_cx = tube_x + (tube_w / 2)
        bulb_cy = tube_y + tube_h + 8

        scale_top_y = tube_y + 15
        scale_bottom_y = tube_y + tube_h - 5
        scale_height = scale_bottom_y - scale_top_y
        temp_range = self.max_temp - self.min_temp

        # --- ÇENTİKLER (Hizası bozulmadan korundu) ---
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        for temp_val in range(int(self.min_temp), int(self.max_temp) + 1, 10):
            ratio = (temp_val - self.min_temp) / temp_range
            tick_y = scale_bottom_y - (ratio * scale_height)
            
            painter.setPen(QPen(QColor(230, 230, 230), 2))
            painter.drawLine(QPointF(tube_x - 12, tick_y), QPointF(tube_x - 4, tick_y))
            painter.drawText(int(tube_x - 42), int(tick_y + 5), 20, 15, Qt.AlignmentFlag.AlignRight, f"{temp_val}")

        # --- CAM DIŞ TÜP ---
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.setBrush(QBrush(QColor(30, 30, 30, 150)))
        painter.drawRoundedRect(QRectF(tube_x, tube_y, tube_w, tube_h), 8, 8)
        painter.drawEllipse(QPointF(bulb_cx, bulb_cy), bulb_radius, bulb_radius)

        # --- KIRMIZI CIVA SÜTUNU ---
        current_ratio = (self.current_temp - self.min_temp) / temp_range
        liquid_top_y = scale_bottom_y - (current_ratio * scale_height)
        liquid_h = bulb_cy - liquid_top_y 
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(220, 20, 20)))
        painter.drawRoundedRect(QRectF(tube_x + 2.5, liquid_top_y, tube_w - 5, liquid_h), 4, 4)
        painter.drawEllipse(QPointF(bulb_cx, bulb_cy), bulb_radius - 2.5, bulb_radius - 2.5)

        painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
        painter.drawEllipse(QPointF(bulb_cx - 5, bulb_cy - 5), 6, 6)

        # --- 6. DİJİTAL SAYAÇ (Düzenlenmiş Hizalama) ---
        # Sayı ve dereceyi tek bir merkezde hizalamak için genişlikleri ayarladık
        text_y = int(bulb_cy + bulb_radius + 20)
        
        # Sayı kısmı (Sağa yaslı veya merkezli)
        painter.setPen(QColor(240, 240, 240))
        painter.setFont(QFont(self.digital_font_family, 26, QFont.Weight.Bold))
        
        # Sayı metni (genişliği 50, merkeze yakın)
        painter.drawText(int(width/2 - 50), text_y, 50, 40, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{int(self.current_temp)}")
        
        # Derece sembolü (sayının hemen yanına)
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(int(width/2), text_y + 5, 30, 20, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, "°C")