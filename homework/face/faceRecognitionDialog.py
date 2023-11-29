import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QGroupBox, QHBoxLayout, \
    QTextEdit, QDialog, QFrame, QMessageBox,QProgressBar

from PyQt5.QtGui import QImage, QPixmap
from homework.logger import Logger
from homework.utils import Utils
import cv2
from PyQt5.QtCore import Qt, QTimer

class FaceRecognitionDialog(QDialog):
    """
    人脸识别的校验

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        log = Logger(filename=Utils.getRootPath() + '/log/smallTool.log')
        self.logger = log.logger
        self.setWindowTitle("人脸识别")
        self.setGeometry(100, 100, 800, 600)
        main_layout = QVBoxLayout()

        self.video_label = QLabel()
        self.start_button = QPushButton("开始识别")
        main_layout.addWidget(self.start_button)
        main_layout.addWidget(self.video_label)
        self.start_button.clicked.connect(self.start_recognition)
        self.setLayout(main_layout)

        # 定义定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)
        # 定义视频捕获对象
        self.cap = None
        try:
            self.logger.info("【人脸识别】开始读取训练模型")
            self.recognizer = cv2.face_LBPHFaceRecognizer.create()
            self.recognizer.read("face_recognizer.yml")  # 请提供已训练好的模型文件路径
            self.logger.info("【人脸识别】读取训练模型成功")
        except Exception as e:
            self.logger.info("【人脸识别】读取训练模型失败,原因: %s" % str(e))

        # 添加一个变量来跟踪是否检测到人脸
        self.face_detected = False



    def start_recognition(self):
        try:
            # 停止定时器
            self.timer.stop()
            # 打开摄像头
            self.cap = cv2.VideoCapture(0)
            # 开启定时器
            self.timer.start(100)
            self.start_button.setDisabled(True)
        except Exception as e:
            QMessageBox.warning(self, "错误", "摄像头打开失败: %s" % str(e))


    def update_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret :
                # 加载 Haar级联分类器，用于检测脸部特征
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                # 将彩色图像（BGR格式）转换为灰度图像
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 检测灰度图像中的人脸，并返回检测到的人脸的位置信息，COLOR_BGR2GRAY包括人脸所在的矩形框的坐标
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                for (x, y, w, h) in faces:
                    # 灰度图像 gray 中提取出检测到的人脸的区域
                    face_roi = gray[y:y + h, x:x + w]
                    #训练的人脸识别模型来识别提取出的人脸区域
                    label, confidence = self.recognizer.predict(face_roi)
                    confidence = round(confidence,2)
                    self.logger.info("【人脸识别】 label = %s, confidence = %s" %(label,confidence))
                    if confidence > 60:
                        self.logger.info("【人脸识别】 识别成功")
                        QMessageBox.information(self, "完成", "人脸识别成功！")
                        self.cap.release()
                        self.timer.stop()
                        self.start_button.setDisabled(False)
                        self.video_label.setPixmap(QPixmap())  # 清空图像
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                # 显示图像
                self.video_label.setPixmap(pixmap.scaled(self.video_label.size()))




