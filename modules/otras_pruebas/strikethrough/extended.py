from kivy.uix.label import Label
from kivy.core.text.markup import MarkupLabel

try:
    import pygame
except:
    raise
#
#pygame_cache = {}
#pygame_cache_order = []
#
#pygame.font.init()


class CoreLabelXMU(MarkupLabel):
    ''' A  core label with extended markup capabilities (underline and strikethrough markups)
    Brendan Scott 6 March 2013
    '''
    def __init__(self, *largs, **kwargs):
        self._style_stack = {}
        self._refs = {}
        super(MarkupLabel, self).__init__(*largs, **kwargs)    
        self.options['underline'] = False
        self.options['strike'] = False


    def _pre_render(self):
        # split markup, words, and lines
        # result: list of word with position and width/height
        # during the first pass, we don't care about h/valign
        self._lines = lines = []
        self._refs = {}
        self._anchors = {}
        spush = self._push_style
        spop = self._pop_style
        options = self.options
        options['_ref'] = None

        for item in self.markup:
            if item == '[b]':
                spush('bold')
                options['bold'] = True
                self.resolve_font_name()
            elif item == '[/b]':
                spop('bold')
                self.resolve_font_name()
            elif item == '[i]':
                spush('italic')
                options['italic'] = True
                self.resolve_font_name()
            elif item == '[/i]':
                spop('italic')
                self.resolve_font_name()
            elif item =='[s]':
                spush('strike')
                options['strike']=True  
            elif item =='[/s]':
                spop('strike')
            elif item =='[u]':
                spush('underline')
                options['underline']=True  
            elif item =='[/u]':
                spop('underline')

            elif item[:6] == '[size=':
                item = item[6:-1]
                try:
                    if item[-2:] in ('px', 'pt', 'in', 'cm', 'mm', 'dp', 'sp'):
                        size = dpi2px(item[:-2], item[-2:])
                    else:
                        size = int(item)
                except ValueError:
                    raise
                    size = options['font_size']
                spush('font_size')
                options['font_size'] = size
            elif item == '[/size]':
                spop('font_size')
            elif item[:7] == '[color=':
                color = parse_color(item[7:-1])
                spush('color')
                options['color'] = color
            elif item == '[/color]':
                spop('color')
            elif item[:6] == '[font=':
                fontname = item[6:-1]
                spush('font_name')
                options['font_name'] = fontname
                self.resolve_font_name()
            elif item == '[/font]':
                spop('font_name')
                self.resolve_font_name()
            elif item[:5] == '[ref=':
                ref = item[5:-1]
                spush('_ref')
                options['_ref'] = ref
            elif item == '[/ref]':
                spop('_ref')
            elif item[:8] == '[anchor=':
                ref = item[8:-1]
                if len(lines):
                    x, y = lines[-1][0:2]
                else:
                    x = y = 0
                self._anchors[ref] = x, y
            #else:
            #    item = item.replace('&bl;', '[').replace(
            #            '&br;', ']').replace('&amp;', '&')
            #    self._pre_render_label(item, options, lines)
                

        # calculate the texture size
        w, h = self.text_size
        if h < 0:
            h = None
        if w < 0:
            w = None
        if w is None:
            w = max([line[0] for line in lines])
        if h is None:
            h = sum([line[1] for line in lines])
        return w, h



    def _render_text(self, text, x, y):
        font = self._get_font()
        if self.options['underline']:
            font.set_underline(True)
        else:
            font.set_underline(False)

        color = [c * 255 for c in self.options['color']]
        color[0], color[2] = color[2], color[0]
        try:
            text = font.render(text, True, color)
            if self.options['strike']:
                ''' draw a horizontal line through the vertical middle of this surface in the foreground colour'''
                r = text.get_rect()
                pygame.draw.line(text, color, r.midleft, r.midright )

            self._pygame_surface.blit(text, (x, y), None, pygame.BLEND_RGBA_ADD)
        except pygame.error:
            pass



class LabelXMU(Label):
    ''' A label with extended markup capabilities (underline and strikethrough markups)
    Brendan Scott 6 March 2013
    '''

    def __init__(self, **kwargs):
        kwargs['markup']=True
        super(LabelXMU, self).__init__(**kwargs)
        d = Label._font_properties
        dkw = dict(zip(d, [getattr(self, x) for x in d]))
        self._label = CoreLabelXMU(**dkw)
