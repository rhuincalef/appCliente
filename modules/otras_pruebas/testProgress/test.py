# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
import threading
import time
from kivy.clock import Clock

class MainApp(App):
	def __init__(self,**kwargs):
		super(MainApp,self).__init__()
		print "instanciada app!"
		self.pb = None
		self.valorProgress = 0

	def build(self):
		box = BoxLayout(orientation='vertical')
		#pb = ProgressBar(max = 100000)
		self.pb = ProgressBar(max = 14682499)
		box.add_widget(self.pb)
		t = threading.Thread(name= 'threadModificarProgressBar',
							target= self.threadModPb,
							args = ())
		t.setDaemon(True)
		t.start()
		print "Iniciado thread...\n"
		#Clock.schedule_interval(self.threadModPb, 0.000005)
		#Clock.schedule_interval(self.threadModPb, 0.0004)
		Clock.schedule_interval(self.actualizarPb, 0.0004)
		return box

	def threadModPb(self):
		while self.valorProgress < self.pb.max:
			time.sleep(0.004)
			self.valorProgress += 8600
			print "Modificado self.valorProgress con valor: %s\n" % self.valorProgress
		print "Fin de thead! desplanificando eventos...\n"
		Clock.unschedule(self.actualizarPb)
		print "smsssssssssssssssssssssssssssss\n"
		print "smsssssssssssssssssssssssssssss\n"
		print "smsssssssssssssssssssssssssssss\n"
		print "smsssssssssssssssssssssssssssss\n"
		print "smsssssssssssssssssssssssssssss\n"


	def actualizarPb(self,dt):
		self.pb.value = self.valorProgress
		print "Actualizada pb con: %s\n" % self.pb.value



	#def threadModPb(self,dt):		
		#time.sleep(0.00041)
	#	self.pb.value += 8600
	#	print "Modificado pb con valor: %s\n" % self.pb.value


if __name__ == '__main__':
    MainApp().run()




