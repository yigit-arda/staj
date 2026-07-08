# indicator_widgets.py

from widgets.gauge import GaugeWidget
from widgets.speedometer import ProfessionalSpeedometer
from widgets.thermometer import VerticalThermometer
from widgets.altitude import VerticalAltitudeBar
from widgets.artificial_horizon import ArtificialHorizon

# Registry mapping for each indicator type: (QWidget subclass, string name of its update method)
_WIDGET_REGISTRY = {
    "gauge":       (GaugeWidget,            "set_value"),
    "speedometer": (ProfessionalSpeedometer,    "set_value"),
    "thermometer": (VerticalThermometer,        "set_temperature"),
    "altitude":    (VerticalAltitudeBar,        "set_altitude"),
    "artificial_horizon": (ArtificialHorizon,  "set_artificial_horizon")
}

class IndicatorWidget:
    """A blueprint wrapper that defines an indicator type and its operational range.

    Note:
        This class itself is NOT a QWidget subclass. It acts as a structural descriptor
        or factory. Since the same indicator configuration might be shared across multiple
        DisplayBarWidget instances simultaneously, and Qt prohibits a single QWidget instance
        from being added to multiple layouts, each layout must invoke `create_instance()` to
        receive its own dedicated QWidget copy.

    Attributes:
        type (str): The string key specifying the indicator type (e.g., "gauge").
        min_val (float or int): The minimum configuration bound for the scale range.
        max_val (float or int): The maximum configuration bound for the scale range.
    """
    
    def __init__(self, w_type, min_val, max_val):
        """Initializes the IndicatorWidget descriptor and matches it against the registry.

        Args:
            w_type (str): The target widget type identifier.
            min_val (float or int): The low boundary value for the gauge scale.
            max_val (float or int): The high boundary value for the gauge scale.

        Raises:
            ValueError: If the provided `w_type` is missing from the registered components list.
        """
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
        """Constructs a concrete QWidget instance and applies its scale limitations.

        Instantiates the underlying subclass mapped in the registry and invokes
        its range setup routine if available.

        Returns:
            QWidget: A unique, newly constructed graphical widget instance ready for layout deployment.
        """
        widget = self._qwidget_cls()
        if hasattr(widget, "set_range"):
            widget.set_range(self.min_val, self.max_val)
        return widget

    def update_method_name(self):
        """Retrieves the target method name used to supply values to this widget type.

        Returns:
            str: The attribute or method name string (e.g., 'set_value', 'set_altitude').
        """
        return self._update_method_name
