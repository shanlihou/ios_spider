import ui


class SearchView(ui.View):
    def __init__(self, attach_func=None):
        self.add_edit()
        self.add_button('btn')
        self.attach_func = attach_func

    def add_edit(self):
        t = ui.TextField()
        t.name = 'edit'
        t.border_color = 'blue'
        self.add_subview(t)
        self.edit = t

    def button_action(self, sender):
        text = self.edit.text
        print(text)
        if self.attach_func:
            self.attach_func(text)

    def add_button(self, name):
        button = ui.Button()
        button.name = name
        button.title = name
        button.border_color = 'blue'
        button.border_width = 1
        button.corner_radius = 3
        button.action = self.button_action
        self.add_subview(button)
        self.button = button

    def layout(self):
        button_width = 100
        self.edit.frame = (0, 0, self.width - button_width, self.height)
        self.button.frame = (self.width - button_width, 0,
                           button_width, self.height)
                           
if __name__ == '__main__':
    v = SearchView()
    v.present()
