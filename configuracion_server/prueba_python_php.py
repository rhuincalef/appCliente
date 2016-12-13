import requests
from json import JSONDecoder	
from requests_toolbelt.multipart.encoder import MultipartEncoder
from clint.textui.progress import Bar as ProgressBar



# PRUEBA DE SUBIDA DE CAPTURA FUNCIONANDO!!!
# url_subir_captura= "http://localhost/repoProyectoBacheo/web/restapi/upload_pcd"
# data = {
# 		"id": str(8).encode("utf-8"),
# 		"nombre": "foo.csv",
# 		# "contenido_archivo_captura":  str('1,2,3\n4,5,6\n7,8,9\n').encode("utf-8")
# 		}
# files ={
# 		# NOTA: "file" es el nombre del campo que se lee con do_upload() en CI,
# 		# open() abre y escribe el contenido del archivo,
# 		# y 'csv' es el tipo de archivo que el servidor acepta antes de realizar
# 		# el do_upload().
# 		"file1": ('foo0.csv',open('foo0.csv', 'rb'),'csv')
# 		# "file1": ('foo1.csv',open('foo1.csv', 'rb'),'csv')
# 		}
# r = requests.post(url_subir_captura, data=data,files=files)
# print "Peticion hecha!"
# print r.text
# print "r.headers: "
# print r.headers



# m = MultipartEncoder(
# 	    fields={'id': str("99").encode("utf-8"),
# 	    		'nombre': "foo.csv",
# 	            'contenido_archivo_captura': ("foo.csv", open("foo.csv", 'rb'),
# 	            	'text/plain')
# 	            }
#     )

# def subir_captura(idfalla,nombreArchivo):
# 	url_subir_captura= "http://localhost/repoProyectoBacheo/web/restapi/upload_pcd"
# 	m = MultipartEncoder(
# 	    fields={'id': str(idfalla).encode("utf-8"),
# 	    		'nombre': nombreArchivo,
# 	            'contenido_archivo_captura': (open(nombreArchivo, 'rb'), 'text/plain')
# 	            }
#     )
# 	request_subir_capturas = requests.post(url_subir_captura,data=m,
#                   headers={'Content-Type': m.content_type})
# 	return request_subir_capturas


# ########################### MAIN PARA EL PROGRAMA ######################################

# m = MultipartEncoder(
#     fields={'id': str(8).encode("utf-8") }
#     )

# url_check_bache= "http://localhost/repoProyectoBacheo/web/restapi/verificar_falla"
# request_verificar_bache = requests.post(url_check_bache, data=m,
#                   headers={'Content-Type': m.content_type})


# print "URL Final: %s" % (request_verificar_bache.url)
# print "La respuesta del server es: "
# print "Status: %s" % request_verificar_bache.status_code
# print "requests.codes.ok: %s" % requests.codes.ok
# if request_verificar_bache.status_code == requests.codes.ok:
# 	print "Entre!"
# 	id_falla = 8
# 	listado_capturas = ["foo.csv","foo1.csv","foo2.csv"]
# 	cant_total_capturas = len(listado_capturas)
# 	acumulado = 0

# 	# bar = ProgressBar(expected_size=100, filled_char='=')
# 	for cap in listado_capturas:
# 		print "EN el for..."
# 		print ""
# 		r = subir_captura(id_falla,cap)
# 		if r.status_code == requests.codes.ok:
# 			acumulado += 1
# 			print "Acumulado: %s %%" % ((acumulado/float(cant_total_capturas))*100)
# 			# bar.show(acumulado)
# 			print "r.text: %s" % str(r.text)
# 			my_json = JSONDecoder().decode(r.text)
# 			id_decod = (my_json["id"]).decode("utf-8")
# 			print "El id: %s - %s" % (type(id_decod),id_decod)
# 			print ""
# 			print "JSON Rertornado : %s" % my_json
# 		else:
# 			print "Error en la subida de archivos!"
# 			print ""
# 			r.raise_for_status()
# 			print "+++++++++++++++++++++++++++++++++++++++++++++++++++"

# else:
# 	print "Error en la peticion! Lanzando excepcion..."
# 	print ""
# 	request_verificar_bache.raise_for_status()
# print "--------------------------------------------"






########################################################################
###################### Funcion con EncoderMonitor ######################
########################################################################
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoderMonitor


# def create_callback(encoder):
#     encoder_len = len(encoder)
#     bar = ProgressBar(expected_size=encoder_len, filled_char='=')
#     def callback(monitor):
#         bar.show(monitor.bytes_read)
#     return callback

def actualizar_progress_bar(monitor):
	print "Subidos: %s bytes ..." % monitor.bytes_read
	print "==========================================="
	print ""
	# bar.show(monitor.bytes_read)


def create_upload():
    return MultipartEncoder({
        'id': str(8).encode("utf-8"),
        'nombre': str("foo.csv").encode("utf-8"),
        #NOTA: Los archivos que se envien al server deben estar indexados
        # por el nombre del archivo de captura (sin extension) para que 
        # funcione la subida.
        'foo0': ('foo0.csv', open("foo0.csv", 'rb'), 'csv'),
        'foo1': ('foo1.csv', open("foo1.csv", 'rb'), 'csv')
        # 'file0': ('progress_bar.py', open(__file__, 'rb'), 'csv'),
        # 'file1': ('progress_bar.py', open(__file__, 'rb'),'csv')
        })

if __name__ == '__main__':
	encoder = create_upload()
	encoder_len = encoder.len
	bar = ProgressBar(expected_size=encoder_len, filled_char='=')
	monitor = MultipartEncoderMonitor(encoder, actualizar_progress_bar)
	url_subir_captura= "http://localhost/repoProyectoBacheo/web/restapi/upload_pcd"
	r = requests.post(url_subir_captura, data=monitor,headers={'Content-Type': monitor.content_type})
	print('\nUpload finished! (Returned status {0} {1})'.format(
		r.status_code, r.reason
	))

