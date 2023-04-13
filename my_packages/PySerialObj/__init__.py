import serial
import time
class PySerialObj:
    def __init__(self, int_name, data={}):
        print('__init_'+int_name)
        self.name = int_name
        self.app = None
        self.bol = None
        self.wait = 0
        self.data = data
        self.data.update({self.name: []})
        self.data['prompt_request'] = []
        self.data['sending'] = []
        self.current_line = 0

    def k_func(self, str_config, v_val):
        if str_config == 'True':
            bol_config = True
        elif str_config == 'wait':
            print('wait: ', v_val)
            self.wait = v_val
            print('self.wait: ', self.wait)
            bol_config = False

        elif str_config == 'open':
            self.ser = serial.Serial('COM3', 9600, timeout=0)
            bol_config = False
        else:
            bol_config = False
            
            if "checknot'" in str_config:
                str_config = str_config.replace("checknot'","")
                if str_config in ''.join(self.data[self.name][self.current_line:]) :
                    bol_config = False
                else:
                    bol_config = True

            elif "not'" in str_config:
                str_config = str_config.replace("not'","")
                if str_config in ''.join(self.data[self.name][self.current_line:]) :
                    bol_config = False
                else:
                    bol_config = True                
                self.current_line = len(self.data[self.name])

            elif "check'" in str_config:
                str_config = str_config.replace("check'","")
                if str_config in ''.join(self.data[self.name][self.current_line:]) :
                    bol_config = True 

            else:
                if str_config in ''.join(self.data[self.name][self.current_line:]) :
                    bol_config = True
                    self.current_line = len(self.data[self.name])

        return bol_config

    def v_func(self,str_config):
        if str_config == 'break':
            bol_config = False
        elif str_config == '{ESC}':
            # self.app.PuTTY.send_keystrokes('{ESC}')
            self.ser.write(str_config.replace('{ESC}'))
            bol_config = False
        else:
            # self.app.PuTTY.type_keys(str_config+'\r\n', with_spaces=True)
            # pyperclip.copy(str_config.replace('<newline>', '\r\n'))
            # self.app.PuTTY.type_keys('#', with_spaces=False)
            # pywinauto.mouse.click(button='right', coords=(100,100))
            # self.app.PuTTY.type_keys(''+'\r\n', with_spaces=True)
            
            self.ser.write(str_config.replace('<newline>', '\r\n'))

        
        send_rec = {"send": str_config}
        time.sleep(self.wait)
        
        while 1:
            try:                
                time.sleep(1)
                f_readlines = self.ser.readline()
                self.data[self.name].append(f_readlines)
                print(''.join(f_readlines))
                self.data[self.name] = f_readlines
                send_rec["recv"] = ''.join(self.data[self.name][self.current_line:])
                # self.current_line = len(f_readlines)
                self.data['sending'].append(send_rec)
            except self.ser.SerialTimeoutException:
                print('Data could not be read')
        
        # with open('C:\\Users\\Paul Aglipay\\Desktop\\putty-out.log') as f:
        #     f_readlines = f.readlines()
        #     print(''.join(f_readlines))
        #     self.data[self.name] = f_readlines
        #     send_rec["recv"] = ''.join(self.data[self.name][self.current_line:])
        #     # self.current_line = len(f_readlines)
        #     self.data['sending'].append(send_rec)
        bol_config = True

        # self.data = {"stuff": "juststuff"}
        return bol_config

if __name__ == "__main__":
    putty = PySerialObj('i')
    putty.k_func('open', 'COM3')