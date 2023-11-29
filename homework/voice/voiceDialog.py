from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QDialog, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QSize
from homework.logger import Logger
from homework.utils import Utils
from ..voice.inputVoice import InputVoice


class VoiceDialog(QDialog):
    def __init__(self, parent=None, input_device='host', output_device='host', language='chinese'):
        super().__init__(parent)
        log = Logger(filename=Utils.getRootPath() + '/log/smallTool.log')
        self.logger = log.logger
        self.rootPath = Utils.getRootPath()
        self.setWindowTitle("语音对话")
        self.setGeometry(100, 100, 1000, 800)
        self.input_device = input_device
        self.output_device = output_device
        self.language = language

        main_layout = QVBoxLayout()
        text = QTextEdit()

        self.start_button = QPushButton()

        self.__changeImage('/image/microphone.png')

        self.start_button.setText("开始语音")

        # 设置按钮的样式表
        self.start_button.setStyleSheet(
            "QPushButton {"
            "border: none;"
            "background-color: transparent;"  # 设置背景透明
            "}"

        )

        self.start_button.clicked.connect(self.start_voice)

        main_layout.addWidget(text)
        main_layout.addWidget(self.start_button)

        self.setLayout(main_layout)
        self.button_flag = 0
        self.inputVoice =  InputVoice()

    def start_voice(self):
        self.logger.info("开始语音对话")
        if self.button_flag == 0:
            self.__changeImage('/image/microphone_gray.png')
            self.start_button.setText("正在录音中...")
            self.button_flag = 1
            self.inputVoice.start_voice()
        elif self.button_flag == 1:
            self.__changeImage('/image/microphone.png')
            self.start_button.setText("开始语音")
            self.button_flag = 0
        pass

    def __changeImage(self, path):
        self.microphone_icon = QIcon(self.rootPath + path)
        self.start_button.setIcon(self.microphone_icon)
        # 设置图标并调整大小
        self.start_button.setIconSize(QSize(100, 100))
