import unittest

from synthetic import dstr, pdstr, DynamicStringDict


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
        
    def test_dstr_fails_to_init_if_string_has_function_calls_in_head (self) :
        string = "<HEAD>[function(text)->result]</HEAD><START><END>"
        self.assertRaises(ValueError, dstr, string)
        
    def test_dstr_as_dict_returns_dstr_dict (self) :
        dstring = dstr("<HEAD></HEAD><START><END>") 
        self.assertIsInstance(dstring.as_dict(), DynamicStringDict)
        
    def test_dstr_as_dict_returns_correct_ids_for_head_and_body (self) :
        dstring = dstr("<HEAD></HEAD><START><END>") 
        dict = dstring.as_dict()
        
        self.assertEqual(dict.head.id, "head")
        self.assertEqual(dict.body.id, "body")
        
    def test_dstr_as_dict_returns_correct_content_for_head_and_body (self) :
        dstring = dstr("<HEAD>head content</HEAD><START>body content<END>") 
        dict = dstring.as_dict()
        
        self.assertEqual(dict.head.content, "head content")
        self.assertEqual(dict.body.content, "body content")
    
    def test_init_of_dstr_by_passing_pdstr (self) :
        pdstring = pdstr("<HEAD>head content</HEAD><START>body content<END>")
        dstring = dstr(pdstring=pdstring)
        
        self.assertIsInstance(dstring, dstr)
        
    def test_init_fails_if_passing_no_string_or_pdstr (self) :
        self.assertRaises(ValueError, dstr)
        
    def test_init_fails_if_passing_both_string_and_pdstr (self) :
        self.assertRaises(ValueError, dstr, "string", pdstr(""))
        
    