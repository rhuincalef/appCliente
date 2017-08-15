# NOTA: Libreria para hacer las peticiones en ajax
# http://docs.python-requests.org/en/master
#TODO: Hacer un parser de json para los datos del servidor.
# Se obtienen del servidor las fallas



URL_SERVIDOR = "http:// algo..."
class ExcepcionAjax(Exception):
    pass

class APIClient:
	def __init__(self,url):
		self.url_servidor = url
		self.cant_total_fallas = 0
	# def parsear_json(self,file_json):
	# 	import json
	# 	with open(file_json) as data_file:    
	# 		data = json.load(data_file)
	# 	return data


	#TODO: Este metodo realiza una peticion al servidor
	# para obtener la cantidad total de fallas
	def get_cant_total_fallas(self):
		return 10


	# Este metodo obtiene de una URL remota un json, que luego retorna como un
	# diccionario. 
	def obtener_baches(self,screen):
		r = requests.get(self.url_servidor,stream = True)
		dic_fallas = {}
		cont_lineas = 0
		for line in r.iter_lines():
			if line:
				decoded_line = line.decode('utf-8')
				print "Linea en json -->"
				print decoded_line
				dic_fallas[decoded_line["id"]] = decoded_line
				cont_lineas += 1
				screen.barra_progreso.actualizar_barra(cont_lineas)

		# print "Diccionario final de fallas es: "
		# print dic_fallas
		return dic_fallas
		# if r.status_code != 200:
		# 	msg_error = 'Error en la peticion: '+r.text
		# 	raise ExcepcionAjax(msg_error)
		# return r.json()



class CargandoFallasInformadasScreen(Screen):


	def __init__(self, **kwargs):
		self.api_client = APIClient(URL_SERVIDOR)

		self.porcentaje_actual = 0
		super(Screen, self).__init__(**kwargs)
   
	def obtener_fallas_servidor(self):
		self.fallas_totales = self.api_client.get_cant_total_fallas()
		self.api_client.obtener_baches(self)
	
	def actualizar_barra(self,linea_actual):
		self.porcentaje_actual += (linea_actual / self.fallas_totales )
		print "porcentaje_actual: ", self.porcentaje_actual
		barra_progreso.value =self.porcentaje_actual 



   