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
        
    def test_component_class_has_atr_is_dynamic_that_defaults_to_false_but_can_be_overwritten_when_creating_a_new_class (self) :
        self.assertFalse(synthetic.Component.is_dynamic)
        
        class NewComponent (synthetic.Component) :
            pass
        
        self.assertFalse(NewComponent.is_dynamic)
        
        class NewDynamicComponent (synthetic.Component) :
            is_dynamic = True
            
        self.assertTrue(NewDynamicComponent.is_dynamic)
        
    def test_default_function_descriptions_component_works_as_expected (self) :
        @synthetic.function(name="evaluate", description="evaluate an arithmetical expression.")
        def evaluate (string: str) -> str :
            return str(eval(string))
        
        @synthetic.function(name="hello", description="say hello to someone")
        def hello (string: str) -> str :
            return "Hello " + string
        
        inst = synthetic.components.FunctionDescriptions()
        self.assertIsInstance(inst, synthetic.components.FunctionDescriptions)
        
        output = inst.format(functions = [evaluate, hello])
        self.assertEqual(output, f"-{evaluate.name}: {evaluate.description}\n-{hello.name}: {hello.description}")
        
    def test_default_function_call_description_component_works_as_expected (self) :
        inst = synthetic.components.FunctionCallDescription()
        self.assertIsInstance(inst, synthetic.components.FunctionCallDescription)
        
        output = inst.format(signature = "[{name}({input})->{output}]")
        self.assertEqual(output, "[{name}({input})->{output}]")
        
        self.assertListEqual(synthetic.load_components(names=["FunctionCallDescription"]), [synthetic.components.FunctionCallDescription])