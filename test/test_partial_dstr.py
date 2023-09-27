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
        string1 = "<HEAD></HEAD><START>"
        string2 = "<HEAD>\ncontent</HEAD>"
        pdstring1 = pdstr(string1)
        pdstring2 = pdstr(string2)
        
        self.assertIsInstance(pdstring1, pdstr)
        self.assertIsInstance(pdstring2, pdstr)
        
    def test_pdstr_fails_to_init_if_string_contains_head_body_tags_with_wrong_order (self):
        string1 = "<HEAD><END></HEAD><START>"
        string2 = "<HEAD>content</HEAD><END>"
        string3 = "<HEAD>\n<START></HEAD>"
        
        self.assertRaises(ValueError, pdstr, string1)
        self.assertRaises(ValueError, pdstr, string2)
        self.assertRaises(ValueError, pdstr, string3)
        
    def test_pdstr_inits_with_eddited_string_if_string_has_nonwhitespace_characters_after_head (self):
        string = "<HEAD>content</HEAD> content "
        
        with self.assertWarns(Warning):
            pdstring = pdstr(string)
        
        self.assertEqual(pdstring.raw, "<HEAD>content</HEAD><START>")
        
        
    def test_pdstr_fails_to_init_if_string_has_nonwhitespace_characters_between_head_and_body (self):
        string1 = "<HEAD>content</HEAD> content <START> content"
        string2 = "<HEAD>content\n</HEAD> content <START>\n"
        
        with self.assertWarns(Warning):
            pdstring1 = pdstr(string1)
        
        with self.assertWarns(Warning):
            pdstring2 = pdstr(string2)
            
        self.assertEqual(pdstring1.raw, "<HEAD>content</HEAD><START> content")
        self.assertEqual(pdstring2.raw, "<HEAD>content\n</HEAD><START>\n")
        
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
    
    def test_pdstr_is_start_method_returns_true_if_is_in_body_and_false_otherwhise (self):
        pdstring1 = pdstr("  ")
        pdstring2 = pdstr("<HEAD>")
        
        self.assertTrue(pdstring1.is_start())
        self.assertFalse(pdstring2.is_start())
        
    def test_pdstr_is_middle_method_returns_true_if_is_in_body_and_false_otherwhise (self):
        pdstring1 = pdstr("<HEAD></HEAD>  ")
        pdstring2 = pdstr("<HEAD></HEAD>    <START><END>")
        
        self.assertTrue(pdstring1.is_middle())
        self.assertFalse(pdstring2.is_middle())
    
    def test_pdstr_is_end_method_returns_true_if_is_in_body_and_false_otherwhise (self):
        pdstring1 = pdstr("<HEAD></HEAD><START><END> ")
        pdstring2 = pdstr("<HEAD>")
        
        self.assertTrue(pdstring1.is_end())
        self.assertFalse(pdstring2.is_end())
    
    def test_pdstr_stop_sequences_method_returns_list_of_str (self) :
        pdstring = pdstr("<HEAD>Hello")
        
        stop = pdstring.stop_sequences()
        self.assertIsInstance(stop, list)
        if len(stop) > 0 : 
            self.assertIsInstance(stop[0], str)
            
    def test_dstr_stop_sequences_method_returns_desired_sequences_if_in_head (self) :
        sequences = [r"<\/HEAD>"]
        pdstring = pdstr("<HEAD>content")

        self.assertListEqual(pdstring.stop_sequences(), sequences)
        
    def test_dstr_stop_sequences_method_returns_desired_sequences_if_in_body (self) :
        sequences = [r"<END>", r"\)->"]
        pdstring = pdstr("<HEAD></HEAD><START> ")
        
        self.assertListEqual(pdstring.stop_sequences(), sequences)
        
    def test_dstr_stop_sequences_method_returns_desired_sequences_if_in_start (self) :
        sequences = ["<HEAD>"]
        pdstring = pdstr(" ")
        
        self.assertListEqual(pdstring.stop_sequences(), sequences)
        
    def test_dstr_stop_sequences_method_returns_desired_sequences_if_in_middle (self) :
        sequences = ["<START>"]
        pdstring = pdstr("<HEAD></HEAD> ")
        
        self.assertListEqual(pdstring.stop_sequences(), sequences)
        
    def test_pdstr_stop_sequences_method_returns_desired_sequences_if_in_end (self) :
        sequences = [""]
        pdstring = pdstr("<HEAD></HEAD><START><END> ")
        
        self.assertListEqual(pdstring.stop_sequences(), sequences)
        
    def test_pdstr_apped_method_changes_location_correcly (self) :
        pdstring1 = pdstr("  ")
        pdstring2 = pdstr("  ")
        string1 = "  "
        string2 = "<HEAD> content"
        string3 = "<HEAD></HEAD>"
        string4 = "<START> content"
        string5 = "content"
        string6 = "<END>     "
        
        pdstring1.append(string1)
        self.assertTrue(pdstring1.is_start())
        pdstring1.append(string2)
        self.assertTrue(pdstring1.is_head())
        pdstring2.append(string3)
        self.assertTrue(pdstring2.is_middle())
        pdstring2.append(string4)
        self.assertTrue(pdstring2.is_body())
        pdstring2.append(string5)
        self.assertTrue(pdstring2.is_body())
        pdstring2.append(string6)
        self.assertTrue(pdstring2.is_end())
        
    def test_pdstr_append_method_returns_new_state_inside_appending_result (self) :
        pdstring = pdstr("<HEAD>")
        string = "content</HEAD><START>"
        
        result = pdstring.append(string)
        self.assertIsInstance(result.state, DynamicState)
        
    def test_pdstr_state_identifies_when_a_function_call_is_made (self) :
        pdstring1 = pdstr("<HEAD></HEAD><START>[function(input)->")
        pdstring2 = pdstr("<HEAD></HEAD><START>content->")
        
        self.assertTrue(pdstring1.is_fcalling())
        self.assertFalse(pdstring2.is_fcalling())
        
    def test_pdstr_get_fcall_method_returns_name_input_str_tuple_if_is_fcalling_is_true (self):
        pdstring = pdstr("<HEAD></HEAD><START>[function(input)->")
        
        name, input = pdstring.get_fcall()
        
        self.assertIsInstance(name, str)
        self.assertIsInstance(input, str)
        
    def test_pdstr_get_fcall_method_fails_if_is_faclling_returns_false (self):
        pdstring1 = pdstr("<HEAD></HEAD><START>not a function call")
        pdstring2 = pdstr("<HEAD></HEAD><START>[function()->reuslt]")
        
        self.assertRaises(ValueError, pdstring1.get_fcall)
        self.assertRaises(ValueError, pdstring2.get_fcall)
        
    