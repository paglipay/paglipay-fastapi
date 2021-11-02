from my_packages.Key import Key
import unittest   # The test framework

class Test_Key(unittest.TestCase):
    def test_k_func(self):
        k = Key('test_k_func', {})
        self.assertEqual(k.k_func('True', '3'), True)

    def test_v_func(self):
        k = Key('test_v_func', {})
        self.assertEqual(k.v_func('hi'), True)
