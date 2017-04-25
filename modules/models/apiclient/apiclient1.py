# -*- coding: utf-8 -*-
# Clase que realiza la comunicacion con el servidor para obtener los baches
#  y subir archivos al servidor
import kivy
kivy.require('1.0.5')

from kivy.app import App
from constantes import *
import requests
from requests.exceptions import ConnectionError
import requests
from json import JSONDecoder	
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
#from clint.textui.progress import Bar as ProgressBar

import utils
import threading

import urllib


#Excepcion para el servidor de la webapp offline.
class ExcepcionServidorOffLine(Exception):
	pass

# Clase para un getInformados vacio! 
class ExcepcionSinInformados(Exception):
	pass

#Excepcion para un error en una peticion Ajax.
class ExcepcionAjax(Exception):
	pass
# Instalar requests con pip y toolbelt request
# sudo pip install requests-toolbelt

class ApiClientApp(object):
	def __init__(self):
		self.conexionServer = requests
		self.bytes_leidos = 0
		self.monitor_bytes_leidos = 0 #Se emplea por el callback del clock que
										#actualiza la vista
		self.ya_actualizado = False
		self.bytes_acumulados = 0

	def getInformados(self,calle1):
		calle = urllib.quote_plus(calle1).encode('utf-8')
		print "Obteniendo baches sobre calle:%s\n " % calle
		try:
			results_json = {}
			peticion = URL_INFORMADOS + calle 
			print "peticion -->"
			print peticion
			response = self.conexionServer.get(peticion)
			if response.status_code == 200:
				results_json = response.json()
				print "La respuesta en formato json es: "
				print results_json
			else:
				msg = "Error en peticion del servidor. Codigo: %s" % response.status_code
				print "\n%s\n\n" % msg
				raise ExcepcionAjax(msg)
		except ValueError,e:
			msg = "Error parseando la peticion a formato JSON.Peticion impresa en la linea de comandos."
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
			print "Cuerpo de la peticion: \n %s" % response.text 
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
			raise ExcepcionAjax(msg)
		except ConnectionError, e:
			print "ConnectionError: %s\n" % e
			msg = "Error al establecer conexion con el servidor.\nServidor fuera de linea."
			raise ExcepcionAjax(msg)
		#RETURN para el servidor remoto
		if len(results_json["datos"]) == 0:
			raise ExcepcionSinInformados("No hay fallas registradas sobre la calle ingresada")
		return self.parsear_inf(results_json["datos"])

	#Metodo de parseo para el diccionario de baches informados.
	def parsear_inf(self,dic):
		valores = dict()
		for key,tupla in dic.iteritems():
			valores[key] = dict(id=int(tupla["id"]),
								calle=str(tupla["calle"]),
								altura=int(tupla["altura"]) )
		print "dic. valores parseados: %s\n" % valores
		return valores



	def postCapturas(self,url,dic_envio,nombreCapturas,bytes_leidos,logger):
		#self.bytes_leidos =  bytes_leidos
		self.bytes_leidos =  0
		#Crea el objeto encoder para el multipart/form-data con el dic_envio de la 
		# peticion correspondiente a la falla actual.
		encoder = self.create_upload(dic_envio,nombreCapturas)
		monitor = MultipartEncoderMonitor(encoder, self.actualizar_datos_callback)
		r = requests.post(url, data=monitor,headers={'Content-Type': monitor.content_type})
		print('\nUpload finished! (Returned status {0} {1})'.format(
			r.status_code, r.reason
		))


		# Se lee la respuesta como un dic con strings unicode y se loguea 
		# el resultado en disco.
		#
		print "Registrando la respuesta...\n"
		dicRespuesta = r.json()
		infolog = str(dicRespuesta["respuesta"]) 
		utils.loggearMensaje(logger,infolog)
		# Si ocurre un 500 Error se lanza una excepcion.
		if (r.status_code != requests.codes.ok) or ( int(dicRespuesta["estadoGeocoding"]) in CODIGOS_ERROR_GEOCODING):
			raise ExcepcionAjax("Error de servidor subiendo las fallas.\nMás información en %s%s" %\
			 (LOGS_DEFAULT_DIR,LOG_FILE_CAPTURAS_INFO_SERVER ))

		return self.bytes_leidos

	# Actualiza los datos que se muestran respecto del nombre del archivo actual
	#  y la cantidad de bytes enviados/cantidad bytes totales.
	def actualizar_datos_callback(self,monitor):
		controlador = App.get_running_app()
		# Se incrementa el contador solamente si termino y no se actualizo
		# previamente.
		self.bytes_acumulados += monitor.bytes_read - self.bytes_leidos
		self.bytes_leidos = monitor.bytes_read
		#self.bytes_acumulados += 8192

		# NOTA: monitor.encoder.finished es llamado cada vez que un archivo
		# termina de subirse.
		#print "En apiclient.actualizar_datos_callback() con self.bytes_leidos: %s ; monitor.bytes_read: %s; self.bytes_acumulados: %s\n" %\
		#			(self.bytes_leidos,monitor.bytes_read,self.bytes_acumulados)

	# Retorna el objeto MultipartEncoder.Obtiene los datos del dic_envio
	# para la falla actual.
	def create_upload(self,dic_envio,nombreCapturas):
		#dic_envio = {
		#				#TODO: Cambiar esto por el idFalla real cuando este subido.
						#'id': str(4).encode("utf-8"),
		#				'id': str(dic_falla["id"]).encode("utf-8"),
		#				'calle': str(dic_falla["calle"]).encode("utf-8"),
		#				'altura': str(dic_falla["altura"]).encode("utf-8")
		#			}
		#for capturaCsv in dic_falla["data_capturas"]:
		#	dic_envio[capturaCsv] = (capturaCsv,open(capturaCsv,'rb'),'csv')

		#NOTA: Los archivos que se envien al server deben estar indexados
		# por el nombre del archivo de captura (sin extension) para que 
		# funcione la subida.
		#for capturaCsv in dic_envio["data_capturas"]:
		#	dic_envio[capturaCsv] = (capturaCsv,open(capturaCsv,'rb'),'csv')

		for capturaCsv in nombreCapturas:
			dic_envio[capturaCsv] = (capturaCsv,open(capturaCsv,'rb'),'csv')

		#print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		#print "dic_envio contiene -->"
		#print dic_envio
		#print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		#print ""
		encoder = MultipartEncoder(dic_envio)
		return encoder

	#Obtiene la direccion(calle,altura) estimada dada una lat,long
	def obtenerDirEstimada(self,latitud,longitud):
		results_json = {}
		peticion = URL_GET_DIRECCION +'latitud/'+ str(latitud) +'/longitud/'+str(longitud) 
		response = self.conexionServer.get(peticion)
		calle = "No disponible"
		#altura = -1
		rangoEstimado1 =rangoEstimado2= -1
		try:
			#Problema con el json enviado desde el server
			if response.status_code == 200:
				results_json = response.json()
				print results_json
			else:
				msg = "Error en peticion del servidor. Codigo: %s" % response.status_code
				print msg

			if results_json["estado"] == 0:
				calle = results_json["calle"].encode("utf8") 
				#altura = int(results_json["altura"] )
				rangoEstimado1 = int(results_json["rangoEstimado1"] )
				rangoEstimado2 = int(results_json["rangoEstimado2"] )

		except ConnectionError, e:
			msg = "Error al establecer conexion con el servidor.\nServidor fuera de linea."
			print msg
			#raise ExcepcionAjax(msg)

		except ValueError,e:
			msg = "Error parseando la peticion a formato JSON.Peticion impresa en la linea de comandos."
			print msg
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
			print "Cuerpo de la peticion: \n %s" % response.text 
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
		except Exception,e:
			msg = "Error desconocido en obtenerDirEstimada(): %s" % e
			print msg
		finally:
			#return (calle,altura)
			return (calle,rangoEstimado1,rangoEstimado2)


