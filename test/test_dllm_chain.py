import unittest

from langchain.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate

from synthetic.llms import DynamicLLM
from synthetic.chains import DynamicLLMChain

class DynamicLLMChainTest (unittest.TestCase):
    def test_dllm_chain_can_be_created_from_dllm_and_prompt_template (self):
        prompt_template = PromptTemplate(input_variables=["input"], template="{input}")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        
        chain = DynamicLLMChain(dllm, prompt_template)
        
        self.assertIsInstance(chain, DynamicLLMChain)
        
    def test_dllm_chain_format_method_accepts_string_string_pairs_and_outputs_final_prompt (self):
        prompt_template = PromptTemplate(input_variables=["input", "output"], template="{input} -> {output}")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        out = chain.format(input="input", output="output")
        self.assertIsInstance(out, str)
        self.assertEqual(out, "input -> output")
        
    def test_dllm_chain_format_method_fails_if_one_input_var_is_missing (self) :
        prompt_template = PromptTemplate(input_variables=["input", "output"], template="{input} -> {output}")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        with self.assertRaises(KeyError) :
            chain.format(input="input")
            
    def test_dllm_chain_format_method_fails_if_one_extra_parameter_is_passed (self):
        prompt_template = PromptTemplate(input_variables=["input"], template="{input}")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        with self.assertRaises(KeyError) :
            chain.format(input="input", output="output")