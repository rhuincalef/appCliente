# -*- coding: utf-8 -*-
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from  kivy.uix.popup import Popup
from kivy.animation import Animation
import numpy
#import pcl
import pypcd
import utils
import os
import subprocess

from os import path
from os import makedirs
from kivy.lang import Builder

import iconfonts
from iconfonts import *

from constantes import *
from capturador import ItemFalla



# Muestra un popup con un boton (por defecto)
#def mostrarDialogo(titulo="",content="",contiene_boton=True,contiene_spinner=False,retornar_animacion=False):
#	layout = GridLayout(cols=1,rows=3)
#	label = Label(text=content,size_hint=(1,0.3))
#	layout.add_widget(label)
#	popup = Popup(title=titulo,
#					content=layout,
#					size_hint=(None, None), 
#					size=(400, 400),
#					auto_dismiss=False)
#	if contiene_spinner:
#		labelRotable = Builder.load_string(SPINNER_LABEL)
		#print "Cargado labelRotable: %s\n" % type(labelRotable)		
#		an = Animation(p=360, duration=1) + Animation(p=0, duration=0)
#		an.repeat = True
##		an.start(labelRotable)
#		layout.add_widget(labelRotable)
#	if contiene_boton:
##		btn = Button(text="Aceptar",size_hint=(1,0.1))
#		layout.add_widget(btn)
#		btn.bind(on_press=popup.dismiss)
#	popup.open()
#	if retornar_animacion:
#		return popup,an
#	return popup

import freenect

#BACKUP!!	
#def conexionSensorEstablecida():		
#	if freenect.sync_get_depth() is None:
#		return False
#	else:
#		return True


#Crea un csv para enviar al servidor.
def generarDataCsv(nombreArchivoCaptura,dirLocal,nombreCaptura):
	#pathFile = dirLocal + "/" + nombreArchivoCaptura
	pathFile = dirLocal + path.sep + nombreArchivoCaptura

	#nube_numpy1 = pcl.load(pathFile).to_array()
	#Se convierte la nube de puntos a un numpy array con shape (LONG_NUBE,3)
	nubeObj = pypcd.PointCloud.from_path(pathFile)
	vacia = map(lambda x:  [x[0],x[1],x[2]] ,nubeObj.pc_data)
	nube_numpy1 = numpy.asarray(vacia)
	

	rows_originales = nube_numpy1.shape[0]
	cols_originales = nube_numpy1.shape[1]
	nube_aplanada = nube_numpy1.flatten()
	# nube_numpy = numpy.asarray(map(lambda x: round(x,2),nube_aplanada))
	my_array = map(lambda x: round(x,2),nube_aplanada)
	nube_numpy = numpy.array(map(lambda x: float(round(x,2)),nube_aplanada))
	nube_dimension_ajustada = nube_numpy.reshape(rows_originales,cols_originales)
	
	#archSalida = nombreCaptura + ".csv"
	archSalida = nombreCaptura + path.extsep +"csv"
	dirCsv = dirLocal + path.sep + CSV_TMP_DIR
	try:
		makedirs(dirCsv)
	except OSError as e:
		if not path.exists(dirCsv):
			#print "Excepcion en OsError: %s\n" % e	
			dirCsv = dirLocal + path.sep 
	finally:
		arch_salida = dirCsv + archSalida
		#print "Guardando csv: %s" % arch_salida
		numpy.savetxt(arch_salida, nube_dimension_ajustada ,fmt="%4.6f", delimiter=",")
		#print "CSV Data generada correctamente: %s" % arch_salida
	return arch_salida	
# generarDataCsv("nueva_1.pcd",".","nueva_1")


# Retorna el tamanio en bytes de un arreglo de archivos.
# Ej. ["1.pcd","2.pcd"]
def calcularTamanio(archivosCaptura):
	bytes = 0
	for arch in archivosCaptura:
		bytes += os.path.getsize(arch)
	return bytes

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

#Instrucciones para generar el .fontd desde el css -->
#https://github.com/kivy-garden/garden.iconfonts
#1. Download Font-Awesome (http://fortawesome.github.io/Font-Awesome/)
#2. Copy both the TTF and CSS files (fonts/fontawesome-webfont.ttf and css/font-awesome.css) to your project
#3. Create and execute a python script to generate your fontd file:
# import iconfonts
# iconfonts.create_fontdict_file('font-awesome.css', 'font-awesome.fontd')
#If everything went well your font dictionary file exists. You can delete the css file (font-awesome.css)

#Genera el .fontd necesario para iconfonts a partir del nombre del .css
def genenerFontDict(nombreCss,nombreFontD):
	#iconfonts.create_fontdict_file('cssIcons/css/font-awesome.css','font-awesome.fontd')
	iconfonts.create_fontdict_file(nombreCss, nombreFontD)

######################## Funciones para la monitorizacion del sensor ###############################


#Librerias para monitoreo usb asincrono -->
from pyudev import Context, Monitor, MonitorObserver
import usb
from sensordata import *

#Retorna un str de hex sin el prefijo '0x'
def convertirAHex(valor):
	cadena = "%04x" % valor
	return cadena

# Escanea los puertos USB y retorna True si todos los dispositivos
# estan listos.
def estaSensorListo():
	busses = usb.busses()
	CAMERA_OK = MOTOR_OK = AUDIO_OK = HUB_OK = False
	for bus in busses:
		devices = bus.devices
		for dev in devices:
			idDev = convertirAHex(dev.idVendor) + ":" + convertirAHex(dev.idProduct)
			#print "Device:%s\n" % dev.filename
			#print "  idVendor: %d 0x(%04x)" % (dev.idVendor, dev.idVendor)
			#print "  idProduct: %d 0x(%04x)" % (dev.idProduct, dev.idProduct)
			#print "idDev= %s; ID_USB_CAMERA: %s\n" % (idDev,ID_USB_CAMERA)
			#print "-----------------------------------------------\n\n"

			if idDev == ID_USB_CAMERA:
				print "Camara detectada!\n"
				CAMERA_OK = True
			if idDev == ID_USB_MOTOR:
				print "Motor detectada!\n"
				MOTOR_OK = True
			if idDev == ID_USB_AUDIO:
				print "Audio detectada!\n"
				AUDIO_OK = True
			if idDev == ID_USB_HUB:
				print "HUB detectado!\n"
				HUB_OK = True
	return CAMERA_OK and MOTOR_OK and AUDIO_OK and HUB_OK 


