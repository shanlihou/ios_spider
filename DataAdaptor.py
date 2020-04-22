import config
import downloader
import os
import controler
import const


class DataAdaptor(object):
    def __init__(self, owner):
        self.owner = owner
        self.files = []

    def change_page(self, isnext):
        pass

    def hate_current(self):
        pass

    def change_index(self, isnext):
        if isnext:
            self.index += 1
        else:
            self.index = self.index - 1 + self.nr_files

        self.index = self.index % self.nr_files
    
    def love_current(self):
        pass

    @property
    def index(self):
        return config.mcIns.get_config(self._config_index_key(), 0)

    @index.setter
    def index(self, value):
        config.mcIns.set_config(self._config_index_key(), value)

    def process_main_data(self, main):
        if not self.nr_files:
            return 
            
        main.data_process(self._get_code_data(), self.page, self.index)

    @property
    def nr_files(self):
        return len(self.files)
    
    def reset_data(self):
        pass

    def _config_index_key(self):
        pass

    def get_cur_img_path(self):
        if not self.nr_files:
            return ''

        if self.index < 0:
            self.index = 0
        elif self.index >= self.nr_files:
            self.index = self.nr_files - 1

        return self.files[self.index]

    def _get_code(self):
        filename = self.files[self.index]
        bname = os.path.basename(filename)
        code = bname.split('.')[0]
        return code

    def _get_code_data(self):
        return controler.get_data_by_code(self._get_code())


class DBDataAdaptor(DataAdaptor):
    def __init__(self, owner, adaptor_type):
        super(DBDataAdaptor, self).__init__(owner)
        self.adaptor_type = adaptor_type
        self.reset_data()
        self.page = 0
    
    def reset_data(self):
        code_state = const.CodeState.hate if self.adaptor_type == const.AdaptorType.hate else const.CodeState.love
        self.files = controler.get_paths_by_state(code_state)

    def _config_index_key(self):
        return 'hate_index' if self.adaptor_type == const.AdaptorType.hate else 'love_index'
        
    def hate_current(self):
        if self.adaptor_type == const.AdaptorType.love:
            if self.nr_files:
                self.files.pop(self.index)
            


class DirDataAdaptor(DataAdaptor):
    def __init__(self, owner, adaptor_type):
        super(DirDataAdaptor, self).__init__(owner)
        self.path = os.path.join(os.getcwd(), self.get_page_name())
        self._deal_dir_files()

    @property
    def page(self):
        return config.mcIns.get_config('view_page', 1)

    @page.setter
    def page(self, value):
        config.mcIns.set_config('view_page', value)

    def get_page_name(self):
        return downloader.get_page_name(self.page)

    def _config_index_key(self):
        return 'index'

    def _deal_dir_files(self):
        self.files = []
        for entry in sorted(os.listdir(self.path)):
            filename = self.path + '/' + entry
            if os.path.isfile(filename):
                if filename.find('.jpg') >= 0 or filename.find('.png') >= 0:
                    code = entry.split('.')[0]
                    if controler.get_state_by_code(code) == const.CodeState.hate:
                        continue

                    self.files.append(filename)

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

        self.path = os.path.join(os.getcwd(), self.get_page_name())
        self.index = 0
        self._deal_dir_files()

    def hate_current(self):
        if not self.nr_files:
            return

        self.files.pop(self.index)


AdaptorDict = {
    const.AdaptorType.dir: DirDataAdaptor,
    const.AdaptorType.love: DBDataAdaptor,
    const.AdaptorType.hate: DBDataAdaptor,
}


def get_adaptor(owner, adaptor_type):
    _class = AdaptorDict[adaptor_type]
    return _class(owner, adaptor_type)

