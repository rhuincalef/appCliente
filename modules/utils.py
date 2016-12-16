from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from  kivy.uix.popup import Popup
import numpy
import pcl
import utils
import os

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
#import pcl
#import numpy

def generarDataCsv(nombreArchivoCaptura,dirLocal,nombreCaptura):
	pathFile = dirLocal + "/" + nombreArchivoCaptura
	print "Convirtiendo archivo %s" % pathFile
	print ""
	nube_numpy1 = pcl.load(pathFile).to_array()
	rows_originales = nube_numpy1.shape[0]
	cols_originales = nube_numpy1.shape[1]
	nube_aplanada = nube_numpy1.flatten()
	# nube_numpy = numpy.asarray(map(lambda x: round(x,2),nube_aplanada))
	my_array = map(lambda x: round(x,2),nube_aplanada)
	nube_numpy = numpy.array(map(lambda x: float(round(x,2)),nube_aplanada))
	nube_dimension_ajustada = nube_numpy.reshape(rows_originales,cols_originales)
	print "nube_dimension_ajustada : "
	print nube_dimension_ajustada
	print "Archivo csv: %s" % nombreCaptura
	print ""
	arch_salida = nombreCaptura + ".csv"
	numpy.savetxt(arch_salida, nube_dimension_ajustada ,fmt="%4.6f", delimiter=",")
	print "CSV Data generada correctamente: %s" % arch_salida
	return arch_salida	
# generarDataCsv("nueva_1.pcd",".","nueva_1")


# Retorna el tamanio en bytes de un arreglo de archivos.
# Ej. ["1.pcd","2.pcd"]
def calcularTamanio(archivosCaptura):
	bytes = 0
	for arch in archivosCaptura:
		bytes += os.path.getsize(arch)
	print "Tamanio con capturas: %s es: %s \n" % (archivosCaptura,bytes)
	return bytes

# class Falla(object):
# 	def __init__(self,idFalla=0,calle="",altura="",data_capturas=[]):
# 		self.idFalla = idFalla
# 		self.calle = calle
# 		self.altura = altura
# 		self.data_capturas = data_capturas

# 	def __repr__(self):
# 		return "(idFalla:%s; calle:%s; altura:%s; data_capturas:%s ); " %\
# 				(str(self.idFalla),self.calle,self.altura,self.data_capturas)

from capturador import ItemFalla
# Retorna un listado de objetos de itemFallas configuradas correctamente, y 
# recibe por parametro cada entrada del diccionario.
def parser_fallas(parsed_dict):
	f = estado = None
	if parsed_dict["tipo"] == "informada":
		estado = Informada(parsed_dict["idFalla"],parsed_dict["calle"],
							parsed_dict["altura"])
		f = ItemFalla()
	else:
		estado = Confirmada(parsed_dict["latitud"],parsed_dict["longitud"])
		f = ItemFalla()
	f.setEstado(estado)
	return f








