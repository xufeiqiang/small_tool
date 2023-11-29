from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTextEdit, QDialog, QTableWidget, QTableWidgetItem, QLabel

import psutil
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
import socket
import speedtest
from homework.logger import Logger
from homework.utils import Utils
import threading


class HostPerformance(QDialog):
    # 添加一个自定义信号和一个槽（slot）
    customSingal = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        log = Logger(filename=Utils.getRootPath() + '/log/smallTool.log')
        self.logger = log.logger
        self.setWindowTitle('性能数据')
        self.setGeometry(200, 200, 1200, 800)

        self.host_data = ''
        self.text_edit = None
        self.lock = threading.Lock()  # 创建锁对象

        # 创建选项卡窗口
        tab_widget = QTabWidget()

        # 创建主机性能数据页面
        host_page = QWidget()
        self.setup_host_tab(host_page)
        tab_widget.addTab(host_page, '主机信息')

        # 创建进程性能数据页面
        process_page = QWidget()
        self.setup_process_tab(process_page)
        tab_widget.addTab(process_page, '进程信息')

        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        self.setLayout(layout)

    def setup_host_tab(self, page):
        self.logger.info("开始获取主机信息!")
        # 获取主机名
        hostname = socket.gethostname()
        # 获取本地IP地址
        ip_address = socket.gethostbyname(hostname)

        # 获取系统性能数据
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        # 获取当前主机上的所有磁盘盘符
        disk_partitions = psutil.disk_partitions(all=True)
        drive_letters = [partition.device for partition in disk_partitions]
        with self.lock:
            self.host_data = "当前主机名: {}\n".format(hostname)
            self.host_data += "ip地址: {}\n".format(ip_address)
            # 构建主机性能数据字符串
            self.host_data += "CPU使用率: {}%\n".format(cpu_usage)
            self.host_data += "内存使用率: {}%\n".format(memory_info.percent)

            self.text_edit = QTextEdit()
            self.text_edit.setPlainText(self.host_data)

        # 连接自定义信号到槽
        self.customSingal.connect(self.update_network_speed)

        # 异步获取网络速度，单独开启一个线程
        t = threading.Thread(target=self.get_network_speed)
        t.start()

        table = QTableWidget()
        table.setColumnCount(4)  # 4列
        table.setHorizontalHeaderLabels(['名称', '总空间 (GB)', '剩余空间 (GB)', '磁盘使用率(%)'])
        table.setSortingEnabled(True)
        # 设置表格的行数为磁盘分区的数量
        table.setRowCount(len(drive_letters))
        for row, drive in enumerate(drive_letters):
            disk_usage = psutil.disk_usage(drive)
            total = round(disk_usage.total / (1024 ** 3), 2)
            free = round(disk_usage.free / (1024 ** 3), 2)
            percent = round(((total - free) / total) * 100, 2)
            table.setItem(row, 0, QTableWidgetItem(str(drive)))
            table.setItem(row, 1, QTableWidgetItem(str(total)))
            table.setItem(row, 2, QTableWidgetItem(str(free)))
            # 创建一个 QTableWidgetItem 并设置文本为磁盘使用率的字符串表示
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, str(percent))
            table.setItem(row, 3, item)
        # 垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(table)
        page.setLayout(layout)
        self.logger.info("获取主机信息结束!")

    def get_network_speed(self):
        """
        由于 获取网络速度很慢，开启异步操作
        :return:
        """
        self.logger.info("开始获取网络速度")
        st = speedtest.Speedtest(timeout=5)
        download_speed = round(st.download() / 1024 / 1024, 2)
        upload_speed = round(st.upload() / 1024 / 1024, 2)
        # 发射一个自定义信号来更新界面
        with self.lock:
            # 对 self.host_data 和 self.text_edit 的访问需要在锁内进行
            self.customSingal.emit(download_speed, upload_speed)
            self.logger.info("获取网络速度结束")

    @pyqtSlot(float, float)
    def update_network_speed(self, download_speed, upload_speed):

        self.logger.info("开始渲染网络速度")
        # 在这里更新界面元素，例如将网络速度显示在文本框中
        self.host_data += "下载网络速度: {}Mbps\n".format(download_speed)
        self.host_data += "上传网络速度: {}Mbps\n".format(upload_speed)
        self.text_edit.setPlainText(self.host_data)
        self.logger.info("渲染网络速度结束")

    def setup_process_tab(self, page):
        # 进程信息
        # 创建表格
        self.logger.info("开始获取进程信息!")
        table = QTableWidget()
        table.setColumnCount(5)  # 5列
        table.setHorizontalHeaderLabels(['PID', '名称', 'CPU(%)', '内存(MB)', 'I/O', '进程路径'])
        table.setSortingEnabled(True)
        # 获取进程性能数据
        table.setRowCount(len(psutil.pids()))
        for row, pid in enumerate(psutil.pids()):
            process = psutil.Process(pid)
            # 填充表格
            table.setItem(row, 0, QTableWidgetItem(str(pid)))
            table.setItem(row, 1, QTableWidgetItem(str(process.name())))
            table.setItem(row, 2, QTableWidgetItem(str(round(process.cpu_percent(), 2))))
            table.setItem(row, 3, QTableWidgetItem(str(round(process.memory_info().rss / (1024 * 1024), 2))))
            table.setItem(row, 4, QTableWidgetItem(
                "Read: {}, Write: {}".format(process.io_counters().read_count, process.io_counters().write_count)))
            # table.setItem(row, 5, QTableWidgetItem(str(process.exe())))
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(table)
        page.setLayout(layout)
        self.logger.info("获取进程信息结束!")
