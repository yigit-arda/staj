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