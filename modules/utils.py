# -*- coding: utf-8 -*-
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from  kivy.uix.popup import Popup
from kivy.animation import Animation
import numpy
import kivy
#import pcl
import pypcd
import utils
import os,sys
import subprocess

from os import path
from os import makedirs
from kivy.lang import Builder

from constantes import *
# Este metodo agrega los directorios de todos los modulos y utilidades que se usan
# al path actual 
def cargarConfiguraciones():
	for pathRecurso in PATHS_MODULOS:
		sys.path.append(os.path.join(os.getcwd(), pathRecurso) )
		print "agregando al path: %s\n" % os.path.join(os.getcwd(), pathRecurso)
	kivy.resources.resource_add_path(RESOURCE_THEME_KIVY)
	print "configuraciones de directorios cargadas!\n"


cargarConfiguraciones()

import iconfonts
from iconfonts import *
from capturador import ItemFalla
import logging,time
import freenect


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




# Configura y retorna una instancia de Logger para el archivo .info.
def instanciarLogger(logFile,logLevel=LOGGING_DEFAULT_LEVEL,appLogging=APP_NAME_LOGGING):
	if not os.path.exists(LOGS_DEFAULT_DIR):
		os.makedirs(LOGS_DEFAULT_DIR)
	logger = logging.getLogger(appLogging)
	hdlr = logging.FileHandler(LOGS_DEFAULT_DIR + logFile)
	formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s",
                              "%d/%m/%Y-- %H:%M:%S")
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.INFO)
	return logger

#Cambia el formato del logger para actualizar la fecha y registrar el msg
# con la fecha y hora actual.
def loggearMensaje(logger,msg):
	print "Llamado loggearMensaje...\n"
	logger.info(msg)
	logger.info("")



# URL CONFIRMADAS -->
# s = "http://localhost/repoProyectoBacheo/restapi/obtener_props_confirmadas"
#

# Retorna la propiedad con caracteres unicode convertidos a string
#
#def adaptarPropiedadConfirmada(elementoDic):
#	nuevoElem = {}
##	nuevoElem = 
#	return nuevoElem
def convertirJson(url):
	from json import JSONDecoder
	JSONDecoder(object_hook=adaptarPropiedadConfirmada).decode()


# Esta funcion escapa un string con caracteres espciales, insertando
# "\\" delante de los caracteres especiales que comienzan con "\\" para que pueda ser levantado con JSON.
# La propiedad confirmada de entrada de la falla fue convertida con str(),
# y para luego ser escapada.

#In [36]: p
#Out[36]: {'clave': 'tipoReparacion', 'valor': 'Cement\xc3\xa1r'}

#In [37]: val  = str(p)

#In [38]: val
#Out[38]: "{'clave': 'tipoReparacion', 'valor': 'Cement\\xc3\\xa1r'}"

#In [41]: json.dumps('Cement\\xc3\\xa1r')
#Out[41]: '"Cement\\\\xc3\\\\xa1r"'


#VERSION QUE FUNCIONA-->
#In [15]: p = {'clave': 'tipoReparacion', 'valor': 'Cement\xc3\xa1r'}

#In [16]: str(p)
#Out[16]: "{'clave': 'tipoReparacion', 'valor': 'Cement\\xc3\\xa1r'}"

#In [17]: str(p).replace('\\x','\\\\x')
#Out[17]: "{'clave': 'tipoReparacion', 'valor': 'Cement\\\\xc3\\\\xa1r'}"

#In [18]: c = str(p).replace('\\x','\\\\x')

# [26]: c
#Out[26]: "{'clave': 'tipoReparacion', 'valor': 'Cement\\\\xc3\\\\xa1r'}"

#In [27]: final = c.replace("'",'"')
#Out[27]: '{"clave": "tipoReparacion", "valor": "Cement\\\\xc3\\\\xa1r"}'

#In [31]: json.loads(final)
#Out[31]: {u'clave': u'tipoReparacion', u'valor': u'Cement\\xc3\\xa1r'}



#Conversión de caracteres de utf8 a unicode
#In [63]: codigo
#Out[63]: '\xc3\xa1'

#In [64]: unicode(codigo,encoding="utf8")
#Out[64]: u'\xe1'

#In [68]: print unicode("Rodrig\xc3\xa1",encoding="utf8")
#Rodrigá


#In [70]: cad =  '{"clave": "tipoReparacion", "valor": "Cement\xc3\xa1r"}'

#In [71]: unicode(cad,encoding="utf8")
#Out[71]: u'{"clave": "tipoReparacion", "valor": "Cement\xe1r"}'

#In [72]: cad2  = unicode(cad,encoding="utf8")

#In [73]: cad2
#Out[73]: u'{"clave": "tipoReparacion", "valor": "Cement\xe1r"}'

#In [74]: json.loads(cad2)
#Out[74]: {u'clave': u'tipoReparacion', u'valor': u'Cement\xe1r'}




# Recibe un diccionario de propiedades y retorna una cadena de las propiedades
# codificadas en unicode (con caracteres especiales convertidos), lista para
# leer como json. 
# NOTA IMPORTANTE: Para decodificar como json se debe convertir a unicode y reemplazar
# los caracteres unicode que comienzan con \xNN con \uNNNN, donde N son numeros
# hexadecimales.
# Equivalencias en representación hexadecimal entre UNICODE Y UTF8 -->
#http://www.utf8-chartable.de/unicode-utf8-table.pl?start=128&number=128&utf8=string-literal&unicodeinhtml=hex

#Problema invalir caracter \xNN-->
#https://stackoverflow.com/questions/4296041/simplejson-loads-get-invalid-escape-x 

#In [145]: json.loads('{"clave": "tipoReparacion", "valor": "Cement\u00e1r"}')
#Out[145]: {u'clave': u'tipoReparacion', u'valor': u'Cement\xe1r'}

#In [146]: print json.loads('{"clave": "tipoReparacion", "valor": "Cement\u00e1r"}')
#{u'clave': u'tipoReparacion', u'valor': u'Cement\xe1r'}

#In [147]: j = json.loads('{"clave": "tipoReparacion", "valor": "Cement\u00e1r"}')

#In [148]: type(j)
#Out[148]: dict

#In [150]: print j['valor']
#Cementár

def escaparCaracteresEspeciales(propiedad):
	print "en escaparCaracteresEspeciales()...\n"
	dic = {}
	dic['clave'] = unicode(propiedad['clave'],encoding="utf8")
	dic['valor'] = unicode(propiedad['valor'],encoding="utf8")
	print "dic nuevo: %s\n" % dic 
	# Se reemplazan las comillas, se eliminan las 'u' de la cadena final y,
	# se reemplazan los \x por \u00 para que cumplan con el estandar de JSON.
	codificada = unicode(dic).replace("'",'"')
	codificada = codificada.replace("u","").replace("\\x","\\u00")
	print "codificada: %s\n" % codificada
	return codificada 






