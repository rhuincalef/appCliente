# Constantes usadas por la interfaz grafica 

# Constante para controlar cuantos niveles puede subir el usuario en 
# el sist. de archivos
ROOT_PCD_FOLDER = "../"


# URL donde el usuario subira las capturas en .pcd
URL_UPLOAD_SERVER = ""
# URL para obtener los baches informados
URL_INFORMADOS  = "http://localhost:8080/api/falla/get/informados"

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
	                'models/captura',
	                'models/apiclient',
	                'models/capturador'
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
SUBFIJO = "_"







