import paramiko
import time
import os, sys
import io
# import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]

# mydict = { "name": "John", "address": "Highway 37" }

# x = mycol.insert_one(mydict)

class ParamikoObj:
    def __init__(self, name, data={}):
        print('ParamikoObj!')
        self.name = name
        self.data = data
        self.data.update({self.name: ['START']})
        self.start_line = 0
        self.capture_dic = {}
        self.ready_prompt = ':~$'
        self.wait = 0
        self.capture_to_file = ''
        self.data['prompt_request'] = []
        self.data['sending'] = []

    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True
        elif str_config == 'False':
            bol_config = False
        elif str_config == 'kill':
            print('kill: ', v_val)
            bol_config = False
            # self.io.exec_command('\x11\x01')       
            # time.sleep(3)
            # self.io.exec_command('\x11')   
            # print('Ctl A')         
            # time.sleep(3)
            # self.io.send('\\')   
            # print('\\')            
            # time.sleep(3)
            # self.io.send('y')    
            # print('y')           
            # time.sleep(3)
            # self.io.send('exit\n')    
            # print('exit')           
            # time.sleep(3)
            # self.v_func('\\\ny\n')
            self.io.close()
        elif str_config == 'wait':
            print('wait: ', v_val)
            self.wait = v_val
            print('self.wait: ', self.wait)
            bol_config = False
        elif str_config == 'return':
            print('return')
            print(v_val)
            if v_val == 'True':
                b_val = True
            elif v_val == 'False':
                b_val = False
            else:
                if "not'" in v_val:
                    v_val = v_val.replace("not'", "")
                    b_val = False
                    try:
                        prop = getattr(self, v_val)
                        if prop == None:
                            b_val = True
                    except:
                        print('getattr error')
                else:
                    b_val = True
                    try:
                        prop = getattr(self, v_val)
                        if prop == None:
                            b_val = False
                    except:
                        print('getattr error')
            print(b_val)
            self.bol = b_val
            bol_config = False
        elif str_config == 'prompt':            
            bol_config = False
            print('prompt: ', v_val, self.data)
            self.data['prompt_request'].append(v_val)
            prompt_out = ''
            if v_val in self.data:
                print('prompt: ', v_val)
                waiting_count = 0
                while True:
                    if self.data[v_val]:
                        if self.data[v_val][0] == '':
                            del self.data[v_val][0]
                        elif self.data[v_val][0] != '':
                            prompt_out = self.data[v_val][0]
                            del self.data[v_val][0]
                            waiting_count = 0
                            break

                    time.sleep(1)
                    print('waiting for input: ' + v_val + 'count: ' + str(waiting_count))
                    if waiting_count > 60:
                        # sys.exit(-1)                        
                        self.data['prompt_request'].remove(v_val)
                        break
                    waiting_count += 1
            
            self.data['prompt_request'].remove(v_val)
            self.v_func(prompt_out)

        elif str_config == 'open':
            bol_config = False
            port = 22
            if 'port' in v_val:
                port = v_val['port']
            
            remote_conn_pre = paramiko.SSHClient()
            remote_conn_pre.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            # k = paramiko.RSAKey.from_private_key_file("./main-key.pem")

            # os.environ['RSA_KEY'] = open('main-key.pem', 'r')
            # print('os.environ.get("RSA_KEY"):', os.environ.get("RSA_KEY"))
            # rsa_out = os.environ.get("RSA_KEY")
            # k = paramiko.RSAKey.from_private_key(io.StringIO(str(rsa_out)))

            # remote_conn_pre.connect(v_val['ip'], username=v_val['username'], password=v_val['password'], pkey = k, port=port, look_for_keys=False,
            #                         allow_agent=False)
            remote_conn_pre.connect(v_val['ip'], username=v_val['username'], password=v_val['password'], port=port, look_for_keys=False,
                                    allow_agent=False)
            print("SSH connection established to %s" % v_val['ip'])

            self.io = remote_conn_pre.invoke_shell(width=5000, height=800)
            self.data[self.name].append('GO')
            self.io.send("\n\n") 


        elif 'capture_to_file' == str_config:
            self.capture_to_file = v_val

            if v_val not in self.capture_dic:
                self.capture_dic[v_val] = {}
                self.capture_dic[v_val]['capture_to_file'] = v_val
                self.capture_dic[v_val]['capture'] = ''
                self.capture_dic[v_val]['capture_to_file_out'] = ''

            bol_config = False
        elif 'capture' == str_config:
            self.capture = v_val
            self.capture_dic[self.capture_to_file]['capture'] = v_val

            bol_config = False
        else:            
            bol_config = False
            print('str_config: ' + str_config)
            print('current_output: ')
            print(self.data[self.name][-1])
            
            if "not'" in str_config:
                str_config = str_config.replace("not'","")
                # if str_config in self.data[self.name][-1].split('\n')[-1]:
                if str_config in self.data[self.name][-1]:
                    bol_config = False
                else:
                    bol_config = True
            else:
                # if str_config in self.data[self.name][-1].split('\n')[-1] :
                if str_config in self.data[self.name][-1] :
                    bol_config = True            
                    self.start_line = len(self.data[self.name]) 

        return bol_config

    def v_func(self, v_val):
        print('v_func: ' + v_val)
        # self.my_send_wait_recieve(v_val)
        # self.data[self.name].append({v_val:output})
        output = self.my_send_wait_recieve(v_val)
        #print('#' * 22 + 'Paramiko Substring outputFullArryOutput:')
        #print(output)
        self.capture_func(output)
        return True
    
    def my_send_wait_recieve(self, send_var=''):
        
        send_str = send_var+'\n'
        print('self.io.write:'+send_str)
        self.io.send(send_str)    
        print('time.sleep(self.wait): ', self.wait) 
        self_wait = self.wait  
        # if self_wait < 3:
        #     self_wait = 3

        time.sleep(self_wait)
        print('#' * 44 + "Sending:" + send_var)
        send_rec = {"send": send_var}

        # self.data['sending'].append(send_var)
        while_count = 0
        while True:       
            time.sleep(.5)
            while_count += 1
            print('while: ', while_count, flush=True)
            if self.io.recv_ready(): 
                self.data[self.name].append(self.io.recv(65535).decode())                
                # if ':~$' in self.data[self.name][-1] :
                while_count = 0
                if self.data[self.name][-1].split('\n')[-1].strip() != '':
                    break
            # else: 
            #     time.sleep(1)


            # if while_count > 15 or self.ready_prompt in self.data[self.name][-1] or 'logout' in self.data[self.name][-1]:
            if 'logout' in self.data[self.name][-1]:                
                print('while break')              
                # print('$'*22, self.data[self.name][-1])
                # print('~'*22, ':~$', ':~$' in self.data[self.name][-1])
                break
        
        # send_rec["recv"] = self.data[self.name][-1].split('\n')[-1]
        send_rec["recv"] = self.data[self.name][-1]
        self.data['sending'].append(send_rec)
        return send_rec["recv"]

    # def capture_func(self, str_val):
    #     for k, v in self.capture_dic.items():
    #         if self.capture_dic[k]['capture'] == "True":                
    #             if self.capture_dic[k]['capture_to_file_out'] == '':
    #                 self.capture_dic[k]['capture_to_file_out'] = str_val
    #             else:
    #                 self.capture_dic[k]['capture_to_file_out'] += '' + str_val
    #         elif self.capture_dic[k]['capture'] == "False" and self.capture_dic[k]['capture_to_file_out'] != '':
    #             clean_text = self.capture_dic[k]['capture_to_file_out']
    #             clean_text = clean_text.replace('visibility', '***')
    #             self.capture_dic[k]['capture_to_file_out'] = clean_text.replace('\r\n', '\n')
    #             # with open(self.capture_dic[k]['capture_to_file'], 'w') as out_f:
    #             #     out_f.write(self.capture_dic[k]['capture_to_file_out'])
    #             self.data[self.capture_dic[k]['capture_to_file']] = self.capture_dic[k]['capture_to_file_out']
    #             self.capture_dic[k]['capture_to_file_out'] = ''

    def capture_func(self, str_val):
        for k, v in self.capture_dic.items():
            if self.capture_dic[k]['capture'] == "True":
                if self.capture_dic[k]['capture_to_file_out'] == '':
                    self.capture_dic[k]['capture_to_file_out'] = str_val
                else:
                    self.capture_dic[k]['capture_to_file_out'] += '' + str_val

            elif self.capture_dic[k]['capture'] == "False" and self.capture_dic[k]['capture_to_file_out'] != '':

                ctf = str(self.capture_dic[k]['capture_to_file'])

                dArry = ctf.split('/')
                directory = ''
                for dn in range(0, len(dArry) - 1):
                    if directory == '':
                        directory = dArry[dn]
                    else:
                        directory += '//' + dArry[dn]

                # directory = dArry[0]+'//'+dArry[1]


                print('directory:')
                print(directory)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                clean_text = self.capture_dic[k]['capture_to_file_out']
                clean_text = clean_text.replace('visibility', '***')
                self.capture_dic[k]['capture_to_file_out'] = clean_text.replace('\r\n', '\n')

                with open(self.capture_dic[k]['capture_to_file'], 'w') as out_f:
                    out_f.write(self.capture_dic[k]['capture_to_file_out'])
                self.capture_dic[k]['capture_to_file_out'] = ''

