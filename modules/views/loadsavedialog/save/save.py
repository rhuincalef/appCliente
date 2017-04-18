# # -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from kivy.app import App



class SaveDialog(GridLayout):
    save = ObjectProperty(None) 
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


def guardar():
	print "Guardado..."
	print ""



from kivy.lang import Builder
Builder.load_file('save.kv')

def dismiss_popup(self):
	print "Cerrando dialog..."
	popup.dismiss()



class Editor(App):
	
	def build(self):
		print "Cargado dialogo guardado de fallas"
		content = SaveDialog(save=guardar, cancel=dismiss_popup)
		if type(content) is None:
			print "Content es None!!!!!\n"
		else:
			print "Content NO es None!!!!!\n"
		# popup = Popup(title="Guardar fallas capturadas", content=content)
		# popup.open()
		return content


if __name__ == '__main__':
    Editor().run()





