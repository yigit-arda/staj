




Screen 0: minimum 16 x 16, current 1024 x 768, maximum 32767 x 32767
HDMI-A-1 connected 1024x768+0+0 (normal left inverted right x axis y axis) 0mm x 0mm
   1024x768      59.92*+
   800x600       59.86  
   640x480       59.38  
   320x240       59.29  
   960x600       59.63  
   928x580       59.88  
   800x500       59.50  
   768x480       59.90  
   720x480       59.71  
   640x400       59.95  
   320x200       58.14  
   1024x576      59.90  
   864x486       59.92  
   720x400       59.27  
   640x350       59.28  
lease-HDMI-A-1 disconnected (normal left inverted right x axis y axis)
   1024x768      60.00 +
   800x600       60.32    56.25  
   848x480       60.00  
   640x480       59.94  













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
#altitude 
------------------------------------------------
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Qt
import functions
from indicators_config import indicatorsList


class DisplayBarWidget(QWidget):
    def __init__(self, node_id, msg_id, parent=None):
        super().__init__(parent)
        self.last_data_list = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

        self.top_row_widget = QWidget(self)
        self.top_row_layout = QHBoxLayout(self.top_row_widget)
        self.top_row_layout.setContentsMargins(5, 0, 5, 0)
        self.top_row_layout.setSpacing(15)

        self.setStyleSheet("DisplayBarWidget { background-color: #F5F5F5; border-radius: 6px; border: 1px solid #CCCCCC; }")

        text_parts = []
        if node_id: text_parts.append(f"Node: {node_id}")
        if msg_id: text_parts.append(f"MSG: {msg_id}")
        filter_text = " | ".join(text_parts)

        self.label_info = QLabel(filter_text, self)
        self.label_info.setStyleSheet("font-weight: bold; color: #0288D1;")
        self.label_info.setFixedWidth(130)
        self.top_row_layout.addWidget(self.label_info)

        self.dropdown = QComboBox(self)
        self.dropdown.addItem("Show Raw Data")

        # Dropdown'da: önce indicatorsList'te tanımlı fonksiyon adları (routing'i olanlar),
        # sonra routing'i olmayan ama functions.py'de bulunan diğer fonksiyonlar (fallback: ham sonucu yazdırır).
        listed_names = []
        for row in indicatorsList:
            fname = row[0]
            if fname not in listed_names:
                listed_names.append(fname)
                self.dropdown.addItem(fname)

        for attr_name in dir(functions):
            attr = getattr(functions, attr_name)
            if callable(attr) and not attr_name.startswith("__") and attr_name not in listed_names:
                self.dropdown.addItem(attr_name)

        self.dropdown.setFixedWidth(160)
        self.dropdown.setStyleSheet("background-color: #FFFFFF; color: #333333; border: 1px solid #BBB;")
        self.dropdown.currentIndexChanged.connect(self.refresh_display)
        self.top_row_layout.addWidget(self.dropdown)

        self.label_data = QLabel("Waiting for data...", self)
        self.label_data.setStyleSheet("color: #D32F2F; font-family: 'Consolas', monospace; font-size: 11pt; font-weight: bold;")
        self.top_row_layout.addWidget(self.label_data, stretch=1)

        self.main_layout.addWidget(self.top_row_widget)

        # --- Fonksiyonun ürettiği TÜM key'ler için dinamik olarak kurulan gösterge alanı ---
        self.indicators_container = QWidget(self)
        self.indicators_layout = QHBoxLayout(self.indicators_container)
        self.indicators_layout.setContentsMargins(5, 5, 5, 5)
        self.indicators_layout.setSpacing(20)
        self.indicators_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.indicators_container)

        self._current_keys = []       # şu an kurulu olan (key) listesi -> değişim algılamak için
        self._widget_instances = {}   # key -> gösterge QWidget'ı
        self._status_labels = {}      # key -> widget'sız (durum) QLabel'ı

    def stop_playback(self):
        # Eski oynatma kuyruğu kaldırıldı; her yeni veri anında tüm göstergelere yansıtılıyor.
        # Bağlantı kesildiğinde arayüzün API uyumluluğu için bu metod korunuyor.
        pass

    def update_live_data(self, data_list):
        self.last_data_list = data_list
        self.refresh_display()

    def _clear_indicators_layout(self):
        while self.indicators_layout.count():
            item = self.indicators_layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        self._widget_instances.clear()
        self._status_labels.clear()
        self._current_keys = []

    def _build_indicators_for(self, matched_rows):
        self._clear_indicators_layout()

        for func_name, key, indicator, label in matched_rows:
            cell = QWidget(self.indicators_container)
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(2)
            cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            title = QLabel(label, cell)
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setStyleSheet("font-weight: bold; color: #555555; font-size: 9pt;")
            cell_layout.addWidget(title)

            if indicator is not None:
                qwidget = indicator.create_instance()
                cell_layout.addWidget(qwidget, alignment=Qt.AlignmentFlag.AlignCenter)
                self._widget_instances[key] = qwidget
            else:
                value_label = QLabel("--", cell)
                value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                value_label.setStyleSheet(
                    "color: #D32F2F; font-family: 'Consolas', monospace; font-weight: bold; font-size: 12pt;"
                )
                cell_layout.addWidget(value_label)
                self._status_labels[key] = value_label

            self.indicators_layout.addWidget(cell)

        self._current_keys = [row[1] for row in matched_rows]

    def refresh_display(self):
        if not self.last_data_list:
            return

        selected_function = self.dropdown.currentText()

        # 1. HAM VERİ (RAW DATA)
        if selected_function == "Show Raw Data":
            self.label_data.setText(", ".join(self.last_data_list))
            self._clear_indicators_layout()
            return

        func = getattr(functions, selected_function, None)
        if func is None:
            self.label_data.setText("Error: fonksiyon bulunamadı")
            self._clear_indicators_layout()
            return

        matched_rows = [row for row in indicatorsList if row[0] == selected_function]

        # Seçili fonksiyon değiştiyse (veya ilk kez seçildiyse) gösterge alanını yeniden kur
        if [row[1] for row in matched_rows] != self._current_keys:
            self._build_indicators_for(matched_rows)

        try:
            result = func(self.last_data_list)
        except Exception as e:
            self.label_data.setText(f"Error: {e}")
            return

        # 2a. indicatorsList'te tanımlı (routing'i olan) fonksiyon
        if matched_rows:
            if not isinstance(result, dict):
                self.label_data.setText(f"Error: '{selected_function}' bir dict döndürmeli")
                return

            summary_parts = []
            for func_name, key, indicator, label in matched_rows:
                value = result.get(key)
                if value is None:
                    continue
                summary_parts.append(f"{label}: {value}")

                if indicator is not None and key in self._widget_instances:
                    try:
                        method_name = indicator.update_method_name()
                        update_method = getattr(self._widget_instances[key], method_name)
                        update_method(value)
                    except (TypeError, ValueError):
                        pass
                elif key in self._status_labels:
                    self._status_labels[key].setText(str(value))

            self.label_data.setText(" | ".join(summary_parts))

        # 2b. Routing'i olmayan fonksiyon: ham sonucu yazdır (gösterge yok)
        else:
            if isinstance(result, dict):
                self.label_data.setText(" | ".join(f"{k}: {v}" for k, v in result.items()))
            else:
                self.label_data.setText(str(result))

    def set_active_state(self, is_active):
        if is_active:
            self.label_info.setStyleSheet("font-weight: bold; color: #0288D1;")
            self.label_data.setStyleSheet("color: #D32F2F; font-family: 'Consolas', monospace; font-size: 11pt; font-weight: bold;")
            self.setStyleSheet("DisplayBarWidget { background-color: #F5F5F5; border-radius: 6px; border: 1px solid #CCCCCC; }")
            self.indicators_container.show()
        else:
            self.label_info.setStyleSheet("color: #9E9E9E; text-decoration: line-through;")
            self.label_data.setStyleSheet("color: #9E9E9E; font-family: 'Consolas', monospace; font-size: 11pt; font-style: italic;")
            self.setStyleSheet("DisplayBarWidget { background-color: #EAEAEA; border-radius: 6px; border: 1px dashed #BBB; }")
            self.indicators_container.hide()
            self.stop_playback()


