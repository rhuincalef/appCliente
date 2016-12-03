
# +Capturador
# 		-ColCapturasTotales
# 		-ColCapturasConfirmadas(Capturas que se van a subir al servidor)
# 		-apiClient
# 		+filtrarCapturas(colCapturasTotales)
# 		+enviarCapturas(apiClient)

import sys,os
from apiclient1 import ApiClientApp
from kivy.adapters.models import SelectableDataItem

class Capturador(object):
	def __init__(self):
		self.colCapturasTotales = []
		self.colCapturasConfirmadas = []
		self.apiClient = ApiClientApp()
        print "Inicializado Capturador"

	def filtrarCapturas(self):
		pass

	def enviarCapturas(self):
		pass

# + Capturador > CapturadorInformado
# 		-ColBachesInformados (Se envian la calle y/o altura y envia los informados en ese rango)
# 		+solicitarInformados()

class ItemFalla(SelectableDataItem):
  def __init__(self,id_falla,calle,altura, is_selected=False, **kwargs):
     super(ItemFalla, self).__init__(is_selected=is_selected, **kwargs)
     self.id = id_falla
     self.calle = calle
     self.altura = altura
     self.is_selected = False

  def __cmp__(self,other):
    if self.id > other.id:
      return 0
    elif self.id == other.id:
      return 0
    else:
      return -1


class CapturadorInformados(Capturador):
    def __init__(self):
        super(CapturadorInformados,self).__init__()
        self.colBachesInformados = []
        print "Inicializado CapturadorInformado"

    def solicitarInformados(self,calle,altura):
        #TODO: Este diccionario se transforma en un diccionario en JSON
        dic_json= {
        "1":{ "id": 1,
            "calle": "Belgrano",
            "altura": 200},
        "2":{ "id": 2,
            "calle": "Irigoyen",
            "altura": 200},
        "3":{ "id": 3,
            "calle": "Ameguino",
            "altura": 200},
        "4":{ "id": 4,
            "calle": "Pellegrini",
            "altura": 200},
        "5":{ "id": 5,
            "calle": "9 de Julio",
            "altura": 200},
        "6":{ "id": 6,
            "calle": "Aedo",
            "altura": 200},
        "7":{ "id": 7,
            "calle": "Callao",
            "altura": 200}
        } 


        for key,tupla in dic_json.iteritems():
            falla = ItemFalla(tupla["id"],tupla["calle"],tupla["altura"])
            self.colBachesInformados.append(falla)

        self.colBachesInformados = sorted(self.colBachesInformados)
        return self.colBachesInformados










