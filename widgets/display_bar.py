from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Qt
import functions
from indicators_config import indicatorsList, FUNCTION_DISPLAY_NAMES


class DisplayBarWidget(QWidget):
    """A dynamic telemetry display widget that presents formatted node and message data.

    Allows user selection of different parser functions via a dropdown menu and
    dynamically renders associated visual indicators or plain text values.

    Attributes:
        last_data_list (list): The most recent data payload received by the widget.
        main_layout (QVBoxLayout): The primary layout container for the entire widget.
        top_row_widget (QWidget): A container widget for the upper telemetry controls.
        top_row_layout (QHBoxLayout): The layout manager for the controls row.
        label_info (QLabel): A label identifying the specific Node and Message IDs.
        dropdown (QComboBox): A selection dropdown containing parsing options.
        label_data (QLabel): A label utilized for rendering raw data or textual fallback metrics.
        indicators_container (QWidget): A container widget housing dynamically built indicator sub-widgets.
        indicators_layout (QHBoxLayout): The layout manager managing the visual indicators.
    """
    def __init__(self, node_id, msg_id, parent=None):
        """Initializes the DisplayBarWidget with layout structures, filtering text, and routing options.

        Args:
            node_id (str or int): The identifier code for the data source node.
            msg_id (str or int): The identifier code for the payload message type.
            parent (QWidget, optional): The parent widget hierarchy assignment. Defaults to None.
        """

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
        self.dropdown.addItem("Show Raw Data", "Show Raw Data")

        
        listed_names = []
        for row in indicatorsList:
            fname = row[0]
            if fname not in listed_names:
                listed_names.append(fname)
                display_text = FUNCTION_DISPLAY_NAMES.get(fname, fname)
                self.dropdown.addItem(display_text, fname)

        for attr_name in dir(functions):
            attr = getattr(functions, attr_name)
            if callable(attr) and not attr_name.startswith("_") and attr_name not in listed_names:
                display_text = FUNCTION_DISPLAY_NAMES.get(attr_name, attr_name)
                self.dropdown.addItem(display_text, attr_name)

        self.dropdown.setFixedWidth(160)
        self.dropdown.setStyleSheet("background-color: #FFFFFF; color: #333333; border: 1px solid #BBB;")
        self.dropdown.currentIndexChanged.connect(self.refresh_display)
        self.top_row_layout.addWidget(self.dropdown)

        self.label_data = QLabel("Waiting for data...", self)
        self.label_data.setStyleSheet("color: #D32F2F; font-family: 'Consolas', monospace; font-size: 11pt; font-weight: bold;")
        self.top_row_layout.addWidget(self.label_data, stretch=1)

        self.main_layout.addWidget(self.top_row_widget)

        
        self.indicators_container = QWidget(self)
        self.indicators_layout = QHBoxLayout(self.indicators_container)
        self.indicators_layout.setContentsMargins(5, 5, 5, 5)
        self.indicators_layout.setSpacing(20)
        self.indicators_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.indicators_container)

        self._current_keys = []       
        self._widget_instances = {}   
        self._status_labels = {}      


    def stop_playback(self):
        """Preserved API hook placeholder for playback queue cancellation compatibility."""
        pass

    def update_live_data(self, data_list):
        """Receives incoming live metrics and triggers a refresh across interface components.

        Args:
            data_list (list): The raw sequence values packaged in the recent network frame.
        """
        self.last_data_list = data_list
        self.refresh_display()

    def _clear_indicators_layout(self):
        """Safely detaches, destroys, and clears any pre-existing dynamic UI indicator instances."""
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
        """Constructs layout clusters dynamically for metrics linked to the selected parser.

        Args:
            matched_rows (list): Configuration tuples extracted from indicatorsList.
        """
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
        """Dispatches payload logs to target functions and rerenders metrics visually or textually."""
        if not self.last_data_list:
            return

        selected_function = self.dropdown.currentData()

        
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

        
        if [row[1] for row in matched_rows] != self._current_keys:
            self._build_indicators_for(matched_rows)

        try:
            result = func(self.last_data_list)
        except Exception as e:
            self.label_data.setText(f"Error: {e}")
            return

        
        if matched_rows:
            if not isinstance(result, dict):
                self.label_data.setText(f"Error: '{selected_function}' bir dict döndürmeli")
                return

            summary_parts = []
            for func_name, key, indicator, label in matched_rows:
                value = result.get(key)
                if value is None:
                    continue
                if isinstance(value, float):
                    summary_parts.append(f"{label}: {value:.2f}")
                else:
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

        
        else:
            if isinstance(result, dict):
                parts = []
                for k, v in result.items():
                    if isinstance(v, float):
                        parts.append(f"{k}: {v:.2f}")
                    else:
                        parts.append(f"{k}: {v}")
                self.label_data.setText(" | ".join(parts))
            else:
                self.label_data.setText(str(result))

    def set_active_state(self, is_active):
        """Alters the styling sheets and structural visibility to match connection state.

        Args:
            is_active (bool): Defines if telemetry feeds are active or dropped/offline.
        """
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
