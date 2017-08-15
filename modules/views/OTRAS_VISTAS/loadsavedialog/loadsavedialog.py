# # -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
import os


#Se carga la definicion de los dialogos en .kv de manera explicita,
# ya que no se respeta la convencion de que el archivo kv tiene el nombre
# de la app en minusucla(sin terminacion App).
#
from kivy.lang import Builder
Builder.load_file("./views/loadsavedialog/"+"loadsavedialog.kv")

class LoadDialog(GridLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(GridLayout):
    save = ObjectProperty(None) 
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)
print "Hecho el registro de las clases!!"
print ""

