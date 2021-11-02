from my_packages.RequestsObj import RequestsObj
import unittest   # The test framework

class Test_Key(unittest.TestCase):
    def test_k_func(self):
        k = RequestsObj('test_k_func', {})
        self.assertEqual(k.k_func('True', '3'), True)

    # def test_v_func(self):
    #     k = RequestsObj('test_v_func', {})
    #     self.assertEqual(k.v_func('hi'), True)

if __name__ == '__main__':
    unittest.main()