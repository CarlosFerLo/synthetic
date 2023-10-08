import unittest
import synthetic

class FunctionsTest (unittest.TestCase) :
    def test_function_can_be_init_with_name_description_and_function_call (self):
        func = synthetic.Function(
            name="name",
            description="description",
            func=lambda x: f"Hello {x}"
        )
        
        self.assertIsInstance(func, synthetic.Function)
        self.assertEqual(func.name, "name")
        self.assertEqual(func.description, "description")
        
    def test_function_decorator_inits_a_function (self):
        @synthetic.function(name="name", description="description")
        def func (input: str) -> str :
            return "Hello " + input
        
        self.assertIsInstance(func, synthetic.Function)
        self.assertEqual(func.name, "name")
        self.assertEqual(func.description, "description")