import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QVBoxLayout, QLabel, \
    QPushButton, QFileDialog, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

from homework.logger import Logger
import cv2
import numpy as np
import os
from homework.utils import Utils


class ImageFormat(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        log = Logger(filename=Utils.getRootPath() + '/log/smallTool.log')
        self.logger = log.logger
        self.initUI()

    def initUI(self):
        self.setWindowTitle('图片处理')
        self.setGeometry(100, 100, 1000, 800)
        layout = QVBoxLayout(self)

        # 创建水平布局
        view_layout = QHBoxLayout(self)

        # 创建图形视图和场景
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        view_layout.addWidget(self.view)

        # 创建预览图形视图和场景
        self.preview_view = QGraphicsView(self)
        self.preview_scene = QGraphicsScene(self)
        self.preview_view.setScene(self.preview_scene)
        view_layout.addWidget(self.preview_view)

        # 创建预览图像项
        self.original_item = QGraphicsPixmapItem()
        self.processed_item = QGraphicsPixmapItem()

        self.scene.addItem(self.original_item)
        # 去除水印后的预览图像项
        self.preview_scene.addItem(self.processed_item)

        # 创建水印去除按钮布局
        buttons_layout = QHBoxLayout(self)

        # 创建上传图片按钮
        upload_button = QPushButton('上传图片', self)
        buttons_layout.addWidget(upload_button)
        upload_button.clicked.connect(self.uploadImage)

        # 创建水印去除按钮
        remove_watermark_button = QPushButton('去除水印', self)
        buttons_layout.addWidget(remove_watermark_button)
        remove_watermark_button.clicked.connect(self.removeWatermark)
        layout.addLayout(view_layout)
        layout.addLayout(buttons_layout)

    def uploadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filepath, _ = QFileDialog.getOpenFileName(self, '上传图片', '', 'Images (*.png *.jpg *.bmp *.jpeg)',
                                                  options=options)
        if filepath:
            self.filepath = filepath
            pixmap = QPixmap(filepath)
            self.original_item.setPixmap(pixmap)

    def removeWatermark(self):
        # 在这里执行去除水印的逻辑
        # 处理后的图片应该显示在self.processed_preview中
        if self.original_item.pixmap() is not None:
            # 加载原始图像和水印模板
            image = cv2.imread(self.filepath)
            watermark = cv2.imread(os.getcwd() + '/template/template.png')

            # 使用模板匹配来查找水印位置
            result = cv2.matchTemplate(image, watermark, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # 获取水印的位置
            h, w, _ = watermark.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            # 在原图上用白色矩形框覆盖水印
            cv2.rectangle(image, top_left, bottom_right, (255, 255, 255), -1)
            path = os.getcwd() + "/template/output_image_with_watermark_detection.jpg"
            try:
                # 保存去除水印后的图像
                cv2.imwrite(path, image)
                pixmap = QPixmap(path)
                self.processed_item.setPixmap(pixmap)
            except Exception as e:
                self.logger.error("【图片去除水印】 发送错误: %s" % str(e))
