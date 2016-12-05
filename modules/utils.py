from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from  kivy.uix.popup import Popup

def conexionSensorEstablecida():
		import freenect
		if freenect.sync_get_depth() is None:
			return False
		else:
			return True


# Muestra un popup con un boton (por defecto)
def mostrarDialogo(titulo="",content="",contiene_boton=True):
	layout = GridLayout(cols=1,rows=2)
	label = Label(text=content,size_hint=(1,0.9))
	layout.add_widget(label)
	popup = Popup(title=titulo,
					content=layout,
					size_hint=(None, None), 
					size=(400, 400),
					auto_dismiss=False)
	if contiene_boton:
		btn = Button(text="Aceptar",size_hint=(1,0.1))
		layout.add_widget(btn)
		btn.bind(on_press=popup.dismiss)

	popup.open()








