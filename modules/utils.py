from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from  kivy.uix.popup import Popup
import numpy
import pcl


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


#Crea un csv para enviar al servidor.
def generarDataCsv(nombreArchivoCaptura,dirLocal,nombreCaptura):
	pathFile = dirLocal + "/" + nombreArchivoCaptura
	print "Convirtiendo archivo %s" % pathFile
	print ""
	nube_numpy1 = pcl.load(pathFile).to_array()
	rows_originales = nube_numpy1.shape[0]
	cols_originales = nube_numpy1.shape[1]
	nube_aplanada = nube_numpy1.flatten()
	nube_numpy = numpy.asarray(map(lambda x: round(x,8),nube_aplanada))
	nube_dimension_ajustada = nube_numpy.reshape(rows_originales,cols_originales)
	print "nube_dimension_ajustada : "
	print nube_dimension_ajustada
	print "Archivo csv: %s" % nombreCaptura
	print ""
	arch_salida = nombreCaptura + ".csv"
	numpy.savetxt(arch_salida, nube_dimension_ajustada , delimiter=",")
	print "CSV Data generada correctamente: %s" % arch_salida
	return arch_salida
	

# generarDataCsv("falla_nueva_1.pcd",".")





