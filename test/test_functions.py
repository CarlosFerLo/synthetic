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
        
    def test_function_callable_can_be_called_by_calling_the_fucntion_and_returns_str(self):
        func = Function(
            name="Sample",
            description="Sample function",
            call=lambda x: x + "World!"
        )
        
        output = func("Hello ")
        self.assertIsInstance(output, str)
    