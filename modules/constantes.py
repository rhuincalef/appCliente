# Constantes usadas por la interfaz grafica 
from os import path
import logging

# Constante para controlar cuantos niveles puede subir el usuario en 
# el sist. de archivos
#ROOT_PCD_FOLDER = "../"
ROOT_PCD_FOLDER = path.pardir + path.sep

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
	                'models/estrategia',
	                'resource/libs'
	              ]

#PATH_ARCHIVO_CONFIGURACION = 'views/config/confViews.cfg'
PATH_ARCHIVO_CONFIGURACION = 'views' + path.sep + 'config' + path.sep + 'confViews' + path.extsep + 'cfg'

#Celeste claro
COLOR_LABELS_RGBA = 102/255.0, 159/255.0, 255/255.0, 0.8
COLOR_HEADERS_TABLA = 0.458, 0.458, 0.458,1
COLOR_TEXTOS = 1,1,1,1



#Constantes de los dialogos de carga y mensajes mostrados por la aplicacion.
PATH_ICONO_RELOJ = 'resource' + path.sep + 'gifs' + path.sep + 'hourglass.gif'
PATH_ICONO_LUPA = 'resource' + path.sep + 'gifs' + path.sep + 'lupa.gif'



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

#EXTENSION_ARCHIVO = ".pcd"
EXTENSION_ARCHIVO = path.extsep + "pcd"
FORMATO_CAPTURA = "pcd"
SUBFIJO = "_"
#EXTENSION_SUBIDA_SERVER_DEFAULT = ".csv"
EXTENSION_SUBIDA_SERVER_DEFAULT = path.extsep + "csv"


# Valor usado para verificar si la vista fue cargada desde la opcion de 
# seleccionar fallas informadas o, si no esta seteado, si es una falla nueva
# con informacion de geoposicionamiento.
FALLA_NO_ESTABLECIDA = -1




# Latitud y longitud de prueba para la calle av. Hipolito Irigoyen, TW
#http://localhost/repoProyectoBacheo/web/restapi/es_calle_valida/latitud/-43.264148/longitud/-65.290654
#LAT_PRUEBA = -43.264148
#LONG_PRUEBA = -65.290654

# Michael Jones[1-99] e Av. Hipolito Irigoyen
#LAT_PRUEBA = -43.2612999
#LONG_PRUEBA = -65.2952564

# Condarco [1150-1198] y Fray Luis Beltran
#LAT_PRUEBA = -43.2599560
#LONG_PRUEBA = -65.2986200

#Cabot[1-98] y Condarco
#LAT_PRUEBA = -43.2589910
#LONG_PRUEBA = -65.2992550


#Moreno[999-1099] y Cutillo
#LAT_PRUEBA,LONG_PRUEBA = -43.2574960,-65.2976790

#Muzio-j [1-99] y Moreno .
#LAT_PRUEBA,LONG_PRUEBA = -43.2568820,-65.2990470


#Ameguino[699-799] y sobernia nacional
#LAT_PRUEBA,LONG_PRUEBA = -43.2591600,-65.3114380

#Pelegrini[700-798] y Moreteau -->Sin conexion
#
LAT_PRUEBA,LONG_PRUEBA = -43.2591350,-65.3081930




CSV_TMP_DIR = "csv" + path.sep #Directorio a parte de los .pcd donde se almacenan
					# los .csv convertidos y que se subiran al servidor

#############################################################################################
#################### Constantes para comunicacion con el  servidor ##########################
#############################################################################################


URL_SERVIDOR_LOCAL = "http://localhost/repoProyectoBacheo/web/"



#URL donde se verificara si la falla se encuentra dada de alta, si es asi se da el
# ok(200) retornando el $id. Sino, se da de alta la falla y se retorna su id, para
# subirla al servidor. 
URL_CHECK_FALLA =  URL_SERVIDOR_LOCAL + "restapi/verificar_falla"

# URL donde el usuario subira las capturas en .pcd
URL_UPLOAD_SERVER = URL_SERVIDOR_LOCAL + "restapi/upload_pcd"

