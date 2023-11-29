from PyQt5.QtWidgets import  QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, \
    QDialog,QTableWidget,QTableWidgetItem,QLabel,QMenu
from homework.logger import Logger
from homework.utils import Utils
import subprocess


class ProxyApplication(QDialog):


    def __init__(self, parent=None):
        super().__init__(parent)
        log = Logger(filename=Utils.getRootPath() + '/log/smallTool.log')
        self.logger = log.logger
        self.setWindowTitle('中间代理')
        self.setGeometry(200, 200, 1200, 800)
        process = subprocess.Popen('mitmweb', shell=True)
        process.wait()
        self.logger.info("mitmweb 初始化成功")
        process2 = subprocess.Popen('google-chrome --proxy-server=127.0.0.1:8080 --ignore-certificate-errors', shell=True)
        process2.wait()
        self.logger.info("mitmweb 设置chrome 为代理浏览器成功")
