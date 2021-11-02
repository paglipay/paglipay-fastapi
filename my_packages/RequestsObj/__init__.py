import requests
import uuid 
import json
import threading
import time

threading_process_data = {}
threads = []

def do_process(v_val, data, uuid_str):
    # print('RequestsObj:do_process:data: ', data)
    # print('RequestsObj:do_process:v_val: ', v_val)

    if 'extra_pass' in v_val:
        for ep in v_val["extra_pass"]:
            if ep in data:
                v_val[ep] = data[ep]
                if 'id' == ep:
                    uuid_str = data[ep]
    
    if 'FileObj' in data:
        # print('RequestsObj:FileObj: ', v_val["FileObj"])
        for fo in data["FileObj"]:
            v_val[fo] = data[fo]

    print('RequestsObj:do_process:v_val: ', v_val)

    v_val_ip = v_val['ip']
    if 'start' in v_val_ip:        
        v_val_ip = v_val['ip'] + '/' + uuid_str

    x = requests.post(
        v_val_ip, 
        json = v_val
    , verify=False)
    # print('RequestsObj: ', x.text)
    # data.update({uuid_str : json.loads(x.text)})
    data.update(json.loads(x.text))

class RequestsObj:
    def __init__(self, name, data={}):
        # print('RequestsObj!')
        self.name = name
        self.data = data
        self.data.update({self.name: []})

    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True
        elif str_config == 'open':
            data = self.data
            uuid_s = str(uuid.uuid1())

            thread = threading.Thread(target=do_process, args=(v_val, data, uuid_s, ))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            bol_config = False

        return bol_config

    def v_func(self, v_val):
        self.data[self.name].append(v_val)
        for t in threads:
            t.join()
        return True