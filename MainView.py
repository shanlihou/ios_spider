import ui
import clipboard
import MyImageView
import const
import controler
import switchText
import config


class MainView(ui.View):
    def __init__(self, adaptor_type=const.AdaptorType.dir):
        self.adaptor_type = adaptor_type
        self.view_dic = {}
        self.button_dic = {}
        self.view_hight = 30
        self.add_view('code', 'code')
        self.add_view('name', 'name')
        self.add_view('actor', 'actor')
        self.add_view('page', 'page')
        self.add_view('index', 'index')
        self.add_button('prev')
        self.add_button('next')
        self.add_button('pprev')
        self.add_button('pnext')
        self.add_mag()
        self.add_seg()
        self.add_img_view()

    def slider_action(self, val):
        mag_str = self.mag_strs[val * 2]
        clipboard.set(mag_str)

    def add_action(self, sender):
        print(sender.name)
        if sender.name == 'next':
            self.img_v.change_index(True)
        elif sender.name == 'prev':
            self.img_v.change_index(False)
        elif sender.name == 'pprev':
            self.img_v.change_page(False)
        elif sender.name == 'pnext':
            self.img_v.change_page(True)

    def seg_action(self, sender):
        print(sender.selected_index)
        controler.change_state_by_code(
            self.view_dic['code'].text, sender.selected_index)

        if sender.selected_index == const.CodeState.hate:
            self.img_v.hate_current()
        elif sender.selected_index == const.CodeState.love:
            self.img_v.love_current()

    def add_seg(self):
        view = ui.SegmentedControl()
        view.name = 'seg'
        view.segments = ['none', 'normal', 'love', 'hate']
        view.action = self.seg_action
        print(view.selected_index)
        self.seg = view
        self.add_subview(view)

    def add_button(self, name):
        button = ui.Button()
        button.name = name
        button.title = name
        button.border_color = 'blue'
        button.border_width = 1
        button.corner_radius = 3
        button.action = self.add_action
        self.add_subview(button)
        self.button_dic[name] = button

    def data_process(self, data, page, index):
        key_list = ['code', 'name', 'actor']
        for key in key_list:
            self.view_dic[key].text = data[getattr(const.CodeIndex, key)]
            print(self.view_dic[key].text)

        mags = data[const.CodeIndex.magnet].split('\n')
        mags_size = [st for i, st in enumerate(mags) if i & 1]
        self.view_dic['page'].text = str(page)
        self.view_dic['index'].text = str(index)
        self.mag.set_text_list(mags_size)
        self.mag_strs = mags
        self.seg.selected_index = data[const.CodeIndex.state]

    def add_mag(self):
        mag = switchText.SwitchTextView()
        self.mag = mag
        self.add_subview(mag)
        mag.add_action(self.slider_action)

    def add_view(self, name, text):
        view = ui.TextView()
        view.text = text
        view.name = name
        self.add_subview(view)
        self.view_dic[name] = view
        
    def on_set_front(self):
        self.img_v.reset_data()

    def add_img_view(self):
        img_v = MyImageView.MyImageView(self.adaptor_type)
        self.add_subview(img_v)
        self.img_v = img_v
        img_v.set_owner(self)

    def layout(self):
        for index, view in enumerate(self.view_dic.values()):
            view.frame = (0, index * self.view_hight,
                          self.width, self.view_hight)

        y_off = self.view_hight * len(self.view_dic)
        img_height = self.height - y_off - self.view_hight * 5
        self.img_v.frame = (0, y_off, self.width, img_height)

        y_off = y_off + img_height
        self.seg.frame = (0, y_off, self.width, self.view_hight)

        y_off = y_off + self.view_hight
        self.mag.frame = (0, y_off, self.width, self.view_hight * 2)

        button_y_off = self.height - self.view_hight * 2
        button_width = 40
        self.button_dic['prev'].frame = (
            0, button_y_off, button_width, self.view_hight)
        self.button_dic['next'].frame = (
            self.width - button_width, button_y_off, button_width, self.view_hight)

        button_y_off = self.height - self.view_hight
        self.button_dic['pprev'].frame = (
            0, button_y_off, button_width, self.view_hight)
        self.button_dic['pnext'].frame = (
            self.width - button_width, button_y_off, button_width, self.view_hight)


if __name__ == '__main__':
    op = 0
    if op == 0:
        view = MainView()
        view.present('fullscreen')
    elif op == 1:
        config.mcIns.set_config('is_u', 1)
