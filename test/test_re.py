import unittest

import synthetic.re as re
import re as std_re

class SyntheticReGexTest(unittest.TestCase) :
    def test_re_module_has_function_compile_that_complies_valid_regex_expressions (self) :
        expression = "valid regex"
        pattern = re.compile(expression)
        self.assertIsInstance(pattern, re.Pattern)
        
    def test_re_compile_function_changes_key_notation_to_named_grup (self) :
        expression = "something {content} more"
        pattern = re.compile(expression)
        
        self.assertIsInstance(pattern, re.Pattern)
        self.assertEqual(pattern, std_re.compile(r"something (?P<content>(.*)) more"))
        
    def test_re_compile_function_accepts_format_requirements_for_key_values_as_a_pattern (self) :
        expression = "something {content} more"
        pattern = re.compile(expression, { "content": r"(\w*)" })
        
        self.assertIsInstance(pattern, re.Pattern)
        self.assertEqual(pattern, std_re.compile(r"something (?P<content>(\w*)) more"))
        
    def test_re_search_function_accepts_str_or_pattern_and_string_and_returns_extended_match_object (self) :
        expression = "something {content} more"
        pattern = re.compile(expression) 
        
        output = re.search(pattern, "something content more")
        self.assertIsInstance(output, re.Match)
        self.assertEqual(output["content"], "content")
        
    def test_re_search_works_if_multiple_groups_are_given (self) :
        expression = "one group: {one}, another group: {two} more content"
        pattern = re.compile(expression)
        
        output = re.search(pattern, "one group: one, another group: two more content")
        self.assertIsInstance(output, re.Match)
        self.assertEqual(output["one"], "one")
        self.assertEqual(output["two"], "two")