#FORMATO A PARSEAR -->
#listadoTiposFalla = [
# 	{
# 	"clave": "tipoFalla",
# 	"valor": "Bache",
# 	"colPropsAsociadas": [
#			 		{"clave": "tipoReparacion", "valor":"Sellado"},
#			 		{"clave": "tipoReparacion", "valor":"Cementado"},
#			 		{"clave": "tipoMaterial", "valor":"Pavimento asfaltico"]},
#			 		{"clave": "tipoMaterial", "valor":"Cemento"},
#			 		...
#					]
#	},
# 	...	
#]
	def parsear_datos_confirmados(self,dic):
		listaTFalla = []
		for tipoFalla in dic:
			dicParseado = {}
			dicParseado["clave"] = str(tipoFalla["clave"])
			dicParseado["valor"] = str(tipoFalla["valor"])
			listaPropsAsociadas = []
			for prop in tipoFalla["colPropsAsociadas"]:
				d = {}
				d["clave"] = str(prop["clave"])
				d["valor"] = str(prop["valor"])
				listaPropsAsociadas.append(d)

			dicParseado["colPropsAsociadas"] = listaPropsAsociadas
			listaTFalla.append(dicParseado)
		return listaTFalla


	def getPropsConfirmados(self):
		results_json = {} 
		try:
			response = self.conexionServer.get(URL_GET_PROPS_CONFIRMADAS)
			if response.status_code == 200:
				results_json = response.json()
			else:
				msg = "Error en peticion del servidor. Codigo: %s" % response.status_code
				raise ExcepcionAjax(msg)
			
		except ValueError,e:
			msg = "Error parseando la peticion a formato JSON.Peticion impresa en la linea de comandos."
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
			print "Cuerpo de la peticion: \n %s" % response.text 
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
			raise ExcepcionAjax(msg)

		except ConnectionError, e:
			msg = "Error al establecer conexion con el servidor.\nServidor fuera de linea.Buscando BD con\n atributos de tipos de fallas en disco."
			raise ExcepcionAjax(msg)
		return self.parsear_datos_confirmados(results_json)


