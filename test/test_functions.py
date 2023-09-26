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
    
    def test_function_describe_method_returns_correct_concadenation_of_name_and_description(self):
        func = Function(
            name="name",
            description="description",
            call=lambda x: x 
        )
        
        description = func.describe()
        
        self.assertIsInstance(description, str)
        self.assertEqual(description, "name: description")