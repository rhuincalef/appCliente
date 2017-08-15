# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from file import XFolder
from os.path import sep, expanduser, isdir, exists, dirname, join, getsize
import re
from notification import XLoading, XConfirmation, XMessage
import threading

from constantes import REGEX_FORMATO_FECHA,PATH_ICONO_LUPA
import datetime
import os
from kivy.event import EventDispatcher

from customwidgets import CustomDropDown

class SeleccionarTipoFallaScreen(Screen,EventDispatcher):

    def __init__(self,**kwargs):
        super(SeleccionarTipoFallaScreen,self).__init__(**kwargs)
        print "Construyendo GUI!\n"
        self.dropdown = CustomDropDown(load_func = CustomDropDown.callbackCargaOpciones)
        self.ids.container_dropbox_falla.add_widget(self.dropdown)


    def buscarDireccion(self):
        print "recogiendo opciones seleccionada del dropdown: %s\n\n" % \
                    self.obtenerCriticidadSeleccionada()

    def obtenerCriticidadSeleccionada(self):
        return self.dropdown.getOpcSeleccionadas()

    def cancelar(self):
        self.habilitarMenuPrincipal()


    #Se rehabilitan las opciones del menu principal del tabbedpanel
    def habilitarMenuPrincipal(self):
        scr = self.manager.get_screen("subMenuCapturarFalla")
        print "type(src): %s\n" % type(scr)
        scr.habilitarOpciones()
        self.manager.current = "subMenuCapturarFalla"
