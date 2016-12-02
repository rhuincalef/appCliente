from kivy.uix.listview import ListItemLabel
from kivy.properties import ListProperty
from kivy.factory import Factory
from kivy.uix.label import Label

class ListItemColoured(Label):
   background_color = ListProperty([0,1,0,1])

#Factory.register('KivyB', module='ListItemColoured')
