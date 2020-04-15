# -*- coding: utf-8 -*-
import pickle
HOOK_SET = {'max_page', 'save_page', 'view_page', 'index'}


class MyConfig(object):
    def __init__(self):
        try:
            self.config = pickle.load(open('myconfig', 'rb'))
        except Exception as e:
            self.config = {}
            
    def hook_name(self, key):
        if self.config.get('is_u', False) and key in HOOK_SET:
            return key + '_u'
        else:
            return key

    def set_config(self, key, value):
        key = self.hook_name(key)
        self.config[key] = value
        pickle.dump(self.config, open('myconfig', 'wb'))

    def get_config(self, key, default=None):
        key = self.hook_name(key)
        return self.config.get(key, default)


mcIns = MyConfig()
if __name__ == '__main__':
    #mcIns.set_config('save_page', 2)
    print(mcIns.config)
    #mcIns.set_config('test1', 1234)
