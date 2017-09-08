from kivy.app import App
from kivy.lang import Builder
import importlib

#Imports para el AutoCompleteTextInput
import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label


#from main import Controlador
from constantes import *

#Imports para el dropdown
from kivy.uix.treeview import TreeView,TreeViewNode,TreeViewLabel
from kivy.graphics import Color, Rectangle


#Imports para el tabbedpanel
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem,TabbedPanelHeader,TabbedPanelStrip

# Se importa resources para agregar el theme de kivy
import kivy.resources

# EventDispatcher para los eventos 
from kivy.event import EventDispatcher
# Imports del widget XFolder
from os.path import sep, expanduser, isdir, dirname
import sys
from kivy.uix.screenmanager import ScreenManager, Screen

from utilscfg import *
import re

class AutoCompleteTextInput(BoxLayout):

    def __init__(self,**kwargs):
        super(AutoCompleteTextInput,self).__init__(**kwargs)
        self.orientation = 'vertical'
        #self.padding = [50,100,50,300]

        self.spinner = None

        #self.textInput = TextInput(text='', multiline=False, size_hint=(1, 0.2))
        self.textInput = TextInput(text='', multiline=False, size_hint=(1, 0.25))
        self.textInput.bind(text = self.autocompletar)

        #NOTA: Este boxlayout tiene las sugerencias y el spinner que se muestra debajo
        # del textinput
        self.boxLayoutSugerencias = BoxLayout(orientation='vertical')
        
        #Se agrega el textinput en el subboxlayout que lo contiene.
        self.add_widget(self.textInput)
        self.add_widget(self.boxLayoutSugerencias)
        #self.controlador = Controlador()
        self.controlador = App.get_running_app()
        
        # ...

        #Se bindea el evento de fin de obtencion de nombres de calles a la gui
        #self.controlador.bind(on_fin_obtencion_direcciones = self.calles_obtenidas_servidor)
        self.controlador.bind(on_fin_obtencion_sugerencias = self.calles_obtenidas_servidor)

        
    
    #Manejador que recibe las calles sugeridas por el servidor.
    # NOTA: args es una tupla (clase Controlador, LISTA DE SUGERENCIAS)
    def calles_obtenidas_servidor(self,*args):
        print "Handler de on_fin_obtencion_sugerencias ejecutado!\n"
        #4. Se agregan los labels que indican las sugerencias de la calle
        # y se bindean el evento on_touch_down con el handler que modifica el text
        # input y remueve todos los widgets.
        self.boxLayoutSugerencias.clear_widgets()
        self.boxLayoutSugerencias.padding = [0,0,0,0]
        for i in xrange(0,len(args[1])):
            lab = Button(text = args[1][i],
                        color = (0,0,0,1),
                        background_normal = ESTILO_AUTOCOMPLETE_OPCIONES )
                        #background_normal = 'atlas://customAppCliente/autocomplete_normal')
            lab.bind(on_press = self.reemplazarContenido)
            self.boxLayoutSugerencias.add_widget(lab)
            #lab.background_normal = 'atlas://customAppCliente/autocomplete_normal'
        self.boxLayoutSugerencias.remove_widget(self.spinner)



    #Este metodo agrega labels que indican las sugerencias disponibles para 
    # autocompletar la calle ingresada por el usuario.
    def autocompletar(self,instance,value):
        if self.textInput.focus:
            # Si es cadena vacia, se borran las sugerencias y no se envia la peticion
            # al servidor.
            if not value.strip():
                #print "\nCADENA VACIA!\n\n\n"
                self.boxLayoutSugerencias.clear_widgets()
                return

            self.boxLayoutSugerencias.clear_widgets()
            #1. Se agrega un spinner mientras se resuelve la peticion (Representado por string "Buscando ...")
            self.spinner = Button(text="Buscando ...",color = (0,0,0,1),
                                    background_normal = ESTILO_AUTOCOMPLETE_OPCIONES )
                                    #background_normal = 'atlas://customAppCliente/autocomplete_normal')

            self.boxLayoutSugerencias.padding = [0,0,0,80]
            self.boxLayoutSugerencias.add_widget(self.spinner)
            threadSugerencias = threading.Thread(name="thread-SolicitarSugerencias",
                                 target = self.controlador.solicitarSugerencias,
                                    args= (value,CANT_SUGERENCIAS,))
            threadSugerencias.setDaemon(True)
            threadSugerencias.start()



    #Cambia el contenido del textinput por el label presionado y borra todos los labels
    # del widget.
    #def reemplazarContenido(self,label,value):
    def reemplazarContenido(self,label):
        print "type(label): %s\n" % type(label)
        #print "value: %s\n" % value
        self.textInput.text = label.text
        self.boxLayoutSugerencias.clear_widgets()

    def getOpcionSeleccionada(self):
        return self.textInput.text

    def limpiar(self):
        self.textInput.text = ''

