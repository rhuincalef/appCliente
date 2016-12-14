# Clase que realiza la comunicacion con el servidor para obtener los baches
#  y subir archivos al servidor
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
from clint.textui.progress import Bar as ProgressBar
from constantes import *


class ExcepcionAjax(Exception):
	pass



# Instalar requests con pip y toolbelt request
# sudo pip install requests-toolbelt

class ApiClientApp(object):
	def __init__(self):
		self.conexionServer = requests
		# Cantidad total de bytes a subir por peticion POST. 
		self.long_total_bytes = 0
		# Nombre de la captura actual subiendo
		self.nombre_archivo_actual = ""

	def getInformados(self,calle):
		print "Obteniendo baches sobre calle: ",calle
		print ""
		try:
			results_json = {}
			peticion = URL_INFORMADOS+ "/" + calle
			response = self.conexionServer.get(URL_INFORMADOS)
			if response.status_code == 200:
				results_json = response.json()
				print "La respuesta en formato json es: "
				print results_json
			else:
				msg = "Error en peticion del servidor. Codigo: %s" % response.status_code
				raise ExcepcionAjax(msg)
				
		except ConnectionError, e:
			msg = "Error al establecer conexion con el servidor.\nServidor fuera de linea."
			raise ExcepcionAjax(msg)

		return results_json


	def postCapturas(self,url,dic_falla):
		#TODO: CAMBIAR ESTO POR LA FALLA QUE CORRESPONDA, CUANDO ESTE SUBIDA AL SERVER!!
		m = MultipartEncoder(fields={'id': str(8).encode("utf-8") })
		request_verificar_bache = requests.post(URL_CHECK_FALLA, data=m,
			headers={'Content-Type': m.content_type})

		if request_verificar_bache.status_code != requests.codes.ok:
			raise ExcepcionAjax("Error comprobando la existencia de la falla en el sistema")

		#Crea el objeto encoder para el multipart/form-data con el dic_falla de la 
		# falla actual.
		encoder = self.create_upload(dic_falla)
		self.long_total_bytes = encoder.len
		# self.nombre_archivo_actual = archivo

		monitor = MultipartEncoderMonitor(encoder, self.actualizar_datos)
		r = requests.post(url, data=monitor,headers={'Content-Type': monitor.content_type})
		print('\nUpload finished! (Returned status {0} {1})'.format(
			r.status_code, r.reason
		))
		if r.status_code != requests.codes.ok:
			raise ExcepcionAjax("Error subiendo las capturas de la falla en calle %s y altura %s .Respuesta del servidor: %s" %\
									(dic_falla["calle"],dic_falla["altura"],r.reason) )


	# Actualiza los datos que se muestran respecto del nombre del archivo actual
	#  y la cantidad de bytes enviados/cantidad bytes totales.
	def actualizar_datos(self,monitor):
		controlador = App.get_running_app()
		controlador.actualizar_datos(monitor.bytes_read,
										self.long_total_bytes)
		print "Actualizado progress_bar"
		print ""
		

	# Retorna el objeto MultipartEncoder.Obtiene los datos del dic_falla
	# para la falla actual.
	def create_upload(self,dic_falla):
		dic_envio = {
						# 'id': str(dic_falla["id"]).encode("utf-8"),
						#TODO: Cambiar esto por el idFalla real cuando este subido.
						'id': str(8).encode("utf-8"),
						'calle': str(dic_falla["calle"]).encode("utf-8"),
						'altura': str(dic_falla["altura"]).encode("utf-8")
					}
		#NOTA: Los archivos que se envien al server deben estar indexados
		# por el nombre del archivo de captura (sin extension) para que 
		# funcione la subida.
		for capturaCsv in dic_falla["data_capturas"]:
			dic_envio[capturaCsv] = (capturaCsv,open(capturaCsv,'rb'),'csv')


		print "dic_falla contiene -->"
		print dic_falla["data_capturas"]
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "dic_envio contiene la siguiente data -->"
		print dic_envio
		print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print ""
		encoder = MultipartEncoder(dic_envio)
		return encoder




