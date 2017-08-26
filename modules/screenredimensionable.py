# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.screenmanager import Screen,ScreenManager
from constantes import ESCALA_PADDING_HORIZONTAL,ESCALA_SPACING_VERTICAL
from kivy.core.window import Window

class ScreenRedimensionable(Screen):
	def __init__(self,**kwargs):
		super(ScreenRedimensionable, self).__init__(**kwargs)

	def redimensionarFooter(self,nuevoAnchoVentana):
		if self.ids.footer_layout is None:
			print "No tiene footer!\n"
			return
		self.ids.footer_layout.padding = [
											nuevoAnchoVentana * ESCALA_PADDING_HORIZONTAL,
											self.ids.footer_layout.padding[1],
											nuevoAnchoVentana * ESCALA_PADDING_HORIZONTAL,
											self.ids.footer_layout.padding[3] 
											]
		self.ids.footer_layout.spacing = [( Window.width * ESCALA_SPACING_VERTICAL ),0]
		print "modificado el spacing y layout en footer!\n"





