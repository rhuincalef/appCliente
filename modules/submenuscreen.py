from kivy.uix.screenmanager import ScreenManager, Screen

class SubMenuScreen(Screen):
	
	def __init__(self,tabbedPanel,**kwargs):
		super(SubMenuScreen,self).__init__(**kwargs)
		self.tabbedPanel = tabbedPanel

 
	def deshabilitarOpciones(self):
		#print "type(self.parent.parent.parent): %s\n" % type(self.parent.parent.parent)
		#self.parent.parent.parent.desHabilitarOpciones()
		self.tabbedPanel.desHabilitarOpciones()


	def habilitarOpciones(self):
		#print "type(self.parent): %s\n" % type(self.parent)
		#print "type(self.parent.parent): %s\n" % type(self.parent.parent)
		#print "type(self.parent.parent.parent): %s\n" % type(self.parent.parent.parent)
		#print "Habilitando las opciones del menu principal!\n"
		#self.parent.parent.parent.habilitarOpciones()
		self.tabbedPanel.habilitarOpciones()