# URL para obtener los baches informados
#URL_INFORMADOS  = "http://localhost:8080/api/falla/get/informados"

# http://localhost/repoProyectoBacheo/web/restapi/obtener_informados/calle/belgrano
URL_INFORMADOS  = URL_SERVIDOR_LOCAL + "restapi/obtener_informados/calle/"

URL_GET_DIRECCION = URL_SERVIDOR_LOCAL + "restapi/obtener_datos_direccion/"

URL_GET_PROPS_CONFIRMADAS = URL_SERVIDOR_LOCAL + "restapi/obtener_props_confirmadas" 


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


# Constante que define el IdFalla(invalido para la BD) para las fallas de la calle,
# con el que se dara de alta en el sistema.  
#
ID_FALLA_NUEVA_DEFECTO = -1





####################################################################################
######################## CONSTANTES PARA FALLAS CONFIRMADAS ########################
####################################################################################
ID_TIPO_MATERIAL_DEFECTO = 1
ID_TIPO_FALLA_DEFECTO = 1
ID_TIPO_ESTADO_CONFIRMADO = 2
ID_USUARIO_CALLEJERO = 1 #Se carga en la BD un usuario que sea el usuario recolector


##########################################################################################################################
############################### CONSTANTES PARA LA BD DE PROPIEDADES CONFIRMADAS(Obtenidas desde el servidor) ############
##########################################################################################################################

LOCAL_BD_PROPS_CONFIRMADAS = "./DB_CONFIRMADAS.json" 



####################################################################################
############################### CONSTANTES PARA LA DB LOCAL DE CAPTURAS ############
####################################################################################
#LOCAL_DB_JSON_NAME = './DB_MUESTRAS_LOCALES_30-03-2017.json'
LOCAL_DB_JSON_NAME = './DB_MUESTRAS_LOCALES_'
#EXTENSION_LOCAL_BD_JSON_NAME = '.json'
EXTENSION_LOCAL_BD_JSON_NAME = path.extsep + 'json'



#Tiempo maximo de espera en segundos para obtener una latitud y longitud
MAX_TIMEOUT_SEGS = 6
INVALID_LAT_LONG = -1
DEVICE_GPS_DEFAULT = "/dev/rfcomm1"




#PATH AL SCRIPT DE VISUALIZACION
PATH_VIEW_PCD_FILE_SCRIPT = "./see_capture.sh"
REMOVE_COMMAND = "rm"



#Constantes de los tipos de formato de almacenamiento de la captura PCD
PCD_XYZ_FORMAT = "XYZ"
PCD_XYZ_RGB_FORMAT = "XYZRGB"
#RGB_CAPTURADOR_PATH = "capturador_RGB/openniViewer"
RGB_CAPTURADOR_PATH = "capturador_RGB" + path.sep + "openniViewer"

#Expresado en seg.
TIMEOUT_FOR_KILLING_PROCESS = 10 

################################################################################################
######################## CONSTANTES PARA LOS ICONOS Y SPINNERS DE LA APP########################
################################################################################################ 
TAMANIO_ICONOS = 32
TAMANIO_SPINNER = 40
COLOR_SPINNER = "'5729ff'"
NOMBRE_FONT_TTF = 'resource'+ path.sep + 'fonts' + path.sep + 'font-awesome' + path.extsep + 'ttf'
NOMBRE_FONT_DICT = 'resource'+ path.sep + 'fonts'+ path.sep +'font-awesome' + path.extsep + 'fontd'

TAMANIO_ICONOS_CTRL_BAR = 18


BTN_BORRAR_SELECTED_COLOR = [1,0,0,1]
BTN_BORRAR_UNSELECTED_COLOR = [1,1,1,1]


SPINNER_LABEL = """
#: import icon iconfonts.icon
Label:
	id: _anim
	markup: True
	text: "%s" %(icon('fa-circle-o-notch',"""+ str(TAMANIO_SPINNER)+""","""+str(COLOR_SPINNER)+"""))
	font_color: 1, 0, 0, 1
	p: 0
	size_hint: (1,0.6)
	canvas:
		Clear
		PushMatrix
		Rotate:
			angle: -self.p
			origin: self.center_x , self.center_y
		Rectangle:
			size: """+str(TAMANIO_SPINNER)+""","""+str(TAMANIO_SPINNER)+"""
			pos: self.center_x - """+str(TAMANIO_SPINNER/2)+""", self.center_y - """+str(TAMANIO_SPINNER/2)+"""
			texture: self.texture
		PopMatrix"""

