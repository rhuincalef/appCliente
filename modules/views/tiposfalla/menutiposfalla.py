# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

class MenuTiposFallaScreen(Screen):
    #Menu para seleccionar las fallas que se traeran del servidor
    def menu_fallas_informadas(self):
    	print "Menu fallas informadas del servidor"
    	self.manager.current = 'settingscreen' 

    def menu_falla_nueva(self):
    	self.manager.current = 'capturaKinect' 

# NOTA: La clase que hereda de App tiene que tener el mismo nombre que el layout del 
# archivo .kv.
# class MenuTiposFallaApp(App):
#     def build(self):
#         self.title = "Capturador de fallas"
#         return MenuTiposFalla()


# if __name__ == '__main__':
#     MenuTiposFallaApp().run()




