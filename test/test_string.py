import unittest

from synthetic.strings import String
from synthetic import AppendResult, AppendResultCode

class StringTest (unittest.TestCase) :
    def test_string_can_be_init_from_str (self) :
        string = String("Hello World!")
        
        self.assertIsInstance(string, String)
        
    def test_string_saves_input_str_in_raw_property (self) :
        string = String("Hello World!")
        
        self.assertIsInstance(string.raw, str)
        self.assertEqual(string.raw, "Hello World!")
        
    def test_add_magic_method_is_implemented_and_returns_append_result (self) :
        string = String("Hello ")
        result = string + "World!"
        
        self.assertIsInstance(result, AppendResult)
        
    def test_add_magic_method_appends_new_str_to_raw_and_returns_code_OK_if_validated (self) :
        string = String("Hello ")
        result = string + "World!"
        
        self.assertEqual(result.code, AppendResultCode.OK)
        self.assertEqual(string.raw, "Hello World!")
        
    