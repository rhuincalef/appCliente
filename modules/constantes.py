# -*- coding: utf-8 -*-

# Constantes usadas por la interfaz grafica 
import os
from os import path
import logging

from kivy.core.window import Window

   
# Constante para controlar cuantos niveles puede subir el usuario en 
# el sist. de archivos
ROOT_PCD_FOLDER = path.pardir + path.sep

TITULO_APP = "Aplicacion de captura de fallas"


#####################################################################################################
#################### CONSTANTES PARA LOS RECURSOS QUE SON CARGADOS DESDE RESOURCE ################### 
#####################################################################################################

# Constantes relacionadas con el dir. de instalacion de kivy
#import os,kivy
#DIR_RAIZ_KIVY = os.path.dirname(kivy.__file__)
#DIR_DEFAULT_THEMES_KIVY = DIR_RAIZ_KIVY + os.path.sep + "data"+ os.path.sep + "images" 

#Comando para crear altas de custom theme en appClienteNuevoDisenio/themeAppCliente: 
# python -m kivy.atlas customAppCliente 1087x621 *




# Constantes de archivo personalizado .atlas para kivy

CUSTOM_THEME_NAME = "customAppCliente.atlas"
DIR_CUSTOM_THEME_KIVY = os.getcwd() + "/resource/themeAppCliente/"


# Constantes de librerias que se cargan desde resource
RESOURCE_LIBRERIA_KIVY_GARDEN = 'resource/libs'
RESOURCE_THEME_KIVY = DIR_CUSTOM_THEME_KIVY


# Constante para los widgets personalizados de los screens
#RESOURCE_CUSTOM_WIDGETS = os.getcwd() + os.path.sep + "resource" + os.path.sep + "customwidgets" 
RESOURCE_CUSTOM_WIDGETS =  "resource" + os.path.sep + "customwidgets" 

RESOURCE_FUNCIONES_PARSING_CFG = "views/config"

