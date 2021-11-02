import ipaddress

import my_packages.CiscoJsonCreateObj.MyIpAddressFuncs as MyIpAddressFuncs

class ExtendedAccessList:
    def __init__(self, config=None):
        #print('ExtendedAccessList')
        self.EACL = ''
        self.remarks = {}
        self.remarks_list = []
        self.text = ''
        self.name = ''
        self.global_entry_dic = {}
        self.myfile = []
        self.log_match = {}
        self.status = {'existing':[], 'source':[]}
        self.net_sources = {}
        self.net_destinations = {}

    def open_parse_acl_get_text(self, path):
        ##print('open_parse_acl')
        # self.open(path)
        self.parse_acl(self.open(path))
        # #print(self.get_text())
        return self.get_text()

    def open(self, path):
        ##print('open')
        with open(path) as myfile:
            for l in myfile:
                # #print(l.strip())
                self.myfile.append(l.strip())

        return self.myfile

    def text_to_list(self,text):
        return text.split('\n')

    def parse_acl_text(self, text):
        self.parse_acl(self.text_to_list(text))

    def parse_acl(self, list):
        ##print('parse_acl')
        remark_name = ''
        for r in list:
            # #print(r.strip())
            r = r.strip()

            if 'ip access-list extended' in r:
                self.name = r
                ##print('self.name:'+self.name)
            elif 'remark' in r:
                if r in self.remarks:
                    #print('Already has remark: '+r)
                    remark_name = r
                else:
                    remark_name = r
                    ##print('remark_name: '+remark_name)
                    self.remarks[remark_name] = []
                    self.remarks_list.append(remark_name)

            elif ('permit' in r or 'deny' in r) and not 'remark' in r:
                #print(''+r)
                if remark_name == '':
                    remark_name = '!remark none'
                    self.remarks[remark_name] = []
                    self.remarks_list.append(remark_name)

                if r in self.global_entry_dic:
                    #print('')
                    self.log_match[r] = 'MATCH Existing!: '#+r+' - '+self.global_entry_dic[r.strip()]
                    self.status['existing'].append(r)
                    #print('MATCH ENTRY!')
                elif self.is_same_source(r, remark_name):
                    #print('self.is_same_source')
                    self.log_match[r] = 'MATCH SOURCE!: '#+r+' - '+self.global_entry_dic[r.strip()]
                    self.status['source'].append(r)
                    #print('MATCH SOURCE!')
                else:
                    self.global_entry_dic[r] = remark_name
                    dic  = self.parse_acl_entry(r, remark_name)
                    ##print(dic)
                    self.remarks[remark_name].append(dic)



    def is_same_source(self, conf, remark):
        # print('is_same_source:'+conf)
        new_dic = self.parse_acl_entry(conf, remark)
        for r in self.remarks_list:
            for e in self.remarks[r]:
                #print(e['source_ip'])
                #print(new_dic['source_ip'])
                if (e['source_ip'] == '0.0.0.0' or new_dic['source_ip'] == '0.0.0.0'):
                    #print('any source')
                    pass
                else:

                    # print(new_dic['source_ip'], " ", new_dic['source_mask'], e['source_ip'], " ", e['source_mask'])
                    new_dic_source_mask = new_dic['source_mask']
                    if new_dic_source_mask.split('.')[0] == '0':
                        new_dic_source_mask = MyIpAddressFuncs.myReverseMask(new_dic_source_mask)
                    
                    new_net = new_dic['source_ip'] + "/" + MyIpAddressFuncs.MaskToCidr(new_dic_source_mask)
                    e_net = e['source_ip'] + "/" + MyIpAddressFuncs.MaskToCidr(e['source_mask'])
                    if ipaddress.ip_network(new_net).subnet_of(ipaddress.ip_network(e_net)):
                        # print("subnet_of: ", new_net, e_net)
                        return True
                    # else:
                    #     print(new_net, e_net)

                    if e['source_ip'] == new_dic['source_ip']:
                        return True
                        
                # for k, v in e.items():
                #     temp_text_build += '\n' + k+':'+v

        return False

    def parse_acl_entry(self, entry_line, remark_name):
        #print('parse_acl_entry: '+entry_line)
        entry_line = entry_line.replace('any','0.0.0.0 255.255.255.255')
        entry_line = entry_line.replace('0.0.0.0/0', '0.0.0.0 255.255.255.255')
        entry_line_arry = entry_line.split(' ')
        col_cnt = 0
        startCol = 0
        last_col = 0
        action = ''
        source_port = ''

        for c in entry_line_arry:
            #print(c)
            if 'permit' in c:
                action = 'permit'
                startCol = col_cnt + 1
                break
            elif 'deny' in c:
                action = 'deny'
                startCol = col_cnt + 3
                break
            col_cnt += 1

        protocol = entry_line_arry[startCol]
        ##print('protocol:'+protocol)

        if entry_line_arry[startCol + 1] == "host":
            source_ip = entry_line_arry[startCol + 2]
            source_mask = '255.255.255.255'
        elif '/' in entry_line_arry[startCol + 1]:
            cidr_source = entry_line_arry[startCol + 1]
            my_ip = ipaddress.ip_interface(cidr_source)
            #source_arry=cidr_source.split('/')
            source_ip = str(my_ip.ip)
            source_mask = str(my_ip.netmask)
            #print('source:'+source_ip+' ~~~~ '+source_mask)
            source_mask = MyIpAddressFuncs.myReverseMask(source_mask)
            entry_line = entry_line.replace(cidr_source, source_ip + ' ' + source_mask)
            startCol = startCol - 1
        else:
            source_ip = entry_line_arry[startCol + 1]
            strMask = entry_line_arry[startCol + 2]
            source_mask = MyIpAddressFuncs.myReverseMask(strMask)

            CIDR_mask = MyIpAddressFuncs.MaskToCidr(source_mask)
            host4 = ipaddress.ip_interface(source_ip +'/'+ CIDR_mask)

            net_source = str(host4.network)
            ##print(net_source)
            if net_source in self.net_sources:
                self.net_sources[net_source] += '\n'+remark_name
            else:
                self.net_sources[net_source] = remark_name

        if entry_line_arry[startCol + 3] == "host":
            destination_ip = entry_line_arry[startCol + 4]
            destination_mask = '255.255.255.255'
        elif '/' in entry_line_arry[startCol + 3]:

            cidr_destination = entry_line_arry[startCol + 3]
            my_ip = ipaddress.ip_interface(cidr_destination)
            #source_arry=cidr_source.split('/')
            destination_ip = str(my_ip.ip)
            destination_mask = str(my_ip.netmask)
            #print('destination:'+destination_ip+' ~~~~ '+destination_mask)
            destination_mask = MyIpAddressFuncs.myReverseMask(destination_mask)
            entry_line = entry_line.replace(cidr_destination, destination_ip+' '+destination_mask)

        elif entry_line_arry[startCol + 3] == 'eq' or entry_line_arry[startCol + 3] == 'gt' or entry_line_arry[startCol + 3] == 'lt':
            source_port = entry_line_arry[startCol + 3] + ' ' + entry_line_arry[startCol + 4]
            destination_ip = entry_line_arry[startCol + 5]
            strMask = entry_line_arry[startCol + 6]
            destination_mask = MyIpAddressFuncs.myReverseMask(strMask)
            last_col = startCol + 6
        else:
            destination_ip = entry_line_arry[startCol + 3]
            strMask = entry_line_arry[startCol + 4]
            destination_mask = MyIpAddressFuncs.myReverseMask(strMask)
            last_col = startCol + 4

            CIDR_mask = MyIpAddressFuncs.MaskToCidr(destination_mask)
            host4 = ipaddress.ip_interface(destination_ip + '/' + CIDR_mask)

            net_destinations = str(host4.network)
            # #print(net_destinations)

            if destination_ip in self.net_destinations:
                self.net_destinations[net_destinations] += '\n'+remark_name
            else:
                self.net_destinations[net_destinations] = remark_name

        final_stuff = ''
        if len(entry_line_arry) > last_col:
            for f in range(last_col+1,len(entry_line_arry)):
                final_stuff += ' ' + entry_line_arry[f]

        dic = {'config':entry_line,
               'remark':remark_name,
               'action':action,
               'protocol':protocol,
               'source_ip':source_ip,
               'source_mask':source_mask,
               'source_port':source_port,
               'destination_ip': destination_ip,
               'destination_mask': destination_mask,
               'final_stuff':final_stuff,

               }
        return dic

    def get_text(self):
        ##print('getText')
        temp_text = 'ip access-list extended '+self.name

        final_text_arry = ['','']
        for r in self.remarks_list:
            # print(r)
            # print(self.remarks[r])

            sample_str = self.list_dic_to_string(self.remarks[r],'config')

            if '0.0.0.0 255.255.255.255 0.0.0.0 255.255.255.255' in sample_str:
                fta = 1
            else:
                fta = 0

            if len(self.remarks[r]) > 0:
                final_text_arry[fta] += '\n' + r
            for e in self.remarks[r]:
                # #print(e['config'])
                final_text_arry[fta] += '\n' + e['config']
                temp_text_build = ''
                for k, v in e.items():
                    temp_text_build += '\n' + k + ':' + v
                #final_text_arry[fta] += '\n' + temp_text_build

        final_text = temp_text + final_text_arry[0] + final_text_arry[1]
        return final_text.replace('0.0.0.0 255.255.255.255', 'any')

    def remove_remark(self):
        print('remove_remark')

    def test_ipaddress(self,ip_address):
        #print('test_ipaddress')
        addr4 = ipaddress.ip_network('192.0.2.1/32').compare_networks(ipaddress.ip_network('192.0.2.0/32'))
        return addr4

    def list_dic_to_string(self, list, key):
        temp_str = ''
        for l in list:
            temp_str += '\n'+l[key]
        return temp_str

    def acl_rebuild(self, acl2):
        #print('acl_rebuild')

        add_entry_list = self.text_to_list(acl2)
        self.parse_acl(add_entry_list)

        #temp_text = self.name
        #temp_footer_text = ''
        # final_text_arry = ['','']
        # for r in self.remarks_list:
        #     # #print(r)
        #     # #print(self.remarks[r])
        #
        #     sample_str = self.list_dic_to_string(self.remarks[r],'config')
        #
        #     if '0.0.0.0 255.255.255.255 0.0.0.0 255.255.255.255' in sample_str:
        #         fta = 1
        #     else:
        #         fta = 0
        #
        #     if len(self.remarks[r]) > 0:
        #         final_text_arry[fta] += '\n' + r
        #
        #     for e in self.remarks[r]:
        #         # #print(e['config'])
        #         final_text_arry[fta] += '\n' + e['config']
        #         temp_text_build = ''
        #         for k, v in e.items():
        #             temp_text_build += '\n' + k + ':' + v
        #         #final_text_arry[fta] += '\n' + temp_text_build
        #
        # final_text = final_text_arry[0] + final_text_arry[1]
        # return final_text.replace('0.0.0.0 255.255.255.255', 'any')




