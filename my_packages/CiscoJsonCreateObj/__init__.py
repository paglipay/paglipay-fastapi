import MyCiscoObjParse as MyCiscoObjParse
# import my_packages.CiscoJsonCreateObj.ExtendedAccessList as ExtendedAccessList
import re
# import pymongo
import json
import ipaddress
import copy

# myclient = pymongo.MongoClient("mongodb+srv://user1:Pa55w0rd@cluster0.ay0lz.mongodb.net/react-portfolio?retryWrites=true&w=majority")
# mydb = myclient["react-portfolio"]
# mycol = mydb["devices"]
# x = mycol.find_one()

class CiscoJsonCreateObj:
    def __init__(self, int_name, data={}):
        # print('__init_'+int_name)
        self.name = int_name
        self.bol = None
        self.data = {}
        self.global_data = data
        self.global_data.update({'networks':{'_list':[]}})
        # self.global_data[int_name] = self.data
        self.obj = None
        self.current_action = None
        self.result_dic = {}
        self.break_it_up = {} 

        self.self_data = {'id_list': []}
        self.devices = {}
        self.dev_to_int = {}

    def k_func(self, str_config, v_val):
        if str_config == 'True':
            bol_config = True
        elif str_config == 'False':
            bol_config = False
        elif str_config == 'open':
            print('open: ', v_val)
            self.obj = MyCiscoObjParse.MyCiscoObjParse(v_val, self.global_data)
            # print('self.obj.output_dic: ', self.obj.output_dic['hostname'])
            bol_config = False
        elif str_config == 'break_it_up':
            # print('break_it_up')
            self.break_it_up = v_val
            bol_config = False
        elif str_config == 'save_as':
            if '.json' in v_val:

                if self.data['hostname']['_list']:
                    # mydict = { "hostname": self.data['hostname']['_list'][0]}
                    # x = mycol.insert_one(mydict)
                    # key = {'key':'value'}
                    interfaces = []
                    for i in self.data['interface']['_list']:
                        int = {'id':i, 
                        'config': self.data['interface'][i]['config'],
                        'description': self.data['interface'][i]['description']['config'],
                        'ip address': self.data['interface'][i]['ip address']['config']
                        }
                        
                        l = i
                        j2 = self.data
                        ip_address_config = j2['interface'][l]['ip address']['config']
                        #print(ip_address_config)
                        if ip_address_config != '' and 'no ip address' not in ip_address_config:
                            # print('\n')
                            # print(j2['interface'][l]['interface']['config'])
                            # print(ip_address_config)
                            ip_address_long = ip_address_config.replace(' ip address ', '')
                            ip_address_arry = ip_address_long.split(' ')

                            if len(ip_address_arry) >= 2:
                                if ip_address_arry[0] != '':
                                    ip4 = ipaddress.IPv4Network((ip_address_arry[0], ip_address_arry[1]), strict=False)
                                    # print(ip4.prefixlen)
                                    # print(ip4.with_prefixlen)

                                    dev_temp = {'network_id': str(ip4.with_prefixlen)}
                                    int.update(dev_temp)
                                    j2['interface'][l].update(dev_temp)
                            else:
                                print('ip address issue: ', v_val)
                                print(j2['interface'][l]['interface']['config'])
                                print(ip_address_config)

                                dev_temp = {'network_id': ""}
                                int.update(dev_temp)
                                j2['interface'][l].update(dev_temp)

                        interfaces.append(int)
                    # data = {"hostname": self.data['hostname']['_list'][0], 'interface':interfaces};
                    # mycol.update(mydict, data, upsert=True);
                else:
                    print('NO HOSTNAME: ', v_val)

                out_file = open(v_val, 'w')
                json.dump(self.data, out_file, indent=2)
                out_file.close()
            
            # self.global_data[self.name]  = self.data
            self.global_data[v_val] = self.data
            # self.global_data[v_val] = copy.deepcopy(self.data)
            # self.global_data[v_val] = copy.copy(self.data)

            # nout_file = open('C:/Users/Paul Aglipay/Desktop/networks.json', 'w')
            # json.dump(self.global_data['networks'], nout_file, indent=2)
            # nout_file.close()
                
            bol_config = False
        else:
            self.current_action = str_config
            bol_config = True
        return bol_config

    def v_func(self, str_config):
        if str_config == 'break':
            bol_config = False
        else:
            # print('#' * 44 + 'SubstringLine:')
            if 'set' == self.current_action:
                self.set(str_config)
            elif 'get' == self.current_action:
                self.get(str_config)
            bol_config = True
        return bol_config

    def __str__(self):
        return self.name


    def set(self, str_config):
        try:
            print(str_config)
        except:
            print(str_config + ' Not Found')

    def get(self, str_config):
        self_obj = self.obj.output_dic

        out_dic = {}
        out_dic[str_config] = {}
        out_dic[str_config]['_list'] = []
        if 'interface' == str_config:
            out_dic[str_config].update({'acl_dic': {}}) 
            net_id = ''      
        for k, v in self_obj.items():
            if str_config == k[0:len(str_config)]:
                # print(k)
                # print(v)
                v_line = v.split('\n')
                out_dic[str_config][k] = {"config": v, "_list": v_line}                
                if str_config in self.break_it_up:
                    for b in self.break_it_up[str_config]:
                        v_arry = v.split('\n')
                        a_result = ''
                        b_result = []
                        for a in v_arry:
                            if b in a:
                                a_result += '\n'+a
                                b_result.append(a)

                                # if b == 'ip address':
                                #     print(b)
                        #out_dic[str_config][k].update({b: a_result[1:]})
                        #out_dic[str_config][k].update({b: a_result})

                        out_dic[str_config][k].update({b: {}})

                        out_dic[str_config][k][b].update({'config': a_result[1:]})
                        out_dic[str_config][k][b].update({'_list': b_result})

                        if str_config == 'interface':                            
                            # print(k, ':', out_dic[str_config][k][b])   
                                          
                            if  b == 'ip address':
                                ip_address_config = out_dic[str_config][k][b]['config'] 
                                if  ip_address_config != '' and 'no ip address' not in ip_address_config:  
                                    ip_address_long = ip_address_config.replace(' ip address ', '')
                                    ip_address_arry = ip_address_long.split(' ')
                                    if len(ip_address_arry) >= 2:
                                        # print('ip_address_arry: ', ip_address_arry)
                                        if ip_address_arry[0] != '':
                                            ip4 = ipaddress.IPv4Network((ip_address_arry[0], ip_address_arry[1]), strict=False)
                                            # print(ip4.prefixlen)
                                            # print(ip4.with_prefixlen)
                                            net_id = ip4.with_prefixlen
                                            out_dic[str_config][k].update({'network_id': ip4.with_prefixlen})
                                            if ip4.with_prefixlen not in self.global_data['networks']:
                                                self.global_data['networks']['_list'].append(ip4.with_prefixlen)
                                                self.global_data['networks'][ip4.with_prefixlen] = []
                                            self.global_data['networks'][ip4.with_prefixlen].append({'interface':k,'ip address':ip_address_long, 'hostname': self.data['hostname']['_list'][0]})
                                
                            elif b == 'ip access-group': 
                                # print(k, ':', out_dic[str_config][k][b])
                                interface_ag = out_dic[str_config][k][b]['_list']
                                # print(interface_ag)
                                for iag in interface_ag:
                                    # print(iag)
                                    iale = iag.replace(' ip access-group ', 'ip access-list extended ')

                                    iale_split = iale.split(' ')
                                    iale_direction = iale_split[-1]
                                    # print('iale_direction: ', iale_direction)
                                    iale_split = iale_split[:-1]
                                    used_acl = ' '.join(iale_split)
                                    # print(used_acl)
                                    out_dic[str_config][k].update({'acl_' + iale_direction: used_acl})
                                    if used_acl not in out_dic['interface']['acl_dic']:
                                        out_dic['interface']['acl_dic'][used_acl] = []
                                    out_dic['interface']['acl_dic'][used_acl].append({'network_id':net_id, 'interface':k, 'direction': iale_direction})

                    if str_config == 'ip access-list extended':
                        # print(k, ':', out_dic[str_config][k][b])    
                        # print(k, ':')    
                        # print(self.data['interface']['_list'])  
                        if k in  self.data['interface']['acl_dic']:
                            # print(self.data['interface']['acl_dic'][k])
                            out_dic[str_config][k].update({'interface_used': self.data['interface']['acl_dic'][k]})
                            for a in self.data['interface']['acl_dic'][k]:
                                # print(self.data['interface'][a['interface']])
                                self.data['interface'][a['interface']]['acl_' + a['direction']] = out_dic[str_config][k]['_list']

                                if 'network_id' in self.data['interface'][a['interface']]:
                                    for x2 in self.global_data['networks'][self.data['interface'][a['interface']]['network_id']]:
                                        if x2['hostname'] == self.data['hostname']['_list'][0] and x2['interface'] == self.data['interface'][a['interface']]['interface']['_list'][0]:
                                            x2.update({'acl_' + a['direction']: {'config': out_dic[str_config][k]['_list']}})

                                # self.global_data['networks'][self.data['interface'][a['interface']]['network_id']].update({'permit':self.global_data['networks']['_list']})

                        else:
                            # print(k, ' NOT USED')
                            out_dic[str_config][k].update({'interface_used': 'NOT USED'})

                out_dic[str_config]['_list'].append(k)

        self.data.update(out_dic)

        # x2.update({'acl_' + a['direction']: out_dic[str_config][k]['_list']})
        # temp_nets = []
        # for n in self.global_data['networks']['_list']:
        #     for n2 in self.global_data['networks'][n]:
        #         # print(out_dic[str_config][k]['_list'])
        #         eacl = ExtendedAccessList.ExtendedAccessList()
        #         eacl.parse_acl(out_dic[str_config][k]['_list'])
        #         # eacl.parse_acl(['ip access-list extended br_aux_mgmt_luskin_out_20180530', ' 10 remark Required for HSRP hello packets', ' 10 permit udp 224.0.0.0 0.255.255.255 172.18.160.0 0.0.1.255'])
        #         # print(eacl.get_text())
        #         test_text = 'remark TEST REMARK\npermit ip ' + n + ' 0.0.0.0 any'
        #         #test_text = 'permit ip 128.98.234.0/24 any eq 3389'

        #         output = eacl.acl_rebuild(test_text)
        #         # print('output:')
        #         # print(eacl.get_text())
        #         temp_nets.append({'hostname': n2['hostname'],'interface': n2['interface'],'ip address': n2['ip address'], 'status':eacl.get_text().split('\n')})
        #         # temp_nets.append({'hostname': self.global_data['networks'][n2]['hostname'], 'interface': self.global_data['networks'][n2]['interface']})

    def save_to_result_dic(self, elems, save_as):
        # print('save_to_dic')
        self.result_dic[save_as] = elems

