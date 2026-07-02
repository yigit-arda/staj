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