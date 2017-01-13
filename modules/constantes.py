# Constantes usadas por la interfaz grafica 

# Constante para controlar cuantos niveles puede subir el usuario en 
# el sist. de archivos
ROOT_PCD_FOLDER = "../"

TITULO_APP = "Capturador de fallas"

SCREEN_PRINCIPAL = 'menu'


# Listado de los modulos que se deben agregar al path de Python.
LISTADO_MODULOS = ['views/config',
					'views/menu',
	                'views/tiposfalla',
	                'views/fallanueva',
	                'views/obtenerfallainformada',
	                'views/seleccionarfallainformada',
	                'views/subircapturas',
	                'views/loadsavedialog',
	                'models/captura',
	                'models/apiclient',
	                'models/capturador',
	                'models/estadofalla',
	                'models/geofencing',
	                'models/estrategia'
	              ]

PATH_ARCHIVO_CONFIGURACION = 'views/config/confViews.cfg'

COLOR_LABELS_RGBA = 0,0.7,0, 1
COLOR_HEADERS_TABLA = 0.458, 0.458, 0.458,1



#####################################################################################
############### VARIABLES GLOBALES USADAS POR KinectViewer ##########################
#####################################################################################
#####################################################################################
# Variables globales respecto del almacenamiento de los
# archivos en disco.
# NOTA: Estas variables seran enviadas por la vista que genere una instancia de
# controller
# NOMBRE_ARCHIVO = "archivoSalida"
# DIR_TRABAJO_PRUEBA = "/home/rodrigo/TESINA-2016-KINECT/aplicacionCliente/modules/views/kinectView"

EXTENSION_ARCHIVO = ".pcd"
FORMATO_CAPTURA = "pcd"
SUBFIJO = "_"


# Valor usado para verificar si la vista fue cargada desde la opcion de 
# seleccionar fallas informadas o, si no esta seteado, si es una falla nueva
# con informacion de geoposicionamiento.
FALLA_NO_ESTABLECIDA = -1


LAT_PRUEBA = 30.0000
LONG_PRUEBA = -10.000



#############################################################################################
#################### Constantes para comunicacion con el  servidor ##########################
#############################################################################################

#URL donde se verificara si la falla se encuentra dada de alta, si es asi se da el
# ok(200) retornando el $id. Sino, se da de alta la falla y se retorna su id, para
# subirla al servidor. 
URL_CHECK_FALLA = "http://localhost/repoProyectoBacheo/web/restapi/verificar_falla"

# URL donde el usuario subira las capturas en .pcd
URL_UPLOAD_SERVER = "http://localhost/repoProyectoBacheo/web/restapi/upload_pcd"

# URL para obtener los baches informados
#URL_INFORMADOS  = "http://localhost:8080/api/falla/get/informados"
URL_INFORMADOS  = "http://localhost/repoProyectoBacheo/web/restapi/obtener_informados"


DIVISOR_EN_MB = 1000000.0

# Tamanio maximo de peticion en POST (en bytes)
# post_max_size en /etc/php5/apache2/php.ini tiene un valor de 30M.
#
# ; Maximum allowed size for uploaded files.
# ; http://php.net/upload-max-filesize
# upload_max_filesize = 25M
#
# ; Maximum number of files that can be uploaded via a single request
# max_file_uploads = 20

MAX_POST_REQUEST_SIZE = 20000000
MAX_FILE_UPLOADS_FOR_REQUEST = 20

