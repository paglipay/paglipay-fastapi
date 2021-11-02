from my_packages.JinjaObj import JinjaObj
from DTree import DTree
import json, yaml
import unittest   # The test framework

class Test_JinjaObj(unittest.TestCase):
    def test_k_func(self):
        k = JinjaObj('test_k_func', {})
        self.assertEqual(k.k_func('True', '3'), True)

    def test_v_func(self):
        k = JinjaObj('test_v_func', {})
        self.assertEqual(k.v_func('hi'), True)

    
    def test_Dtree(self):
        print('app.py HERE')
        flask_data = {}
        flask_process = {}
        import_obj_instance = {}
        json_file = 'my_packages/JinjaObj/json/_create_list.json'
        d = DTree(json.load(open(json_file)), name=json_file, import_obj_instance=import_obj_instance, data=flask_data)
        self.assertEqual(json.load(open('my_packages/JinjaObj/json/out.json')), d.data['my_packages/JinjaObj/json/data.json'])   
        self.assertEqual(yaml.safe_load(open('my_packages/JinjaObj/json/out.yml')), d.data['my_packages/JinjaObj/json/data.yml'])    
    
if __name__ == '__main__':
    unittest.main()
