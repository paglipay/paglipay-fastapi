
class MyCiscoObjParse:
    def __init__(self, file_path=None, data={}):
        # print('MyCiscoObjParse: file_path: ', file_path, data)
        self.output_dic = {}
        self.output_list = []
        self.config = ''
        self.data = data
        if file_path in self.data:
            f = self.data[file_path].split('\n')
            # del self.data[v_val]
        else:
            with open(file_path) as file:
                f = file.readlines()

        obj_dic = {}
        obj_name = ''
        obj_prop = ''

        for l in f:
            # print('l:' + l)
            self.config += '\n' + l
            if l != '' and  l[0] != ' ':
                obj_name = l.strip()
                obj_prop = obj_name
                # print('obj_name:' + obj_name)
                if obj_name != '':
                    self.output_list.append(obj_name)

            elif  l != '' and l[0] == ' ' and '!' != l[0]:
                obj_prop += '\n ' + l.strip()

            if obj_name != '':
                obj_dic[obj_name] = obj_prop

        self.output_dic = obj_dic
        # return obj_dic