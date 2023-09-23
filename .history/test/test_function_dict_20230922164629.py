import unittest

from synthetic.function import FunctionDict

class FunctionDictTest (unittest.TestCase):
    def test_functiondict_init_fails_if_no_input_or_output_keys_on_dict (self):
        dict = { "foo": "bar" }
        
        self.assertRaises(FunctionDict, ValueError, dict)

        
        