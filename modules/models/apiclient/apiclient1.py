# Clase que realiza la comunicacion con el servidor para obtener los baches
#  y subir archivos al servidor
from constantes import URL_INFORMADOS,URL_UPLOAD_SERVER
import requests
from requests.exceptions import ConnectionError

class ExcepcionAjax(Exception):
	pass



# Instalar requests con pip y toolbelt request
# sudo pip install requests-toolbelt

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

	def postCapturas(self,url,dic_fallas):
		dic_archivos_csv = dic_fallas["data_capturas"]
		for archivo,datos in dic_archivos_csv.iteritems():
			# files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
			files = {'file': (archivo, datos) }
			# "data" tiene el valor separado por comas, 
			# "files" es el nombre del archivo+contenido de este.
			r = requests.post(url, files=files,data=dic_fallas, headers=)
			if r.status_code != 200:
				raise ExcepcionAjax("Error en el envio de captura al servidor.")






