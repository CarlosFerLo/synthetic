import unittest

from langchain.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate

from synthetic import dstr
from synthetic.llms import DynamicLLM
from synthetic.chains import DynamicLLMChain

class DynamicLLMChainTest (unittest.TestCase):
    def test_dllm_chain_can_be_created_from_dllm_and_prompt_template (self):
        prompt_template = PromptTemplate(input_variables=["input"], template="<HEAD>{input}</HEAD>")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        
        chain = DynamicLLMChain(dllm, prompt_template)
        
        self.assertIsInstance(chain, DynamicLLMChain)
        
    def test_dllm_chain_format_method_accepts_string_string_pairs_and_outputs_final_prompt (self):
        prompt_template = PromptTemplate(input_variables=["input", "output"], template="<HEAD>{input}</HEAD><START>{output}<END>")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        out = chain.format(input="input", output="output")
        self.assertIsInstance(out, str)
        self.assertEqual(out, "<HEAD>input</HEAD><START>output<END>")
        
    def test_dllm_chain_fails_to_init_if_prompt_template_template_is_not_a_valid_pdstr (self) :
        prompt_template = PromptTemplate(input_variables=["input"], template="{input}</HEAD>")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        
        self.assertRaises(ValueError, DynamicLLMChain, prompt_template, dllm)
        
    def test_dllm_chain_format_method_fails_if_one_input_var_is_missing (self) :
        prompt_template = PromptTemplate(input_variables=["input", "output"], template="<HEAD>{input}</HEAD><START>{output}<END>")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        with self.assertRaises(KeyError) :
            chain.format(input="input")
            
    def test_dllm_chain_format_method_fails_if_one_extra_parameter_is_passed (self):
        prompt_template = PromptTemplate(input_variables=["input"], template="<HEAD>{input}</HEAD>")
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        with self.assertRaises(KeyError) :
            chain.format(input="input", output="output")
            
    def test_dllm_chain_can_be_run_by_passing_correct_kwargs_and_returns_dstr (self):
        prompt_template = PromptTemplate(input_variables=["input"], template="<HEAD>{input}</HEAD><START>")
        llm = FakeListLLM(responses=["output<END>"])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        output = chain.run(input = "input")
        
        self.assertIsInstance(output, dstr)
        self.assertEqual(output.raw, "<HEAD>input</HEAD><START>output<END>")
        
    def test_dllm_chain_fails_if_format_fails (self):
        prompt_template = PromptTemplate(input_variables=["input"], template="<HEAD>{input}</HEAD><START>")
        llm = FakeListLLM(responses=["output<END>"])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        with self.assertRaises(KeyError) :
            chain.run()
        with self.assertRaises(KeyError) :
            chain.run(input="input", output="output")
    
    def test_dllm_chain_fails_to_run_if_format_does_not_validate (self):
        prompt_template = PromptTemplate(input_variables=["input"], template="<HEAD>{input}</HEAD><START>")
        llm = FakeListLLM(responses=["output<END>"])
        dllm = DynamicLLM(llm=llm)
        chain = DynamicLLMChain(dllm, prompt_template)
        
        with self.assertRaises(ValueError) :
            chain.run(input="<END>")