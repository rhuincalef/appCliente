from kivy.app import App
#from kivy.lang import Builder

#Imports para el AutoCompleteTextInput
import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label


from main import Controlador
from constantes import *

#Imports para el dropdown
from kivy.uix.treeview import TreeView,TreeViewNode,TreeViewLabel
from kivy.graphics import Color, Rectangle


#Imports para el tabbedpanel
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem,
                                    TabbedPanelHeader,TabbedPanelStrip

# Se importa resources para agregar el theme de kivy
import kivy.resources

# EventDispatcher para los eventos 
from kivy.event import EventDispatcher


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
        self.controlador = Controlador()
        
        # ...

        #Se bindea el evento de fin de obtencion de nombres de calles a la gui
        self.controlador.bind(on_fin_obtencion_direcciones = self.calles_obtenidas_servidor)

        
    
    #Manejador que recibe las calles sugeridas por el servidor.
    # NOTA: args es una tupla (clase Controlador, LISTA DE SUGERENCIAS)
    def calles_obtenidas_servidor(self,*args):
        #4. Se agregan los labels que indican las sugerencias de la calle
        # y se bindean el evento on_touch_down con el handler que modifica el text
        # input y remueve todos los widgets.
        self.boxLayoutSugerencias.clear_widgets()
        self.boxLayoutSugerencias.padding = [0,0,0,0]
        for i in xrange(0,len(args[1])):
            lab = Button(text = args[1][i],
                        color = (0,0,0,1),
                        background_normal = 'atlas://customAppCliente/autocomplete_normal')
            lab.bind(on_press = self.reemplazarContenido)
            self.boxLayoutSugerencias.add_widget(lab)
            #lab.background_normal = 'atlas://customAppCliente/autocomplete_normal'
        self.boxLayoutSugerencias.remove_widget(self.spinner)



    #Este metodo agrega labels que indican las sugerencias disponibles para 
    # autocompletar la calle ingresada por el usuario.
    def autocompletar(self,instance,value):
        print "\n\nVALOR ACTUAL TEXTINPUT: %s\n\n" % value
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
                                    background_normal = 'atlas://customAppCliente/autocomplete_normal')

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



class CustomDropDown(TreeView):

    root_options = {
                        'text': '',
                        'color_selected': (25.0/255.0, 152.0/255.0, 229.0/255.0,0.3),
                        'minimum_height': 500
                    }

    def __init__(self,**kwargs):
        super(CustomDropDown,self).__init__(**kwargs)
        self.toggle_node(self.root)


    #def callbackCargaOpciones(self,treeview, node):
    @staticmethod
    def callbackCargaOpciones(treeview, node):
        #TODO: SOLICITAR NOMBRES DE ATRIBUTOS
        #nombres = ['baja', 'media','alta','INVALIDA','INVALIDA']
        #dicNombres = self.getCriticidadesHabilitadas()
        dicNombres = CustomDropDown.getCriticidadesHabilitadas()
        print "dicNombres tiene: %s\n" % dicNombres
        if len(treeview.children) <= 0:
            for elem in dicNombres:
                if not elem["estaHabilitada"]:
                    element = TreeViewLabel(text = elem["nombre"] +": "+elem["descripcion"] ,
                                        color_selected = (25.0/255.0, 152.0/255.0, 229.0/255.0,0.3),
                                        disabled = True,
                                        disabled_color = (223.0/255.0, 221.0/255.0, 221.0/255.0,0.3)
                                        )
                    print "Esta deshabilitado: %s\n" % elem['nombre']
                    element.no_selection = True                    
                else:
                    element = TreeViewLabel(text = elem["nombre"] +": "+elem["descripcion"] ,
                                        color_selected = (25.0/255.0, 152.0/255.0, 229.0/255.0,0.3)
                                        )

                #element.bind(on_touch_down = self.on_pressed_element)
                element.bind(on_touch_down = treeview.on_pressed_element)
                yield element

    #def on_pressed_element(self,label,mouseEvt):
    #@staticmethod
    def on_pressed_element(self,label,mouseEvt):
        print "Presione un elemento del tree! %s\n" % label.text
        #Se colapsa el padre del elemento seleccionado
        #self.tv.toggle_node(label.parent_node)
        self.toggle_node(label.parent_node)
        label.parent_node.text = label.text
        label.parent_node.bold = True
        print "type(label.parent_node):%s\n" % type(label.parent_node)
        print "type(label.parent_node.parent_node):%s\n" % type(label.parent_node.parent)
        with label.parent_node.canvas.after:
            label.parent_node.canvas.after.clear()
            Color(25.0/255.0, 152.0/255.0, 229.0/255.0,0.3)
            Rectangle(pos = label.parent_node.pos, size = label.parent_node.size)

        self.getOpcSeleccionadas()


    def getOpcSeleccionadas(self):
        print "Los elementos seleccionados son:\n\n"
        print "Nodos seleccionados: %s\n" % self.selected_node.text
        #if self.tv.selected_node is not None:
        #    print "Nodos seleccionados: %s\n" % self.tv.selected_node.text
        #else:
        #    print "deshabilitado nodo!\n"
        #print "\n"

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


