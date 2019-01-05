
import sys
from PyQt5 import QtWidgets,QtCore
import client
import socket

class ServerThread(Thread):
    def __init__(self,window):
        Thread.__init__(self)
        self.window = window



    def run(self):
        TCP_IP = '0.0.0.0'
        TCP_PORT = 8888
        BUFFER_SIZE = 20
        tcpServer = socket.socket()






# create the application and the main window
app = qtwidgets.qapplication(sys.argv)
window = qtwidgets.qmainwindow()
window.setstylesheet(open("./style.qss", "r").read())
button = qtwidgets.qpushbutton(window)

button.settext('click!')
# setup stylesheet

# run
window.show()
app.exec_()