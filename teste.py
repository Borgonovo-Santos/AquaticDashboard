import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPolygon
from PyQt5.QtCore import QTimer, Qt, QPoint, QRect

class BoatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 200, 200)  # Definir o tamanho do widget
        self.setStyleSheet("background-color: lightblue;")  # Cor de fundo do widget

        # Variáveis para controlar a posição do barco virtual
        self.position_x = self.width() // 2
        self.position_y = self.height() // 2

        # Variáveis para controlar a direção do "bow wave"
        self.bow_wave_width = 30
        self.bow_wave_height = 30
        self.bow_wave_position = self.position_x

        # Variáveis para controlar a direção do barco virtual
        self.direction = QPoint(0, -1)  # Inicialmente apontando para cima

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Desenhar o "bow wave"
        bow_wave_polygon = QPolygon([
            QPoint(self.position_x - self.bow_wave_width // 2, self.position_y),  # Ponta do "V"
            QPoint(self.position_x + self.bow_wave_width // 2, self.position_y),  # Ponta do "V"
            QPoint(self.position_x, self.position_y + self.bow_wave_height)  # Base do "V"
        ])
        painter.setBrush(QBrush(Qt.blue))
        painter.drawPolygon(bow_wave_polygon)

        # Desenhar o barco
        painter.setBrush(QBrush(Qt.red))
        painter.drawEllipse(QPoint(self.position_x, self.position_y), 10, 10)  # Barco como um círculo

    def moveBoat(self, direction):
        # Atualizar a posição do barco virtual com base na direção
        self.position_x += direction.x()
        self.position_y += direction.y()

        # Limitar a posição do barco dentro do widget
        self.position_x = max(0, min(self.width(), self.position_x))
        self.position_y = max(0, min(self.height(), self.position_y))

        # Atualizar a posição do "bow wave" com base na posição do barco
        self.bow_wave_position = self.position_x

        # Redesenha o widget
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard do Barco")
        self.setGeometry(100, 100, 800, 600)  # Definir o tamanho da janela principal

        # Criar o widget da gadget boat
        boat_widget = QWidget(self)
        boat_widget.setGeometry(self.width() * 2 // 3, 0, self.width() // 3, self.height() // 2)  # Definir o tamanho e posição da gadget boat
        boat_widget.setStyleSheet("background-color: lightgreen; border: 2px solid white;")  # Cor de fundo e borda

        # Adicionar o widget do barco à gadget boat
        self.boat = BoatWidget(boat_widget)
        self.boat.setGeometry(10, 10, boat_widget.width() - 20, boat_widget.height() - 20)

        # Timer para atualizar a posição do "bow wave" periodicamente
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.boat.update)
        self.timer.start(50)  # Atualizar a cada 50 milissegundos

    def keyPressEvent(self, event):
        # Lidar com eventos de teclado para mover o barco virtualmente
        key = event.key()
        if key == Qt.Key_Up:
            self.boat.moveBoat(QPoint(0, -1))  # Mover para cima
        elif key == Qt.Key_Down:
            self.boat.moveBoat(QPoint(0, 1))  # Mover para baixo
        elif key == Qt.Key_Left:
            self.boat.moveBoat(QPoint(-1, 0))  # Mover para a esquerda
        elif key == Qt.Key_Right:
            self.boat.moveBoat(QPoint(1, 0))  # Mover para a direita

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