#display_bar
--------------------------------------
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

class FilterWidget(QWidget):
    def __init__(self, node_id, msg_id, on_toggle, on_delete, parent=None):
        super().__init__(parent)
        self.node_id = node_id
        self.msg_id = msg_id
        self.is_active = True
        self.on_toggle = on_toggle
        self.on_delete = on_delete

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        text_parts = []
        if node_id: text_parts.append(f"Node: {node_id}")
        if msg_id: text_parts.append(f"MSG: {msg_id}")
        filter_text = " | ".join(text_parts)

        self.label = QLabel(filter_text, self)
        layout.addWidget(self.label)
        layout.addStretch()

        self.btn_visible = QPushButton("Active", self)
        self.btn_visible.setFixedWidth(55)
        self.btn_visible.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 10px; font-weight: bold; }")
        self.btn_visible.clicked.connect(self.toggle_active)
        layout.addWidget(self.btn_visible)

        self.btn_delete = QPushButton("X", self)
        self.btn_delete.setFixedWidth(25)
        self.btn_delete.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; }")
        self.btn_delete.clicked.connect(self.delete_filter)
        layout.addWidget(self.btn_delete)

    def toggle_active(self):
        self.is_active = not self.is_active
        if self.is_active:
            self.btn_visible.setText("Active")
            self.btn_visible.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 10px; font-weight: bold; }")
            self.label.setStyleSheet("")
        else:
            self.btn_visible.setText("Passive")
            self.btn_visible.setStyleSheet("QPushButton { background-color: #757575; color: white; font-size: 10px; font-weight: bold; }")
            self.label.setStyleSheet("color: #757575; text-decoration: line-through;")
        
        self.on_toggle(self)

    def delete_filter(self):
        self.on_delete(self)



#filter widget
------------------------------------------------------------------
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


#gauge
----------------------------------------------------------------
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


