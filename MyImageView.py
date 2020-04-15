# coding: utf-8

import ui
import os
import sys
import controler
import const
import config
import downloader
import switchText
import clipboard


class SelectType (object):
    love = 0
    hate = 1

class MyImageView(ui.View):
    def __init__(self):
        self.root = os.path.expanduser('~')
        self.rootlen = len(self.root)
        self.page = config.mcIns.get_config('view_page', 1)
        config.mcIns.set_config('view_page', self.page)
        page_name = downloader.get_page_name(self.page)
        self.path = os.path.join(os.getcwd(), page_name)
        # self.path = os.getcwd()
        self.root = self.path[self.rootlen:]
        self.color = 'white'
        self.x_off = 0
        self.y_off = 0
        self.scr_height = None
        self.scr_width = None
        self.scr_cor = 2.0
        self.ratio = 1.0
        self.index = config.mcIns.get_config('index', 0)

        self.deal_dir_files()
        print('files = ' + str(self.nr_files))
        if self.nr_files > 0:
            self.deal_img()
        else:
            print('Sorry, no images in this directory.')
            sys.exit()
    
    def set_index(self, index):
        self.index = index
        config.mcIns.set_config('index', index)

    def deal_dir_files(self):
        self.files = []
        for entry in sorted(os.listdir(self.path)):
            filename = self.path + '/' + entry
            if os.path.isfile(filename):
                if filename.find('.jpg') >= 0 or filename.find('.png') >= 0:
                    self.files.append(filename)
        self.nr_files = len(self.files)

    def set_owner(self, owner):
        self.owner = owner
        self.owner.data_process(self.get_code_data(), self.page, self.index)

    def get_code(self):
        filename = self.files[self.index]
        bname = os.path.basename(filename)
        code = bname.split('.')[0]
        return code

    def get_code_data(self):
        return controler.get_data_by_code(self.get_code())

    def draw(self):
        self.scr_height = self.height
        self.scr_width = self.width
        path = ui.Path.rect(0, 0, self.scr_width, self.scr_height)
        ui.set_color(self.color)
        path.fill()
        self.x_off = (self.scr_width - (self.img_width *
                                        self.ratio / self.scr_cor)) / 2
        # self.y_off = (self.scr_height - (self.img_height*self.ratio/self.scr_cor)) / 2
        self.y_off = 0
        self.img.draw(self.x_off, self.y_off, self.img_width * self.ratio /
                      self.scr_cor, self.img_height * self.ratio / self.scr_cor)

    def change_page(self, isnext):
        max_page = config.mcIns.get_config('max_page', 1)
        if isnext:
            self.page += 1
            if self.page > max_page:
                self.page = max_page
                return
        else:
            self.page -= 1
            if self.page < 1:
                self.page = 1
                return

        config.mcIns.set_config('view_page', self.page)
        page_name = downloader.get_page_name(self.page)
        self.path = os.path.join(os.getcwd(), page_name)
        self.root = self.path[self.rootlen:]
        self.index = 0
        config.mcIns.set_config('index', self.index)
        self.deal_dir_files()
        self.deal_img()
        self.owner.data_process(self.get_code_data(), self.page, self.index)
        self.layout()
        self.set_needs_display()

    def change_index(self, isnext):
        if isnext:
            self.index += 1
        else:
            self.index = self.index - 1 + self.nr_files

        self.set_index(self.index % self.nr_files)
        self.deal_img()
        self.owner.data_process(self.get_code_data(), self.page, self.index)
        self.layout()
        self.set_needs_display()

    def deal_img(self):
        if self.index < 0:
            self.set_index(0)
        elif self.index >= self.nr_files:
            self.set_index(self.nr_files - 1)
            
        self.img = ui.Image.named(self.files[self.index])
        self.img_width, self.img_height = self.img.size
        self.name = self.root + '/' + self.files[self.index]

    def layout(self):
        scr_height_real = self.height * self.scr_cor
        scr_width_real = self.width * self.scr_cor
        y_ratio = scr_height_real / self.img_height
        x_ratio = scr_width_real / self.img_width
        # 1.0 = okay, <1.0 = Image to small, >1.0 = Image to big
        if x_ratio == 1.0 and y_ratio == 1.0:
            self.ratio = 1.0  # perfect size
        elif x_ratio == 1.0 and y_ratio > 1.0:
            self.ratio = 1.0  # perfect width
        elif x_ratio > 1.0 and y_ratio == 1.0:
            self.ratio = 1.0  # perfect height
        elif x_ratio > 1.0 and y_ratio > 1.0:
            self.ratio = 1.0  # show image in original size
        elif x_ratio >= 1.0 and y_ratio < 1.0:
            self.ratio = y_ratio  # shrink height
        elif x_ratio < 1.0 and y_ratio >= 1.0:
            self.ratio = x_ratio  # shrink width
        elif x_ratio < 1.0 and y_ratio < 1.0:
            if x_ratio < y_ratio:  # which side?
                self.ratio = x_ratio
            else:
                self.ratio = y_ratio
        else:
            print('This should never happen. :(')


class MainView(ui.View):
    def __init__(self):
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
        if sender.selected_index == SelectType.hate:
            pass
            
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
        self.seg.selected_index = -1
    
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

    def add_img_view(self):
        img_v = MyImageView()
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
