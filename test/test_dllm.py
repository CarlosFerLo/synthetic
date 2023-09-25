import unittest

from langchain.llms import FakeListLLM

from synthetic import pdstr, dstr, AppendResultCode
from synthetic.llms import DynamicLLM, GenerationError

class DynamicLLMTest(unittest.TestCase) :
    def test_dynamic_llm_can_be_init_with_llm (self) :
        llm = FakeListLLM(responses=["example"])
        dllm = DynamicLLM(llm)
        
        self.assertIsInstance(dllm, DynamicLLM)
        
    def test_dynamic_llm_can_be_called_with_a_pdstr_and_returns_dstr (self) :
        llm = FakeListLLM(responses=["<START>content<END>"])
        dllm = DynamicLLM(llm)
        
        pdstring = pdstr("<HEAD>content</HEAD>")
        dstring = dllm(pdstring)
        
        self.assertIsInstance(dstring, dstr)
        self.assertEqual(dstring.raw, "<HEAD>content</HEAD>" + "<START>content<END>")
        
    def test_dynamic_llm_call_fails_if_does_not_complete_dstr_on_max_iter (self) :
        llm = FakeListLLM(responses=["content"])
        dllm = DynamicLLM(llm, max_iter=1)
        
        pdstring = pdstr("<HEAD>")
        self.assertRaises(GenerationError, dllm, pdstring)
        
    def test_dynamic_llm_call_fails_if_append_to_pdstr_returns_ERROR_code (self) :
        llm = FakeListLLM(responses=["<START><END>"])
        dllm = DynamicLLM(llm)
        
        pdstring1, pdstring2 = pdstr("<HEAD>"), pdstr("<HEAD>")
        
        self.assertEqual(pdstring1.append("<START><END>").code, AppendResultCode.ERROR)
        self.assertRaises(GenerationError, dllm, pdstring2)
        
    def test_dynamic_llm_can_handle_multiple_sequential_generation_calls_to_llm (self) :
        llm = FakeListLLM(responses=["content</HEAD>", "<START>content<END>"])
        dllm = DynamicLLM(llm)
        
        pdstring = pdstr("<HEAD>")
        dstring = dllm(pdstring)
        
        self.assertEqual(dstring.raw, "<HEAD>content</HEAD><START>content<END>")
        
    def test_dynamic_llm_init_accepts_prefix_to_prompt_for_generation (self) :
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm, prefix="prefix")
        
        self.assertIsInstance(dllm, DynamicLLM)
        
    def test_dynamic_llm_appends_prompt_to_prefix_with_build_prompt_method (self) :
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm, prefix="prefix")
        
        prompt = dllm.build_prompt("<HEAD>")
        self.assertIsInstance(prompt, str)
        self.assertEqual(prompt, "prefix<HEAD>")
        
    