import ui
from TabbedView import TabbedView
import MainView
import const


if __name__ == '__main__':
    v = TabbedView()
    v.addtab(MainView.MainView())
    v.addtab(MainView.MainView(const.AdaptorType.love))
    v.addtab(MainView.MainView(const.AdaptorType.hate))
    v.focus_tab_by_index(0)
    v.present()
