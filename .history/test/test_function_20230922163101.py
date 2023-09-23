import unittest

from synthetic.function import Function, FunctionDict

class FunctionTest (unittest.TestCase):
    def test_function_init_with_name_description_inference (self) :
        def test_inference (input: FunctionDict) -> FunctionDict :
            return input
        
        func = Function(
            name="Sample",
            description="Sample description",
            inference=test_inference
        )
        
        self.assertIsInstance(func, Function)