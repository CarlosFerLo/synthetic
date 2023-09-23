import unittest

from synthetic import pdstr

class PartialDynamicStringTest (unittest.TestCase) :
    def test_pdstr_can_be_init_from_base_head_body_str (self):
        string = "<HEAD></HEAD><START><END>"
        dstring = pdstr(string)
        
        self.assertIsInstance(dstring, pdstr)
        
    def test_dstr_fails_to_init_if_string_is_not_valid (self) :
        string = "Not valid"
        self.assertRaises(ValueError, pdstr, string)
        
    
    