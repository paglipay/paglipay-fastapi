import json, yaml
import sys
# from tqdm import tqdm
class DTree:
    def __init__(self, config, name='', import_obj_instance={}, current_module_name=None, data={}):
        # print('DTree HERE!!!' + '#'*50)
        # print(name)
        self.name = name
        self.config = config
        self.import_obj_instance  = import_obj_instance
        self.current_module_name = current_module_name
        self.data = data
        self.bol = False
        sys.path.append('./my_packages')
        self.begin_process(self.config)

    def init_import_obj(self, module_name):
        # print('init_import_obj: ' + module_name)
        if module_name in self.import_obj_instance:
            self.current_module_name = module_name
        else:
            my_class = getattr(__import__(module_name), module_name)
            self.current_module_name = module_name
            self.import_obj_instance[self.current_module_name] = my_class(module_name, self.data)

    def begin_process(self, config):
        self.bol = self.process(config)

    def k_process(self, config, v_val):
        # print('k_process: ', config, v_val)
        if '.json' in config:
            return DTree(json.load(open(config)), config, self.import_obj_instance, self.current_module_name, self.data).bol
        elif '.yml' in config:
            return DTree(yaml.safe_load(open(config)), config, self.import_obj_instance, self.current_module_name, self.data).bol
        else:
            return self.import_obj_instance[self.current_module_name].k_func(config, v_val)

    def v_process(self, config):
        # print('v_process: ', config)
        if '.json' in config:
            if config in self.data:
                d = DTree(self.data[config], config, self.import_obj_instance, self.current_module_name, self.data)
            else:
                d = DTree(json.load(open(config)), config, self.import_obj_instance, self.current_module_name, self.data)
            return d.bol
        elif '.yml' in config:
            if config in self.data:
                d = DTree(self.data[config], config, self.import_obj_instance, self.current_module_name, self.data)
            else:
                d = DTree(yaml.safe_load(open(config)), config, self.import_obj_instance, self.current_module_name, self.data)
            return d.bol
        else:
            return self.import_obj_instance[self.current_module_name].v_func(config)

    def process(self, config):
        if isinstance(config, (list,)):
            for l in config:
                if self.process(l) == False:
                    pass
        elif isinstance(config, (dict,)):
            for k, v in config.items():
                if k == 'import':
                    self.init_import_obj(v)
                else:
                    if self.k_process(k, v):
                        return self.process(v)
        else:
            self.v_process(config)

