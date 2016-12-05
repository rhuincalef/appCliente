# Clase que realiza la comunicacion con el servidor para obtener los baches
#  y subir archivos al servidor
from constantes import URL_INFORMADOS,URL_UPLOAD_SERVER
import requests
from requests.exceptions import ConnectionError

class ExcepcionAjax(Exception):
	pass


class ApiClientApp(object):
	def __init__(self):
		self.conexionServer = requests

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



