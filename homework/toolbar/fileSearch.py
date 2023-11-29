from PyQt5.QtWidgets import  QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, \
    QDialog,QTableWidget,QTableWidgetItem,QLabel,QMenu
import psutil
import os
import subprocess
import concurrent.futures
from PyQt5.QtCore import Qt
from homework.logger import Logger
import time
from homework.utils import Utils



class FileSearch(QDialog):


    def __init__(self, parent=None):
        super().__init__(parent)
        log = Logger(filename=Utils.getRootPath()+'/log/smallTool.log')
        self.logger = log.logger
        self.setWindowTitle("文件搜索")
        self.setGeometry(100, 100, 800, 600)

        # 创建弹框中的元素
        self.input_box = QLineEdit(self)
        self.search_button = QPushButton('搜索', self)
        self.search_button.clicked.connect(self.searchFiles)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['文件名', '文件路径'])

        # 设置表格列宽
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 500)


        # 创建右键菜单
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.showContextMenu)

        # 创建布局
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.input_box)
        hbox.addWidget(self.search_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)

        # 将布局添加到弹框中
        self.setLayout(vbox)


    def searchFiles(self):
        search_query = self.input_box.text()
        if not search_query:
            return
        self.search_button.setEnabled(False)  # 禁用按钮
        self.logger.info("开始搜索文件")
        # 获取当前主机上的所有磁盘盘符
        disk_partitions = psutil.disk_partitions(all=True)
        drive_letters = [partition.device for partition in disk_partitions]

        # 创建一个线程池，每个线程负责搜索不同的磁盘.
        # todo 还有没有更优的方式解决？这样去匹配太慢了。
        begin = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            # 提交文件搜索任务给线程池
            # futures = []
            for drive in drive_letters:  # 修改为需要搜索的磁盘列表
                future = executor.submit(self.performSearch, search_query, drive)
                future.add_done_callback(self.handle_search_result)
                # futures.append(future)

            # 等待所有搜索任务完成
            # concurrent.futures.wait(futures)
        end = time.time()
        self.logger.info("【%s】 本次搜索文件, 共耗时:%s秒!!!" % (search_query, int(end - begin)))
        self.search_button.setEnabled(True)

    def performSearch(self, search_query, drive):
        result = []
        for root, _, files in os.walk(drive):
            for filename in files:
                if search_query in filename:
                    file_path = os.path.join(root, filename)
                    result.append((filename, file_path))
        return result

    def handle_search_result(self, future):
        result = future.result()
        for filename, file_path in result:
            self.insertRow(filename, file_path)



    def insertRow(self, filename, file_path):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(filename))
        self.table.setItem(row_position, 1, QTableWidgetItem(file_path))
        self.table.viewport().update()  # 立即刷新表格，使结果可见

    def showContextMenu(self, pos):
        menu = QMenu(self)
        # 获取右键点击的单元格的位置
        item = self.table.itemAt(pos)
        file_path = item.text()
        open_action = menu.addAction("打开")
        open_path_action = menu.addAction("打开路径")
        copy_action = menu.addAction("复制完整路径和文件名")
        action = menu.exec_(self.table.mapToGlobal(pos))
        if action == open_action:
            # 执行打开文件操作
            try:
                # 使用start命令打开文件
                subprocess.Popen(['start', file_path], shell=True)
            except FileNotFoundError:
                self.logger.error("【打开文件】 发生异常: 文件未找到！")
            except Exception as e:
                self.logger.error("【打开文件】 发送错误: %s" % str(e))
        elif action == open_path_action:
            # 执行打开文件路径操作
            try:
                # 使用文件资源管理器（Windows资源管理器）打开文件所在目录
                subprocess.Popen(['explorer', '/select,', file_path], shell=True)
            except FileNotFoundError:
                self.logger.error("【打开文件位置】 发生异常: 文件未找到！")
            except Exception as e:
                self.logger.error("【打开文件位置】 发送错误: %s" % str(e))
        elif action == copy_action:
            # 执行复制路径和文件名操作
            pass