###########################################################################################################
########################## CONSTANTES PARA LOS ARGUMENTOS POR LINEA DE COMANDOS  ##########################
###########################################################################################################
OPCIONES_GPS = ['fakegps','realgps']
OPCIONES_CAPTURA = ['xyz_rgb','xyz']

TIPO_GPS_DEFAULT = OPCIONES_GPS[0]  #Alternativa 'realgps'
TIPO_CAPTURA_DEFAULT = OPCIONES_CAPTURA[0] # Alternativa 'xyz'


# Timeout para cerrar la aplicacion porque no se reciben datos del
# sensor Kinect.
TIMEOUT_KINECT_SEG = 5


# CONSTANTES PARA LOGGING EN ARCHIVO
APP_NAME_LOGGING = "appCliente"

#Archivo con capturas corruptas.
LOGS_DEFAULT_DIR = "_logs/"

LOG_FILE_CAPTURAS_CORRUPTAS_DEFAULT = "capturasCorruptas.log"
LOG_FILE_CAPTURAS_INFO_SERVER = "infoServidor.log"
LOG_FILE_CAPTURAS_PROPS_CONFIRMADA = "infoCargaPropiedades.log"
#Usado para el metodo subir_archivos que llama a filtrarCapturas()
LOG_FILE_FILTRADO_CAPS = "infoFiltradoCaps.log"

LOGGING_DEFAULT_LEVEL = logging.INFO

###########################################################################################################
########################## CONSTANTES DE CODIGOS DE ERROR DE GEOCODING DEL SERVIDOR  ##########################
###########################################################################################################
#NOTA: Estas constantes se encuentran definidas en la webapp en application/config/constants.php
#

DIRECCION_PHP_DIRECCION_NO_RETORNADA = -1
DIRECCION_PHP_PETICION_SIN_RESULTADOS = -2
DIRECCION_PHP_QUOTA_EXCEDIDA = -3
DIRECCION_PHP_OPERACION_GEOCODING_NO_SOPORTADA = -4
DIRECCION_PHP_API_KEY_INVALIDA = -5
DIRECCION_PHP_LAT_LONG_NO_VALIDAS = -6
DIRECCION_PHP_HTTP_ADAPTER_TIMEOUT_EXCEDIDO = -7
DIRECCION_PHP_EXCEPCION_GENERICA = -8
DIRECCION_PHP_PETICION_INTERSECCION_FALLIDA = -9
DIRECCION_PHP_INTERSECCION_TIMEOUT_EXCEDIDO = -10
FALLA_PHP_CALLE_NO_DISPONIBLE = -11
DIRECCION_PHP_LAT_LONG_FUERA_CIUDAD = -12
FALLA_INVALIDA = -13

CODIGOS_ERROR_GEOCODING = [ DIRECCION_PHP_DIRECCION_NO_RETORNADA,
DIRECCION_PHP_PETICION_SIN_RESULTADOS,
DIRECCION_PHP_QUOTA_EXCEDIDA,
DIRECCION_PHP_OPERACION_GEOCODING_NO_SOPORTADA,
DIRECCION_PHP_API_KEY_INVALIDA,
DIRECCION_PHP_LAT_LONG_NO_VALIDAS,
DIRECCION_PHP_HTTP_ADAPTER_TIMEOUT_EXCEDIDO,
DIRECCION_PHP_EXCEPCION_GENERICA,
DIRECCION_PHP_PETICION_INTERSECCION_FALLIDA,
DIRECCION_PHP_INTERSECCION_TIMEOUT_EXCEDIDO,
FALLA_PHP_CALLE_NO_DISPONIBLE,
DIRECCION_PHP_LAT_LONG_FUERA_CIUDAD,
FALLA_INVALIDA ]











