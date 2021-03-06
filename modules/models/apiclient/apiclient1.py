# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from constantes import *
import requests
from requests.exceptions import ConnectionError
import requests
from json import JSONDecoder	
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
import utils
import threading
import urllib


# 
class ExcepcionSinInformados(Exception):
	"""Clase para un getInformados vacio. """
	pass

class ExcepcionAjax(Exception):
	"""Excepcion para un error en una peticion Ajax al servidor. """
	pass

class ExcepcionDesconexion(Exception):
	""" Excepcion por desconexion con el servidor. """
	pass

class ApiClientApp(object):
	"""Clase que realiza la comunicacion con el servidor para obtener los baches y 
		subir archivos al servidor."""
	def __init__(self):
		self.conexionServer = requests
		self.bytes_leidos = 0
		self.monitor_bytes_leidos = 0 #Se emplea por el callback del clock que
										#actualiza la vista
		self.ya_actualizado = False
		self.bytes_acumulados = 0

	def getInformados(self,calle1):
		""" Metodo para la obtencion de fallas informadas desde el servidor web. """
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

	def parsear_inf(self,dic):
		"""Metodo de parseo para el diccionario de baches informados."""
		valores = dict()
		for key,tupla in dic.iteritems():
			valores[key] = dict(id=int(tupla["id"]),
								calle=str(tupla["calle"]),
								altura=int(tupla["altura"]) )
		print "dic. valores parseados: %s\n" % valores
		return valores


	def postCapturas(self,url,dic_envio,nombreCapturas,bytes_leidos,logger):
		self.bytes_leidos =  0
		try:
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
			print "Registrando la respuesta...\n"
			dicRespuesta = r.json()
			infolog = str(dicRespuesta["respuesta"]) 
			utils.loggearMensaje(logger,infolog)

			# Si ocurre un 500 Error se lanza una excepcion.
			if (r.status_code != requests.codes.ok) or ( int(dicRespuesta["estadoGeocoding"]) in CODIGOS_ERROR_GEOCODING):
				raise ExcepcionAjax("Error de servidor subiendo las fallas.\nMás información en %s%s" %\
				 (LOGS_DEFAULT_DIR,LOG_FILE_CAPTURAS_INFO_SERVER ))

			return self.bytes_leidos
		except ConnectionError as e:
			msgError = "Error de conexion con el servidor.\n Servidor Offline."
			print msgError
			raise ExcepcionDesconexion(msgError)
	
		#except Exception as e:
		#	msgError = "Error desconocido al intentar enviar capturas al servidor(%s)" % e
		#	raise ExcepcionDesconexion(msgError)
		#finally:
		#	print msgError


	
	def actualizar_datos_callback(self,monitor):
		"""Actualiza los datos que se muestran respecto del nombre del archivo actual
			y la cantidad de bytes enviados/cantidad bytes totales. """
		controlador = App.get_running_app()
		# Se incrementa el contador solamente si termino y no se actualizo
		# previamente.
		self.bytes_acumulados += monitor.bytes_read - self.bytes_leidos
		self.bytes_leidos = monitor.bytes_read

		# NOTA: monitor.encoder.finished es llamado cada vez que un archivo
		# termina de subirse.
		#print "En apiclient.actualizar_datos_callback() con self.bytes_leidos: %s ; monitor.bytes_read: %s; self.bytes_acumulados: %s\n" %\
		#			(self.bytes_leidos,monitor.bytes_read,self.bytes_acumulados)



	def create_upload(self,dic_envio,nombreCapturas):
		"""Retorna el objeto MultipartEncoder.Obtiene los datos del dic_envio para la falla actual.

		El formato de los archivos subidos recibido en dic_envio es el siguiente:
		dic_envio = {
						'id': str(4).encode("utf-8"),
						'id': str(dic_falla["id"]).encode("utf-8"),
						'calle': str(dic_falla["calle"]).encode("utf-8"),
						'altura': str(dic_falla["altura"]).encode("utf-8")
					}.

		"""
		#NOTA: Los archivos que se envien al server deben estar indexados
		# por el nombre del archivo de captura (sin extension) para que 
		# funcione la subida.
		for capturaCsv in nombreCapturas:
			dic_envio[capturaCsv] = (capturaCsv,open(capturaCsv,'rb'),'csv')
		encoder = MultipartEncoder(dic_envio)
		return encoder

	def obtenerDirEstimada(self,latitud,longitud):
		"""Obtiene la direccion(calle,altura) estimada dado la latitud y longitud. """
		results_json = {}
		peticion = URL_GET_DIRECCION +'latitud/'+ str(latitud) +'/longitud/'+str(longitud) 
		response = self.conexionServer.get(peticion)
		calle = "No disponible"
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
				print "calle casteada: %s\n" % calle
				print "results_json[rangoEstimado1]: %s\n" % results_json["rangoEstimado1"] 
				print "results_json[rangoEstimado2]: %s\n" % results_json["rangoEstimado2"] 
				if results_json["rangoEstimado1"] is not None:
					rangoEstimado1 = int(results_json["rangoEstimado1"] )
				if results_json["rangoEstimado2"] is not None:
					rangoEstimado2 = int(results_json["rangoEstimado2"] )

		except ConnectionError, e:
			msg = "Error al establecer conexion con el servidor.\nServidor fuera de linea."
			print msg
		except ValueError,e:
			msg = "Error parseando la peticion a formato JSON.Peticion impresa en la linea de comandos."
			print msg
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
			print "Cuerpo de la peticion: \n %s" % response.text 
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
		except Exception,e:
			msg = "Error desconocida (%s) en obtenerDirEstimada(): %s" % (type(e),e)
			print msg
		finally:
			print "En finally...\n"
			print "rangoEstimado1: %s\n" % rangoEstimado1
			print "rangoEstimado2: %s\n" % rangoEstimado2
			return (calle,rangoEstimado1,rangoEstimado2)

	
	def parsearDatosConfirmados(self,dic):
		"""Realiza el parseo de propiedades confirmadas obtenidas desde el servidor.

		Formato que parsea desde el servidor el metodo parsearDatosConfirmados():

		listadoTiposFalla = [
			{
			"clave": "tipoFalla",
			"valor": "Bache",
			"colPropsAsociadas": [
					 		{"clave": "tipoReparacion", "valor":"Sellado"},
					 		{"clave": "tipoReparacion", "valor":"Cementado"},
					 		{"clave": "tipoMaterial", "valor":"Pavimento asfaltico"]},
					 		{"clave": "tipoMaterial", "valor":"Cemento"},
					 		...
							]
			},
			...	
		].
		"""
		listaTFalla = []
		print "4...\n"
		for tipoFalla in dic:
			dicParseado = {}
			dicParseado["clave"] = str(tipoFalla["clave"].encode("utf-8"))
			dicParseado["valor"] = str(tipoFalla["valor"].encode("utf-8"))
			#NOTA: Los "tiposFalla" y sus propiedades asociadsa directas tienen
			# id asociado. Las propsAsociadas de estas propiedades no.
			dicParseado["id"] = str(tipoFalla["id"].encode("utf-8"))
			listaPropsAsociadas = []
			for prop in tipoFalla["colPropsAsociadas"]:
				d = {}
				d["clave"] = str(prop["clave"].encode("utf-8"))
				d["valor"] = str(prop["valor"].encode("utf-8"))
				d["id"] = str(prop["id"].encode("utf-8"))
				#Si la subpropiedad tiene propiedades asociadas se las asocia.
				#Esta parte se emplea para la "ponderacion" que se asocia a la criticidad.
				d["colPropsAsociadas"] = []
				if prop.has_key("colPropsAsociadas"):
					for e in prop["colPropsAsociadas"]:
						aux = {}
						aux["clave"] = str(e["clave"].encode("utf-8"))
						aux["valor"] = e["valor"]
						d["colPropsAsociadas"].append(aux)

				listaPropsAsociadas.append(d)

			dicParseado["colPropsAsociadas"] = listaPropsAsociadas
			listaTFalla.append(dicParseado)
		print "5...\n"
		print "listaTFalla:\n %s \n" % listaTFalla
		return listaTFalla

	def getPropsConfirmados(self):
		"""Realiza la obtencion de propiedades confirmadas al servidor. """
		results_json = {} 
		print "EN getPropsConfirmadas()...\n"
		try:
			response = self.conexionServer.get(URL_GET_PROPS_CONFIRMADAS,timeout = 8)
			#response = self.conexionServer.get(URL_GET_PROPS_CONFIRMADAS)
			print "Respuesta servidor: %s\n" % response
			if response.status_code == 200:
				results_json = response.json()
				print "type(results_json): %s\n" % results_json
			else:
				msg = "Error en peticion del servidor. Codigo: %s" % response.status_code
				raise ExcepcionAjax(msg)
			print "2...\n"
		except ValueError,e:
			print "Value error en getProspConfirmada()!\n"
			msg = "ValueError: Error parseando la peticion a formato JSON (response.text = %s)\n" % response.text
			raise ExcepcionAjax(msg)

		except ConnectionError, e:
			print "ConnectionError en getPropsConfirmados()!\n"
			#msg = "Error al establecer conexion con el servidor.\n (Excepcion ConnectionError: %s)" % e.message
			msg = "Error al establecer conexion con el servidor.Inaccesible."
			print msg
			raise ExcepcionAjax(msg)
		print "3...\n"
		return self.parsearDatosConfirmados(results_json)


	
	def solicitarSugerencias(self,nombreCalle,cantMaximaSugerencias):
		"""Metodo empleado en el autcompletar para la busqueda de fallas sobre una calle, dado un nombre de calle
			y una cantidad maxima de sugerencias (configurada en constantes.py). """

		#2. Se hace una peticion ajax al servidor al controlador.Se envian la cadena y
		# la cantidad al servidor para obtener solamente esa cantidad como maximo.
		# controlador.obtenerSugerenciasCalles(myCalle,CANT_SUGERENCIAS) y se obtienen
		# las calles que tienen esa secuencia de caracteres con regex's.
		print "En solicitarSugerencias()!!!\n\n"
		sugerenciasObtenidas = []
		calleCodificada = urllib.quote_plus(nombreCalle.encode("utf-8"))
		
		print "calleCodificada(%s)!!!\n\n" % calleCodificada
		
		results_json = {}
		peticion = URL_OBTENER_SUGERENCIAS_CALLES + "/calle/" + calleCodificada + \
			"/cantmaxsugerencias/" + str(cantMaximaSugerencias)

		print "peticion enviada:\n\n %s \n" % peticion
		try:
			response = self.conexionServer.get(peticion)
			if response.status_code == 200:
				results_json = response.json()
				sugerenciasObtenidas = results_json
				print "La respuesta en formato json de solicitarSugerencias() es: "
				print results_json
			else:
				msg = "Error en peticion del servidor. Codigo: %s" % response.status_code
				print "\n%s\n\n" % msg

		except ValueError,e:
			msg = "Error parseando la peticion a formato JSON.Peticion impresa en la linea de comandos."
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
			print "Cuerpo de la peticion: \n %s" % response.text 
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
			
		except ConnectionError, e:
			print "ConnectionError: %s\n" % e
			msg = "Error al establecer conexion con el servidor.\nServidor fuera de linea."
			
		except Exception, e:
			print "Excepcion desconocida en solicitarSugerencias(): %s\n" % e
			msg = "Excepcion desconocida en solicitarSugerencias(): %s\n" % e

		finally:
			return sugerenciasObtenidas
