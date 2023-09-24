import unittest

from synthetic import pdstr

class PartialDynamicStringTest (unittest.TestCase) :
    def test_pdstr_can_be_init_from_base_head_body_str (self) :
        string = "<HEAD></HEAD><START><END>"
        pdstring = pdstr(string)
        
        self.assertIsInstance(pdstring, pdstr)
        
    def test_pdstr_fails_to_init_if_string_is_not_valid (self) :
        string = "Not valid"
        self.assertRaises(ValueError, pdstr, string)
        
    
    def test_pdstr_can_be_init_if_string_has_partial_head_body_structure (self) :
        string = "<HEAD></HEAD><START>"
        pdstring = pdstr(string)
        
        self.assertIsInstance(pdstring, pdstr)
        
    def test_pdstr_fails_to_init_if_string_contains_head_body_tags_with_wrong_order (self):
        string = "<HEAD><END></HEAD><START>"
        pdstring = pdstr(string)
        
        self.assertIsInstance(pdstring, pdstr)
        
    def test_pdstr_saves_input_string_in_raw_prop_if_inits (self):
        string = "<HEAD>content</HEAD><START>content<END>"
        pdstring = pdstr(string)
        
        self.assertEqual(pdstring.raw, "<HEAD>content</HEAD><START>content<END>")