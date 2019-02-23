# -*- coding: utf-8 -*-
# 机器人授课项目
#
# Created by: A1 Project
#
# 2018年12月
"""[主程序客户端]
负责人:gy
功能:...
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
import ui_client

from camera_thread import CameraThread
from ppt_control import PlayControllerThread
from ppt_preprocess import PreprocessThread


class MainClient(QMainWindow, ui_client.Ui_Dialog):
    def __init__(self):
        QMainWindow.__init__(self)
        ui_client.Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.directory = ''
        self.play_thread_running_flag = False  # 播放线程没有启动
        self.num = 0
        # 子线程暂停
        self.mutex = QtCore.QMutex()
        self.stopped = False

        # 控件点击事件
        self.btn_connect.clicked.connect(self.on_connect)
        self.btn_upload.clicked.connect(self.on_upload)
        self.btn_openpath.clicked.connect(self.on_open)

        # ppt控制
        self.btn_play.clicked.connect(self.on_play)
        self.btn_prev.clicked.connect(self.on_prev)
        self.btn_next.clicked.connect(self.on_next)
        self.btn_expand.clicked.connect(self.on_expand)

        # 摄像头控制
        self.btn_open_camera.clicked.connect(self.on_open_camera)
        self.btn_close_camera.clicked.connect(self.on_close_camera)

        # 日志控制
        self.btn_clear_log.clicked.connect(self.on_clear_log)

    # camera
    # @pyqtSlot(QImage)
    def setImage(self, image):
        self.camera_view.setPixmap(QPixmap.fromImage(image))

    def on_open(self):
        # 起始路径
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        self.directory = directory
        print(directory)

        if directory:
            dirs = os.listdir(directory)
            wav_count = 0
            for i in dirs:  # 循环读取路径下的文件并筛选输出
                if os.path.splitext(i)[1] == ".pptx":  # 筛选pptx文件
                    print(i)
                    self.log_view.insertPlainText("载入"+i+"幻灯片\n")
                    self.log_view.ensureCursorVisible()
                if os.path.splitext(i)[1] == ".ps":  # 筛选ps文件
                    print(i)
                    self.log_view.insertPlainText("载入"+i+"控制脚本\n")
                    self.log_view.ensureCursorVisible()
                if os.path.splitext(i)[1] == ".mp3":  # 筛选wav文件
                    print(i)
                    wav_count += 1
            if wav_count != 0:
                self.log_view.insertPlainText("载入"+str(wav_count)+"个音频文件\n")
                self.log_view.ensureCursorVisible()

    def on_upload(self):
        directory = QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*.pptx);;ppt Files (*.ppt)")

        print(directory)

        if directory[0] != '':
            self.log_view.insertPlainText("正在上传ppt文件到服务器...\n")
            self.log_view.ensureCursorVisible()

            self.log_view.insertPlainText("载入PPT文件,生成播放资源...\n")
            self.log_view.ensureCursorVisible()

            self.ppt_view.setPixmap(QPixmap("/Users/kou2n/Projects/renxin/play/screenshot/1.jpg"))

            self.ppt_view.setStyleSheet("border: 2px solid red")
            self.ppt_view.setScaledContents(True)
            self.ppt_view.setStyleSheet("border: none ")

            # 预处理线程
            self.preprocess_thread = PreprocessThread()
            self.preprocess_thread.complete_preprocess.connect(
                self.complete_preprocess_callback)

            self.preprocess_thread.update_log_view.connect(
                self.preprocess_callback)

            self.preprocess_thread.path = directory[0]
            self.preprocess_thread.start()

    def on_clear_log(self):
        self.log_view.clear()

    def on_open_camera(self):
        self.btn_open_camera.setEnabled(False)

        # 摄像头线程
        self.camera_thread = CameraThread(self)
        self.camera_thread.changePixmap.connect(self.setImage)
        self.camera_thread.close_camera.connect(self.close_camera_callback)
        self.camera_thread.raise_hand.connect(self.raise_hand_callback)

        self.camera_thread.start()

        self.log_view.insertPlainText("正在打开摄像头...\n")
        self.log_view.ensureCursorVisible()

    def on_close_camera(self):

        self.log_view.insertPlainText("正在关闭摄像头...\n")
        self.log_view.ensureCursorVisible()
        self.btn_open_camera.setEnabled(True)
        # 结束子进程循环
        self.camera_thread.__del__()

    def on_connect(self):
        self.log_view.insertPlainText("正在连接服务器...\n")
        self.log_view.ensureCursorVisible()

    def on_play(self):
        # play函数调用次数
        self.num += 1
        # print("函数调用次数"+str(self.num))
        if not self.play_thread_running_flag:
            # 修改标志
            self.play_thread_running_flag = True
            self.log_view.insertPlainText("开始播放PPT...\n")
            self.log_view.ensureCursorVisible()

            self.ppt_view.setPixmap(QPixmap("/Users/kou2n/Projects/renxin/play/screenshot/1.jpg"))
            self.ppt_view.setStyleSheet("border: 2px solid red")
            self.progress_bar.setValue(0)

            self.thread = PlayControllerThread(self)
            self.thread.update_ppt_view.connect(self.update_ppt_view_callback)
            self.thread.update_subtitle_view.connect(self.update_subtitle_view_callback)

            self.thread.end_play.connect(self.end_play_callback)

            self.thread.start()  # 启动线程

        # 下次点击按钮暂停播放
        else:
            if (self.num % 2) == 0:
                # 暂停线程
                self.thread.pause()
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/resource/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off,)
                self.btn_play.setIcon(icon)
            else:
                # 恢复线程
                self.thread.resume()
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/resource/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.btn_play.setIcon(icon)

    def on_prev(self):
        self.log_view.insertPlainText("前一页...\n")
        self.log_view.ensureCursorVisible()

    def on_next(self):
        self.log_view.insertPlainText("后一页...\n")
        self.log_view.ensureCursorVisible()

    def on_expand(self):
        self.log_view.insertPlainText("全屏播放...\n")
        self.log_view.ensureCursorVisible()
        # self.ppt_view.setVisible(False)
        # self.resize(842, 322)
        # 后续加入全屏播放功能

    # emit函数发送的参数需要在回调函数里声明传参i是当前页数
    def update_ppt_view_callback(self, current_page_id):
        print("第"+current_page_id+"页")
        self.ppt_view.setPixmap(QPixmap("./play/screenshot/"+current_page_id+".jpg"))
        # self.ppt_view.setStyleSheet("border: 2px solid red")
        self.ppt_view.setScaledContents(True)

        self.progress_bar.setValue(int(current_page_id) * 10)

    def update_subtitle_view_callback(self, subtitle):
        self.subtitle_view.setText(subtitle)

    def end_play_callback(self):
        self.ppt_view.setStyleSheet("border: none")
        self.subtitle_view.clear()
        self.progress_bar.setValue(0)
        # 播放结束恢复标志
        self.play_thread_running_flag = False
        self.num = 0

        self.log_view.insertPlainText("PPT播放完成...\n")
        self.log_view.ensureCursorVisible()

        self.ppt_view.setStyleSheet("border-image: url(:/icons/resource/loading.png)50;")
        self.ppt_view.setText("A1-Project 授课机器人客户端")

    def close_camera_callback(self):
        self.camera_thread.__del__()
        self.camera_view.clear()

    def preprocess_callback(self, log):
        self.log_view.insertPlainText(log)
        self.log_view.ensureCursorVisible()

    def complete_preprocess_callback(self):
        self.log_view.insertPlainText("播放资源生成结束...\n")
        self.log_view.ensureCursorVisible()

    def raise_hand_callback(self, hand_status):
        self.log_view.insertPlainText("检测到"+hand_status+"举起...\n")
        self.log_view.ensureCursorVisible()

        # 暂停线程
        self.thread.pause()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resource/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off,)
        self.btn_play.setIcon(icon)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 载入样式
    app.setStyleSheet(open("./style.qss", "r").read())
    md = MainClient()
    md.show()

    sys.exit(app.exec_())
