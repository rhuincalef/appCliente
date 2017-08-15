import io
import picamera as p
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


# Fuente -->
# https://groups.google.com/forum/#!topic/kivy-users/-Pl4v-fohc0


class testApp(App):
    
    def build(self):    
        self.b= BoxLayout()
        self.image_composition = Image()
        self.cam = p.PiCamera()
        self.cam.resolution = 1600,896
        self.stream=io.BytesIO()
        self.cam.capture(self.stream, 'rgb')
        self.cam.close()
        self.stream.seek(0)
        self.tex = Texture.create(size=(1600,896), colorfmt='rgb')
        self.tex.blit_buffer(self.stream.getvalue(), colorfmt='rgb', bufferfmt='ubyte')
        with self.image_composition.canvas:
            Rectangle(texture = self.tex, size = (1600,896))
        print 'final'
        self.b.add_widget(self.image_composition)
        return self.b


testApp().run()
