import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QGroupBox, QHBoxLayout, \
    QTextEdit, QDialog, QFrame, QMessageBox,QProgressBar

import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from homework.logger import Logger
from homework.utils import Utils
from pathlib import Path
import numpy as np


class FaceEntryDialog(QDialog):
    """
    人脸信息采集
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        log = Logger(filename=Utils.getRootPath() + '/log/smallTool.log')
        self.logger = log.logger
        self.setWindowTitle("人脸采集")
        self.setGeometry(100, 100, 800, 600)
        main_layout = QVBoxLayout()
        # 第一块 - 姓名输入
        name_layout = QHBoxLayout()
        name_label = QLabel("姓名:")
        self.name_input = QLineEdit()
        self.start_button = QPushButton("开始采集")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(self.start_button)


        # 第二块 - 人脸录制框
        self.video_label = QLabel()

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()

        # 将二块内容添加到主布局中
        main_layout.addLayout(name_layout)
        main_layout.addWidget(self.video_label)
        self.setLayout(main_layout)
        main_layout.addWidget(self.progress_bar)

        # 定义定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)

        # 定义视频捕获对象
        self.cap = None

        # 连接按钮的点击事件到槽函数
        self.start_button.clicked.connect(self.start_recording)

        self.face_images = []
        self.face_labels = []
        self.maxSchedule = 300

    def start_recording(self):
        self.logger.info("【人脸采集】数据采集开始")
        self.schedule = 0
        self.progress_bar.setMaximum(self.maxSchedule)
        self.progress_bar.show()
        name = self.name_input.text()
        if name:
            try:
                # 打开摄像头
                self.cap = cv2.VideoCapture(0)
                # 开启定时器
                self.timer.start(100)
                self.start_button.setDisabled(True)
            except Exception as e:
                QMessageBox.warning(self, "错误", "摄像头打开失败: %s" % str(e))
        else:
            QMessageBox.warning(self, "警告", "请输入姓名")

    def update_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret and self.schedule <= self.maxSchedule:
                # 加载 Haar级联分类器，用于检测脸部特征
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
                # 将彩色图像（BGR格式）转换为灰度图像
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 检测灰度图像中的人脸，并返回检测到的人脸的位置信息，COLOR_BGR2GRAY包括人脸所在的矩形框的坐标
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                # x 坐标, y 坐标,矩形框的宽度（width）,矩形框的高度（height）
                for (x, y, w, h) in faces:
                    self.schedule += 1
                    self.progress_bar.setValue(self.schedule)
                    # 标记人脸位置
                    cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0))
                    # 检测眼睛
                    # eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                    # if len(eyes) > 0:
                    #     message = "请摘掉眼镜"
                    #     # 在图像上绘制提示消息
                    #     # 为了支持中文字符集，请使用合适的字体文件路径（示例使用微软雅黑）
                    #     cv2.putText(frame, message, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    # 从图像中截取出检测到的人脸部分
                    face_img = frame[y:y + h, x:x + w]
                    jpg_path = Utils.getRootPath() + "/data/" + self.name_input.text()
                    directory_path =  Path(jpg_path)
                    directory_path.mkdir(parents=True, exist_ok=True)
                    # 将人脸图像和特征保存到文件
                    cv2.imwrite(jpg_path+ "/"+self.name_input.text() + "_" + str(self.schedule) + ".jpg", face_img)
                    # lbph_recognizer.save(eigenface_path)
                    self.face_images.append(gray)
                    self.face_labels.append(self.schedule)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                # 显示图像
                self.video_label.setPixmap(pixmap.scaled(self.video_label.size()))
            else:
                self.cap.release()
                self.timer.stop()
                self.start_button.setDisabled(False)
                self.logger.info("【人脸采集】数据采集完成,总共 %s:" % self.schedule)
                QMessageBox.information(self, "完成", "人脸数据已经采集完成！\n开始训练模型,请不要关闭窗口,等待模型训练完成！！！")
                self.logger.info("【人脸采集】开始训练模型" )
                try:
                    recognizer = cv2.face_LBPHFaceRecognizer.create()
                    # 开始训练
                    recognizer.train(self.face_images, np.array(self.face_labels))
                    # 保存训练好的模型
                    recognizer.save("face_recognizer.yml")
                except Exception as e:
                    self.logger.error("【人脸采集】 模型训练失败, 原因:" % str(e))
                self.logger.info("【人脸采集】模型训练完成了！")
                self.video_label.setPixmap(QPixmap())  # 清空图像
                QMessageBox.information(self, "完成", "模型已经训练完成了！")
                # 隐藏进度条
                self.progress_bar.hide()
                self.face_images = []
                self.face_labels = []



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FaceEntryDialog()
    window.show()
    sys.exit(app.exec_())
