# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton, ListItemLabel, ListView
from kivy.uix.listview import CompositeListItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
# from kivy.uix.floatlayout import FloatLayout





# NOTA: Libreria para hacer las peticiones en ajax
# http://docs.python-requests.org/en/master
#TODO: Hacer un parser de json para los datos del servidor.
# Se obtienen del servidor las fallas


class ExcepcionAjax(Exception):
    pass



class ServidorAPI:
	def __init__(self):
		pass
	# def parsear_json(self,file_json):
	# 	import json
	# 	with open(file_json) as data_file:    
	# 		data = json.load(data_file)
	# 	return data

	# Este metodo obtiene de una URL remota un json, que luego retorna como un
	# diccionario. 
	def obtener_baches(self,url_servidor):
		r = requests.get(url_servidor)
		if r.status_code != 200:
			msg_error = 'Error en la peticion: '+r.text
			raise ExcepcionAjax(msg_error)
		return r.json()





# Se solicitan los valores al servidor
def solicitar_valores_servidor():
  #TODO: Completar esta URL
  url_servidor = ""
  return {
      "0":{ "id": 1,
          "calle": "Belgrano",
          "altura": 200},
      "1":{ "id": 2,
          "calle": "Irigoyen",
          "altura": 200},
      "2":{ "id": 3,
          "calle": "Ameguino",
          "altura": 200},
      "3":{ "id": 4,
          "calle": "Pellegrini",
          "altura": 200},
      "4":{ "id": 5,
          "calle": "9 de Julio",
          "altura": 200},
      "5":{ "id": 6,
          "calle": "Aedo",
          "altura": 200},
      "6":{ "id": 7,
          "calle": "Callao",
          "altura": 200}
  }



class SettingScreen(Screen):
   
    def __init__(self, **kwargs):
      # item_strings = ["{0}".format(index) for index in range(100)]
      #self.item_strings = self.cargar_ids_fallas()
      self.integers_dict = solicitar_valores_servidor()  

      # self.integers_dict = {str(i): {'text': str(i), 'is_selected': False} for i in range(100)}
      # # Se parsea el .kv de la clase cuando se llama al constructor de la superclase.
      super(Screen, self).__init__(**kwargs)


    def get_adapter(self):
      return self.adaptador

    # def cargar_ids_fallas(self):
    #   return ["0","1","2"]

   # This is quite an involved args_converter, so we should go through the
    # details. A CompositeListItem instance is made with the args
    # returned by this converter. The first three, text, size_hint_y,
    # height are arguments for CompositeListItem. The cls_dicts list
    # contains argument sets for each of the member widgets for this
    # composite: ListItemButton and ListItemLabel.
    def args_converter(self,row_index, an_obj):
      return {
        'text': an_obj['id'],
        'size_hint_y': None,
        'height': 25,
        'cls_dicts': [{'cls': ListItemLabel,
                       'kwargs': {'text': "{0}".format(an_obj["id"]) }},
                       {
                           'cls': ListItemLabel,
                           'kwargs': {
                               'text': "{0}".format(an_obj["calle"]),
                               'is_representing_cls': True}},
                       {
                           'cls': ListItemLabel,
                           'kwargs': { 'text': "{0}".format(an_obj["altura"]) }}]}

