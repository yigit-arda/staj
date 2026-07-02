import os

from PySide6.QtWidgets import QWidget 
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QFontDatabase
from PySide6.QtCore import Qt, QRect, QRectF, QPointF

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

class VerticalAltitudeBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Sağdan ve soldan boşluk bırakabilmek için minimum genişliği artırdık.
        self.setMinimumSize(100, 220)
        self.setMaximumSize(140, 220) 
        self.current_altitude = 0.0
        self.min_altitude = 0.0
        self.max_altitude = 3000.0
        self.digital_font_family = load_digital_font()

    def set_range(self, min_val, max_val):
        self.min_altitude = float(min_val)
        self.max_altitude = float(max_val)
        self.current_altitude = max(self.min_altitude, min(self.current_altitude, self.max_altitude))
        self.update()

    def set_altitude(self, value):
        self.current_altitude = max(self.min_altitude, min(float(value), self.max_altitude))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # 1. BAR ALANININ BOYUTLARINI TANIMLAMA
        bar_width = 50
        bar_height = height - 100  
        
        # Tasarımı merkeze almak yerine, yazılara yer açmak için barı komple sağa kaydırdık.
        # Bu değer, rakamların sol sınıra çarpmasını engeller.
        sol_bosluk = 45 
        bar_x = sol_bosluk 
        bar_y = 20

        bar_rect = QRectF(bar_x, bar_y, bar_width, bar_height)

        # 2. AÇIK MAVİ ARKA PLAN
        sky_blue = QColor(135, 206, 250) 
        painter.setBrush(QBrush(sky_blue))
        painter.setPen(QPen(QColor(80, 85, 90), 2)) 
        painter.drawRect(bar_rect)

        # 3. YAN TARAFTAKİ ÖLÇEK ÇİZGİLERİ VE RAKAMLAR
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        
        alt_range = self.max_altitude - self.min_altitude
        num_ticks = 3
        for i in range(num_ticks + 1):
            tick_ratio = i / num_ticks
            tick_alt = self.min_altitude + alt_range * tick_ratio
            tick_y = bar_y + bar_height - (tick_ratio * bar_height)
            
            # Çentik çizgisi
            painter.drawLine(int(bar_x - 8), int(tick_y), int(bar_x), int(tick_y))
            
            # Çentik yazısı. Çizimi sola doğru taşırmadan çentiklerin yanına hizalıyoruz.
            # X başlangıcını 0'a çekerek kırpılmayı engelledik, genişliği bar'ın hemen önüne kadar verdik.
            painter.drawText(0, int(tick_y - 10), int(bar_x - 12), 20, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{tick_alt:.0f}")

        # 4. ANLIK YÜKSEKLİK SİYAH ÇİZGİSİ
        ratio = 0.0 if alt_range == 0 else (self.current_altitude - self.min_altitude) / alt_range
        ratio = max(0.0, min(1.0, ratio))
        indicator_y = bar_y + bar_height - (ratio * bar_height)

        pointer_pen = QPen(QColor(0, 0, 0), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap)
        painter.setPen(pointer_pen)
        painter.drawLine(int(bar_x), int(indicator_y), int(bar_x + bar_width), int(indicator_y))

        # 5. BARIN ALTINDAKİ DİJİTAL YAZI
        painter.setPen(QColor(235, 235, 235))
        painter.setFont(QFont(self.digital_font_family, 20, QFont.Weight.Bold))
        
        text_val = f"{int(self.current_altitude)} m"
        text_rect_y = bar_y + bar_height + 20
        # Metni tüm genişliğe yayıp ortalıyoruz (bar sağa kaysa da metin widget ortasında durur)
        painter.drawText(0, int(text_rect_y), width, 20, Qt.AlignmentFlag.AlignCenter, text_val)