from iconfonts import *
from constantes import *
register('default_font',NOMBRE_FONT_TTF, NOMBRE_FONT_DICT)

class CustomDropDown(TreeView):

    ICONO_DEFAULT_DROPDOWN = "%s"% icon('fa-plus',TAMANIO_PLUS_ICON_DROPDOWN)

    root_options = {
                        'text': ICONO_DEFAULT_DROPDOWN,
                        'markup': True,
                        'font_size':TAMANIO_PLUS_ICON_DROPDOWN,
                        'color_selected': COLOR_DROPDOWN_ROW_SELECCIONADO
                        #,'opened': 'atlas://customAppCliente/tree_closed'
                    }

    def __init__(self,screen,**kwargs):
        super(CustomDropDown,self).__init__(**kwargs)
        self.toggle_node(self.root)
        self.bind(on_node_expand = self.ocultarLabels)
        self.bind(on_node_collapse = self.mostrarLabels)
        self.screen = screen

    #Evento usado para ocular los labels que se encuentran detras del customdropdown
    def ocultarLabels(self,customDropdown,treeViewLabel):
        print "type(self.parent): %s, id: %s\n" % (type(self.parent.parent),self.parent.parent.id)
        self._toggleGUI(customDropdown,True)
        
    #Evento usado para mostrar nuevamente los labels que se encuentran detras del customdropdown
    def mostrarLabels(self,customDropdown,treeViewLabel):
        self._toggleGUI(customDropdown,False)
    

    #Este metodo al habilitarse un dropdown, deshabilita el resto y sus lables asociados
    def _toggleGUI(self,customDropdown,estanDeshabilitadosWidgets):
        print "type (customDropdown):%s,  customDropdown.id: %s\n" % (type(customDropdown),customDropdown.id)
        print "type (customDropdown.parent.id):%s,  customDropdown.parent.id: %s\n" % (type(customDropdown.parent.id),
                                                                                            customDropdown.parent.id)
        #NOTA: "elemento" a este nivel es un sublayout
        for elemento in self.parent.parent.children:
            print "recorriendo elemento: %s\n" % type(elemento)
            print "recorriendo elemento.id: %s\n" % elemento.id
            if (elemento.id is not None) and not (elemento.id == customDropdown.parent.id):
                elemento.disabled = estanDeshabilitadosWidgets
                print "deshabilitado: %s !\n\n" % elemento.id



    # BACKUP!!
    #Este metodo al habilitarse un dropdown, deshabilita el resto y sus lables asociados
    #def _toggleGUI(self,customDropdown,estanDeshabilitadosWidgets):
    #    print "type (dropdown):%s,  dropdown.id: %s\n" % (type(customDropdown),customDropdown.id)
    #    for elemento in self.parent.children:
    #        print "recorriendo elemento: %s\n" % type(elemento)
    #        print "recorriendo elemento.id: %s\n" % elemento.id
    #        if (elemento.id is not None) and not (elemento.id == customDropdown.id) \
    #                                    and not (elemento.id == PREFIJO_LABEL_DROPDOWN+customDropdown.id):
    #            elemento.disabled = estanDeshabilitadosWidgets
    #            print "deshabilitado: %s !\n\n" % elemento.id


    @staticmethod
    def callbackCargaTiposFalla(treeview, node):
        controlador = App.get_running_app()
        #dicNombres = controlador.capturador.getPropsConfirmados()
        dicNombres = controlador.getPropsConfirmados()
        print "En callbackCargaTiposFalla con dicNombres propiedades tiene: %s\n" % \
                                                                        dicNombres
        if len(treeview.children) <= 0:
            for elem in dicNombres:
                estaDeshabilitada = True
                if elem.estaHabilitada():
                    estaDeshabilitada = False
                print "customwidgets dropdown type(elem): %s\n" % type(elem)
                print "estaDeshabilitada: %s\n" % estaDeshabilitada
                print "elem.estaHabilitada(): %s\n" % elem.estaHabilitada()
                element = TreeViewLabel(
                                        text = elem.getValor(),
                                        #text = "[u] " + elem.getValor() + " [/u]",
                                        disabled = estaDeshabilitada,
                                        markup = True,
                                        disabled_color = COLOR_DROPDOWN_TEXTO_DESHABILITADO,
                                        color_selected = COLOR_DROPDOWN_ROW_SELECCIONADO,
                                        even_color = COLOR_ROW_PAR_DROPDOWN,
                                        odd_color = COLOR_ROW_IMPAR_DROPDOWN,
                                        #disabled_outline_color = COLOR_DROPDOWN_ITEM_DESHABILITADO_OUTLINE,
                                        font_size = TAMANIO_ELEMENTOS_CUSTOM_DROPDOWN
                                        )
                element.no_selection = estaDeshabilitada
                print "Propiedad deshabilitada %s: %s\n" % (elem.getValor(),
                                                                estaDeshabilitada)
                #element.bind(on_touch_down = treeview.on_pressed_element)
                element.bind(on_touch_down = treeview.on_pressed_tipo_falla)
                yield element


    # Este metodo establece el texto del nodo raiz(root) del CustomDropdown
    # estableciendolo como opcion actual seleccionada.
    def setTextoSeleccion(self,label):
        self.toggle_node(label.parent_node)
        label.parent_node.text = label.text
        label.parent_node.bold = True



    def on_pressed_tipo_falla(self,label,mouseEvt):
        print "Presione un elemento tipo falla en el tree! %s\n" % label.text
        self.setTextoSeleccion(label)
        #Se cargan las props del tipoFalla seleccionado
        self.cargarPropsAsociadas(label.text)


    def on_pressed_propiedad(self,label,mouseEvt):
        print "Presione una propiedad del tipo de falla en el tree! %s\n" % label.text
        self.setTextoSeleccion(label)


    #Este metodo realiza la carga de elementos
    def cargarPropsAsociadas(self,nombreTipoFalla):
        print "En cargarPropsAsociadas()...\n"
        # Se limpian los layouts de los dropwdowns
        controlador = App.get_running_app()
        propsConfirmados = controlador.getPropsConfirmados()
        print "controlador.getPropsConfirmados(): %s...\n" % controlador.getPropsConfirmados()
        print "len(controlador.getPropsConfirmados()): %s...\n" % len(controlador.getPropsConfirmados())
        
        tipoFalla = propsConfirmados.getTipoFallaPorValor(nombreTipoFalla)
        mainLayout = self.parent.parent

        estaDeshabilitada = True
        if tipoFalla.estaHabilitada():
            estaDeshabilitada = False

        print "screen obtenido: %s\n" % type(self.screen)
        print "tipoFalla.getValor(): %s\n ; tipoFalla.estaHabilitada(): %s\n" % \
                                    (tipoFalla.getValor(),tipoFalla.estaHabilitada())
        #Se obtienen los strings de las propiedades asociadas a un tipoFalla
        tiposMaterial = propsConfirmados.getPropsAsociadasATipoFalla(nombreTipoFalla,"tipoMaterial")
        subLayout = self.screen.dropdownTipoMaterial.resetearDropdown("subLayoutTipoMaterial","TipoMaterial")
        self.reInicializarDropDownTipoMaterial(subLayout)
        self.screen.dropdownTipoMaterial.cargarOpciones(tiposMaterial,estaDeshabilitada)

        criticidades = propsConfirmados.getPropsAsociadasATipoFalla(nombreTipoFalla,"criticidad")
        subLayout = self.screen.dropdownCriticidad.resetearDropdown("subLayoutTipoCriticidad","TipoCriticidad")
        self.reInicializarDropDownCriticidad(subLayout)
        self.screen.dropdownCriticidad.cargarOpciones(criticidades,estaDeshabilitada)



    def resetearDropdown(self,subLayoutNombre,nombreDrop):
        print "self.screen.layout_principal:%s\n" % self.screen.layout_principal
        subLayout = None
        for x in self.screen.layout_principal.children:
            print "w.id: %s\n" % x.id
            if x.id == subLayoutNombre:
                subLayout = x
                for widget in x.children:
                    if widget.id == nombreDrop:
                        x.remove_widget(widget)
                        print "ENCONTRADO Y REMOVIDO DROP!!!\n"
                        break
        return subLayout

    def reInicializarDropDownCriticidad(self,subLayout):        
        self.screen.dropdownCriticidad = CustomDropDown(self.screen,
                                                id="TipoCriticidad",
                                                size_hint_y = None,
                                                size_hint_x = 1)
        subLayout.add_widget(self.screen.dropdownCriticidad)
        print "Agregado dropdown criticidad de nuevo!\n"


    def reInicializarDropDownTipoMaterial(self,subLayout):        
        self.screen.dropdownTipoMaterial = CustomDropDown(self.screen,
                                                id="TipoMaterial",
                                                size_hint_y = None,
                                                size_hint_x = 1)
        subLayout.add_widget(self.screen.dropdownTipoMaterial)
        print "Agregado dropdown tipo material de nuevo!\n"



    # Genera el string con los iconos segun el tipo de ponderacion.Este metodo
    # es exclusivo para el la criticidad asociada a un tipo de falla
    def generarStrIconos(self,propiedad):
        cadenaOpcion = ""
        print "propiedad: %s\n" % propiedad
        print "propiedades de criticidad: %s\n" % propiedad.getColPropsAsociadas()
        for subProp in propiedad.getColPropsAsociadas():
            print "recorriendo propiedades asociadas: %s\n" % subProp
            if subProp.getClave() == "ponderacion":
                if float(subProp.getValor()) <= PONDERACION_CRITICIDAD_BAJA:
                    #cadenaOpcion = "%s " % (icon('fa-exclamation-triangle',
                    cadenaOpcion = "%s " % (icon('cf-peligro',
                                                        TAMANIO_ICONOS,
                                                        color=COLOR_PONDERACION_BAJA).encode("utf-8")) 
                elif float(subProp.getValor()) > PONDERACION_CRITICIDAD_BAJA and \
                                float(subProp.getValor()) <= PONDERACION_CRITICIDAD_MEDIA:
                    cadenaOpcion = "%s%s " % ( (icon('cf-peligro',
                                                        TAMANIO_ICONOS,
                                                        color=COLOR_PONDERACION_MEDIA).encode("utf-8")),
                                                (icon('cf-peligro',
                                                        TAMANIO_ICONOS,
                                                        color=COLOR_PONDERACION_MEDIA).encode("utf-8"))
                                                )
                elif float(subProp.getValor()) > PONDERACION_CRITICIDAD_MEDIA and \
                            float(subProp.getValor()) <= PONDERACION_CRITICIDAD_ALTA:
                    cadenaOpcion = "%s%s%s " % ( (icon('cf-peligro',
                                                        TAMANIO_ICONOS,
                                                        color=COLOR_PONDERACION_ALTA).encode("utf-8")),
                                                (icon('cf-peligro',
                                                        TAMANIO_ICONOS,
                                                        color=COLOR_PONDERACION_ALTA).encode("utf-8")),
                                                (icon('cf-peligro',
                                                        TAMANIO_ICONOS,
                                                        color=COLOR_PONDERACION_ALTA).encode("utf-8"))
                                                )
                break
        return cadenaOpcion





    #Carga los elementos en el dropdown actual en base a una lista de strings
    def cargarOpciones(self,elementos,estanDesHabilitadas):
        print "En cargarOpciones()...\n"
        for prop in elementos:
            print "prop.getClave(): %s\n" % prop.getClave()
            print "prop.getValor(): %s\n" % prop.getValor()
            cadOpcion = prop.getValor()
            if prop.getClave() == "criticidad":
                print "entre a generarSTRIconos()!\n"
                cadOpcion = self.generarStrIconos(prop) + prop.getValor()
                
            print "agregando cadOpcion generada: %s\n" % cadOpcion
            element = TreeViewLabel(
                                    text = cadOpcion,
                                    disabled = estanDesHabilitadas,
                                    markup = True,
                                    disabled_color = COLOR_DROPDOWN_TEXTO_DESHABILITADO,
                                    color_selected = COLOR_DROPDOWN_ROW_SELECCIONADO,
                                    even_color = COLOR_ROW_PAR_DROPDOWN,
                                    odd_color = COLOR_ROW_IMPAR_DROPDOWN,
                                    font_size = TAMANIO_ELEMENTOS_CUSTOM_DROPDOWN
                                    )
            self.add_node(element)
            print "Esta deshabilitado %s: %s \n" % (cadOpcion, estanDesHabilitadas)
            element.no_selection = estanDesHabilitadas
            element.bind(on_touch_down = self.on_pressed_propiedad)



    # Este metodo retorna el contenido textual de una opcion que contiene iconos + contenido textual.
    # Se emplea unicamente en la propiedad asociada criticidad.
    # Retorna la cadena exacta si no contiene el patron, o el contenido textual si lo contiene.
    #filtrarContenidoOpcion(1,'[color=ff0000][size=32][font=resource/fonts/font-awesome.ttf]\xef\x81\xb1[/font][/size][/color] Pavimento  r\xc3\xadgido')
    def filtrarContenidoOpcion(self,cadena,filtrarPorSeparador = False):
        print "en filtrarContenidoOpcion()...\n"
        patron = re.compile(PATRON_ICONO_DROPDOWN)
        if patron.match(cadena) is not None:
            colCads = cadena.split()
            cad = ""
            for index in xrange(0,len(colCads)):
                if index == 0:
                    continue
                cad += colCads[index] + " "
            print "cad final: %s\n" % cad

            patron = re.compile(PATRON_SEPARADOR_CRITICIDAD_DROPDOWN)
            if filtrarPorSeparador and (patron.match(cad) is not None):
                print "filtrando por separador...\n"
                cad = cad.split(CARACTER_SEPARADOR_CRITICIDAD)[POSICION_INTERES_PARA_CRITICIDAD]
                print "cadena filtrada por separador final: %s\n" % cad
                return cad
        else:
            print "cadena final: %s\n" % cadena
            return cadena



    #Retorna la opcion seleccinada en el treeview
    def getOpcSeleccionadas(self,filtrarPorSeparador = False):
        if self.selected_node is None:
            return self.selected_node
        print "Existen nodos seleccionados!\n"
        return self.filtrarContenidoOpcion(self.selected_node.text,
                                            filtrarPorSeparador = filtrarPorSeparador)


    #Este metodo retorna las criticidades para los baches y las grietas
    # implementadas para la tesina
    @staticmethod
    def getCriticidadesHabilitadas():
        #TODO: Esta linea significa una peticion al servidor de todas las criticidades
        criticidades = CRITICIDADES 
        for elem in criticidades:
            elem["estaHabilitada"] = False
            if elem["id"] in IDS_CRITICIDADES_HABILITADAS:
                elem["estaHabilitada"] = True
        return criticidades

    def reestablecer(self):
        self.root.text = CustomDropDown.ICONO_DEFAULT_DROPDOWN 



