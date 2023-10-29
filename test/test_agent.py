import unittest
from typing import List

import synthetic
import synthetic.re as re

class AgentsTest (unittest.TestCase) :
    def test_agent_init_with_llm_prompt_template_and_functions (self) :
        llm = synthetic.llms.FakeLLM(responses=[""])
        prompt_template = synthetic.PromptTemplate(template="{query}", input_variables=["query"])

        agent = synthetic.Agent(
            llm=llm, prompt_template=prompt_template
        )
        
        self.assertIsInstance(agent, synthetic.Agent)
        self.assertEqual(agent.llm, llm)
        self.assertEqual(agent.prompt_template, prompt_template)
        
    def test_agent_init_with_optional_functions_parameter (self) :
        llm = synthetic.llms.FakeLLM(responses=[""])
        prompt_template = synthetic.PromptTemplate(template="{query}", input_variables=["query"])
        
        @synthetic.function(name="name", description="description")
        def func (input: str) -> str :
            return "Hello " + input
        
        agent = synthetic.Agent(llm=llm, prompt_template=prompt_template, functions=[func])
        
        self.assertIsInstance(agent, synthetic.Agent)
        self.assertListEqual(agent.functions, [func])

    def test_agent_init_with_optional_function_signature_parameter (self) :
        llm = synthetic.llms.FakeLLM(responses=[""])
        prompt_template =  synthetic.PromptTemplate(template="{query}", input_variables=["query"])
        
        agent = synthetic.Agent(llm=llm, prompt_template=prompt_template,
                                signature="[{name}({input}){output}]")
        
        self.assertIsInstance(agent, synthetic.Agent)
        self.assertEqual(agent.signature, "[{name}({input}){output}]")
        
    def test_agent_validates_signature (self) :
        llm = synthetic.llms.FakeLLM(responses=[""])
        prompt_template =  synthetic.PromptTemplate(template="{query}", input_variables=["query"])
        
        with self.assertRaises(synthetic.InvalidSignatureError):
            synthetic.Agent(llm=llm, prompt_template=prompt_template,
                            signature="[{name}]")
        with self.assertRaises(synthetic.InvalidSignatureError):
            synthetic.Agent(llm=llm, prompt_template=prompt_template,
                            signature="[{input}]")
        with self.assertRaises(synthetic.InvalidSignatureError):
            synthetic.Agent(llm=llm, prompt_template=prompt_template,
                            signature="[{output}]")
        with self.assertRaises(synthetic.InvalidSignatureError):
            synthetic.Agent(llm=llm, prompt_template=prompt_template,
                            signature="[{name}:{input}]")
        with self.assertRaises(synthetic.InvalidSignatureError):
            synthetic.Agent(llm=llm, prompt_template=prompt_template,
                            signature="[{name}:{output}]")
        with self.assertRaises(synthetic.InvalidSignatureError):
            synthetic.Agent(llm=llm, prompt_template=prompt_template,
                            signature="[{input}:{output}]")
            
    def test_agent_signature_gets_compiled_to_signature_pattern (self) :
        llm = synthetic.llms.FakeLLM(responses=[""])
        prompt_template =  synthetic.PromptTemplate(template="{query}", input_variables=["query"])
        signature = "Action: {name}\n" \
                    "Action Input: {input}\n" \
                    "Output: {output}\n"
                    
        agent = synthetic.Agent(llm, prompt_template, signature=signature)

        pattern = re._compile("Action: (?P<name>(\\S*))\nAction Input: (?P<input>(.*))\nOutput: (?P<output>(.*))\n") 
        
        self.assertIsInstance(agent.signature_pattern, re.Pattern)
        self.assertEqual(agent.signature_pattern, pattern)
         
    def test_agent_partial_sognature_pattern_gets_generated_and_compiled (self) :
        llm = synthetic.llms.FakeLLM(responses=[""])
        prompt_template =  synthetic.PromptTemplate(template="{query}", input_variables=["query"])
        signature = "Action: {name}\n" \
                    "Action Input: {input}\n" \
                    "Output: {output}\n" 
                    
        agent = synthetic.Agent(llm, prompt_template=prompt_template, signature=signature)
        pattern = re._compile("Action: (?P<name>(\\S*))\nAction Input: (?P<input>(.*))\nOutput: $", flags=re.M)
        
        self.assertEqual(agent.partial_signature, "Action: {name}\nAction Input: {input}\nOutput: ")
        self.assertIsInstance(agent.partial_signature_pattern, re.Pattern)
        self.assertEqual(agent.partial_signature_pattern, pattern)
        
    def test_agent_calls_function_with_function_signature (self) :
        llm = synthetic.llms.FakeLLM(responses=["[evaluate(1 + 1)->more things", "something"])
        prompt_template = synthetic.PromptTemplate(template="{query}", input_variables=["query"]) 
        
        @synthetic.function(name="evaluate", description="")
        def evaluate (a) :
            return str(eval(a))
        agent = synthetic.Agent(llm, prompt_template, functions=[evaluate])
        
        output = agent.call(query="add 1 + 1")
        
        self.assertIsInstance(output, synthetic.AgentOutput)
        self.assertEqual(output.generation, "[evaluate(1 + 1)->2]something")
        self.assertEqual(output.raw, "add 1 + 1[evaluate(1 + 1)->2]something")
    
    def test_agent_output_contains_function_calls_and_it_contains_a_function_call_data_structure (self) :
        llm = synthetic.llms.FakeLLM(responses=["[evaluate(1 + 1)->more things", "something"])
        prompt_template = synthetic.PromptTemplate(template="{query}", input_variables=["query"]) 
        
        @synthetic.function(name="evaluate", description="")
        def evaluate (a) :
            return str(eval(a))
        agent = synthetic.Agent(llm, prompt_template, functions=[evaluate])
        
        output = agent.call(query="add 1 + 1")
        
        self.assertIsInstance(output.function_calls[0], synthetic.FunctionCall)
        self.assertEqual(output.function_calls[0].name, "evaluate")
        self.assertEqual(output.function_calls[0].input, "1 + 1")
        self.assertEqual(output.function_calls[0].output, "2")
        
    def test_agent_can_be_init_with_optional_component_list_static_components_are_passed_to_the_prompt_template_and_dynamic_ones_stores_in_property (self) :
        llm = synthetic.llms.FakeLLM(responses=[])
        prompt_template = synthetic.PromptTemplate(template="<Component/>", input_variables=[])
        
        class DynamicComponent(synthetic.Component) :
            is_dynamic = True
            
        agent = synthetic.Agent(llm=llm, prompt_template=prompt_template, components=[synthetic.Component, DynamicComponent])
        
        self.assertIsInstance(agent, synthetic.Agent)
        self.assertListEqual(agent.components, [ DynamicComponent ])
        self.assertLessEqual(agent.prompt_template.components, [ synthetic.Component ])
        
    def test_agent_passes_all_its_properties_to_the_prompt_template_for_formatting (self) :
        llm = synthetic.llms.FakeLLM(responses=[""])
        prompt_template = synthetic.PromptTemplate(template="<MyComponent/>", input_variables=[])
        
        @synthetic.function(name="evaluate", description="")
        def evaluate (string: str) -> str :
            return str(eval(string))
        class MyComponent (synthetic.Component) :
            name="MyComponent"
            def format (self, **kwargs) -> str :
                functions: List[synthetic.Function] = kwargs.get("functions")
                return " ".join([ f.name for f in functions])
            
        agent = synthetic.Agent(llm=llm, prompt_template=prompt_template, functions=[evaluate], components=[MyComponent])
        
        output = agent.call()
        
        self.assertEqual(output.raw, "evaluate")
        