if __name__ == '__main__':

    myAclCheck = ExtendedAccessList()
    path = 'New Text Document2.txt'
    myAclCheck.name = 'Testing_Name'
    output = myAclCheck.open_parse_acl_get_text(path)
    #print(output)

    test_text = 'remark TEST REMARK\npermit ip 192.168.2.0/24 0.0.0.0 any'
    #test_text = 'permit ip 128.98.234.0/24 any eq 3389'

    myAclCheck.acl_rebuild(test_text)
    #print('output:')
    #print(myAclCheck.get_text())

    # final_text = ''
    # for r in myAclCheck.remarks_list:
    #
    #     for e in myAclCheck.remarks[r]:
    #         # #print(e['config'])
    #         final_text += '\n' + e['source_ip']
    #         temp_text_build = ''
    #         for k, v in e.items():
    #             temp_text_build += '\n' + k + ':' + v
    #
    # #print(final_text)
    # #print(temp_text_build)

    ##print(myAclCheck.net_sources)

    # #print('Source:')
    # source_net_result = ''
    # for k,v in myAclCheck.net_sources.items():
    #     ##print(k)
    #     source_net_result += ',\n'+k
    #     ##print(v)
    # #print(source_net_result)
    #
    # #print('Destinations:')
    # net_destinations_result = ''
    # for k, v in myAclCheck.net_destinations.items():
    #     ##print(k)
    #     net_destinations_result += ',\n'+k
    #     ##print(v)
    # #print(net_destinations_result)
