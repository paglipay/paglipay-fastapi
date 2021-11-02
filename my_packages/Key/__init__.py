class Key:
    def __init__(self, name, data={}):
        # print('Key!')
        self.name = name
        self.data = data
        self.data.update({self.name: []})

    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True

        return bol_config

    def v_func(self, v_val):
        print('v_func: ', v_val)
        self.data[self.name].append(v_val)
        return True