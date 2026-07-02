import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtCore import QTimer

class ArtificialHorizon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pitch = 0.0  
        self.roll = 0.0   
        self.setMinimumSize(200, 200)

    def update_attitude(self, pitch, roll):
        self.pitch = pitch
        self.roll = roll
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 

        width = self.width()
        height = self.height()
        
        side = min(width, height)
        radius = side / 2.0

        painter.translate(width / 2.0, height / 2.0)

        clip_path = QPainterPath()
        clip_path.addEllipse(QPointF(0, 0), radius, radius)
        painter.setClipPath(clip_path)

        # -------------------------------------------------------------------
        # HAREKETLİ KATMAN
        # -------------------------------------------------------------------
        painter.save()
        painter.rotate(-self.roll)
        
        pitch_factor = radius / 45.0
        painter.translate(0, self.pitch * pitch_factor)

        bg_size = int(side * 2)

        # Gökyüzü (Mavi)
        painter.setPen(Qt.PenStyle.NoPen) 
        painter.setBrush(QColor(0, 114, 198))
        painter.drawRect(-bg_size, -bg_size, bg_size * 2, bg_size)

        # Yer (Kahverengi)
        painter.setBrush(QColor(122, 75, 41))
        painter.drawRect(-bg_size, 0, bg_size * 2, bg_size)

        # Ufuk Çizgisi
        painter.setPen(QPen(Qt.GlobalColor.white, 3))
        painter.drawLine(int(-bg_size), 0, int(bg_size), 0) 

        # -------------------------------------------------------------------
        # PITCH KADEME ÇİZGİLERİ VE SAYISAL DEĞERLER (YENİ EKLENEN KISIM)
        # -------------------------------------------------------------------
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        
        # Dinamik font ayarı
        font = painter.font()
        font.setPixelSize(int(radius * 0.12)) # Font büyüklüğünü widget'a göre ayarla
        font.setBold(True)
        painter.setFont(font)

        for i in range(-30, 40, 10):
            if i == 0: continue 
            y_pos = int(-i * pitch_factor)
            line_length = int(radius * 0.3)
            
            # Kademe çizgisini çiz
            painter.drawLine(-line_length, y_pos, line_length, y_pos)

            # Sayısal değer (Havacılık standardı olarak genelde mutlak değer kullanılır: 10, 20)
            text = str(abs(i))
            
            # Yazıların hizalanacağı görünmez kutuların boyutları
            rect_width = int(radius * 0.4)
            rect_height = int(radius * 0.2)
            margin = 5 # Çizgiden kaç piksel uzak olacağı
            
            # Sol Taraf Metni (Sağa yaslı)
            left_rect = QRectF(-line_length - rect_width - margin, y_pos - rect_height / 2, rect_width, rect_height)
            painter.drawText(left_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
            
            # Sağ Taraf Metni (Sola yaslı)
            right_rect = QRectF(line_length + margin, y_pos - rect_height / 2, rect_width, rect_height)
            painter.drawText(right_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)

        painter.restore()

        # -------------------------------------------------------------------
        # SABİT KATMAN (Uçak İkonu)
        # -------------------------------------------------------------------
        
        # Dış Çerçeve
        painter.setPen(QPen(QColor(50, 50, 50), 6))
        painter.setBrush(Qt.BrushStyle.NoBrush) 
        painter.drawEllipse(QPointF(0, 0), radius - 3, radius - 3)

        # Uçak İkonu
        pen = QPen(QColor(255, 140, 0), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        
        painter.drawPoint(0, 0)
        
        painter.drawLine(QPointF(-radius * 0.6, 0), QPointF(-radius * 0.15, 0))
        painter.drawLine(QPointF(-radius * 0.15, 0), QPointF(-radius * 0.15, radius * 0.1))
        
        painter.drawLine(QPointF(radius * 0.6, 0), QPointF(radius * 0.15, 0))
        painter.drawLine(QPointF(radius * 0.15, 0), QPointF(radius * 0.15, radius * 0.1))

'''
import sys
import math
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = QWidget()
    main_window.setWindowTitle("Artificial Horizon - Uçuş Simülasyonu")
    main_window.resize(400, 400)
    
    layout = QVBoxLayout(main_window)
    horizon_widget = ArtificialHorizon()
    layout.addWidget(horizon_widget)
    
    main_window.show()

    # ==========================================
    # GERÇEKÇİ UÇUŞ DÖNGÜSÜ (QTimer ile)
    # ==========================================
    time_counter = 0.0

    def simulate_flight():
        global time_counter
        # Zaman akış hızı (Daha yavaş manevralar için bu sayıyı küçültebilirsin)
        time_counter += 0.03  

        # 1. Ana Manevralar (Yumuşak salınımlar)
        # Uçak yavaşça tırmanıp alçalıyor (Max 15 derece)
        base_pitch = math.sin(time_counter) * 15.0 
        
        # Uçak sağa/sola yatıyor (Max 30 derece, pitch'ten daha yavaş bir periyotla)
        base_roll = math.cos(time_counter * 0.6) * 30.0 

        # 2. Çevresel Etkiler (Türbülans ve titreşim)
        # Hızlı ama çok küçük sapmalar yaratarak motor titreşimi/rüzgar hissi verir
        turbulence_pitch = math.sin(time_counter * 15) * 0.4
        turbulence_roll = math.cos(time_counter * 25) * 0.8

        # 3. Değerleri birleştir ve arayüzü güncelle
        final_pitch = base_pitch + turbulence_pitch
        final_roll = base_roll + turbulence_roll

        horizon_widget.update_attitude(pitch=final_pitch, roll=final_roll)

    # Timer'ı saniyede 50 kare (50 FPS) çalışacak şekilde kuruyoruz
    timer = QTimer()
    timer.timeout.connect(simulate_flight)
    timer.start(20) # 20 milisaniyede bir simulate_flight tetiklenir

    sys.exit(app.exec())
'''