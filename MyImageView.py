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
import controler
import DataAdaptor
import utils


class MyImageView(ui.View):
    def __init__(self, adaptor_type):
        # self.path = os.getcwd()
        self.color = 'white'
        self.x_off = 0
        self.y_off = 0
        self.scr_height = None
        self.scr_width = None
        self.scr_cor = 2.0
        self.ratio = 1.0
        self.img = None
        self.adaptor = DataAdaptor.get_adaptor(self, adaptor_type)

        # start here
        self.deal_img(True)

    def set_owner(self, owner):
        self.owner = owner
        self.process_owner_data()

    def draw(self):
        self.scr_height = self.height
        self.scr_width = self.width
        path = ui.Path.rect(0, 0, self.scr_width, self.scr_height)
        ui.set_color(self.color)
        path.fill()
        if not self.img:
            return
        self.x_off = (self.scr_width - (self.img_width *
                                        self.ratio / self.scr_cor)) / 2
        self.y_off = 0
        self.img.draw(self.x_off, self.y_off, self.img_width * self.ratio /
                      self.scr_cor, self.img_height * self.ratio / self.scr_cor)

    def reset_data(self):
        self.adaptor.reset_data()
        self.deal_img()

    def search_data(self, search_str):
        self.adaptor.search_data(search_str)
        self.deal_img()

    def change_page(self, isnext):
        self.adaptor.change_page(isnext)
        self.deal_img()

    def process_owner_data(self):
        self.adaptor.process_main_data(self.owner)

    def hate_current(self):
        self.adaptor.hate_current()
        self.deal_img()

    def love_current(self):
        self.adaptor.love_current()
        self.deal_img()

    def change_index(self, isnext):
        self.adaptor.change_index(isnext)
        self.deal_img()

    def deal_img(self, isInit=False):
        img_path = self.adaptor.get_cur_img_path()
        if not img_path:
            return
        img_path = utils.fix_path(img_path)
        print(img_path, os.path.exists(img_path))
        self.img = ui.Image.named(img_path)
        self.img_width, self.img_height = self.img.size
        if not isInit:
            self.process_owner_data()
            self.layout()
            self.set_needs_display()

    def touch_began(self, a):
        x = a.location[0]
        print(x)
        if x < self.width / 2:
            self.change_index(False)
        else:
            self.change_index(True)

    def layout(self):
        if not self.img:
            return

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
        
        #self.ratio = 0.01


if __name__ == '__main__':
    m = MyImageView(1)
    m.present()
