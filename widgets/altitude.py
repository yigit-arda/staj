import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtCore import QTimer

class ArtificialHorizon(QWidget):
    """A custom PySide6 widget that visualizes aircraft attitude.

    Displays a dynamic artificial horizon indicating pitch and roll angles
    using standard aviation colors (blue sky, brown ground), a dynamic pitch 
    ladder, and a static aircraft reference icon.
    """

    def __init__(self, parent=None):
        """Initializes the Artificial Horizon widget.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.pitch = 0.0  
        self.roll = 0.0   
        self.setMinimumSize(200, 200)

    def set_artificial_horizon(self, attitude_data):
        """Updates the pitch and roll values and triggers a UI repaint.

        Extracts the pitch and roll from a single packed data structure 
        to maintain compatibility with the single-argument routing system.

        Args:
            attitude_data (tuple or list): A sequence containing exactly two float 
                values representing (pitch, roll) in degrees.
        """
        # Check if incoming data matches expected format (tuple/list)
        if isinstance(attitude_data, (tuple, list)) and len(attitude_data) == 2:
            self.pitch = attitude_data[0]
            self.roll = attitude_data[1]
            self.update()
        else:
            # If invalid data format is received (e.g. single float),
            # you can reset to defaults or simply ignore/pass.
            pass

    def paintEvent(self, event):
        """Handles the rendering of the artificial horizon graphics.

        Draws the rotating sky/ground background, translates the pitch ladder, 
        and superimposes the static aircraft reference frame on top.

        Args:
            event (QPaintEvent): The paint event parameters provided by PyQt.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 

        width = self.width()
        height = self.height()
        
        side = min(width, height)
        radius = side / 2.0

        # Center the coordinate system
        painter.translate(width / 2.0, height / 2.0)

        # Clip drawings to a circular mask
        clip_path = QPainterPath()
        clip_path.addEllipse(QPointF(0, 0), radius, radius)
        painter.setClipPath(clip_path)

        # -------------------------------------------------------------------
        # DYNAMIC LAYER (Sky, Ground, and Pitch Ladder)
        # -------------------------------------------------------------------
        painter.save()
        painter.rotate(-self.roll)
        
        pitch_factor = radius / 45.0
        painter.translate(0, self.pitch * pitch_factor)

        bg_size = int(side * 2)

        # Sky (Blue)
        painter.setPen(Qt.PenStyle.NoPen) 
        painter.setBrush(QColor(0, 114, 198))
        painter.drawRect(-bg_size, -bg_size, bg_size * 2, bg_size)

        # Ground (Brown)
        painter.setBrush(QColor(122, 75, 41))
        painter.drawRect(-bg_size, 0, bg_size * 2, bg_size)

        # Horizon Line
        painter.setPen(QPen(Qt.GlobalColor.white, 3))
        painter.drawLine(int(-bg_size), 0, int(bg_size), 0) 

        # -------------------------------------------------------------------
        # PITCH LADDER LINES AND NUMERICAL VALUES
        # -------------------------------------------------------------------
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        
        # Dynamic font scaling based on widget radius
        font = painter.font()
        font.setPixelSize(int(radius * 0.12)) 
        font.setBold(True)
        painter.setFont(font)

        for i in range(-30, 40, 10):
            if i == 0: continue 
            y_pos = int(-i * pitch_factor)
            line_length = int(radius * 0.3)
            
            # Draw ladder line
            painter.drawLine(-line_length, y_pos, line_length, y_pos)

            # Numerical value (Aviation standards usually display absolute values: 10, 20)
            text = str(abs(i))
            
            # Dimensions for text bounding boxes
            rect_width = int(radius * 0.4)
            rect_height = int(radius * 0.2)
            margin = 5 # Padding distance away from the line
            
            # Left Text (Right-aligned)
            left_rect = QRectF(-line_length - rect_width - margin, y_pos - rect_height / 2, rect_width, rect_height)
            painter.drawText(left_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
            
            # Right Text (Left-aligned)
            right_rect = QRectF(line_length + margin, y_pos - rect_height / 2, rect_width, rect_height)
            painter.drawText(right_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)

        painter.restore()

        # -------------------------------------------------------------------
        # STATIC LAYER (Aircraft Reference Icon & Outer Ring)
        # -------------------------------------------------------------------
        
        # Outer Bezel
        painter.setPen(QPen(QColor(50, 50, 50), 6))
        painter.setBrush(Qt.BrushStyle.NoBrush) 
        painter.drawEllipse(QPointF(0, 0), radius - 3, radius - 3)

        # Aircraft Reference Icon
        pen = QPen(QColor(255, 140, 0), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        
        # Center dot
        painter.drawPoint(0, 0)
        
        # Left wing bar
        painter.drawLine(QPointF(-radius * 0.6, 0), QPointF(-radius * 0.15, 0))
        painter.drawLine(QPointF(-radius * 0.15, 0), QPointF(-radius * 0.15, radius * 0.1))
        
        # Right wing bar
        painter.drawLine(QPointF(radius * 0.6, 0), QPointF(radius * 0.15, 0))
        painter.drawLine(QPointF(radius * 0.15, 0), QPointF(radius * 0.15, radius * 0.1))
