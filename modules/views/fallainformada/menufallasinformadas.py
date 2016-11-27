# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
# from kivy.uix.floatlayout import FloatLayout


class MenuFallasInformadasScreen(Screen):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    pass

# NOTA: La clase que hereda de App tiene que tener el mismo nombre que el layout del 
# archivo .kv.
# class MenuTiposFallaApp(App):
#     def build(self):
#         self.title = "Capturador de fallas"
#         return MenuTiposFalla()


# if __name__ == '__main__':
#     MenuTiposFallaApp().run()




