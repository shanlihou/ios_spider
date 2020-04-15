import ui
import math

class SwitchTextView (ui.View):
    def __init__(self):
        self.add_text_view('text')
        self.add_switch('slider')
        self.add_button('button')
        self.text_list = []
        self.button_cb = None
    
    def add_button(self, name):
        button = ui.Button()
        button.name = name
        button.title = name
        button.border_color = 'blue'
        button.border_width = 1
        button.corner_radius = 3
        button.action = self._add_action
        self.add_subview(button)
        self.button = button
    
    def add_action(self, func):
        self.button_cb = func
        
    def _add_action(self, sender):
        if not self.button_cb:
            return
            
        if not self.text_list:
            return
            
        val =self.get_index()
        self.button_cb(val)
    
    def set_text_list(self, text_list):
        self.text_list = text_list
        if self.text_list:
            self.tex_view.text = text_list[0]
        
    def add_text_view(self, name):
        t = ui.TextView()
        t.name = name
        self.add_subview(t)
        self.tex_view = t
        
    def add_switch(self, name):
        s = ui.Slider()
        self.add_subview(s)
        s.action = self.slider_action
        self.slider = s
        
    def get_index(self):
        t_len = len(self.text_list)
        val = round(self.slider.value * (t_len - 1))
        return val
        
    def slider_action(self, sender):
        if not self.text_list:
            return
        
        val = self.get_index()
        self.tex_view.text = self.text_list[val]
    
    def layout(self):
        half_width = self.width // 2
        half_height = self.height // 2
        self.tex_view.frame = (0, 0, half_width, half_height)
        
        self.button.frame = (half_width, 0, half_width, half_height)
        
        self.slider.frame = (0, half_height, self.width, half_height)
    
        
if __name__ == '__main__':
    st = SwitchTextView()
    st.set_text_list(['a', 'b', 'c', 'd'])
    st.present('fullscreen')
        