#Clase principal de la GUI que agrupa por submenus los screenmangers que realizan
# el control de las transiciones
class MyTabbedPanel(TabbedPanel):
    
    def __init__(self,**kwargs):
        super(MyTabbedPanel,self).__init__(**kwargs)
        #background_image: '/home/rodrigo/TESINA-2016-KINECT/sky-01.jpg'
        self._inicilizarSubScreens()
        print "despues de inicializar...\n"
        #Window.borderless =  True
        #Window.clearcolor = (1, 0, 0, 1)


    # Crea el TabbedPanelItem con el nombre y screenmanager(layout) y,
    # se lo asigna al tabbedpanel menu principal.
    #  
    def inicializarOpcionSubMenu(self,tituloSubMenu,screenManager):
        tpItem = TabbedPanelItem(text = tituloSubMenu)
        tpItem.background_down = 'atlas://customAppCliente/tab_btn_pressed'
        tpItem.content = screenManager
        self.add_widget(tpItem)
        tpItem.bind(on_press = self._cambioSubMenu)


    #main.cargar_vistas()
    def cargar_vistas(self,tituloSubMenu,listaVistas):
        sm = ScreenManager()
        for kev,tupla in listaVistas.iteritems():   
            print "Leyendo en directorio :%s\n" % os.getcwd()
            print "tupla actual: %s\n\n" % tupla
            Builder.load_file(os.getcwd() + sep + tupla["ruta_kv"])
            MyClass = getattr(importlib.import_module(tupla["modulo"]), 
            tupla["clase"])
            print "Leyendo clase: %s de tipo: %s\n\n" % (tupla["clase"],tupla["tipo"])
            screen = None
            if tupla["tipo"] == TIPO_SUB_MENU:
                screen = MyClass(self,name=tupla["nombre_menu"])
            else:
                screen = MyClass(name=tupla["nombre_menu"])
            sm.add_widget(screen)
        # Crea un tabbedpanelItem para el screen manager con el nombre leido de la 
        # configuracion
        self.inicializarOpcionSubMenu(tituloSubMenu,sm) 


    # Carga instancia cada screenmanger y le agrega los screens que le corresponden
    # segun un archivo de configuracion.
    def _inicilizarSubScreens(self):
        # Se agrega el path de cada modulo y se parsea la configuracion
        # de cada submenu como screens
        for dicSubMenu in LISTADO_SUB_MENUS:
            dirRaizModulo = os.getcwd() + sep + dicSubMenu["dirRaizModulo"]
            sys.path.append(dirRaizModulo)
            #confSubMenu = self.leer_configuracion(dicSubMenu["pathConfig"])
            confSubMenu = leer_configuracion(dicSubMenu["pathConfig"])
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
        for widg in self.walk(restrict=True):
            if isinstance(widg, TabbedPanelStrip):
                print "hijos: %s\n" % widg.children
                for hijo in widg.children:
                    if not hijo == self.current_tab:
                        print "deshabilitando elemento: %s\n" % widg
                        hijo.disabled = True
    

    #Este metodo retorna las criticidades para los baches y las grietas
    # implementadas para la tesina
    def getCriticidadesHabilitadas(self):
        #TODO: Esta linea significa una peticion al servidor de todas las criticidades
        criticidades = CRITICIDADES 
        for elem in criticidades:
            elem["estaHabilitada"] = False
            if elem["id"] in IDS_CRITICIDADES_HABILITADAS:
                elem["estaHabilitada"] = True
        return criticidades

    def _cambioSubMenu(self,instancia):
        print "Se presiono panelBD!!type(instancia): %s\n" % type(instancia)
        print "type(instancia.content): %s\n" % type(instancia.content)
        self.screenManagerActivo = instancia.content
        #self.desHabilitarOpciones()




