# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from file import XFolder
from os.path import sep, expanduser, isdir, exists, dirname, join, getsize
import re
from notification import XLoading, XConfirmation, XMessage
import threading

from constantes import REGEX_FORMATO_FECHA,PATH_ICONO_LUPA,PATRON_SUBFIJO_ARCHIVOS_BD_CONFIRMADAS
import datetime
import os
from kivy.event import EventDispatcher

from screenredimensionable import ScreenRedimensionable

class FileFilterScreen(ScreenRedimensionable,EventDispatcher):

    def __init__(self,**kwargs):
        super(FileFilterScreen,self).__init__(**kwargs)
        #self.padding = [50,100,50,300]
        #Var que se emplea para almacenar los archivos seleccioandos actualmente
        self.archSeleccionados = []
        self.popup = None
        self.register_event_type('on_fin_busqueda_archivos')

    def sonDatosValidos(self):
        patronArchivo = self.ids.text_input_patron.text 
        directoriosBusqueda = self.ids.text_input_lista_directorios.text
        if not (self.esFechaValida(patronArchivo)):
            XMessage( title='Datos inválidos', text='El formato de la fecha no es válido')
            return

        if not (self.sonDirsValidos(directoriosBusqueda)[0]):
            XMessage( title='Datos inválidos', text='El directorio %s no es un directorio válido' % \
                                                    str(self.sonDirsValidos(directoriosBusqueda)[1]))
            return
        print "\n\nDATOS PARSEADOS CORRECTAMENTE!!! \n"
        print "patronArchivo: %s\n" % patronArchivo
        print "directoriosBusqueda: %s\n\n" % directoriosBusqueda
        return True

    def esFechaValida(self,patronArchivo):
        print "en es fecha valida!\n"
        esFechaValida = False
        expr = re.compile(REGEX_FORMATO_FECHA)
        matchObj =  expr.match(patronArchivo)
        if matchObj is None:
            return esFechaValida
        #Si son datos validos se comprueba la validez de la fecha
        try:
            fecha = matchObj.group(0)
            print "fecha obtenida: %s\n" % fecha
            datetime.datetime.strptime(fecha,"%d-%m-%Y")
            esFechaValida = True
        except (ValueError,Exception) as e:
            print "Error al convertir la fecha: %s\n" % e
        finally:
            return esFechaValida

    
    # Se retorna una lista de directorios que contienen algun path y no son
    # caracteres vacios.
    def parsearDirs(self,cadDirs):
        cadenas = [] 
        for cad in cadDirs.split(","):
            if cad.strip():
                cadenas.append(cad)
        return cadenas

    #Verifica que exista el path y que sea un directorio
    def sonDirsValidos(self,directoriosBusqueda):
        dirsParseados = self.parsearDirs(directoriosBusqueda)
        if len(dirsParseados) == 0:
            return (False,"''")
        for cad in dirsParseados:
            if not (exists(cad) or isdir(cad)):
                return (False,cad)
        return (True,"")

    def on_fin_busqueda_archivos(self,instance):
        pass

    def buscarArchivo(self):
        print "Buscando archivo: %s en directorios: %s\n\n" % (self.ids.text_input_patron.text ,
                                                               self.ids.text_input_lista_directorios.text)
        if self.sonDatosValidos():
            print "Datos validos enviados al metodo de busqueda: \n\n"
            print "Patron de archivo: %s\n" % self.ids.text_input_patron.text
            print "Directorios seleccionados: %s\n" % self.ids.text_input_lista_directorios.text

            self.popup = self.mostrarDialogoEspera(title ="Buscando archivos",
                                        content= "Estimando direcciones de capturas confirmadas...")
            self.bind(on_fin_busqueda_archivos = self.mostrarResultados)            
            t = threading.Thread(name = "thread-FiltradoArchivos",
                                    target = self.threadFiltrarArchivos)
            t.setDaemon(True)
            t.start()


    #Parsear el string con los directorios, buscar en cada uno archivos con el patron y
    # llamar al controlador para emitir el evento "on_fin_busqueda_archivos".  
    def threadFiltrarArchivos(self):
        patronArchivo = self.ids.text_input_patron.text
        listaDirectorios = self.parsearDirs(self.ids.text_input_lista_directorios.text)
        archivosFiltrados = []
        for nombreDir in listaDirectorios:
            print "Iterando directorio: %s...\n" % nombreDir
            for dirPath, dirs, files in os.walk(nombreDir):
                for file in files:
                    # Si el archivo concuerda con el patron y la extension
                    # se genera el fullpath y se lo almacena para mostrarlo posteriormente 
                    #TODO: PERFECCIONAR ESTO PARA QUE SOLO BUSQUE EL PATRON 
                    # "SUBFIJO_ARCHIVOS_BD_CONFIRMADAS" SI EL ARCHIVO TERMINA CON ESA EXTENSION!!
                    #if file.find(patronArchivo) != -1 and file.find(SUBFIJO_ARCHIVOS_BD_CONFIRMADAS):
                    if file.find(patronArchivo) != -1 and (re.compile(".*\.json$").match(file) is not None):
                        fullPathArch = join(dirPath,file)
                        archivosFiltrados.append(fullPathArch)

        print "\nArchivos filtrados: %s\n\n" % archivosFiltrados
        if len(archivosFiltrados) == 0:
            controlador = App.get_running_app()
            controlador.mostrarDialogoMensaje(title="Filtrado de archivos",
                                        text="No existen archivos de BD relacionados a esa fecha")
            self.popup.dismiss()
            return

        self.dispatch('on_fin_busqueda_archivos',archivosFiltrados)

    # Si existen resultados encontrados se carga el screen que tiene una lista
    # de resultados; Sino, se muestra un dialogo indicando que no se encontraron 
    # archivos con ese nombre.
    def mostrarResultados(self,instance,args):
        print "En mostrarResultados(), recibiendo archivos filtrados\n %s\n\n" % \
                    type(instance)
        print "En mostrarResultados(), recibiendo archivos filtrados\n %s\n\n" % \
                    type(args)
        print "args: %s\n" % args
        screen = self.manager.get_screen('resultadosFiltrados')
        
        print "obtenido screen\n"
        screen.agregarArchivosFiltrados(args)
        self.popup.dismiss()
        print "agregadosArchivosFiltrados()!\n"
        self.manager.current = "resultadosFiltrados"

    #Se llama desde todos los lugares donde es necesario mostrar
    # un dialogo de carga
    def mostrarDialogoEspera(self,title="",content="",gif = PATH_ICONO_LUPA):
        dialogo = XLoading(title=title,
                            content = content,
                            auto_open=False,
                            gif = gif,
                            size_hint_x = 0.5,
                            size_hint_y = 0.4)
        dialogo.open()
        return dialogo

    #Este metodo debe abrir el XFolder para navegar los archivos.
    def onXFolderSeleccionado(self):
        print "Presione el btn para activar el xFolder \n"
        XFolder(on_dismiss = self._filepopup_callback, 
                path = expanduser(u'~'),
                dirselect = True,
                multiselect = True)

    def _filepopup_callback(self, instance):
        if instance.is_canceled():
            return

        print "\nLa seleccion hecha es: %s\n" % (instance.selection)
        self.archSeleccionados = instance.selection
        strSeleccion = ""
        for d in self.archSeleccionados:
            strSeleccion += d + ","    
        print "\nLa strSeleccion es: %s\n" % strSeleccion
        self.ids.text_input_lista_directorios.text = strSeleccion

    def cancelar(self):
        print "cancelar seleccion!\n"
        self.archSeleccionados = []
        print "Limpiando campos del screen...\n"
        self.ids.text_input_patron.text = ''
        self.ids.text_input_lista_directorios.text = ''
        self.habilitarMenuPrincipal()

    #Se rehabilitan las opciones del menu principal del tabbedpanel
    def habilitarMenuPrincipal(self):
        scr = self.manager.get_screen("subMenuSeleccionarBD")
        print "type(src): %s\n" % type(scr)
        scr.habilitarOpciones()
        self.manager.current = "subMenuSeleccionarBD"
