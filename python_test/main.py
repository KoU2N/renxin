import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication

from client import Ui_dialog


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.myButton = QtWidgets.QPushButton(self)
        self.myButton.setObjectName("myButton")
        self.myButton.setText("Test")
        self.myButton.clicked.connect(self.msg)

    def msg(self):
        directory1 = QFileDialog.getExistingDirectory(self,
                                    "选取文件夹",
                                    "C:/")                                 #起始路径
        print(directory1)

        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "C:/",
                                    "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        print(fileName1,filetype)

        files, ok1 = QFileDialog.getOpenFileNames(self,
                                    "多文件选择",
                                    "C:/",
                                    "All Files (*);;Text Files (*.txt)")
        print(files,ok1)

        fileName2, ok2 = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    "C:/",
                                    "All Files (*);;Text Files (*.txt)")

if __name__=="__main__":



    app = QApplication(sys.argv)
    #载入样式
    app.setStyleSheet(open("./style.qss", "r").read())

    Dlg = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(Dlg)

    Dlg.show()
    sys.exit(app.exec())