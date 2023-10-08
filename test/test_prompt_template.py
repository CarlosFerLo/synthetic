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
        self.assertRaises(synthetic.PromptTemplateError, prompt_template.format, query="query", response="response", other="other")
        
        