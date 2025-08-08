from tool import Ui_Mainwindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileSystemModel, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
import os
import threading

import rename_worker
import datetime

PRE_REGULAR = "(.+)-(.+)-(.+)"
PRE_REPLACE_RULE = "【常规】(MATCH2)-(DIR3)-(MATCH1)-(DIR1)-(ORDER)-(MATCH3)"
MATCH_REGULAR = "MATCH"
DIR_REGULAR = "DIR"
ORDER_REGULAR = "ORDER"

class ToolMainWindow(Ui_Mainwindow):
    def __init__(self):
        super().__init__()
        # self.work_thread = threading.Thread(target=self.rename_worker_thread)
        self.work_items = dict()  # 用于存储工作项
        self.work_status = False  # 用于标记工作状态
        self.work_target_types = []

    def rename_files(self):
        directly_text = self.work_items["directly_text"]
        replace_rule = self.work_items["replace_rule"]
        prefix_rule = self.work_items["prefix_rule"]
        filetype_filter = self.work_items["filetype_filter"]

        total_files = 0

        for dir in self.work_items["dirs"]:
            dirs3 = rename_worker.get_last_three_dirs(dir)
            if (not dirs3 or len(dirs3) < 3):
                self.log_message(f"目录 {dir} 不包含足够的子目录，跳过重命名")
                continue

            dirs3 = list(dirs3)
            dirs3.reverse()  # 反转列表以获取正确的顺序
            dir1, dir2, dir3 = dirs3[-3], dirs3[-2], dirs3[-1]

            matches = rename_worker.regular_check(replace_rule, dirs3[1])
            if (not matches or len(matches) < 3):
                self.log_message(f"目录 {dir} 的二级目录名不符合正则规则，跳过重命名")
                continue

            original_filenames = rename_worker.get_all_filenames(dir)

            order = 1
            for filename in original_filenames:
                if not os.path.isfile(filename):
                    self.log_message(f"跳过非文件项: {filename}")
                    continue

                # new_name = os.path.basename(filename)
                new_name = prefix_rule
                extension = os.path.splitext(filename)[1]

                for i in range(0, 3):
                    new_name = new_name.replace(f"({DIR_REGULAR}{i+1})", dirs3[i])
                
                for i in range(0, len(matches)):
                    new_name = new_name.replace(f"({MATCH_REGULAR}{i+1})", matches[i])

                new_name = new_name.replace(f"({ORDER_REGULAR})", f"{total_files:03d}")  # 使用四位数格式化订单号

                new_name += extension  # 添加文件扩展名
                if filetype_filter:
                    if extension[1:] not in filetype_filter:
                        self.log_message(f"文件 {filename} 的扩展名 {extension} 不在过滤列表中，跳过重命名")
                        continue

                self.log_message(f"尝试将文件 {filename} -> {new_name}")
                if not rename_worker.change_file_name(filename, new_name):
                    self.log_message(f"重命名文件 {filename} 失败")

                order += 1
                total_files += 1
        self.log_message(f"转换操作完成，共重命名 {total_files} 个文件")

    def rename_worker_thread(self):
        """
        Worker thread to handle renaming operations.
        This method will be run in a separate thread to avoid blocking the UI.
        """

        if self.work_status:
            self.log_message("工作线程已在运行，无法重复启动")
            return

        self.work_status = True
        self.log_message("工作线程已启动")

        try:
            self.rename_files()
        except Exception as e:
            self.log_message(f"重命名操作出错: {e}")

        self.work_status = False
        self.work_items = dict()  # Reset work items for the new thread


    def setupUi(self, Mainwindow):
        super().setupUi(Mainwindow)
        
        # 创建主布局
        main_layout = QVBoxLayout(self.centralwidget)
        
        # 在treeView上方添加一些空间
        # main_layout.addSpacing(20)  # 添加20像素的空间
        
        # 设置文件系统模型
        self.model = QFileSystemModel()
        self.model.setRootPath('')  # 设置为根目录
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(''))  # 设置根索引为根目录
        self.treeView.setAutoScroll(True)  # 启用自动滚动
        
        # 将treeView添加到布局，设置拉伸因子为3（占更多空间）
        main_layout.addWidget(self.treeView, 1)
        
        # 添加输入框区域
        input_layout = QVBoxLayout()
        
        # 第一行：查找文本
        search_layout = QHBoxLayout()
        search_label = QLabel("选中的文件夹:")
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText("选择想要的文件夹...")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.searchLineEdit)
        input_layout.addLayout(search_layout)
        
        # 第二行：替换文本
        replace_layout = QHBoxLayout()
        replace_label = QLabel("一级目录正则:")
        self.replaceLineEdit = QLineEdit()
        self.replaceLineEdit.setPlaceholderText("输入一级目录文件夹匹配正则...")
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replaceLineEdit)
        input_layout.addLayout(replace_layout)
        # 第三行：文件类型选择
        filetype_label = QLabel("文件类型过滤:")
        self.filetypeLineEdit = QLineEdit()
        self.filetypeLineEdit.setPlaceholderText("如: txt|jpg|png, 多个用|分隔")
        replace_layout.addWidget(filetype_label)
        replace_layout.addWidget(self.filetypeLineEdit)
        self.filetypeLineEdit.setText("mp4|mkv|avi")  # 默认设置为常见视频格式
        
        # 第三行：前缀/后缀
        prefix_layout = QHBoxLayout()
        prefix_label = QLabel("二级目录文件名替换规则:")
        self.prefixLineEdit = QLineEdit()
        self.prefixLineEdit.setPlaceholderText("输入替换规则...")
        # suffix_label = QLabel("添加后缀:")
        # self.suffixLineEdit = QLineEdit()
        # self.suffixLineEdit.setPlaceholderText("在文件名后添加...")
        prefix_layout.addWidget(prefix_label)
        prefix_layout.addWidget(self.prefixLineEdit)
        # prefix_layout.addWidget(suffix_label)
        # prefix_layout.addWidget(self.suffixLineEdit)
        input_layout.addLayout(prefix_layout)
        
        # 将输入框布局添加到主布局
        main_layout.addLayout(input_layout)
        
        # 创建按钮的水平布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.pushButton)
        button_layout.addStretch()  # 添加弹性空间，让按钮靠左
        
        # 将按钮布局添加到主布局
        main_layout.addLayout(button_layout)
        
        # 添加日志输出窗口
        self.logTextEdit = QPlainTextEdit(self.centralwidget)
        self.logTextEdit.setObjectName("logTextEdit")
        self.logTextEdit.setReadOnly(True)  # 设置为只读
        
        # 将日志窗口添加到布局，设置拉伸因子为1（占较少空间）
        main_layout.addWidget(self.logTextEdit, 2)
        
        # 设置布局的边距
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        self.pushButton.clicked.connect(self.start_conversion)
        self.treeView.clicked.connect(self.get_selected_path)
        
        # 添加欢迎日志
        self.log_message("应用程序已启动")
    
    def log_message(self, message):
        """添加日志消息到日志窗口"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logTextEdit.appendPlainText(log_entry)
        
        # 自动滚动到底部
        scrollbar = self.logTextEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def start_conversion(self):
        """开始转换操作"""
        directly_text = self.searchLineEdit.text()
        # self.log_message(f"开始转换操作，选中的文件夹: {directly_text}")
        if not directly_text:
            self.log_message("未选中文件夹，无法进行转换操作")
            return
        if not os.path.isdir(directly_text):
            self.log_message(f"选中的路径不是一个有效的文件夹: {directly_text}")
            return

        if not rename_worker.has_sub_dir(directly_text):
            self.log_message(f"选中的文件夹 {directly_text} 不包含两重子文件夹，无法进行转换操作")
            return

        self.log_message(f"选中的文件夹 {directly_text} 开始转换...")

        dirs, error_text = rename_worker.has_sub_dir_with_details(directly_text)
        if error_text:
            self.log_message(error_text)
            return

        self.work_items["dirs"] = dirs
        self.work_items["directly_text"] = directly_text
        self.work_items["replace_rule"] = self.replaceLineEdit.text()
        self.work_items["prefix_rule"] = self.prefixLineEdit.text()
        self.work_items["filetype_filter"] = self.filetypeLineEdit.text().split('|')

        # self.work_thread.start()  # 启动工作线程

        thread = threading.Thread(target=self.rename_worker_thread)
        thread.start()  # 启动工作线程
        thread.join()  # 等待线程完成
        self.log_message("转换操作已完成")

    def get_selected_path(self):
        index = self.treeView.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            
            # 判断是否是文件夹
            if self.model.isDir(index):
                self.log_message(f"选中文件夹: {path}")
                self.searchLineEdit.setText(path)
            else:
                self.log_message("未选中文件夹")
                self.searchLineEdit.setText("")
        else:
            self.log_message("未选中任何文件或文件夹")
            self.searchLineEdit.setText("")

    def setupPreConfig(self):
        self.replaceLineEdit.setText(PRE_REGULAR)
        self.prefixLineEdit.setText(PRE_REPLACE_RULE)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Mainwindow = QtWidgets.QMainWindow()
    ui = ToolMainWindow()
    ui.setupUi(Mainwindow)
    ui.setupPreConfig()
    Mainwindow.show()
    sys.exit(app.exec_())