from screenredimensionable import ScreenRedimensionable

#Clase principal de la GUI que agrupa por submenus los screenmangers que realizan
# el control de las transiciones
class MyTabbedPanel(TabbedPanel):
    
    def __init__(self,**kwargs):
        super(MyTabbedPanel,self).__init__(**kwargs)
        #background_image: '/home/rodrigo/TESINA-2016-KINECT/sky-01.jpg'
        # NOTA: Esta variable tiene indexados por el "nombre_menu" los screens y submenus de
        # cada uno de los archivos de configuracion de cada submenu.
        # Se usa desde el controlador(App) para algunos metodos concurrentes. 
        self.subMenus = {}

        self._inicializarSubScreens()

        #AGREGADO RODRIGO
        self.background_image = ESTILO_FONDO_TABBED_PANEL
        print "despues de inicializar...\n"

        
    #Retorna el Strip con todos los tabbedpanel items del menu.
    def getTabbedPanelStrip(self):
        return self._tab_strip.children            

    def getSubMenuPorNombre(self,nombreSubMenu):
        return self.subMenus[nombreSubMenu]


    # Obtiene todas las screens que se cargaron desde los
    # archivos de configuracion de cada submenu (.cfg), excepto aquellos
    # que son screens de tipo SubMenu.
    def getScreensRedimensionables(self):
        colScreens = []
        for nombreMenu,screen in self.subMenus.iteritems():
            if isinstance(screen,ScreenRedimensionable):
                print "nombreMenu: %s\n" % nombreMenu
                print "screen: %s\n" % screen
                colScreens.append(screen)
        print "retornando todas las screens...\n"
        return colScreens


    # Crea el TabbedPanelItem con el nombre y screenmanager(layout) y,
    # se lo asigna al tabbedpanel menu principal.
    #  
    def inicializarOpcionSubMenu(self,tituloSubMenu,nombreMenu,screenManager):
        tpItem = TabbedPanelItem(id= PREFIJO_ID_TP_ITEM + nombreMenu,
                                    text = tituloSubMenu)
        #tpItem = TabbedPanelItem(text = tituloSubMenu)
        #tpItem.background_down = 'atlas://customAppCliente/tab_btn_pressed'
        tpItem.background_down = ESTILO_TABBED_PANEL_PRESIONADO
        tpItem.background_normal = ESTILO_TABBED_PANEL_NORMAL

        tpItem.content = screenManager
        self.add_widget(tpItem)
        tpItem.bind(on_press = self._cambioSubMenu)


    #mytabbedpanel.cargar_vistas()
    def cargar_vistas(self,tituloSubMenu,listaVistas):
        sm = ScreenManager()
        print "\nLeyendo listaVistas: %s\n" % listaVistas
        for kev,tupla in listaVistas.iteritems():
            Builder.load_file(os.getcwd() + sep + tupla["ruta_kv"])
            MyClass = getattr(importlib.import_module(tupla["modulo"]), 
                                tupla["clase"])
            print "Leyendo clase: %s de tipo: %s\n\n" % (tupla["clase"],tupla["tipo"])
            screen = None
            
            # Los submenus contienen una referencia al widget padre que los contiene,
            # por lo que si es un submenu se pasa el tabbedpanel por parametro.
            if tupla["tipo"] == TIPO_SUB_MENU:
                screen = MyClass(self,name=tupla["nombre_menu"])
            else:
                screen = MyClass(name=tupla["nombre_menu"])
            
            self.subMenus[tupla["nombre_menu"]] = screen
            sm.add_widget(screen)
        # Crea un tabbedpanelItem para el screen manager con el nombre leido de la 
        # configuracion
        # Se pasa el ID
        self.inicializarOpcionSubMenu(tituloSubMenu,listaVistas['1']["nombre_menu"],sm) 


    # Carga instancia cada screenmanger y le agrega los screens que le corresponden
    # segun un archivo de configuracion.
    def _inicializarSubScreens(self):
        # Se agrega el path de cada modulo y se parsea la configuracion
        # de cada submenu como screens
        for dicSubMenu in LISTADO_SUB_MENUS:
            dirRaizModulo = os.getcwd() + sep + dicSubMenu["dirRaizModulo"]
            print "dirRaizModulo: %s\n\n" % dirRaizModulo
            sys.path.append(dirRaizModulo)
            confSubMenu = leer_configuracion(dicSubMenu["pathConfig"])
            print "\nInicializando subscreen: %s\n\n" % dicSubMenu 
            self.cargar_vistas(dicSubMenu["titulo"],confSubMenu)


    #Estos metodos habilitan y deshabilitan las opciones del tabbedpanel, cuando
    # se pulsan algunos de los botones que ingresan a algun submenu
    #def habilitarOpciones(self,evt):
    def habilitarOpciones(self):
        for widg in self.walk(restrict=True):
            if isinstance(widg, TabbedPanelStrip):
                print "hijos: %s\n" % widg.children
                for hijo in widg.children:
                    if not hijo == self.current_tab:
                        print "habilitando elemento: %s\n" % widg
                        hijo.disabled = False


    #def desHabilitarOpciones(self,evt):
    def desHabilitarOpciones(self):
        print "en tabbedpanel.desHabilitarOpciones()\n"
        for widg in self.walk(restrict=True):
            print "iterando... %s\n" % type(widg)
            if isinstance(widg, TabbedPanelStrip):
                print "hijos: %s\n" % widg.children
                for hijo in widg.children:
                    if not hijo == self.current_tab:
                        print "deshabilitando elemento: %s\n" % widg
                        hijo.disabled = True
    

    def _cambioSubMenu(self,instancia):
        print "Se presiono panelBD!!type(instancia): %s\n" % type(instancia)
        print "type(instancia.content): %s\n" % type(instancia.content)
        self.screenManagerActivo = instancia.content
        #self.desHabilitarOpciones()


