import unittest

from synthetic.functions import Function

class FunctionTest (unittest.TestCase) :
    def test_function_init_by_name_description_callable(self):
        func = Function(
            name="Sample",
            description="Sample function",
            call=lambda x: x + "World!"
        )
        
        self.assertIsInstance(func, Function)