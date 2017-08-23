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
				self.dropdownCriticidad = None
		self.layout_principal = GridLayout(id="layout_principal",
											cols = 1,
											rows = 9,
											size_hint_y = None,
											orientation = 'vertical')
		self.layout_principal.setter('height')
		#self.layout_principal.bind(minimum_height = self.layout_principal.setter('height'))
		self.layout_principal.bind(minimum_height = self.calcular_height )
		self.inicializarDropDownPrincipal()



	# Este metodo establece la altura maxima del layout, lo que determina
	# hasta que punto el usuario puede scrollear sobre este.
	def calcular_height(self,instance,value):
		self.layout_principal.height = 940


	# Calcula el espacio reservado para cada una de las opciones de los customdropdown
	def calcularSpacingEntreLayouts(self,cantidadCriticidades):
		contador = 0
		for i in xrange(1,cantidadCriticidades):
			print "Iterando valor i:%s\n" % i
			contador += PADDING_POR_WIDGET
			print "contador actual: %s\n" % contador 
		self.layout_principal.spacing = [0, contador]


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
		#Se establece el idFalla como una falla no establecida
		controlador.agregarData("idFalla",FALLA_NO_ESTABLECIDA)
		

	#NOTA: Se deben constuir a mano los dropdowns para que funcionen correctamente
	# Inicializa el dropdown estableciendo todos los tipos de falla
	# en el dropdown y estableciendo el tipo de falla a la falla que
	# tiene index=0 por defecto.
	def inicializarDropDownPrincipal(self):
		labPrincipal = Label(id = "labelPrincipal",text='Seleccione los atributos con los que el tipo de falla se subira al servidor',
							size_hint =(1,None),
							color = COLOR_TEXTOS)
		
		print "En inicializarDropDownPrincipal()... \n"
		#controlador = App.get_running_app()
		#dicNombres = controlador.getPropsConfirmados()
		#cantMaximaOpcionesDropwdown = 0
		#print "type(todasPropsConfirmadas): %s\n" % type(dicNombres)
		#print "todas las propiedades confirmadas: %s\n" % dicNombres

		self.inicializarTipoFalla(label = None)
		#longitud = len(dicNombres)
		#print "LONGITUD: %s\n" % longitud

		self.inicializarTipoMaterial()
		#cantOpcTipoMaterial = todasPropsConfirmadas.getCantPropsTipoFalla("tipoMaterial") 
		#if cantMaximaOpcionesDropwdown < cantOpcTipoMaterial:
		#	cantMaximaOpcionesDropwdown = cantOpcTipoMaterial

		self.inicializarTipoCriticidad()
		#cantOpcCriticidad = todasPropsConfirmadas.getCantPropsTipoFalla("criticidad") 
		#if cantMaximaOpcionesDropwdown < cantOpcCriticidad:
		#	cantMaximaOpcionesDropwdown = cantOpcCriticidad
		
		self.inicializarFooter()
		self.ids.main_scroll_view.add_widget(self.layout_principal)
		#print "valor final cantMaximaOpcionesDropwdown: %s\n" % cantMaximaOpcionesDropwdown
		#self.calcularSpacingEntreLayouts(cantMaximaOpcionesDropwdown)
		self.calcularSpacingEntreLayouts(6)
	

	def inicializarTipoFalla(self,label=None):
		subLayout = GridLayout(id="subLayoutTipoFalla",
					cols = 1,
					rows = 2,
					size_hint_y = None,
					orientation = 'vertical')
		if label is not None:
			subLayout.add_widget(label)

		labReparacion = Label(id= PREFIJO_LABEL_DROPDOWN + "TipoFallaDropdown",
							text='%s Seleccione el tipo de falla' % (icon('cf-bache', TAMANIO_CUSTOM_ICONOS)) ,
							#text='%s Seleccione el tipo de falla' % (icon('cf-bache', TAMANIO_ICONOS)) ,
							
							markup=True,
							size_hint_y = None,
							size_hint_x = 1,
							color = COLOR_TEXTOS)
		subLayout.add_widget(labReparacion)

		self.dropdownTipoFalla = CustomDropDown(self,id="TipoFallaDropdown",
												size_hint_y = None,
												size_hint_x = 1,
												load_func = CustomDropDown.callbackCargaTiposFalla)
		subLayout.add_widget(self.dropdownTipoFalla)
		self.layout_principal.add_widget(subLayout)
		


	def inicializarTipoMaterial(self,label=None):
		subLayout = GridLayout(id="subLayoutTipoMaterial",
					cols = 1,
					rows = 2,
					size_hint_y = None,
					orientation = 'vertical')
		if label is not None:
			subLayout.add_widget(label)

		labReparacion = Label(id= PREFIJO_LABEL_DROPDOWN + "TipoMaterial",
							#text='%s Seleccione el tipo de material' % (icon('cf-tipomaterial', TAMANIO_ICONOS)) ,
							text='%s Seleccione el tipo de material' % (icon('cf-tipomaterial', TAMANIO_CUSTOM_ICONOS)) ,
							markup=True,
							size_hint_y = None,
							size_hint_x = 1,
							color = COLOR_TEXTOS)
		subLayout.add_widget(labReparacion)

		self.dropdownTipoMaterial = CustomDropDown(self,id="TipoMaterial",
												size_hint_y = None,
												size_hint_x = 1)
		subLayout.add_widget(self.dropdownTipoMaterial)
		self.layout_principal.add_widget(subLayout)


	def inicializarTipoCriticidad(self,label=None):
		subLayout = GridLayout(id="subLayoutTipoCriticidad",
					cols = 1,
					rows = 2,
					size_hint_y = None,
					orientation = 'vertical')
		if label is not None:
			subLayout.add_widget(label)

		labReparacion = Label(id= PREFIJO_LABEL_DROPDOWN + "TipoCriticidad",
							text='%s Seleccione la criticidad' % (icon('fa-exclamation-triangle', TAMANIO_ICONOS)) ,
							markup=True,
							size_hint_y = None,
							size_hint_x = 1,
							color = COLOR_TEXTOS)
		subLayout.add_widget(labReparacion)

		self.dropdownCriticidad = CustomDropDown(self,id="TipoCriticidad",
												size_hint_y = None,
												size_hint_x = 1)
												#,load_func = CustomDropDown.callbackCargaOpciones)
		subLayout.add_widget(self.dropdownCriticidad)
		self.layout_principal.add_widget(subLayout)
		#return len(CustomDropDown.getCriticidadesHabilitadas())


	def inicializarFooter(self):
		layout = GridLayout(
							rows = 1,
							cols = 2,
							orientation = 'horizontal',
							size_hint_y = None,
							padding = (0,50,0,0)
							#size_hint= (1,0.05),
							#padding = (0,10,0,0)
							)
		btnAcept = Button(text = 'Aceptar')
		btnAcept.bind(on_press = self.aceptar)
		layout.add_widget(btnAcept)
		btnCancel = Button(text = 'Cancelar')
		btnCancel.bind(on_press = self.cancelar)
		layout.add_widget(btnCancel)
		self.layout_principal.add_widget(layout)



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


	# Este metodo busca dentro de los sublayouts del layout principal un sublayout
	# con un nombre dado y, dentro de este, un widget con un nombre especificado.
	def _obtenerWidgetPorId(self,nombreSubLayout,nombreWidget):
		print "En _obtenerWidgetPorId()..\n"
		for subLayout in self.layout_principal.children:
			print "En subLayout.id: %s..\n" % subLayout.id
			if subLayout.id == nombreSubLayout:
				print "encontrado sublayout: %s\n" % nombreSubLayout
				for widget in subLayout.children:
					print "En widget.id: %s , nombreWidget:%s..\n" % (widget.id,nombreWidget)
					if widget.id == nombreWidget:
						print "Encontrado widget!:%s..\n" % type(widget)
						return widget
		return None
	
	
	def aceptar(self,evt):
		#Se envian los datos de la falla
		controlador = App.get_running_app()
		screen = self.manager.get_screen('dialogopropscaptura')

		tipoFalla = self._obtenerWidgetPorId("subLayoutTipoFalla","TipoFallaDropdown").getOpcSeleccionadas()
		criticidad = self._obtenerWidgetPorId("subLayoutTipoCriticidad","TipoCriticidad").getOpcSeleccionadas()
		tipoMaterial = self._obtenerWidgetPorId("subLayoutTipoMaterial","TipoMaterial").getOpcSeleccionadas()

		print "props leidas: %s, %s, %s \n\n" % (tipoFalla,tipoMaterial,criticidad)
		if (tipoFalla is None) or (criticidad is None) or (tipoMaterial is None):
			controlador.mostrarDialogoMensaje(title="Error de propiedades",
												text="Debe seleccionar tipo de reparacion y tipo de material\n antes de continuar con la captura de fallas nuevas."
												)			
			return

		controlador.agregarData("tipoFalla",tipoFalla)
		controlador.agregarData("tipoMaterial",tipoMaterial)
		controlador.agregarData("criticidad",criticidad)
		self.manager.current = 'dialogopropscaptura'



	#Reestablece el contenido sin seleccionar de todos los dropdowns
	def reestablecerDropDowns(self):
		for subLayout in self.layout_principal.children:
			print "Iterando elemento: %s\n" % subLayout.id
			if subLayout.id == "subLayoutTipoCriticidad" or \
						subLayout.id == "subLayoutTipoFalla" or \
						subLayout.id == "subLayoutTipoMaterial":						
				for widget in subLayout.children:
					if widget.id == "TipoFallaDropdown" or widget.id == "TipoCriticidad" or \
								 widget.id == "TipoMaterial":
						widget.reestablecer()

	#Borra la info temporal almacenada en controlador
	def borrarData(self):
		controlador = App.get_running_app()
		try:
			controlador.getData("criticidad")
			controlador.borrarData("criticidad")
		except (KeyError,Exception) as e:
			print "Clave criticidad en controlador inexistente!\n"
		
		try:
			controlador.getData("tipoFalla")
			controlador.borrarData("tipoFalla")
		except (KeyError,Exception) as e:
			print "Clave tipoFalla en controlador inexistente!\n"
			
		try:
			controlador.getData("tipoMaterial")
			controlador.borrarData("tipoMaterial")
		except (KeyError,Exception) as e:
			print "Clave tipoMaterial en controlador inexistente!\n"



	def cancelar(self,evt):
		self.manager.get_screen("subMenuCapturarFalla").habilitarOpciones()
		self.reestablecerDropDowns()
		self.manager.current = 'subMenuCapturarFalla'
