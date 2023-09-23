import unittest

from synthetic import dstr

class DynamicStringTest (unittest.TestCase):
    def test_dstr_can_be_init_from_base_head_body_str (self) :
        string = "<HEAD></HEAD><START><END>"
        dstring = dstr(string)
        
        self.assertIsInstance(dstring, dstr)