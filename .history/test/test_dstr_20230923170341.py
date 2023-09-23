import unittest

from synthetic import dstr, DynamicStringDict


class DynamicStringTest (unittest.TestCase):
    def test_dstr_can_be_init_from_base_head_body_str (self) :
        string = "<HEAD></HEAD><START><END>"
        dstring = dstr(string)
        
        self.assertIsInstance(dstring, dstr)
        
    def test_dstr_fails_to_init_if_string_is_not_valid (self) :
        string = "Not valid"
        self.assertRaises(ValueError, dstr, string)
        
    def test_dstr_fails_to_init_if_string_has_text_between_head_and_body (self) :
        string = "<HEAD></HEAD>text<START><END>"
        self.assertRaises(ValueError, dstr, string)
        
    def test_dstr_to_dict_returns_dstr_dict (self) :
        dstring = dstr("<HEAD></HEAD><START><END>") 
        self.assertIsInstance(dstring, DynamicStringDict)