class ProfessionalSpeedometer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(180, 180)
        self.setMaximumSize(240, 240)
        self.current_value = 0.0
        self.min_value = 0.0
        self.max_value = 50.0
        # "kırmızı bölge" eşiği aralığın yüzde kaçından sonra başlasın (görsel uyarı)
        self.warn_ratio = 0.6
        self.digital_font_family = load_digital_font()

    def set_range(self, min_val, max_val):
        self.min_value = float(min_val)
        self.max_value = float(max_val)
        self.current_value = max(self.min_value, min(self.current_value, self.max_value))
        self.update()

    def set_value(self, value):
        self.current_value = max(self.min_value, min(float(value), self.max_value))
        self.update()

    def paintEvent(self, event):
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

        # 1. DIŞ METALİK ÇERÇEVE
        painter.save()
        frame_pen = QPen(QColor(80, 85, 90), 2)
        painter.setPen(frame_pen)
        painter.drawEllipse(arc_rect)
        painter.restore()

        # 2. ARKA PLAN SABİT KADRAN YAYI
        base_pen = QPen(QColor(45, 48, 50), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(base_pen)
        painter.drawArc(int(rect_x), int(rect_y), int(size), int(size), arc_start * 16, -270 * 16)

        # 3. DİNAMİK RENKLENDİRME (min..max aralığına göre)
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
        painter.setFont(QFont(self.digital_font_family, 20, QFont.Weight.Bold))
        painter.drawText(int(cx - 50), int(cy + 10), 100, 40, Qt.AlignmentFlag.AlignCenter, f"{self.current_value:.1f}")


#speedometer
---------------------------------
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


#thermometer
---------------------------------------
# functions.py
"""
Her fonksiyon, ham data_list'i (seri porttan gelen string parçaları)
işleyip anlamlı isimlerle (key) bir dict döndürür. Hangi key'in hangi
göstergeye/etikete gideceği artık burada değil, indicators_config.py
içindeki indicatorsList'te tanımlıdır.
"""


def servoValues(data_list):
    # TODO: gerçek parse mantığı data_list'in formatına göre yazılacak.
    # Şimdilik hocanın verdiği örnek sabit değerlerle iskelet:
    if not data_list:
        return {"pos": 0, "setPt": 0, "srvStatus": 0, "sensorStatus": 0}

    return {
        "pos": float(data_list[0]) if len(data_list) > 0 else 0,
        "setPt": float(data_list[1]) if len(data_list) > 1 else 0,
        "srvStatus": data_list[2] if len(data_list) > 2 else "0",
        "sensorStatus": data_list[3] if len(data_list) > 3 else "0",
    }


def speedValues(data_list):
    if not data_list:
        return {"speed": 0}
    return {"speed": float(data_list[0]) * 0.005}


def tempValues(data_list):
    if not data_list:
        return {"temp": 0}
    return {"temp": (float(data_list[0]) * 0.005) - 10}


def altValues(data_list):
    if not data_list:
        return {"alt": 0}
    return {"alt": float(data_list[0])}
    

# --- FARKLI TİPLERİ AYNI ANDA GETİREN FONKSİYON ÖRNEKLERİ ---
# Tek fonksiyon, birden fazla FARKLI tip widget'ı aynı anda besleyebilir.
# indicators_config.py'de aynı fonksiyon adına birden fazla satır tanımlayarak
# hangi key'in hangi widget'a (hangi tipte olursa olsun) gideceğini eşliyoruz.

def flightStatus(data_list):
    """Hız + sıcaklık + irtifa + bir gauge + iki metin durumu aynı anda."""
    if not data_list:
        return {"spd": 0, "tmp": 0, "alt": 0, "roll": 0, "engineStatus": "0", "gpsStatus": "0"}

    def _f(idx, default=0.0):
        try:
            return float(data_list[idx])
        except (IndexError, ValueError):
            return default

    return {
        "spd": _f(0) * 0.005,           # -> speedometer
        "tmp": (_f(1) * 0.005) - 10,    # -> thermometer
        "alt": _f(2),                   # -> altitude bar
        "roll": _f(3),                  # -> gauge (-15..15 gibi)
        "engineStatus": data_list[4] if len(data_list) > 4 else "0",   # -> düz metin
        "gpsStatus": data_list[5] if len(data_list) > 5 else "0",      # -> düz metin
    }


def servoAndTemp(data_list):
    """Servo pozisyonu (gauge) + ortam sıcaklığı (thermometer) birlikte."""
    if not data_list:
        return {"servoPos": 0, "ambientTemp": 0}

    def _f(idx, default=0.0):
        try:
            return float(data_list[idx])
        except (IndexError, ValueError):
            return default

    return {
        "servoPos": _f(0),
        "ambientTemp": (_f(1) * 0.005) - 10,
    }
  #function.py
-------------------------------
# indicator_widgets.py
"""
IndicatorWidget: bir gösterge TİPİNİN (gauge / speedometer / thermometer / altitude)
ve min-max aralığının TARİFİNİ tutan sarmalayıcı sınıf.

Önemli: Bu sınıfın kendisi bir QWidget DEĞİLDİR. Çünkü aynı "tarif"
(örn. servoGauge_1 = IndicatorWidget("gauge", -10, 10)) birden fazla
DisplayBarWidget içinde aynı anda gösterilebilir; Qt'de aynı QWidget
nesnesi iki farklı layout'a eklenemez. Bu yüzden her DisplayBar,
create_instance() çağırarak KENDİ QWidget kopyasını alır.
"""

from widgets.gauge import GaugeWidget
from widgets.speedometer import ProfessionalSpeedometer
from widgets.thermometer import VerticalThermometer
from widgets.altitude import VerticalAltitudeBar

# Her tip için: (QWidget sınıfı, değer güncelleme metodunun adı)
_WIDGET_REGISTRY = {
    "gauge":       (GaugeWidget,               "set_value"),
    "speedometer": (ProfessionalSpeedometer,    "set_value"),
    "thermometer": (VerticalThermometer,        "set_temperature"),
    "altitude":    (VerticalAltitudeBar,        "set_altitude"),
}


class IndicatorWidget:
    def __init__(self, w_type, min_val, max_val):
        if w_type not in _WIDGET_REGISTRY:
            raise ValueError(
                f"Bilinmeyen indicator tipi: '{w_type}'. "
                f"Geçerli tipler: {list(_WIDGET_REGISTRY.keys())}"
            )
        self.type = w_type
        self.min_val = min_val
        self.max_val = max_val
        self._qwidget_cls, self._update_method_name = _WIDGET_REGISTRY[w_type]

    def create_instance(self):
        """Somut bir QWidget kopyası üretir ve min/max aralığını uygular."""
        widget = self._qwidget_cls()
        if hasattr(widget, "set_range"):
            widget.set_range(self.min_val, self.max_val)
        return widget

    def update_method_name(self):
        return self._update_method_name


#indicator_widgets
---------------------------------
# indicators_config.py
"""
Burada:
  1) Kullanılacak gösterge "tarifleri" (tip + min/max) tanımlanır.
  2) indicatorsList: her satır bir (fonksiyon_adı, veri_key'i, gösterge, etiket)
     eşlemesidir. Aynı fonksiyon_adı ile birden fazla satır olabilir; bir
     fonksiyon seçildiğinde o fonksiyon_adına sahip TÜM satırlar aynı anda
     bar üzerinde gösterilir.

  widget alanı None ise, o key sadece metin (durum/flag) olarak gösterilir,
  hiçbir gösterge widget'ı çizilmez.
"""

from indicator_widgets import IndicatorWidget

# --- type, minVal, maxVal ---
servoGauge_1    = IndicatorWidget("gauge", -10, +10)
servoGauge_2    = IndicatorWidget("gauge", -15, +15)
rollGauge       = IndicatorWidget("gauge", -15, +15)
speedometer_ind = IndicatorWidget("speedometer", 0, 50)
thermometer_ind = IndicatorWidget("thermometer", -10, 40)
altitude_ind    = IndicatorWidget("altitude", 0, 3000)

# [function_adı, key_adı, indicator, etiket]
indicatorsList = [
    ["servoValues", "pos",           servoGauge_1, "Position"],
    ["servoValues", "setPt",         servoGauge_2, "Setpoint"],
    ["servoValues", "srvStatus",     None,         "Servo Status"],
    ["servoValues", "sensorStatus",  None,         "Sensor Status"],

    ["speedValues", "speed",         speedometer_ind, "Speed"],
    ["tempValues",  "temp",          thermometer_ind, "Temp"],
    ["altValues",   "alt",           altitude_ind,    "Altitude"],

    # --- Aynı fonksiyon, FARKLI tip widget'ları aynı anda besliyor ---
    ["flightStatus", "spd",            speedometer_ind, "Speed"],
    ["flightStatus", "tmp",            thermometer_ind, "Temp"],
    ["flightStatus", "alt",            altitude_ind,    "Altitude"],
    ["flightStatus", "roll",           rollGauge,        "Roll"],
    ["flightStatus", "engineStatus",   None,             "Engine"],
    ["flightStatus", "gpsStatus",      None,             "GPS"],

    ["servoAndTemp", "servoPos",       servoGauge_1,     "Servo Pos"],
    ["servoAndTemp", "ambientTemp",    thermometer_ind,  "Ambient Temp"],
]


#indicators_config
----------------------------------------
import sys
import os
import math
import functions
from datetime import datetime
from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QRectF, QPointF, QTimer, Qt, QStringListModel, QEvent
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel, 
                               QLineEdit, QMainWindow, QMenuBar, QPlainTextEdit, 
                               QPushButton, QSizePolicy, QStatusBar, QWidget, QMessageBox, 
                               QVBoxLayout, QSpacerItem, QCompleter, QListWidget, QListWidgetItem,
                               QFileDialog, QRadioButton, QButtonGroup, QFrame, QScrollArea) 
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from widgets.display_bar import DisplayBarWidget
from widgets.filter_widget import FilterWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 750)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.cb_port = QComboBox(self.centralwidget)
        self.cb_port.setObjectName(u"cb_port")
        
        self.cb_baud = QComboBox(self.centralwidget)
        self.cb_baud.setObjectName(u"cb_baud")
        
        self.date = QLabel(self.centralwidget)
        self.date.setObjectName(u"date")
        
        self.Refresh = QPushButton(self.centralwidget)
        self.Refresh.setObjectName(u"Refresh")
        font1 = QFont()
        font1.setBold(True)
        self.Refresh.setFont(font1)
        
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setStyleSheet(u"QPlainTextEdit {\n"
"    background-color: black;\n"
"    color: #00FF00; \n"
"    font-family: \"Consolas\", \"Courier New\", monospace;\n"
"    font-size: 12pt;\n"
"}")
        self.plainTextEdit.setReadOnly(True)
        
        self.start_stop = QPushButton(self.centralwidget)
        self.start_stop.setObjectName(u"start_stop")
        
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.label_node_id = QLabel(self.widget)
        self.label_node_id.setObjectName(u"label_node_id")
        self.horizontalLayout.addWidget(self.label_node_id)

        self.le_node_id = QLineEdit(self.widget)
        self.le_node_id.setObjectName(u"le_node_id")
        self.horizontalLayout.addWidget(self.le_node_id)

        self.label_msg_id = QLabel(self.widget)
        self.label_msg_id.setObjectName(u"label_msg_id")
        self.horizontalLayout.addWidget(self.label_msg_id)

        self.le_msg_id = QLineEdit(self.widget)
        self.le_msg_id.setObjectName(u"le_msg_id")
        self.horizontalLayout.addWidget(self.le_msg_id)

        self.btn_apply_filter = QPushButton(self.widget)
        self.btn_apply_filter.setObjectName(u"btn_apply_filter")
        self.horizontalLayout.addWidget(self.btn_apply_filter)

        self.btn_clear_filter = QPushButton(self.widget)
        self.btn_clear_filter.setObjectName(u"btn_clear_filter")
        self.horizontalLayout.addWidget(self.btn_clear_filter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Innovita Terminal & Aircraft UI", None))
        self.date.setText(QCoreApplication.translate("MainWindow", u"Date", None))
        self.Refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.start_stop.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.label_node_id.setText(QCoreApplication.translate("MainWindow", u"Node ID", None))
        self.label_msg_id.setText(QCoreApplication.translate("MainWindow", u"MSG ID", None))
        self.btn_apply_filter.setText(QCoreApplication.translate("MainWindow", u"Add Filter", None)) 
        self.btn_clear_filter.setText(QCoreApplication.translate("MainWindow", u"Clear Filters", None))
            
class TerminalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.serial_port = QSerialPort(self)
        self.serial_port.readyRead.connect(self.read_serial_data)

        self.active_filters = []
        
        self.log_file = None
        self.log_folder = ""
        self.base_log_name = ""
        self.current_log_index = 0
        self.log_line_count = 0
        self.MAX_LOG_SIZE = 1024 * 1024
        self.is_logging = False

        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(10, 10, 10, 10)
        self.top_layout.setSpacing(10)
        self.top_layout.addWidget(self.ui.date)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.ui.cb_port)
        self.top_layout.addWidget(self.ui.cb_baud)
        self.top_layout.addWidget(self.ui.start_stop)
        self.top_layout.addWidget(self.ui.Refresh)

        self.right_panel_layout = QVBoxLayout()
        
        self.filter_list_label = QLabel("Active Filters List", self)
        font_gauge = QFont()
        font_gauge.setBold(True)
        self.filter_list_label.setFont(font_gauge)
        
        self.filter_list_widget = QListWidget(self)
        self.filter_list_widget.setMinimumWidth(220)
        self.filter_list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        self.filter_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.right_panel_layout.addWidget(self.filter_list_label)
        self.right_panel_layout.addWidget(self.filter_list_widget)
        self.right_panel_layout.addStretch()

        # === DÜZELTME: GÖRÜNÜM GEÇİŞ BUTONU TANIMLANDI VE EKLEDİ ===
        self.btn_toggle_view = QPushButton("Switch to Terminal", self)
        self.btn_toggle_view.setStyleSheet("background-color: #008CBA; color: white; font-weight: bold; padding: 6px; border-radius: 4px;")
        self.btn_toggle_view.clicked.connect(self.toggle_center_view)
        self.right_panel_layout.addWidget(self.btn_toggle_view)

        self.btn_toggle_log = QPushButton("📂 Log Menu", self)
        self.btn_toggle_log.setStyleSheet("background-color: #3f51b5; color: white; font-weight: bold; padding: 5px;")
        self.btn_toggle_log.clicked.connect(self.toggle_log_panel)
        self.right_panel_layout.addWidget(self.btn_toggle_log)

        self.setup_log_panel()
        self.right_panel_layout.addWidget(self.log_panel)

        self.center_layout = QVBoxLayout()
        self.center_layout.addWidget(self.ui.widget)

        # === DÜZELTME: SCROLL AREA MANTIĞI TAM TANIMLANDI ===
        self.display_bars_container = QWidget(self)
        self.display_bars_layout = QVBoxLayout(self.display_bars_container)
        self.display_bars_layout.setContentsMargins(0, 5, 0, 5)
        self.display_bars_layout.setSpacing(5)
        self.display_bars_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Yukarı yasla

        self.display_scroll_area = QScrollArea(self)
        self.display_scroll_area.setWidgetResizable(True)
        self.display_scroll_area.setWidget(self.display_bars_container)
        self.display_scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # Layout'a hem scroll alanını hem terminali ekliyoruz
        self.center_layout.addWidget(self.display_scroll_area)
        self.center_layout.addWidget(self.ui.plainTextEdit)

        # Başlangıçta sadece display barlar açık, terminal gizli
        self.ui.plainTextEdit.hide()

        self.content_layout = QHBoxLayout()
        self.content_layout.addLayout(self.center_layout, stretch=4)
        self.content_layout.addLayout(self.right_panel_layout, stretch=1)

        self.main_layout = QVBoxLayout(self.ui.centralwidget)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.content_layout)

        self.data_buffer = ""
        self.node_history = []
        self.msg_history = []

        self.node_model = QStringListModel(self.node_history, self)
        self.node_completer = QCompleter(self.node_model, self)
        self.node_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.le_node_id.setCompleter(self.node_completer)
        self.ui.le_node_id.installEventFilter(self)

        self.msg_model = QStringListModel(self.msg_history, self)
        self.msg_completer = QCompleter(self.msg_model, self)
        self.msg_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.le_msg_id.setCompleter(self.msg_completer)
        self.ui.le_msg_id.installEventFilter(self)

        self.ui.start_stop.setText("Start")
        self.ui.cb_baud.addItem("Select Baud")
        self.ui.cb_baud.addItems(["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_datetime)
        self.clock_timer.start(1000)
        self.update_datetime()

        self.refresh_ports()
        
        self.ui.Refresh.clicked.connect(self.clear_terminal)
        self.ui.start_stop.clicked.connect(self.toggle_connection)
        self.ui.btn_apply_filter.clicked.connect(self.add_filter) 
        self.ui.btn_clear_filter.clicked.connect(self.clear_filters)

    def setup_log_panel(self):
        self.log_panel = QFrame(self)
        self.log_panel.setStyleSheet("QFrame { background-color: #E0E0E0; border: 1px solid #999999; border-radius: 5px; }")
        self.log_panel.hide()
        
        layout = QVBoxLayout(self.log_panel)
        layout.setContentsMargins(10, 10, 10, 10)
        
        path_layout = QHBoxLayout()
        self.le_log_path = QLineEdit(self)
        self.le_log_path.setPlaceholderText("Select Log Folder...")
        self.le_log_path.setReadOnly(True)
        self.le_log_path.setStyleSheet("background-color: white; color: black;")
        self.btn_browse_log = QPushButton("...", self)
        self.btn_browse_log.setFixedWidth(30)
        self.btn_browse_log.clicked.connect(self.browse_log_folder)
        path_layout.addWidget(self.le_log_path)
        path_layout.addWidget(self.btn_browse_log)
        layout.addLayout(path_layout)
        
        self.radio_all_logs = QRadioButton("All Logs")
        self.radio_all_logs.setChecked(True)
        self.radio_filtered_logs = QRadioButton("Filtered Logs")
        
        self.radio_all_logs.setStyleSheet("color: #212121; font-weight: bold;")
        self.radio_filtered_logs.setStyleSheet("color: #212121; font-weight: bold;")
        
        self.log_mode_group = QButtonGroup(self)
        self.log_mode_group.addButton(self.radio_all_logs)
        self.log_mode_group.addButton(self.radio_filtered_logs)
        
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_all_logs)
        radio_layout.addWidget(self.radio_filtered_logs)
        layout.addLayout(radio_layout)
        
        ctrl_layout = QHBoxLayout()
        self.btn_log_start_stop = QPushButton("Start", self)
        self.btn_log_start_stop.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_log_start_stop.clicked.connect(self.toggle_logging)
        
        self.btn_log_finish = QPushButton("Finish", self)
        self.btn_log_finish.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.btn_log_finish.clicked.connect(self.finish_logging)
        self.btn_log_finish.setEnabled(False)
        
        ctrl_layout.addWidget(self.btn_log_start_stop)
        ctrl_layout.addWidget(self.btn_log_finish)
        layout.addLayout(ctrl_layout)

    def toggle_log_panel(self):
        if self.log_panel.isHidden():
            self.log_panel.show()
            self.btn_toggle_log.setText("📂 Close Log Menu")
        else:
            self.log_panel.hide()
            self.btn_toggle_log.setText("📂 Log Menu")

    def toggle_center_view(self):
        if self.ui.plainTextEdit.isHidden():
            self.ui.plainTextEdit.show()
            self.display_scroll_area.hide()
            self.btn_toggle_view.setText("Switch to Display Bars")
            self.btn_toggle_view.setStyleSheet("background-color: #E65100; color: white; font-weight: bold; padding: 6px; border-radius: 4px;")
        else:
            self.ui.plainTextEdit.hide()
            self.display_scroll_area.show()
            self.btn_toggle_view.setText("Switch to Terminal")
            self.btn_toggle_view.setStyleSheet("background-color: #008CBA; color: white; font-weight: bold; padding: 6px; border-radius: 4px;")

    def browse_log_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory for Logs")
        if folder:
            self.log_folder = folder
            self.le_log_path.setText(folder)

    def toggle_logging(self):
        if not self.log_folder:
            QMessageBox.warning(self, "Warning", "Please select a folder for log files first.")
            return

        if not self.is_logging:
            self.is_logging = True
            self.btn_log_start_stop.setText("Stop")
            self.btn_log_start_stop.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
            self.btn_log_finish.setEnabled(True)
            self.ui.plainTextEdit.appendPlainText(f"--- LOGGING STARTED ---")
            
            if not self.base_log_name:
                self.base_log_name = f"CS_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
                self.current_log_index = 0
                self.log_line_count = 0
            
            self.check_and_open_log_file()
        else:
            self.is_logging = False
            self.btn_log_start_stop.setText("Start")
            self.btn_log_start_stop.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
            self.ui.plainTextEdit.appendPlainText(f"--- LOGGING PAUSED ---")

    def check_and_open_log_file(self):
        if self.log_file is None or self.log_file.closed:
            filename = f"{self.base_log_name}_{self.current_log_index}.csv"
            filepath = os.path.join(self.log_folder, filename)
            
            is_new_file = not os.path.exists(filepath)
            self.log_file = open(filepath, 'a', encoding='utf-8')
            
            if is_new_file:
                self.log_file.write("Timestamp,Node ID,MSG ID,Data\n")
                self.log_file.flush()

    def finish_logging(self):
        self.is_logging = False
        self.btn_log_start_stop.setText("Start")
        self.btn_log_start_stop.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_log_finish.setEnabled(False)
        
        if self.log_file and not self.log_file.closed:
            self.log_file.close()
            
        self.ui.plainTextEdit.appendPlainText(f"--- LOGGING FINISHED (Saved as {self.base_log_name}_{self.current_log_index}.csv) ---")
        
        self.base_log_name = ""
        self.current_log_index = 0
        self.log_line_count = 0

    def write_to_log(self, node_id, msg_id, data_list, is_filtered_out):
        if not self.is_logging:
            return
            
        if self.radio_filtered_logs.isChecked() and is_filtered_out:
            return

        self.check_and_open_log_file()
        
        timestamp = datetime.now().strftime('%H:%M:%S:%f')[:-3]
        data_str = ",".join(data_list) if data_list else "NO DATA"
        
        log_line = f"{timestamp},{node_id},{msg_id},{data_str}\n"
        self.log_file.write(log_line)
        self.log_file.flush()

        filename = f"{self.base_log_name}_{self.current_log_index}.csv"
        filepath = os.path.join(self.log_folder, filename)
        
        if os.path.exists(filepath) and os.path.getsize(filepath) >= self.MAX_LOG_SIZE:
            self.log_file.close()             
            self.current_log_index += 1       
            self.check_and_open_log_file()    

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if obj == self.ui.le_node_id:
                self.node_completer.setCompletionPrefix("")
                self.node_completer.complete()
            elif obj == self.ui.le_msg_id:
                self.msg_completer.setCompletionPrefix("")
                self.msg_completer.complete()
        return super().eventFilter(obj, event)

    def update_history(self, new_value, history_list, model):
        if not new_value: return
        if new_value in history_list: history_list.remove(new_value)
        history_list.insert(0, new_value)
        if len(history_list) > 5: history_list.pop()
        model.setStringList(list(history_list))

    def update_datetime(self):
        self.ui.date.setText(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    def refresh_ports(self):
        self.ui.cb_port.clear()
        self.ui.cb_port.addItem("Select Port")
        for port in QSerialPortInfo.availablePorts():
            self.ui.cb_port.addItem(port.portName())

    def clear_terminal(self):
        if QMessageBox.question(self, "Refresh", "Are you sure you want to clear the terminal?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.ui.plainTextEdit.clear()

    def add_filter(self):
        node_id_str = self.ui.le_node_id.text().strip()
        msg_id_str = self.ui.le_msg_id.text().strip()

        if not node_id_str and not msg_id_str:
            QMessageBox.warning(self, "Empty Input", "Please enter at least a Node ID or a MSG ID to add a filter.")
            return

        if node_id_str: 
            try:
                node_id_val = int(node_id_str)
                if not (0 <= node_id_val <= 15):
                    QMessageBox.warning(self, "Invalid Node ID", "Node ID must be between 0 and 15.")
                    return 
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Node ID must be a numeric value.")
                return

        if msg_id_str: 
            try:
                msg_id_val = int(msg_id_str)
                if not (0 <= msg_id_val <= 255):
                    QMessageBox.warning(self, "Invalid MSG ID", "MSG ID must be between 0 and 255.")
                    return 
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "MSG ID must be a numeric value.")
                return

        for f_obj in self.active_filters:
            if f_obj['node_id'] == node_id_str and f_obj['msg_id'] == msg_id_str:
                QMessageBox.information(self, "Duplicate Filter", "This filter has already been added to the list.")
                return

        if node_id_str: self.update_history(node_id_str, self.node_history, self.node_model)
        if msg_id_str: self.update_history(msg_id_str, self.msg_history, self.msg_model)

        display_bar = DisplayBarWidget(node_id_str, msg_id_str)
        self.display_bars_layout.addWidget(display_bar)

        item = QListWidgetItem(self.filter_list_widget)
        filter_widget = FilterWidget(node_id_str, msg_id_str, self.on_filter_changed, self.remove_single_filter, self)
        item.setSizeHint(filter_widget.sizeHint())
        self.filter_list_widget.addItem(item)
        self.filter_list_widget.setItemWidget(item, filter_widget)

        self.active_filters.append({
            'node_id': node_id_str,
            'msg_id': msg_id_str,
            'is_active': True,
            'display_bar': display_bar,
            'filter_widget': filter_widget,
            'list_item': item
        })

        info = f"Added Filter -> Node: '{node_id_str or 'Any'}', MSG: '{msg_id_str or 'Any'}'"
        self.ui.plainTextEdit.appendPlainText(f"--- {info} ---")

        self.ui.le_node_id.clear()
        self.ui.le_msg_id.clear()

    def on_filter_changed(self, triggered_widget):
        for f_obj in self.active_filters:
            if f_obj['filter_widget'] == triggered_widget:
                f_obj['is_active'] = triggered_widget.is_active
                f_obj['display_bar'].set_active_state(triggered_widget.is_active)
                break
        self.ui.plainTextEdit.appendPlainText("--- Filter States Updated ---")

    def remove_single_filter(self, triggered_widget):
        for f_obj in self.active_filters:
            if f_obj['filter_widget'] == triggered_widget:
                self.display_bars_layout.removeWidget(f_obj['display_bar'])
                f_obj['display_bar'].deleteLater()
                
                row = self.filter_list_widget.row(f_obj['list_item'])
                self.filter_list_widget.takeItem(row)
                
                self.active_filters.remove(f_obj)
                self.ui.plainTextEdit.appendPlainText(f"--- Removed Filter: Node: {f_obj['node_id'] or 'Any'} | MSG: {f_obj['msg_id'] or 'Any'} ---")
                break

    def clear_filters(self):
        for f_obj in self.active_filters:
            self.display_bars_layout.removeWidget(f_obj['display_bar'])
            f_obj['display_bar'].deleteLater()
            
        self.filter_list_widget.clear()
        self.active_filters.clear()
        self.ui.le_node_id.clear()
        self.ui.le_msg_id.clear()
        self.ui.plainTextEdit.appendPlainText("--- All Filters Cleared ---")

    def toggle_connection(self):
        if self.serial_port.isOpen():
            self.serial_port.close()
            self.ui.start_stop.setText("Start")
            self.ui.plainTextEdit.appendPlainText("=== Connection Closed ===")
            
            # --- STOP'A BASILDIĞINDA GELECEK VERİ AKIŞINI KESEN MOTOR ---
            self.data_buffer = "" # Tampon temizlenir ki arkada kalan veri parse edilmesin.
            for f_obj in self.active_filters:
                f_obj['display_bar'].stop_playback() # Tüm aktif göstergeler durdurulur.
        else:
            if self.ui.cb_port.currentIndex() == 0 or self.ui.cb_baud.currentIndex() == 0:
                QMessageBox.warning(self, "Warning", "Select a valid port and baud rate")
                return

            port_name = self.ui.cb_port.currentText()
            baud_rate = int(self.ui.cb_baud.currentText())
            
            self.serial_port.setPortName(port_name)
            self.serial_port.setBaudRate(baud_rate)
            
            if self.serial_port.open(QSerialPort.ReadWrite):
                self.ui.start_stop.setText("Stop")
                self.ui.plainTextEdit.appendPlainText(f"=== {port_name} Connection Started ===")
                self.data_buffer = ""
            else:
                QMessageBox.critical(self, "Error", f"Could not open {port_name}. It might be in use.")

    def read_serial_data(self):
        raw_data = self.serial_port.readAll().data().decode('utf-8', errors='ignore')
        self.data_buffer += raw_data

        while '\n' in self.data_buffer:
            line, self.data_buffer = self.data_buffer.split('\n', 1)
            self.parse_and_display(line)

    def parse_and_display(self, line):
        clean = line.replace('\0', '').strip()
        
        if not clean: return
        
        parts = [p.strip() for p in clean.split(',')]
        length = len(parts)

        if length < 3: return
        if(parts[0] != "iy" or parts[-1] != "ky"): return
            
        current_node_id = self.convert_to_decimal(parts[1])
        current_msg_id = self.convert_to_decimal(parts[2])

        doesDataExist = length >= 5
        data_list = parts[3:-1] if doesDataExist else []
        data_str = ", ".join(data_list) if doesDataExist else "NO DATA"

        is_filtered_out = False

        if self.active_filters:
            match_found = False
            has_enabled_filter = False

            for f_obj in self.active_filters:
                if not f_obj['is_active']:
                    continue  
                
                has_enabled_filter = True
                
                node_match = (f_obj['node_id'] == current_node_id) if f_obj['node_id'] else True
                msg_match = (f_obj['msg_id'] == current_msg_id) if f_obj['msg_id'] else True
                
                if node_match and msg_match:
                    match_found = True
                    f_obj['display_bar'].update_live_data(data_list)

            if has_enabled_filter and not match_found:
                is_filtered_out = True

        self.write_to_log(current_node_id, current_msg_id, data_list, is_filtered_out)

        if is_filtered_out:
            return

        self.ui.plainTextEdit.appendPlainText(f"[{datetime.now().strftime('%H:%M:%S')}] Node: {current_node_id}, MSG: {current_msg_id}, Data: [{data_str}]")

    def convert_to_decimal(self, value_str):
        if value_str.lower().startswith("0x"):
            try:
                return str(int(value_str, 16))
            except ValueError:
                return value_str
        return value_str

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TerminalApp()
    window.show()
    sys.exit(app.exec())
  #main
-----------------------------

'''
import indicator_widgets
## type, minVal, maxVal
servoGauge_1 = indicator_widgets("gauge",-10,+10) 
servoGauge_2 = indicator_widgets("gauge",-15,+15)
speedometer = indicator_widgets("speedometer",0,+50)
thermometer =  indicator_widgets("thermometer",-10,40)
altitude = indicator_widgets("altitude",0,3000)
sensor1 = indicator_widgets("artificial_horizon",-100,100,-100,100)



indicatorsList = [ 
    ["servoValues","gauge","gauge",None,None]
]


def lineValues(data_list):
    return ["x","87.5","y","15.87","z","3.56"]

def servoValues(data_list):

    return ["pos","3.15","setPt","3.30","srvStatus","1","sensorStatus","0"]
'''
