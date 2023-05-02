import sys
from math import sqrt
from PyQt5.QtWidgets import QPushButton, QApplication, QFrame, QMainWindow, QWidget, QGridLayout, QLabel, QDialog, QDialogButtonBox, QStackedLayout,  QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt 

class RoomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Room Dimensions')

        self.width_label = QLabel('Width (m):')
        self.width_edit = QLineEdit()
        self.width_edit.setValidator(QDoubleValidator())

        self.length_label = QLabel('Length (m):')
        self.length_edit = QLineEdit()
        self.length_edit.setValidator(QDoubleValidator())

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        width_layout = QHBoxLayout()
        width_layout.addWidget(self.width_label)
        width_layout.addWidget(self.width_edit)
        layout.addLayout(width_layout)
        length_layout = QHBoxLayout()
        length_layout.addWidget(self.length_label)
        length_layout.addWidget(self.length_edit)
        layout.addLayout(length_layout)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_dimensions(self):
        width = int(self.width_edit.text())
        length = int(self.length_edit.text())
        return width, length 


class SpeakerOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.squares = []

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.blue, 8, Qt.SolidLine)
        qp.setPen(pen)
        brush = QBrush(QColor("#FF00FF"), Qt.CrossPattern)
        qp.setBrush(brush)

        # Draw blue squares
        for square in self.squares:
            print('Blue squares', square)
            qp.drawRect(*square)


class RoomLayout(QWidget):
    DISTANCE = 4
    
    def __init__(self, width, length, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.length = length
        self.square_size = 50
        self.padding = 10
        self.setMinimumSize(self.width * self.square_size + 2 * self.padding,
                             self.length * self.square_size + 2 * self.padding)


    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        brush = QBrush(QColor("#F0F0F0"), Qt.SolidPattern)
        qp.setBrush(brush)

        for i in range(self.width):
            for j in range(self.length):
                x = i * self.square_size + self.padding
                y = j * self.square_size + self.padding
                print('All squares', x, y, self.square_size, self.square_size)
                qp.drawRect(x, y, self.square_size, self.square_size)

    def add_speaker_squares(self):
        squares = []

        # Add blue squares
        for i in range(self.width):
            for j in range(self.length):
                x = i * self.square_size + self.padding
                y = j * self.square_size + self.padding
                square = (x, y, self.square_size, self.square_size)
                squares.append(square)

        self.overlay = SpeakerOverlay(self)
        self.overlay.squares = squares
        return self.overlay


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Room Layout")

        # Get the dimensions of the room from the user
        dialog = RoomDialog()
        # if dialog.exec_() == QDialog.Accepted:
        #     self.room_width, self.room_length = dialog.get_dimensions()
        # else:
        #     self.room_width = self.room_length = 0
        self.room_width = 10
        self.room_length = 8

        widget = QWidget()
        self.layout = QVBoxLayout()

        # Create the room layout widget
        self.room_layout = RoomLayout(self.room_width, self.room_length)
        self.layout.addWidget(self.room_layout)

        # Add a button to add new speaker squares
        add_speaker_button = QPushButton('Add Speaker Squares', self)
        add_speaker_button.clicked.connect(self.add_speaker_squares)
        self.layout.addWidget(add_speaker_button)

        # Arrange the widgets in a layout
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def add_speaker_squares(self):
        self.overlay = self.room_layout.add_speaker_squares()

        # Create the stacked layout and add the widgets
        self.stack = QStackedLayout()
        # self.stack.addWidget(self.room_layout)
        self.stack.addWidget(self.overlay)

        # Set the stacked layout as the main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stack)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
