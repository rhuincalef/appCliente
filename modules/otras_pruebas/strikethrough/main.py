from kivy.app import App
from kivy import kivy_options
from extended import LabelXMU

kivy_options['text']='pygame'

class LabelWithMarkup(App):
    def build(self):
        root = LabelXMU(text=r"Some [b]bold[/b] [i]italic[/i] [u] underlined[/u] [s] strikethrough[/s] and plain text",   font_size=22)
        return root

if __name__ == '__main__':
    LabelWithMarkup().run()