# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.event import EventDispatcher
from kivy.uix.button import Button
from kivy.event import EventDispatcher
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox

# Este widget es un box layout que agrupa un CheckBox y un label que indica la opcion
# que se selecciono.
class RadioGroup(BoxLayout):

    def __init__(self,text="",**kwargs):
        super(RadioGroup,self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.cb = CheckBox(group='1')
        self.cb.size_hint = (0.1,1)
        self.add_widget(self.cb)
        self.contenido = Label(text = text)
        self.contenido.size_hint = (0.9,1)
        self.add_widget(self.contenido)

    def estaSeleccionado(self):
        print "\n\ncheckbox con contenido %s activo: %s\n" % \
                (self.contenido.text,self.cb.active)
        return self.cb.active

    def obtenerTexto(self):
        return self.contenido.text

    def getCheckBox(self):
        return self.cb


class ContainerRadioGroup(BoxLayout):

    def __init__(self,listadoElementos=[],**kwargs):
        super(ContainerRadioGroup,self).__init__(**kwargs)
        self.orientation = 'vertical'
        for arch in listadoElementos:
            radio1 = RadioGroup(text = arch)
            radio1.getCheckBox().bind(active = self.on_checkbox_active)
            self.add_widget(radio1)

    def on_checkbox_active(self,checkbox, value):
        if value:
            print "\n\nEl contenido seleccionado es: %s\n" % \
                                    self.obtenerContenidoSeleccionado()

    #Retorna el contenido del checkbox que se encuentra activo
    def obtenerContenidoSeleccionado(self):
        result = None
        for widget in self.walk(restrict=False):
            if isinstance(widget,RadioGroup):
                if widget.estaSeleccionado():
                    result = widget.obtenerTexto()
                    break
        return result

from notification import XMessage
from os import path
from screenredimensionable import ScreenRedimensionable

class ResultadosFiltradosScreen(ScreenRedimensionable):

    def __init__(self,**kwargs):
        super(ResultadosFiltradosScreen,self).__init__(**kwargs)
        self.contenedorOpciones = None

    def agregarArchivosFiltrados(self,archivos):
        print "en agregarArchivosFiltrados\n"
        self.ids.layout_elementos_filtrados.clear_widgets()
        self.contenedorOpciones = ContainerRadioGroup(archivos)
        self.ids.layout_elementos_filtrados.add_widget(self.contenedorOpciones)

    def cancelar(self):
        self.ids.layout_elementos_filtrados.clear_widgets()
        print "Limpiados resultados del screen!\n"
        self.manager.current = "fileFilter"

    def seleccionarArchivo(self):
        opcion = self.contenedorOpciones.obtenerContenidoSeleccionado()
        if opcion is None:
            XMessage(title = "Seleccion de opcion",
                        text = "Debe selecionar una opción para cargar")
            return
        print "\n\nLA OPCION SELECCIONADA FUE -------------->\n: %s\n\n" % opcion
        # Se inicializa TinyBD con la opcion seleccionada por el 
        # usuario (BD de muestras locales creada anteriormente por el usuario).
        controlador = App.get_running_app()
        controlador.inicializarBDLocal(fullPathBD = opcion)
        archivoBD = controlador.getBDLocalMuestras().getNombreBDLocal()
        #Se muestra un mensaje y se regresa al menu principal
        controlador.mostrarDialogoMensaje(title = 'Carga de BD Muestras anterior',
                                            text = 'BD de Muestras locales %s \n cargada exitosamente!' % \
                                            archivoBD)
        self.manager.current = "subMenuSeleccionarBD"
