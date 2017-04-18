#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from os.path import join, dirname

root = '''
Button:
	text: app.filetext
	on_release: app.mostrar_dialogo_visualizar()
'''
from kivy.properties import StringProperty
from os.path import join, dirname
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.event import EventDispatcher


#Import usado para el bindeo dinamico de metodos handlers de evento_ok y evento_cancel
#a la clase ConfirmPopup.
import types

#https://gist.github.com/kived/742397a80d61e6be225a#file-confirmpopup-py
class ConfirmPopup(Popup,EventDispatcher):
	def __init__(self,titulo = "",msg = "",ok_callback = None,
						cancel_callback = None,
						evento_ok = None,
						evento_cancel = None,
						args = [],
						**kwargs):

		super(ConfirmPopup, self).__init__(size=(400,400),**kwargs)
		super(EventDispatcher, self).__init__(**kwargs)
		layout = GridLayout(cols=1,rows=2)
		label = Label(text=msg,size_hint=(1,0.9))
		layout.add_widget(label)
		self.title = titulo
		self.content = layout
		#self.size = (400,400)
		#self.auto_dismiss = False
		#Se agrega el layout de los botones
		layout_btns = GridLayout(cols=2,rows=1)
		btn1 = Button(text="Si",size_hint=(1,0.1))
		layout_btns.add_widget(btn1)
		btn2 = Button(text="No",size_hint=(1,0.1))
		layout_btns.add_widget(btn2)
		btn1.bind(on_press=self.ok)
		btn2.bind(on_press=self.cancel)
		layout.add_widget(layout_btns)
		self.ok_callback = ok_callback
		self.cancel_callback = cancel_callback
		self.args = args
		self.evento_ok = evento_ok
		self.evento_cancel = evento_cancel
		if (self.evento_ok is not None):
			self.register_event_type(self.evento_ok)
			print "Registrado evento_ok: %s\n" % self.evento_ok
		if (self.evento_cancel is not None):
			self.register_event_type(self.evento_cancel)


	def getArgs(self):
		return self.args

	#def patch_me(target):
	#    def method(target,x):
	#		print "x=",x
	#		print "called from", target
	#	target.method = types.MethodType(method,target)


	def on_iniciar_dialogo_descarte_captura(self):
		pass
	
	def ok(self,evt):
		self.ok_callback(self.args)
		if (self.evento_ok is not None):
			print "Disparando evento_ok: %s\n" % self.evento_ok
			self.dispatch(self.evento_ok)
		self.dismiss()
	
	def cancel(self,evt):
		self.cancel_callback(self.args)
		if (self.evento_cancel is not None):
			print "Disparando evento_cancel: %s\n" % self.evento_cancel
			self.dispatch(self.evento_cancel)
		self.dismiss()


class Capturador:
	def descartar(self,nombresCapturas):
		for captura in nombresCapturas:
			print "Borrando la captura %s de disco\n" % captura



class TestApp(App):
	filetext = StringProperty('Press Me')
	
	def __init__(self,**kwargs):
		super(TestApp, self).__init__(**kwargs)
		self.capturador = Capturador()
		self.capturadorInformados = Capturador()

	def build(self):

		return Builder.load_string(root)
	
	def mostrar_dialogo_visualizar(self):
		print "Presionado"
		# NOTA: El nombre de la captura .pcd y .csv  son enviados desde el metodo capturador.capturar()
		# en appCliente
		capturaPcd = 'mycaptura.pcd'
		capturaCsv = 'mycaptura.csv'

		popupVisualizar = ConfirmPopup(titulo="Dialogo de prueba",
						msg="¿Desea visualizar la captura?",
						ok_callback = self.mostrar_captura,
						cancel_callback = self.no_mostrar_captura,
						evento_ok =  'on_iniciar_dialogo_descarte_captura',
						evento_cancel =  'on_iniciar_dialogo_descarte_captura',
						args = [capturaPcd,capturaCsv] )

		popupVisualizar.bind(on_iniciar_dialogo_descarte_captura = self.mostrarDialogoConservar)
		popupVisualizar.open()

	def mostrarDialogoConservar(self,nombresCaptura):
		print "En mostrarDialogoConservar()...\n"
		popupConservar = ConfirmPopup(titulo="Dialogo de prueba 2",
						msg="¿Desea conservar la captura?",
						ok_callback = self.conservar,
						cancel_callback = self.descartar,
						args = nombresCaptura)
		popupConservar.open()


	def descartar(self,popup):
		print "En descartar()..."
		capturas = popup.getArgs()
		print "Las capturas recibidsa son :%s\n" % capturas
		self.capturador.descartar(capturas)
		self.capturadorInformados.descartar(capturas)


	def conservar(self,popup):
		print "Se conserva la captura en disco!"
	
	def mostrar_captura(self,args):
		print "Visualizando captura...\n"

	def no_mostrar_captura(self,args):
		print "No se visualizara la captura...\n"



if __name__ == '__main__':
	TestApp().run()