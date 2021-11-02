import json
import yaml
import jinja2
from jinja2 import Template
import sys
import os
import re
import time
import ast
#import Customobj


class JinjaObj:
    def __init__(self, int_name, data={}):
        # print('__init_'+int_name)
        # super().__init__(data)
        self.jinja_dic = []
        self.name = int_name
        self.json_config = []
        self.bol = None
        self.data = data
        self.out = ''
        self.key = None

    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True
        elif str_config == 'False':
            bol_config = False
        elif str_config == 'key':
            if 'key' in self.data:
                v_val = self.data['key']
            print('key')
            print(v_val)
            self.key = v_val
            bol_config = False
        elif str_config == 'value':
            if 'value' in self.data:
                v_val = self.data['value']
            print('value')
            print(v_val)

            self.jinja_dic.append({self.key[0]: v_val[0]})
            bol_config = False
        elif str_config == 'open':
            # print('open:'+v_val)
            if '.txt' in v_val:
                if v_val in self.data:                        
                    t = Template(self.data[v_val])
                else:          
                    folder_path = '../../'
                    env = jinja2.Environment(
                        loader=jinja2.PackageLoader(__name__,
                                                    folder_path))
                    t = env.get_template(v_val)

                if isinstance(self.jinja_dic, (list,)):
                    j_out = t.render(results=self.jinja_dic)
                else:
                    j_out = t.render(**self.jinja_dic)
                # print(j_out)
                j_out = j_out.replace('\n', '')
                # print(j_out)
                # self.json_config.append(j_out)
                j_out = ast.literal_eval(j_out)
                self.json_config.append(j_out)

            elif '.json' in v_val:
                # try:
                folder_path = '../../'
                env = jinja2.Environment(
                    loader=jinja2.PackageLoader(__name__,
                                                folder_path))
                t = env.get_template(v_val)
                if isinstance(self.jinja_dic, (list,)):
                    j_out = t.render(results=self.jinja_dic)
                else:
                    j_out = t.render(**self.jinja_dic)

                #j_out = t.render(results=self.jinja_dic)
                # print('j_out:')
                #Remove newline before eval
                j_out = j_out.replace('\n', '')
                j_out = j_out.replace('\\', '')
                # print(j_out)
                # self.json_config.append(j_out)
                j_out = ast.literal_eval(j_out)
                self.json_config.append(j_out)
            
            else:
                # try:
                folder_path = '../../'
                env = jinja2.Environment(
                    loader=jinja2.PackageLoader(__name__,
                                                folder_path))
                t = env.get_template(v_val)

                j_out = t.render(**self.jinja_dic)
                # print('j_out txt:')
                # print(j_out)
                self.out = j_out

                # except:
                #     print("Failed:" + v_val)
                #     # sys.exit(-1)

            bol_config = False

        elif str_config == 'list_dics':
            # print('list_dics:')

            if 'list_dics' in self.data:
                try:
                    print('list_dics')
                    # print(self.data['list_dics'])

                    list_dics_temp = []

                    regex = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

                    self_data_list_dics = list(
                        filter(lambda x2: True, self.data['list_dics']))

                    for ld in self_data_list_dics:
                        ld = ld.replace('\r\n', ',')
                        ld = ld.replace('\n', ',')
                        ld = ld.replace('\r', ',')
                        ld = ld.split(',')

                        for _ in ld:
                            if re.findall(regex, _):
                                prompt_out = _
                            else:
                                prompt_out = ''

                            if prompt_out != '':
                                list_dics_temp.append(prompt_out.strip())

                    if not list_dics_temp and re.findall(regex, self.data['list_dics']):
                        list_dics_temp.append(self.data['list_dics'])

                    j2 = list_dics_temp

                    # print(j2)
                    self.jinja_dic = j2
                    del self.data['list_dics']
                except:
                    print("Failed to open .txt file list_dics")
                    # sys.exit(-1)
            else:
                if '.json' in v_val:
                    if v_val in self.data:
                        self.jinja_dic = self.data[v_val]
                        # del self.data[v_val]
                    else:
                        try:
                            f = open(v_val)
                            j2 = json.load(f)
                            print(j2)
                            self.jinja_dic = j2
                            self.data[v_val] = j2
                        except:
                            print("Failed to open JSON file list_dics")
                            sys.exit(-1)
                elif '.txt' in v_val:
                    if v_val in self.data:
                        self.jinja_dic = self.data[v_val].splitlines()
                        # del self.data[v_val]

                    else:
                        try:
                            print('.txt')
                            j2 = open(v_val).read().splitlines()

                            # print(j2)
                            self.jinja_dic = j2
                        except:
                            print("Failed to open .txt file list_dics")
                            # sys.exit(-1)

            bol_config = False

        elif str_config == 'dics':
            if '.json' in v_val:
                try:
                    f = open(v_val)
                    j2 = json.load(f)
                    print(j2)
                except:
                    print("Failed to open JSON file dics")
                    sys.exit(-1)

                print(j2)
                self.jinja_dic = j2
            else:
                self.jinja_dic = v_val

            print('self.jinja_dic:', self.jinja_dic)

            bol_config = False

        elif str_config == 'save_as':
            # print('self.json_config')
            # print(self.json_config)
            if '.json' in v_val:
                self_json_config = self.json_config
                if len(self.json_config) == 1 and len(self.json_config[0]) > 0:
                    self_json_config = self.json_config[0]
                    
                if '.net.json' in v_val or 'out.json' in v_val:
                    directory = '/'.join(v_val.split('/')[:-1])
                    # print('directory:')
                    # print(directory)
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    out_file = open(v_val, 'w')

                    json.dump(self_json_config, out_file, indent=2)
                    out_file.close()

                self.data[v_val] = self_json_config
                if 'output' in self.data:
                    self.data['output'] = self.json_config

                self.json_config = []

            elif '.yaml' in v_val or '.yml' in v_val:

                self_json_config = self.json_config
                if len(self.json_config) == 1 and len(self.json_config[0]) > 0:
                    self_json_config = self.json_config[0]
                    
                directory = '/'.join(v_val.split('/')[:-1])
                # print('directory:')
                # print(directory)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                out_file = open(v_val, 'w')

                yaml.dump(self_json_config, out_file, indent=2)
                out_file.close()

                self.data[v_val] = self_json_config
                if 'output' in self.data:
                    self.data['output'] = self.json_config

                self.json_config = []

            else:
                print('print(self.out):')
                print(self.out)
                self_out = self.out.replace('\\', '')
                if '.net.txt' in v_val or 'out.txt' in v_val:
                    with open(v_val, 'w') as out_file:
                        out_file.write(self_out)
                        self.out = ''

                self.data[v_val] = self_out

            bol_config = False

        elif str_config == 'jsonfile_dic':
            dict = {"test": "etd"}
            try:
                f = open(v_val+"_dict.json", "w")
                f.write(str(dict))
                f.close()
            except:
                print("Failed to jsonfile_dic file:" + v_val)

            bol_config = False

        elif str_config == 'jsonfy_text':

            try:
                self.jsonfy_text(v_val)
            except:
                print("Failed to jsonfy_text file:" + v_val)

            bol_config = False

        elif str_config == 'insert':
            bol_config = self.json_insert(v_val)

        elif str_config == 'append':
            bol_config = self.json_append(v_val)

        elif str_config == 'dynamic_edit_list':
            #print('v_val:' + str(v_val))
            for ji, jl in enumerate(self.json_config):
                # print('ji:' + str(ji))
                # print('jl:' + str(jl))
                if ji in v_val:
                    # if isinstance(jl, (dict,)):
                    for dk, dv in self.json_config[ji].items():
                        #print(dk + ': ' + str(dv))
                        self.json_config[ji] = {"True": dv}
                else:
                    # if isinstance(jl, (dict,)):
                    for dk, dv in self.json_config[ji].items():
                        #print(dk + ': ' + str(dv))
                        self.json_config[ji] = {"False": dv}

            bol_config = False

        return bol_config

    def v_func(self, str_config):
        if str_config == 'break':
            bol_config = False
        else:
            if '.json' in str_config:
                try:
                    f = open(str_config)
                    j2 = json.load(f)
                    print(j2)
                except:
                    print("Failed to open JSON file1")
                    # sys.exit(-1)

                print(self.json_config)
                # return j2

            bol_config = True
        return bol_config

    def jsonfy_text(self, v_val):
        try:
            with open(v_val) as f:
                for l in f:
                    i = {"not')#": "./json/paramiko/wait_till_cisco.json"}
                    self.json_config.append(i)
                    l = l.strip()
                    i = {")#": l}
                    self.json_config.append(i)
        except:
            print("Failed to open file:" + v_val)

    def json_append(self, v_val):
        if '.json' in v_val:
            try:
                f = open(v_val)
                j2 = json.load(f)
                print(j2)
            except:
                print("Failed to open JSON file1")
                # sys.exit(-1)

            for i in j2:
                self.json_config.append(i)
            # print(self.json_config)
            bol_config = False
        else:
            bol_config = False

        return bol_config

    def json_insert(self, v_val):
        if '.json' in v_val:
            try:
                f = open(v_val)
                j2 = json.load(f)
                print(j2)
            except:
                print("Failed to open JSON file1")
                # sys.exit(-1)

            for i in j2:
                self.json_config.insert(1, i)

            print(self.json_config)
            bol_config = False
        else:
            bol_config = False

        return bol_config


if __name__ == "__main__":
    print('')
