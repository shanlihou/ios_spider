import ui
from TabbedView import TabbedView
import MainView
import const


def tab_show():
    v = TabbedView()
    v.addtab(MainView.MainView())
    v.addtab(MainView.MainView(const.AdaptorType.love))
    v.addtab(MainView.MainView(const.AdaptorType.hate))
    v.focus_tab_by_index(0)
    v.present()


class HomeView(ui.View):
    def __init__(self):
        self.button_dic = {}
        self.button_height = 30
        self.add_button('search')
        self.add_button('main')

    def show_search(self):
        mv = MainView.MainView(const.AdaptorType.search)
        mv.present()

    def button_action(self, sender):
        if sender.name == 'main':
            tab_show()
        elif sender.name == 'search':
            self.show_search()

    def add_button(self, name):
        button = ui.Button()
        button.name = name
        button.title = name
        button.border_color = 'blue'
        button.border_width = 1
        button.corner_radius = 3
        button.action = self.button_action
        self.add_subview(button)
        self.button_dic[name] = button

    def layout(self):
        y_off = 0
        for index, bt in enumerate(self.button_dic.values()):
            bt.frame = (0, y_off + index * (self.button_height + 10),
                        self.width, self.button_height)


def main():
    v = HomeView()
    v.present()


if __name__ == '__main__':
    main()
