from typing import Any, List
import unittest
import synthetic

class PromtTemplateTest (unittest.TestCase):
    def test_prompt_template_init_with_template_str_and_input_variables_and_saves_as_prop (self) :
        prompt_template = synthetic.PromptTemplate(
            template = "{query}",
            input_variables = ["query"]
        )
        
        self.assertIsInstance(prompt_template, synthetic.PromptTemplate)
        self.assertEqual(prompt_template.template, "{query}")
        self.assertListEqual(prompt_template.input_variables, ["query"])
        
    def test_promt_template_fails_to_init_if_template_does_not_contain_all_input_variables (self) :
        self.assertRaises(synthetic.PromptTemplateError, synthetic.PromptTemplate, template="some text", input_variables=["query"])
        
    def test_prompt_template_format_method_accepts_any_kwarg_in_input_variables_returns_str_and_raises_if_there_is_an_unexpected_input_or_one_missing (self) :
        prompt_template = synthetic.PromptTemplate(
            template = "{query} and {response}",
            input_variables = ["query", "response"]
        )
        
        result = prompt_template.format(query="query", response="response")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "query and response")
        
        self.assertRaises(synthetic.PromptTemplateError, prompt_template.format, query="query")

        result = prompt_template.format(query="query", response="response", other="other")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "query and response")
  
    def test_prompt_template_accepts_optional_components_list_at_init (self) :
        components = [ synthetic.Component ] 
      
        prompt_template = synthetic.PromptTemplate(
            template="<Component/>{query}", input_variables=["query"],
            components=components
        )
        
        self.assertIsInstance(prompt_template, synthetic.PromptTemplate)
        self.assertListEqual(prompt_template.components, components)
        
    def test_prompt_template_has_a_method_to_add_components (self) :
        prompt_template = synthetic.PromptTemplate(
            template="<Component/>{query}", input_variables=["query"],
            components=[ synthetic.Component ]
        )
        
        class MyComponent (synthetic.Component) :
            name = "MyComponent"
        
        prompt_template.add_components([ MyComponent ])
        self.assertListEqual(prompt_template.components, [ synthetic.Component, MyComponent ])
        
    def test_prompt_template_raises_prompt_template_error_component_conflict_if_two_components_have_the_same_name (self) :
        with self.assertRaises(synthetic.ComponentConflictError) :
            prompt_template = synthetic.PromptTemplate(template="{query}", input_variables=["query"], components=[synthetic.Component, synthetic.Component])
        
        prompt_template = synthetic.PromptTemplate(template="{query}", input_variables=["query"], components=[synthetic.Component])    
        with self.assertRaises(synthetic.ComponentConflictError) :
            prompt_template.add_components([synthetic.Component])
            
    def test_prompt_template_format_method_substitutes_signatures_by_the_component_format_output (self) :
        class MyComponent (synthetic.Component) :
            name="MyComponent"
            
            def format(self, **kwargs: Any) -> str:
                return "MyComponent"
            
        prompt_template = synthetic.PromptTemplate(template="<MyComponent/>", input_variables=[], components=[MyComponent])
        prompt = prompt_template.format()
        
        self.assertEqual(prompt, "MyComponent")
        
    def test_prompt_template_format_method_accepts_extra_keyword_arguments_and_pass_them_to_component_format (self) :
        class MyComponent (synthetic.Component) :
            name = "MyComponent"
            
            def format(self, name: str, **kwargs) -> str :
                return f"Hello {name}"
            
        prompt_template = synthetic.PromptTemplate(template="<MyComponent/>", input_variables=[], components=[MyComponent])
        prompt = prompt_template.format(name="Carlos")
        
        self.assertEqual(prompt, "Hello Carlos") 
        
    def test_prompt_template_format_method_raises_error_if_keyword_argument_from_a_component_not_passed (self) :
        class MyComponent (synthetic.Component) :
            name = "MyComponent"
            
            def format(self, name: str, **kwargs) -> str :
                return f"Hello {name}"
            
        prompt_template = synthetic.PromptTemplate(template="<MyComponent/>", input_variables=[], components=[MyComponent])
        self.assertRaises(synthetic.PromptTemplateError, prompt_template.format)
        
    def test_prompt_template_checks_all_components_are_static_and_raises_error_if_try_to_add_a_dynamic_component_to_it (self):
        class MyComponent (synthetic.Component) :
            name = "MyComponent"
            is_dynamic = True
            
        with self.assertRaises(synthetic.DynamicComponentInPromptTemplateError):
            synthetic.PromptTemplate(template="<MyComponent/>", input_variables=[], components=[MyComponent])
                  
    def test_prompt_template_imports_standard_components_used_in_the_template_if_use_the_default_tag_signature (self) :
        prompt_template = synthetic.PromptTemplate(
            template="<FunctionDescriptions/>",
            input_variables=[]
        )
        
        self.assertListEqual(prompt_template.components, [synthetic.components.FunctionDescriptions])
        
    def test_prompt_template_does_not_import_standard_components_if_a_component_with_the_same_name_is_already_being_used (self) :
        class MyComponent (synthetic.Component) :
            name = "FunctionDescriptions"
            def format(self, **kwargs: Any) -> str:
                return "Hello World!"
            
        prompt_template = synthetic.PromptTemplate(
            template="<FunctionDescriptions/>",
            input_variables=[],
            components=[MyComponent]
        )
        
        self.assertListEqual(prompt_template.components, [MyComponent])