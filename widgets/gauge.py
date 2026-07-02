import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QRectF, QPointF


class GaugeWidget(QWidget):
    """Genel amaçlı, min/max aralığında düz ibre göstergesi.

    Eskiden 'tur sayacı' (odometer) mantığındaydı; artık speedometer ile
    aynı 270 derecelik yay mantığını kullanıyor ama sabit 0..max yerine
    dışarıdan verilen (min_val, max_val) aralığını gösteriyor.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(150, 150)
        self.setMaximumSize(200, 200)
        self.min_value = -10.0
        self.max_value = 10.0
        self.value = 0.0

    def set_range(self, min_val, max_val):
        self.min_value = float(min_val)
        self.max_value = float(max_val)
        self.value = max(self.min_value, min(self.value, self.max_value))
        self.update()

    def set_value(self, value):
        self.value = max(self.min_value, min(float(value), self.max_value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width, height = self.width(), self.height()
        size = min(width, height) - 40
        cx, cy = width / 2, height / 2
        radius = size / 2

        arc_rect = QRectF(cx - radius, cy - radius, size, size)
        arc_start = 225

        value_range = self.max_value - self.min_value
        ratio = 0.0 if value_range == 0 else (self.value - self.min_value) / value_range
        ratio = max(0.0, min(1.0, ratio))

        # Dış çerçeve
        painter.setPen(QPen(QColor(80, 85, 90), 2))
        painter.drawEllipse(arc_rect)

        # Arka plan (sabit) yay
        painter.setPen(QPen(QColor(45, 48, 50), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawArc(arc_rect, arc_start * 16, -270 * 16)

        # Aktif değer yayı
        current_span = -(ratio * 270)
        painter.setPen(QPen(QColor(0, 200, 255), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawArc(arc_rect, arc_start * 16, int(current_span * 16))

        # Çentikler ve uç değer etiketleri
        painter.save()
        font = QFont("Segoe UI", 9, QFont.Weight.Bold)
        painter.setFont(font)
        start_rot = 135

        num_main_ticks = 4
        for i in range(num_main_ticks + 1):
            tick_ratio = i / num_main_ticks
            rot_angle = start_rot + tick_ratio * 270
            tick_val = self.min_value + value_range * tick_ratio
 
            painter.save()
            painter.translate(cx, cy)
            painter.rotate(rot_angle)
            painter.setPen(QPen(QColor(200, 200, 200), 2))
            painter.drawLine(int(radius - 18), 0, int(radius - 8), 0)

            painter.translate(radius - 34, 0)
            painter.rotate(-rot_angle)
            painter.setPen(QColor(220, 220, 220))
            painter.drawText(QRectF(-20, -12, 40, 24), Qt.AlignmentFlag.AlignCenter, f"{tick_val:.0f}")
            painter.restore()
        painter.restore()

        # İbre
        needle_angle = start_rot + (ratio * 270)
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(needle_angle)
        painter.setPen(QPen(QColor(255, 60, 60), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(0, 0, int(radius - 24), 0)
        painter.setBrush(QColor(255, 60, 60))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(0, 0), 6, 6)
        painter.restore()

        # Dijital değer
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Consolas", 15, QFont.Weight.Bold))
        painter.drawText(QRectF(cx - 55, cy + radius * 0.32, 110, 26),
                          Qt.AlignmentFlag.AlignCenter, f"{self.value:.2f}")
        

    

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width, height = self.width(), self.height()
        # Kenarlardan biraz boşluk bırakalım
        size = min(width, height) - 40
        cx, cy = width / 2, height / 2
        radius = size / 2

        # Halkanın çizileceği dörtgen alan
        arc_rect = QRectF(cx - radius, cy - radius, size, size)

        value_range = self.max_value - self.min_value
        ratio = 0.0 if value_range == 0 else (self.value - self.min_value) / value_range
        ratio = max(0.0, min(1.0, ratio))

        # --- 1. Arka Plan Halkası ---
        # Saydamımsı, koyu renkli tam bir daire (360 derece)
        bg_pen = QPen(QColor(45, 48, 50), 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawEllipse(arc_rect)

        # --- 2. Aktif İlerleme Yayı ---
        # Üstten (saat 12 yönünden) başlaması için 90 dereceyi seçiyoruz.
        # PySide'da açılar 16 ile çarpılarak verilir ve negatif değerler saat yönünü ifade eder.
        arc_start = 90
        current_span = -(ratio * 360) 
        
        active_pen = QPen(QColor(0, 200, 255), 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(active_pen)
        # Sadece değer 0'dan büyükse yay çiz (hata vermemesi için küçük bir kontrol)
        if current_span != 0:
            painter.drawArc(arc_rect, arc_start * 16, int(current_span * 16))

        # --- 3. Merkezdeki Dijital Değer ---
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Consolas", 24, QFont.Weight.Bold))
        
        # Yazıyı widget'ın tam ortasına hizalıyoruz
        text_rect = QRectF(0, 0, width, height)
        # İstersen "{self.value:.2f}" kısmını ".1f" yaparak tek ondalığa düşürebilirsin
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, f"{self.value:.2f}")