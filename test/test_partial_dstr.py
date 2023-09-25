import unittest

from synthetic import pdstr, AppendResult, AppendResultCode, DynamicState, Location

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
        string1 = "<HEAD><END></HEAD><START>"
        string2 = "<HEAD>content</HEAD><END>"
        
        self.assertRaises(ValueError, pdstr, string1)
        self.assertRaises(ValueError, pdstr, string2)
        
    def test_pdstr_fails_to_init_if_string_has_nonwhitespace_characters_after_head (self):
        string = "<HEAD>content</HEAD> content "
        
        self.assertRaises(ValueError, pdstr, string)
        
    def test_pdstr_fails_to_init_if_string_has_nonwhitespace_characters_between_head_and_body (self):
        string = "<HEAD>content</HEAD> content <START>"
        
        self.assertRaises(ValueError, pdstr, string)
        
    def test_pdstr_init_works_for_empty_str (self) :
        pdstring = pdstr("")
        
        self.assertIsInstance(pdstring, pdstr)
        
    def test_pdstr_init_works_for_whitespace_str (self) :
        pdstring = pdstr("  \n  ")
        
        self.assertIsInstance(pdstring, pdstr)
        
    def test_pdstr_saves_input_string_in_raw_prop_if_inits (self):
        string = "<HEAD>content</HEAD><START>content<END>"
        pdstring = pdstr(string)
        
        self.assertEqual(pdstring.raw, "<HEAD>content</HEAD><START>content<END>")
        
    def test_pdstr_append_method_adds_input_str_to_raw (self):
        string = "<HEAD>content</HEAD><START>"
        pdstring = pdstr(string)
        
        pdstring.append("content")
        
        self.assertEqual(pdstring.raw, "<HEAD>content</HEAD><START>content")
        
    def test_pdstr_append_method_returns_append_result (self):
        string = "<HEAD>content</HEAD><START>"
        pdstring = pdstr(string)
        
        output = pdstring.append("content")
        
        self.assertIsInstance(output, AppendResult)
        
    def test_pdstr_apped_method_returns_append_result_ok_if_succeeds (self):
        string = "<HEAD>content</HEAD><START>"
        pdstring = pdstr(string)
        
        output = pdstring.append("content")
        
        self.assertEqual(output.code, AppendResultCode.OK)
        
    def test_pdstr_append_method_returns_append_result_error_if_fails (self):
        string = "<HEAD>content</HEAD>"
        pdstring = pdstr(string)
        
        output = pdstring.append("<END>")
        
        self.assertEqual(output.code, AppendResultCode.ERROR)
        
    def test_pdstr_allows_no_function_calls_in_head (self):
        string1 = "<HEAD>[function(text)->response]"
        string2 = "<HEAD>[function(text)->resopnse]</HEAD>"
        
        self.assertRaises(ValueError, pdstr, string1)
        self.assertRaises(ValueError, pdstr, string2)
        
    def test_pdstr_allows_no_partial_function_calls_in_head (self) :
        string = "<HEAD>[function(text)"
        
        self.assertRaises(ValueError, pdstr, string)
        
    def test_pdstr_computes_state_when_init (self) :
        pdstring = pdstr("<HEAD> content")
        
        self.assertIsInstance(pdstring._state, DynamicState)
        
    def test_pdstr_computes_state_location_correcly (self):
        start = pdstr("")._state.location
        head = pdstr("<HEAD> ")._state.location
        middle = pdstr("<HEAD></HEAD>")._state.location
        body = pdstr("<HEAD>content</HEAD><START>content ")._state.location
        end = pdstr("<HEAD>content</HEAD><START>content<END>")._state.location
        
        self.assertEqual(start, Location.START)
        self.assertEqual(head, Location.HEAD)
        self.assertEqual(middle, Location.MIDDLE)
        self.assertEqual(body, Location.BODY)
        self.assertEqual(end, Location.END)
        
    def test_pdstr_is_head_method_returns_true_if_is_in_head_and_false_otherwhise (self):
        pdstring1 = pdstr("<HEAD> content")
        pdstring2 = pdstr("<HEAD></HEAD>")
        
        self.assertTrue(pdstring1.is_head())
        self.assertFalse(pdstring2.is_head())
        
    def test_pdstr_is_body_method_returns_true_if_is_in_body_and_false_otherwhise (self):
        pdstring1 = pdstr("<HEAD></HEAD><START>")
        pdstring2 = pdstr("<HEAD>")
        
        self.assertTrue(pdstring1.is_body())
        self.assertFalse(pdstring2.is_body())
    
    def test_pdstr_stop_sequences_method_returns_list_of_str (self) :
        pdstring = pdstr("<HEAD>Hello")
        
        stop = pdstring.stop_sequences()
        self.assertIsInstance(stop, list)
        if len(stop) > 0 : 
            self.assertIsInstance(stop[0], str)
            
    def test_dstr_stop_sequences_method_returns_desired_sequences_if_in_head (self) :
        sequences = ["</HEAD>"]
        pdstring = pdstr("<HEAD>content")
        
        self.assertTrue(pdstring.is_head())
        self.assertListEqual(pdstring.stop_sequences(), sequences)
        
    