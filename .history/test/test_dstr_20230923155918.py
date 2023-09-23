import unittest

from synthetic import dstr

class DynamicStringTest (unittest.TestCase):
    def test_dstr_can_be_init_from_base_head_body_str (self) :
        string = "<HEAD></HEAD><START><END>"
        dstring = dstr(string)
        
        self.assertIsInstance(dstring, dstr)
        
    def test_dstr_fails_to_init_if_string_is_not_valid (self) :
        string = "Not valid"
        self.assertRaises(ValueError, dstr, string)