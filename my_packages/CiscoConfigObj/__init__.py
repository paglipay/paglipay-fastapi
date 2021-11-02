import jinja2
from jinja2 import Template
import json

class CiscoConfigObj:
    def __init__(self, name, data={}):
        print('CiscoConfigObj: ')
        self.name = name
        self.data = data
        self.data.update({self.name: []})
        self.out = ''
        self.device = {}
        self.jinja_dic = {}
    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True
        elif str_config == 'open':
            if v_val in self.data:
                self.device = self.data[v_val]
            else:
                self.device = json.load(open(v_val))
        elif str_config == 'config':  
            folder_path = v_val['folder_path']
            # f = open(v_val)
            # j2 = json.load(open(v_val))

            for l in v_val['config_list']:
                # print(l)
                self.jinja_dic = json.load(open(folder_path + '/' + l + '.json'))
                
                for k, v in self.jinja_dic.items():
                    for obj_id in self.device[k]['_list']:
                        self.jinja_dic.update({k:self.device[k][obj_id]['config']})


                # print('self.jinja_dic: ', self.jinja_dic)
                env = jinja2.Environment(
                    loader=jinja2.PackageLoader(__name__, '../../'))
                t = env.get_template(folder_path + '/' + l + '.j2')

                j_out = t.render(**self.jinja_dic)
                self.out += j_out + '\n'
        elif str_config == 'save_as':
            if '.net.txt' in v_val or 'out.txt' in v_val:
                with open(v_val, 'w') as out_file:
                    out_file.write(self.out)
                    self.out = ''

            self.data[v_val] = self.out

        if str_config == 'True':
            bol_config = True

        return bol_config

    def v_func(self, v_val):
        print('v_func: ', v_val)
        self.data[self.name].append(v_val)
        return True