import unittest 
import synthetic
import synthetic.re as re

class ComponentsTest (unittest.TestCase) :
    def setUp(self) -> None:
        super().setUp()
        synthetic.Component._reset_idx()
    
    def test_component_has_name_atr_at_init (self) :
        name = synthetic.Component.name
        
        self.assertIsInstance(name, str)
        self.assertEqual(name, "Component")
        
    def test_component_has_class_method_that_returns_signature (self) :
        signature = synthetic.Component.signature()
        
        self.assertIsInstance(signature, re.Pattern)
        self.assertEqual(signature, re.compile("<Component/>"))
        
    def test_component_can_be_init_and_id_changes_each_time (self) :
        comp1 = synthetic.Component()
        comp2 = synthetic.Component()
        
        self.assertEqual(comp1.id, "Component-1")
        self.assertEqual(comp2.id, "Component-2")
        
    def test_component_instance_of_the_main_class_raises_not_implemented_error_if_format_method_used (self) :
        comp1 = synthetic.Component()
        
        with self.assertRaises(NotImplementedError) :
            comp1.format()
            
    def test_component_instance_of_a_subclass_returns_str_and_accepts_kwargs_in_the_format_method (self) :
        class MyComponent(synthetic.Component) :
            def format (self, **kwargs) -> str :
                string = kwargs.get("string", None)
                
                return string
            
        comp1 = MyComponent()
        string = comp1.format(string="string")
        
        self.assertIsInstance(string, str)
        self.assertEqual(string, "string")
        