from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

class FilterWidget(QWidget):
    """A custom widget representing a removable and toggleable filter item.

    Displays the node and message IDs associated with a specific data filter. 
    Provides interactive UI elements to either pause (toggle active/passive state) 
    or completely remove the filter from the system.

    Attributes:
        node_id (str or int): The target node identifier for the filter.
        msg_id (str or int): The target message identifier for the filter.
        is_active (bool): Indicates whether the filter is currently active or passive.
        on_toggle (callable): Callback function executed when the filter's state is toggled.
        on_delete (callable): Callback function executed when the filter is deleted.
        label (QLabel): The text label displaying the filter's identification details.
        btn_visible (QPushButton): The button used to toggle the active/passive state.
        btn_delete (QPushButton): The button used to trigger the deletion of the widget.
    """
    def __init__(self, node_id, msg_id, on_toggle, on_delete, parent=None):
        """Initializes the FilterWidget with its identifiers and callback actions.

        Args:
            node_id (str or int): The target node identifier.
            msg_id (str or int): The target message identifier.
            on_toggle (callable): The function to call when the active state changes. 
                Passes the widget instance as an argument.
            on_delete (callable): The function to call when the delete button is clicked. 
                Passes the widget instance as an argument.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        
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
        """Toggles the filter's state between active and passive.

        Updates the toggle button's text and background color, alongside the main 
        label's styling to visually reflect the current state (e.g., strikethrough 
        when passive). Triggers the on_toggle callback afterward.
        """
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
        """Initiates the deletion of the filter widget.

        Triggers the on_delete callback, passing the current widget instance 
        so the parent container can handle its removal and cleanup.
        """
        self.on_delete(self)
