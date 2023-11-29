import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor
import math


class FoodWheel(QWidget):
    def __init__(self, food_items):
        super().__init__()
        self.food_items = food_items
        self.angle = 0
        self.target_angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pie)
        self.timer.start(50)
        self.setFixedSize(400, 400)

    def update_pie(self):
        self.angle += 5
        if self.angle >= self.target_angle:
            self.target_angle = random.randint(0, 360)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = min(center_x, center_y) * 0.8

        start_angle = 0
        for i, item in enumerate(self.food_items):
            span_angle = 360 / len(self.food_items)
            if self.angle >= start_angle and self.angle < start_angle + span_angle:
                arrow_length = radius * 0.7
                arrow_x = center_x + arrow_length * math.cos(math.radians(self.angle))
                arrow_y = center_y - arrow_length * math.sin(math.radians(self.angle))
                painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                painter.drawLine(center_x, center_y, arrow_x, arrow_y)

            painter.setPen(QPen(Qt.NoPen))
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            painter.setBrush(QBrush(color))
            painter.drawPie(10, 10, 2 * radius, 2 * radius, start_angle * 16, span_angle * 16)

            start_angle += span_angle

        font = QFont("Arial", 12)
        painter.setFont(font)
        painter.drawText(10, self.height() - 30, "点击开始按钮开始旋转")


class PieChartApp(QMainWindow):
    def __init__(self, food_items):
        super().__init__()
        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle("Random Pie Chart")
        self.chart = PieChart(food_items)
        self.setCentralWidget(self.chart)

        start_button = QPushButton("开始")
        start_button.clicked.connect(self.start_rotation)
        self.chartLayout = self.layout()
        self.chartLayout.addWidget(start_button)

    def start_rotation(self):
        self.chart.target_angle = random.randint(0, 360)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    food_items = ["食物1", "食物2", "食物3", "食物4", "食物5", "食物6"]
    window = PieChartApp(food_items)
    window.show()
    sys.exit(app.exec_())
