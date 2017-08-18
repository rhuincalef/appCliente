# -*- coding: utf-8 -*-
# import kivy
# kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color,Rectangle

from kivy.core.window import Window

from utils import *
from iconfonts import *
from constantes import *

from customwidgets import CustomDropDown

class PropsFallaConfirmadaScreen(Screen):

	def __init__(self,**kwargs):
		super(PropsFallaConfirmadaScreen, self).__init__(**kwargs)
		self.dropdownTipoFalla =self.dropdownTipoMaterial  = \
				self.dropdownTipoReparacion = None
		self.inicializarDropDown()

	def on_enter(self):
		controlador = App.get_running_app()
		# Si no existen propiedades para los tipos de falla cargadas se
		# se vuelve a la pantalla anterior 
		if not controlador.estanCargadasPropTipoFalla():
			controlador.mostrarDialogoMensaje(title="Error de propiedades TipoFalla",
												text="No se pueden capturar fallas nuevas hasta descargar\nlos tipos de propiedades desde el servidor.\nConectese a internet e inicie la aplicacion nuevamente \npara obtener una copia de los \natributos necesarios de los tipos de falla."
											)
			self.manager.current = 'menutiposfalla'
			return
		#Se cargan solamente los tipos de falla en el dropdown
		#listado = controlador.getPropsConfirmados()
		#if self.mainButtonFalla is None and self.mainButtonReparacion is None and self.mainButtonMaterial is None:
		#	self.inicializarDropDown(listado)
		#Se establece el idFalla como una falla no establecida
		controlador.agregarData("idFalla",FALLA_NO_ESTABLECIDA)
		

	#NOTA: Se deben constuir a mano los dropdowns para que funcionen correctamente
	# Inicializa el dropdown estableciendo todos los tipos de falla
	# en el dropdown y estableciendo el tipo de falla a la falla que
	# tiene index=0 por defecto.
	def inicializarDropDown(self):
		labPrincipal = Label(text='Seleccione los atributos con los que el tipo de falla se subira al servidor',
							size_hint =(1,0.05),color = COLOR_TEXTOS)
		self.ids.layout_principal.add_widget(labPrincipal)
		self.inicializarTipoFalla()
		self.inicializarTipoReparacion()
		self.inicializarTipoMaterial()
		self.inicializarFooter()
	
	def inicializarTipoFalla(self):
		labReparacion = Label(id= PREFIJO_LABEL_DROPDOWN + "TipoFallaDropdown",
							text='%s Seleccione el tipo de reparacion' % (icon('fa-gavel', TAMANIO_ICONOS)) ,
							markup=True,
							size_hint =(1,0.20),
							color = COLOR_TEXTOS)
		self.ids.layout_principal.add_widget(labReparacion)
		self.dropdownTipoFalla = CustomDropDown(id="TipoFallaDropdown",
												load_func = CustomDropDown.callbackCargaOpciones)
		self.ids.layout_principal.add_widget(self.dropdownTipoFalla)


	def inicializarTipoReparacion(self):
		# Inicializacion del boton y dropdown de Tipo de Reparacion
		labReparacion = Label( id=PREFIJO_LABEL_DROPDOWN + "TipoReparacionDropwdown",
							text='%s Seleccione el tipo de reparacion' % (icon('fa-gavel', TAMANIO_ICONOS)) ,
							markup=True,
							size_hint =(1,0.20),
							color = COLOR_TEXTOS)
		self.ids.layout_principal.add_widget(labReparacion)
		self.dropdownTipoReparacion = CustomDropDown(id="TipoReparacionDropwdown",
													load_func = CustomDropDown.callbackCargaOpciones)
		self.ids.layout_principal.add_widget(self.dropdownTipoReparacion)

	def inicializarTipoMaterial(self):
		# Inicializacion del boton y dropdown de Tipo de Material
		labMaterial = Label(id=PREFIJO_LABEL_DROPDOWN + "TipoMaterialDropdown",
							text='%s Seleccione el tipo de material' % (icon('fa-cubes', TAMANIO_ICONOS)) ,
							markup=True,
							size_hint =(1,0.20),
							color = COLOR_TEXTOS )
		self.ids.layout_principal.add_widget(labMaterial)
		self.dropdownTipoMaterial = CustomDropDown(id="TipoMaterialDropdown",
													load_func = CustomDropDown.callbackCargaOpciones)
		self.ids.layout_principal.add_widget(self.dropdownTipoMaterial)


	def inicializarFooter(self):
		layout = GridLayout(rows = 1,cols = 2,orientation = 'horizontal',
								size_hint= (1,0.05))
		btnAcept = Button(text = 'Aceptar')
		btnAcept.bind(on_press = self.aceptar)
		layout.add_widget(btnAcept)
		btnCancel = Button(text = 'Cancelar')
		btnCancel.bind(on_press = self.cancelar)
		layout.add_widget(btnCancel)
		self.ids.layout_principal.add_widget(layout)


	def actualizar_btn_mat(self,drop,btnNombre):
		setattr(self.mainButtonMaterial, 'text', btnNombre)


	def actualizar_btn_rep(self,drop,btnNombre):
		setattr(self.mainButtonReparacion, 'text', btnNombre)


	# Este metodo cambia el tipo de falla seleccionado en el dropdown
	# y cambia los atributos de los dropdownTipoMaterial y dropdownTipoReparacion
	def cambiarAttrTiposFalla(self,dropdown,btnNombre):
		#Se limpian los dropdowns antes de cargarlos
		#Se cambia el valor del boton que contiene al dropdown por el tipo de falla
		#elegido
		setattr(self.mainButtonFalla, 'text', btnNombre)

		self.dropdownTipoReparacion.clear_widgets()
		self.dropdownTipoMaterial.clear_widgets()

		controlador = App.get_running_app()
		#Se busca el tipo de falla seleccionado en la coleccion de los 
		#tipos cargados, y se retornan sus atributos
		atributos = controlador.getAtributosAsociados(btnNombre)
		print "Atributos obtenidos: %s\n" % atributos
		for elem in atributos:
			print "Iterando elemento.getClave(): %s\n" % elem.getClave()
			print "Iterando elem.getValor(): %s\n" % elem.getValor()
			#BACKUP!
			#btn = Button(text = str(elem.getValor()),size_hint_y=None, height=44)
			btn = Button(text = str(elem.getValor()),size_hint_y=None, height=44)
			if elem.getClave() == 'tipoReparacion':
				btn.bind(on_release=lambda btn: self.dropdownTipoReparacion.select(btn.text))
				self.dropdownTipoReparacion.add_widget(btn)
			else:
				btn.bind(on_release=lambda btn: self.dropdownTipoMaterial.select(btn.text))
				self.dropdownTipoMaterial.add_widget(btn)

		#Se reestablecen los valores del boton principal que contiene al dropdown
		setattr(self.mainButtonMaterial, 'text', "Seleccione el tipo de material")
		setattr(self.mainButtonReparacion, 'text', "Seleccione el tipo de reparación")
		#setattr(self.mainButtonReparacion, 'text', "Seleccione el tipo de reparacion")
		print "Cambiados attrs de tiposFalla...\n"



	# Al seleccionar un tipo de falla se carga el tipo de material y 
	# el tipo de reparacion. Al seleccionar se envia como argumento la
	# propiedad tipo de falla.
	# 
	def on_select(self,tipoFallaProp):
		print "Ingrese en on_select()...\n"
		print "ELiminando widgets viejos\n"
		dropdownTipoMaterial.clear_widgets()
		dropdownTipoReparacion.clear_widgets()
		print "Agregando widgets nuevos...\n"
		colProps = tipoFallaProp.getColPropsAsociadas()
		for p in colProps:
			btn = Button(text = p.getValor())
			if p.getValor() == "tipoReparacion":
				btn.bind(on_release = lambda elem: dropdownTipoReparacion.select(p))
				dropdownTipoReparacion.add_widget(btn)
			else:
				btn.bind(on_release = lambda elem: dropdownTipoMaterial.select(p))
				dropdownTipoMaterial.add_widget(btn)


	
	def aceptar(self,evt):
		#Se envian los datos de la falla
		screen = self.manager.get_screen('dialogopropscaptura')
		controlador = App.get_running_app()
		if not controlador.sonPropiedadesValidas(self.mainButtonFalla.text,
											self.mainButtonReparacion.text,
											self.mainButtonMaterial.text):
			controlador.mostrarDialogoMensaje(title="Error de propiedades",
												text="Debe seleccionar tipo de reparacion y tipo de material\n antes de continuar con la captura de fallas nuevas."
												)			
			return
		
		controlador.agregarData("tipoFalla",self.mainButtonFalla.text)
		controlador.agregarData("tipoReparacion",self.mainButtonReparacion.text)
		controlador.agregarData("tipoMaterial",self.mainButtonMaterial.text)
		self.manager.current = 'dialogopropscaptura'


	def cancelar(self,evt):
		self.manager.get_screen("subMenuCapturarFalla").habilitarOpciones()  
		self.manager.current = 'subMenuCapturarFalla'
