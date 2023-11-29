import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar,QAction,QVBoxLayout,QWidget,QLabel,QPushButton,QHBoxLayout,QComboBox

from homework.toolbar.hostPerformance import HostPerformance
from homework.toolbar.fileSearch import FileSearch
from homework.toolbar.imageFormat import ImageFormat
from homework.utils import Utils
from homework.face.faceEntryDialog import FaceEntryDialog
from homework.face.faceRecognitionDialog import FaceRecognitionDialog
from homework.voice.voiceDialog import VoiceDialog
from homework.toolbar.proxyApplication import ProxyApplication


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rootPath = Utils.getRootPath()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Small Tools')
        self.setGeometry(1000, 100, 450, 800)
        self.setStyleSheet("background-color: #f0f0f0;")

        # 创建一个容器，用于包含人脸识别模块和语言模块
        main_container = QWidget(self)
        self.setCentralWidget(main_container)

        # 创建垂直布局，用于容器中的新控件
        main_layout = QVBoxLayout()


        # 创建人脸识别模块
        face_recognition_module = self.create_face_recognition_module()
        main_layout.addWidget(face_recognition_module)

        # 创建语言模块
        language_module = self.create_language_module()
        main_layout.addWidget(language_module)

        main_container.setLayout(main_layout)

        # 创建工具栏
        toolbar = QToolBar()
        self.addToolBar(Qt.RightToolBarArea, toolbar)

        # 添加工具栏按钮
        host_action = QAction(QIcon(self.rootPath + '/image/host_device.png'), '查看主机性能', self)
        file_action = QAction(QIcon(self.rootPath + '/image/file_search.png'), '文件搜索', self)
        image_format_action = QAction(QIcon(self.rootPath + '/image/image_format.png'), '去除图片水印', self)
        mitmproxy_action = QAction(QIcon(self.rootPath + '/image/mitmproxy.png'), '网站中间代理', self)

        host_action.triggered.connect(self.show_host_performance)
        file_action.triggered.connect(self.file_search)
        image_format_action.triggered.connect(self.show_image_format)
        mitmproxy_action.triggered.connect(self.mitmproxy_app)


        # 将按钮添加到工具栏
        toolbar.addAction(host_action)
        toolbar.addAction(file_action)
        toolbar.addAction(image_format_action)
        toolbar.addAction(mitmproxy_action)

    def create_face_recognition_module(self):
        face_module = QWidget(self)
        face_module.setStyleSheet("border: 2px solid #ccc; border-radius: 10px;")

        # 创建垂直布局，用于人脸识别模块
        face_layout = QVBoxLayout()

        label_icon = QLabel()
        pixmap = QPixmap(self.rootPath+ '/image/face.png')
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
        label_icon.setPixmap(pixmap)

        label_text = QLabel("人脸识别")

        face_layout.addWidget(label_icon, alignment=Qt.AlignCenter)
        face_layout.addWidget(label_text, alignment=Qt.AlignCenter)

        btn_face_entry = QPushButton("人脸采集")
        btn_face_entry.clicked.connect(self.show_face_entry_dialog)

        btn_face_recognition = QPushButton("人脸识别")
        btn_face_recognition.clicked.connect(self.show_face_recognition_dialog)

        btn_face_entry.setStyleSheet(
            "background-color: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px;")
        btn_face_recognition.setStyleSheet(
            "background-color: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px;")

        face_layout.addWidget(btn_face_entry)
        face_layout.addWidget(btn_face_recognition)

        face_module.setLayout(face_layout)
        return face_module

    def create_language_module(self):
        language_module = QWidget(self)
        language_module.setStyleSheet("border: 2px solid #ccc; border-radius: 10px;")

        # 创建垂直布局，用于语言模块
        language_layout = QVBoxLayout()

        l1_layout = QVBoxLayout()

        label_icon = QLabel()
        pixmap = QPixmap(self.rootPath +'/image/language.png')
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
        label_icon.setPixmap(pixmap)

        label_text = QLabel("AI语音")

        l1_layout.addWidget(label_icon, alignment=Qt.AlignCenter)
        l1_layout.addWidget(label_text, alignment=Qt.AlignCenter)

        l2_layout = QHBoxLayout()
        input_device_label = QLabel("请选择语音输入设备")
        self.input_device_combo = QComboBox()
        self.input_device_combo.addItem("当前主机","host")
        self.input_device_combo.addItem("音箱","speaker")
        self.input_device_combo.addItem("耳机","earphone")
        self.input_device_combo.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        input_device_label.setStyleSheet("border: none; background: transparent;")

        l3_layout = QHBoxLayout()
        output_device_label = QLabel("请选择语音输出设备")
        self.output_device_combo = QComboBox()
        self.output_device_combo.addItem("当前主机","host")
        self.output_device_combo.addItem("音箱","speaker")
        self.output_device_combo.addItem("耳机","earphone")
        self.output_device_combo.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        output_device_label.setStyleSheet("border: none; background: transparent;")

        l4_layout = QHBoxLayout()
        self.language_combo = QComboBox()
        language_label = QLabel("请选择语言")
        self.language_combo.addItem("中文","chinese")
        self.language_combo.addItem("日语","japanese")
        self.language_combo.addItem("英语","english")
        self.language_combo.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        language_label.setStyleSheet("border: none; background: transparent;")

        l2_layout.addWidget(input_device_label)
        l2_layout.addWidget(self.input_device_combo)

        l3_layout.addWidget(output_device_label)
        l3_layout.addWidget(self.output_device_combo)


        l4_layout.addWidget(language_label)
        l4_layout.addWidget(self.language_combo)

        start_language = QPushButton("开始语音对话")
        start_language.setStyleSheet(
            "background-color: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px;")

        start_language.clicked.connect(self.start_language_clicked)

        language_layout.addLayout(l1_layout)
        language_layout.addLayout(l2_layout)
        language_layout.addLayout(l3_layout)
        language_layout.addLayout(l4_layout)
        language_layout.addWidget(start_language)

        language_module.setLayout(language_layout)

        return language_module


    def show_host_performance(self):
        hostPerformance =  HostPerformance()
        hostPerformance.exec_()


    def file_search(self):
        fileSearch =  FileSearch()
        fileSearch.exec_()

    def show_image_format(self):
        imageFormat = ImageFormat()
        imageFormat.exec_()

    def show_face_entry_dialog(self):
        # 创建并显示 "人脸录入" 对话框
        face_entry_dialog = FaceEntryDialog()
        face_entry_dialog.exec_()

    def show_face_recognition_dialog(self):
        face_recognition_dialog = FaceRecognitionDialog()
        face_recognition_dialog.exec_()

    def start_language_clicked(self):
        # 获取下拉框的选项值
        input_device = self.input_device_combo.currentText()
        output_device = self.output_device_combo.currentText()
        language = self.language_combo.currentText()
        voiceDialog = VoiceDialog(input_device = input_device,output_device= output_device,language= language)
        voiceDialog.exec_()

    def mitmproxy_app(self):
        proxyApp = ProxyApplication()
        proxyApp.exec_()


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