PATHS_MODULOS = [	
					RESOURCE_CUSTOM_WIDGETS,
					RESOURCE_LIBRERIA_KIVY_GARDEN,
					RESOURCE_FUNCIONES_PARSING_CFG,
					'models/captura',
	                'models/apiclient',
	                'models/capturador',
	                'models/estadofalla',
	                'models/geofencing',
	                'models/estrategia'
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


EXTENSION_RECORRIDO_DEFAULT = '.rec'



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

# Ej. ".pcd",".csv"
#EXTENSION_SUBIDA_SERVER_DEFAULT = path.extsep + "csv"
EXTENSION_SUBIDA_SERVER_DEFAULT = path.extsep + "pcd"


# Valor usado para verificar si la vista fue cargada desde la opcion de 
# seleccionar fallas informadas o, si no esta seteado, si es una falla nueva
# con informacion de geoposicionamiento.
FALLA_NO_ESTABLECIDA = -1




# Latitud y longitud de prueba para la calle av. Hipolito Irigoyen, TW
#http://localhost/repoProyectoBacheo/web/restapi/es_calle_valida/latitud/-43.264148/longitud/-65.290654
#LAT_PRUEBA = -43.264148
#LONG_PRUEBA = -65.290654

# Michael Jones[1-99] y Av. Hipolito Irigoyen
#LAT_PRUEBA = -43.261299
#LAT_PRUEBA longitud -
#LONG_PRUEBA = -65.2952564

# Condarco [1150-1198] y Fray Luis Beltran
#LAT_PRUEBA = -43.2599560
#LONG_PRUEBA = -65.2986200

#Cabot[1-98] y Condarco
#LAT_PRUEBA,LONG_PRUEBA = -43.2589910,-65.2992550


#Moreno[999-1099] y Cutillo
#LAT_PRUEBA,LONG_PRUEBA = -43.2574960,-65.2976790

#Muzio-j [1-99] y Moreno .
#LAT_PRUEBA,LONG_PRUEBA = -43.2568820,-65.2990470


#Ameguino[699-799] y sobernia nacional
#LAT_PRUEBA,LONG_PRUEBA = -43.2591600,-65.3114380

#Pelegrini[700-798] y Moreteau -->Sin conexion
#
#LAT_PRUEBA,LONG_PRUEBA = -43.2591350,-65.3081930


PATH_ARCH_UBICACIONES_FALSAS = "latitudesFalsas.json"

#############################################################################################
#################### Constantes para comunicacion con el  servidor ##########################
#############################################################################################


#Servidor local rodrigo(Ultima version localhost:80)
URL_SERVIDOR_LOCAL = "http://localhost/web/"
#URL_SERVIDOR_LOCAL = "http://localhost/web111/"


#Servidor Externo
#URL_SERVIDOR_LOCAL = "http://192.168.0.105/web/"


#URL donde se verificara si la falla se encuentra dada de alta, si es asi se da el
# ok(200) retornando el $id. Sino, se da de alta la falla y se retorna su id, para
# subirla al servidor. 
URL_CHECK_FALLA =  URL_SERVIDOR_LOCAL + "restapi/verificar_falla"

# URL donde el usuario subira las capturas en .pcd
URL_UPLOAD_SERVER = URL_SERVIDOR_LOCAL + "restapi/upload_pcd"

# http://localhost/repoProyectoBacheo/web/restapi/obtener_informados/calle/belgrano
URL_INFORMADOS  = URL_SERVIDOR_LOCAL + "restapi/obtener_informados/calle/"

URL_GET_DIRECCION = URL_SERVIDOR_LOCAL + "restapi/obtener_datos_direccion/"

# http://localhost:81/web/restapi/obtener_props_confirmadas
URL_GET_PROPS_CONFIRMADAS = URL_SERVIDOR_LOCAL + "restapi/obtener_props_confirmadas" 


# URL para obtener las opciones de Autocompletado de appCliente
# Ej. de invocacion -->
# http://localhost/repoProyectoBacheo/web/restapi/obtener_sugerencias_calle/calle/ca/cantmaxsugerencias/4

#http://localhost/repoProyectoBacheo/web/restapi/obtener_sugerencias_calle/calle/ca/cantmaxsugerencias/4
URL_OBTENER_SUGERENCIAS_CALLES = URL_SERVIDOR_LOCAL + "restapi/obtener_sugerencias_calle"

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

LOCAL_DB_JSON_NAME = './DB_MUESTRAS_LOCALES_'

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
RGB_CAPTURADOR_PATH = "capturador_RGB" + path.sep + "openniViewer"

#Expresado en seg.
TIMEOUT_FOR_KILLING_PROCESS = 10 

################################################################################################
######################## CONSTANTES PARA LOS ICONOS Y SPINNERS DE LA APP########################
################################################################################################ 

TAMANIO_ICONOS = 32
TAMANIO_CUSTOM_ICONOS = 65
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

# Timeout para cerrar la aplicacion porque no se reciben datos del sensor Kinect.
TIMEOUT_KINECT_SEG = 2

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

############################################################################################
################################ CONSTANTES DE AUTOCOMPLETE ################################
############################################################################################

#Autocomplete (Obtener fallas del servidor)
CANT_SUGERENCIAS = 3

# Archivos modificados en servidor -->
# -config/routes.php
# -controllers/api_rest.php
# -models/calle.php
#
REGEX_FORMATO_FECHA = '.*\d+-\d+-\d+.*'
PATRON_SUBFIJO_ARCHIVOS_BD_CONFIRMADAS = ".*\.json$"

#CONSTANTES PARA LA CARGA DE SUBMENUS CON SCREENMANAGERS INDEPENDIENTES
LISTADO_SUB_MENUS = [
				        #Menu con las opciones para seleccionar la BD en JSON:
				        #   1. Crear BD actual de capturas 
						#   2. Anexar capturas a BD de capturas anteriores
						{
							"titulo" : "Seleccionar BD",
							"dirRaizModulo": "views/subMenuSeleccionarBD",
							"pathConfig" : "views/subMenuSeleccionarBD"+ path.sep + "config" +\
								path.sep + "subMenuSeleccionarBD.cfg"

						},

						#Menu de captura de fallas con las opciones:
				        #   1."Capturar falla nueva"
				        #   2."Obtener fallas informadas"
				        #   3."Capturar falla informada"
						{
							"titulo" : "Captura de fallas",
							"dirRaizModulo": "views/subMenuCapturarFallas",
							"pathConfig" : "views/subMenuCapturarFallas"+ path.sep + "config" +\
								path.sep + "subMenuCapturarFallas.cfg"
						},

						#Menu de subida de archivos al servidor con las opciones:
        				#   1."Subir capturas al servidor"
						{
							"titulo" : "Subida archivos",
							"dirRaizModulo": "views/subMenuServidor",
							"pathConfig" : "views/subMenuServidor"+ path.sep + "config" +\
								path.sep + "subMenuServidor.cfg"
						},

				        #Menu de persistencia de recorridos con las opciones:
				        #   1."Guardar recorrido de fallas capturadas"
				        #   2."Cargar recorrido de fallas"
						{
							"titulo" : "Almacenar recorrido",
							"dirRaizModulo": "views/subMenuRecorrido",
							"pathConfig" : "views/subMenuRecorrido"+ path.sep + "config" +\
								path.sep + "subMenuRecorrido.cfg"
						}
					]

# Constante para identificar el tipo de elemento de los archivos de configuracion
TIPO_SUB_MENU = "subMenu"
TIPO_SCREEN = "screen"

# Constantes para el tamanio de los iconos en screen "propsTipoFalla" (solicitado en 
# modulo customwidgets)
TAMANIO_PLUS_ICON_DROPDOWN = 22
TAMANIO_ELEMENTOS_CUSTOM_DROPDOWN = '18sp' 
PREFIJO_LABEL_DROPDOWN = "label"
TAMANIO_TEXTO_LABELS_DROPDOWN = '24sp'

#Espacio que se reserva horizontalmente por opcion de cada CustomDropdown
PADDING_POR_WIDGET = 36

#Ponderaciones para los tipos de criticidad de las fallas
PONDERACION_BAJA_CRITICIDAD = 1
PONDERACION_MEDIA_CRITICIDAD = 1.15
PONDERACION_ALTA_CRITICIDAD = 1.5
ESTADO_POR_DEFAULT_SUBIDA_CAPTURAS = "Confirmado"

# Estos son los IDs que se emplean para indicar los tipos de falla y sus respectivos
# tipos de material y criticidades habilitados. Estos IDS se corresponden con los de 
# la tabla "TipoFallaModelo".
IDS_TIPOS_FALLA_HABILITADOS = [2,3]

PONDERACION_CRITICIDAD_BAJA = 1
PONDERACION_CRITICIDAD_MEDIA = 1.15
PONDERACION_CRITICIDAD_ALTA = 1.5


#COLOR DE LAS CRITICIDADES EN RGB(Capturar falla confirmada)

#AMARILLO BAJA -->
COLOR_PONDERACION_BAJA = 'F2F939'
#NARANJA MEDIA -->
COLOR_PONDERACION_MEDIA = 'ff890b'
#ALTA ROJO -->
COLOR_PONDERACION_ALTA = 'FF0000'

# Patrones para usar con regex.
# Patron para detectar texto con etiquetas de marcado 
PATRON_ICONO_DROPDOWN = ".*\[/\color\].*"

# Patron para detectar la separacion de propiedades por ":".
# Si el nombre y la descripcion de una propiedad de la falla se separa por ":", entonces
# se procede a filtrar solamente el nombre. Este caso se aplica a la criticidad de una falla 
#
CARACTER_SEPARADOR_CRITICIDAD = ":"
PATRON_SEPARADOR_CRITICIDAD_DROPDOWN = ".*" + CARACTER_SEPARADOR_CRITICIDAD + ".*"
POSICION_INTERES_PARA_CRITICIDAD = 0

#Prefijo con el que se generan ID's unicos para los TabbedPanelItem
# sumado al titulo del submenu (PREFIJO_ID_TP_ITEM + tituloSubMenu)
PREFIJO_ID_TP_ITEM = "TpItem_"


#####################################################################################################################
############################## CONSTANTES DEL FOOTER QUE CONTIENE LOS BOTONES DE LA APP##############################
#####################################################################################################################

COL_DEFAULT_WIDTH = 150
ROW_DEFAULT_HEIGHT = 50
ESCALA_PADDING_HORIZONTAL = 0.24
ESCALA_SPACING_VERTICAL = 0.20
DEFAULT_PADDING_VERTICAL = 50

DEFAULT_PADDING_HORIZONTAL = Window.width * ESCALA_PADDING_HORIZONTAL

DEFAULT_SPACING = [( Window.width * ESCALA_SPACING_VERTICAL ),0]


# Constante para el estilo de los botones de las opciones principales que
# aparecen en los submenus de appCliente.
# 
ESTILO_BOTON_DEFAULT_OPCIONES_MENU = 'atlas://customAppCliente/button'
ESTILO_BOTON_DEFAULT_PRESIONADO = 'atlas://customAppCliente/button_pressed'
ESTILO_CHECKBOX_DESSELECCIONADO = 'atlas://customAppCliente/checkbox_off'
ESTILO_CHECKBOX_SELECCIONADO = 'atlas://customAppCliente/checkbox_on'

#Estilos para el strip del tabbedpanel principal
ESTILO_TABBED_PANEL_PRESIONADO = 'atlas://customAppCliente/tab_btn_pressed'
ESTILO_TABBED_PANEL_NORMAL = 'atlas://customAppCliente/tab_btn'
ESTILO_AUTOCOMPLETE_OPCIONES = 'atlas://customAppCliente/autocomplete_normal'

#Mapa con zoom-out mayor

ESTILO_FONDO_TABBED_PANEL = 'atlas://customAppCliente/tabv8'

#Estilo de los dialogos que se invocan con controlador.mostrarDialogo()

ESTILO_BACKGROUND_MODAL_XBASE = 'atlas://customAppCliente/modalview-background'

#Estilos de los items que se muestran en los listview de capturarfallainformada y subirfalla

#ESTILO_BOTON_SELECCIONADO_LIST_VIEW = 'atlas://customAppCliente/button_listview_seleccionado'
ESTILO_BOTON_SELECCIONADO_LIST_VIEW = 'atlas://customAppCliente/button_listview_seleccionado2'
ESTILO_BOTON_NO_SELECCIONADO_LIST_VIEW = 'atlas://customAppCliente/button_listview_no_seleccionado'

COLOR_SEPARADOR_POPUPS = [1,1,1,1]

#Constantes para el texto en cada Label del CustomDropDown

COLOR_DROPDOWN_TEXTO_DESHABILITADO = (94.0/255, 94.0/255, 94.0/255,0.4)

#Constantes para el row del CustomDropDown

COLOR_DROPDOWN_ROW_SELECCIONADO = (25.0/255.0, 152.0/255.0, 255.0/255.0,0.3)
COLOR_ROW_PAR_DROPDOWN = (0.0/255.0,0.0/255.0,255/255.0,0.6) 
COLOR_ROW_IMPAR_DROPDOWN = COLOR_ROW_PAR_DROPDOWN

#Estilo que representa el color del treeviewlabel "root" cuando se
# selecciona una opcion.

ESTILO_ROOT_TREELABEL_SELECCIONADO = (COLOR_DROPDOWN_ROW_SELECCIONADO[0],
										COLOR_DROPDOWN_ROW_SELECCIONADO[1],
										COLOR_DROPDOWN_ROW_SELECCIONADO[2],
										0.50)

# Estilos que se usan para los botones del listado en los screens
# "capturarfallainformada" y "subirfalla".

COLOR_ITEMS_LISTADO_NO_SELECCIONADO = [ 35/255.0, 235/255.0, 237/255.0, 1]
COLOR_ITEMS_LISTADO_SELECCIONADO = [25/255.0, 105/255.0, 204/255.0, 1]

PATH_LOG_PRINCIPAL = "_logs/log.txt"

#AZUL OSCURO
COLOR_PRUEBA_LISTVIEW_ITEM_NO_SELECCIONADO = [ 1,46,136 ] 

#CELESTE CLARO
COLOR_PRUEBA_LISTVIEW_ITEM_SELECCIONADO = [ 5,152,255 ]

#INCREMENTO PARA LLEGAR A CELESTE CLARO
COLOR_PRUEBA_LISTVIEW_ITEM_SELECCIONADO = [ 4,106,119 ]

ESTILO_TREE_VIEW = '''
<TreeViewNode>:
    canvas.before:
        Color:
            rgba: self.color_selected if self.is_selected else self.odd_color if self.odd else self.even_color
        Rectangle:
            pos: [self.parent.x, self.y] if self.parent else [0, 0]
            size: [self.parent.width, self.height] if self.parent else [1, 1]
        Color:
            rgba: 1, 1, 1, int(not self.is_leaf)
        Rectangle:
            source: 'atlas://customAppCliente/tree_%s' % ('opened' if self.is_open else 'closed')
            #size: 16, 16
            size: 21, 21
            pos: self.x - 20, self.center_y - 8
    canvas.after:
        Color:
            rgba: .5, .5, .5, .2
        Line:
            points: [self.parent.x, self.y, self.parent.right, self.y] if self.parent else []'''
