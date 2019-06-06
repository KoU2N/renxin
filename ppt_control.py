# -*- coding: utf-8 -*-
"""[脚本控制模块]
负责人:zz
功能:控制ppt播放
"""
# import win32com.client
# import win32api
# import win32con
#
# import pythoncom


# import pyaudio
# import wave
from playsound import playsound
from PyQt5.QtCore import pyqtSlot,QThread,pyqtSignal,QMutex

from PyQt5.QtCore import *

VK_CODE = {
	'spacebar':0x20,
	'down_arrow':0x28,
}
class PlayControllerThread(QThread):
	update_ppt_view = pyqtSignal(str)  # 括号里填写信号传递的参数
	update_subtitle_view = pyqtSignal(str)

	end_play = pyqtSignal()


	def __init__(self,lines):
		super().__init__()
		#pythoncom.CoInitialize()
		print('start')
		#self.app = win32com.client.Dispatch("PowerPoint.Application")
		# self.app = win32com.client.GetActiveObject("PowerPoint.Application")
		#self.ppt = PlayControllerThread()

		self.lines = self.get_lines()
		self.pause_flag = False

		###启动暂停线程
		self.mutex = QMutex()
		self.pauseCond =QWaitCondition()
		self.stopped = False
		###

	# def __del__(self):
	# 	self.wait()
	def resume(self):
		self.mutex.lock()
		self.pause_flag = False
		self.mutex.unlock()
		self.pauseCond.wakeAll()
	def pause(self):
		self.mutex.lock()
		self.pause_flag = True
		self.mutex.unlock()

	def run(self):

		for i, line in enumerate(self.lines):

			###启动暂停线程功能
			self.mutex.lock()
			if self.pause_flag:
				self.pauseCond.wait(self.mutex)
			self.mutex.unlock()
			###


			wav = self.get_wav(line)
			text = self.get_text(line)

			print('play : ' + wav + '.wav')
			print('text : ' + text)

			try:
				self.update_subtitle_view.emit(text)
				self.play(wav)
			finally:
				self.update_ppt_view.emit(str(i+1))

			# if (self.get_page(self.lines[i]) > self.get_page(line)-1) :
			# 	# 进行任务操作  and (not self.pause_flag)
			# 	self.update_ppt_view.emit(str(i + 1))  # 发射信号
			# 	continue  # self.ppt.nextPage()

		self.end_play.emit()
	def get_lines(self):
		lines = []
		with open('./play/controll.ps', 'r', encoding='utf8') as reader:
			for i, line in enumerate(reader):
				lines.append(line)
		return lines

	def get_page(self, string):
		# return string[:(string.find('-')+1)].strip()
		return (int(string.split('_')[0]) - 1)

	def get_text(self, string):
		return string[string.find('|'):].strip()

	def get_wav(self, string):
		return string[:string.find('|')].strip()



	# def fullScreen(self):
	# 	#全屏播放
	# 	if self.hasActivePresentation():
	# 		self.app.ActivePresentation.SlideShowSettings.Run()
	# 		return self.getActivePresentationSlideIndex()
	#
	# def click(self):
	# 	win32api.keybd_event(VK_CODE['spacebar'],0,0,0)
	# 	win32api.keybd_event(VK_CODE['spacebar'],0,win32con.KEYEVENTF_KEYUP,0)
	# 	return self.getActivePresentationSlideIndex()
	#
	# def gotoSlide(self,index):
	# 	#跳转到指定的页面
	# 	if self.hasActivePresentation():
	# 		try:
	# 			self.app.ActiveWindow.View.GotoSlide(index)
	# 			return self.app.ActiveWindow.View.Slide.SlideIndex
	# 		except:
	# 			self.app.SlideShowWindows(1).View.GotoSlide(index)
	# 			return self.app.SlideShowWindows(1).View.CurrentShowPosition
	#
	# def nextPage(self):
	# 	if self.hasActivePresentation():
	# 		count = self.getActivePresentationSlideCount()
	# 		index = self.getActivePresentationSlideIndex()
	# 		return index if index >= count else self.gotoSlide(index+1)
	#
	# def prePage(self):
	# 	if self.hasActivePresentation():
	# 		index =  self.getActivePresentationSlideIndex()
	# 		return index if index <= 1 else self.gotoSlide(index-1)
	#
	# def getActivePresentationSlideIndex(self):
	# 	#得到活跃状态的PPT当前的页数
	# 	if self.hasActivePresentation():
	# 		try:
	# 			index = self.app.ActiveWindow.View.Slide.SlideIndex
	# 		except:
	# 			index = self.app.SlideShowWindows(1).View.CurrentShowPosition
	# 	return index
	#
	# def getActivePresentationSlideCount(self):
	# 	#返回处于活跃状态的PPT的页面总数
	# 	return self.app.ActivePresentation.Slides.Count
	#
	# def getPresentationCount(self):
	# 	#返回打开的PPT数目
	# 	return self.app.Presentations.Count
	#
	# def hasActivePresentation(self):
	# 	#判断是否有打开PPT文件
	# 	return True if self.getPresentationCount() > 0 else False
	#
	# def play_wav(self,name):
	# 	#define stream chunk
	# 	chunk = 1024
	#
	# 	#open a wav format music
	# 	f = wave.open(r"./play/" + name + ".wav","rb")
	# 	#instantiate PyAudio
	# 	p = pyaudio.PyAudio()
	# 	#open stream
	# 	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
	# 					channels = f.getnchannels(),
	# 					rate = f.getframerate(),
	# 					output = True)
	# 	#read data
	# 	data = f.readframes(chunk)
	#
	# 	#paly stream
	# 	while data != '':
	# 		stream.write(data)
	# 		data = f.readframes(chunk)
	#
	# 	#stop stream
	# 	stream.stop_stream()
	# 	stream.close()
	#
	# 	#close PyAudio
	# 	p.terminate()

	def play(self,name):
		playsound("./play/" + name + ".mp3")

# if __name__ == '__main__':
# 	ppt = PPTControler()
# 	ppt.fullScreen()
# 	text = ppt.get_text()
# 	# idx = {'pre' : '', 'now' : ''}
# 	for i in range(ppt.getActivePresentationSlideCount()):
# 		str = text[0]
# 		text = text[1:]
# 		# str = bytes(str, encoding = "utf8")
# 		print('play : ' + ppt.get_wav(str) + '.wav')
# 		print('text : ' + ppt.get_str(str))
# 		time.sleep(1)
# 		ppt.nextPage()
