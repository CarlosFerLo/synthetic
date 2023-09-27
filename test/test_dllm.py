import unittest

from langchain.llms import FakeListLLM

from synthetic import pdstr, dstr, AppendResultCode
from synthetic.llms import DynamicLLM, GenerationError
from synthetic.functions import Function

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
        llm = FakeListLLM(responses=["content</HEAD>", "content<END>"])
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
        
    def test_dynamic_llm_appends_head_start_tag_to_pdstr_if_state_location_is_start_after_generation (self) :
        llm = FakeListLLM(responses=["","content", "</HEAD><START><END>"])
        dllm = DynamicLLM(llm=llm, prefix="prefix")
        
        # If no <HEAD> tag was appended this run would fail
        result = dllm(pdstr("   "))
        self.assertIsInstance(result, dstr)
        
    def test_dynamic_llm_appends_body_start_tag_to_pdstr_if_state_location_is_middle_after_generation (self) :
        llm = FakeListLLM(responses=["","content", "<END>"])
        dllm = DynamicLLM(llm=llm, prefix="prefix")
        
        # If no <HEAD> tag was appended this run would fail
        result = dllm(pdstr("<HEAD>content</HEAD>"))
        self.assertIsInstance(result, dstr)
        
    def test_dynamic_llm_init_accepts_list_of_functions_and_saves_it_in_functions (self) :
        llm = FakeListLLM(responses=[""])
        functions = [
            Function(
                name="function",
                description="description",
                call=lambda x: x
            )
        ]
        
        dllm = DynamicLLM(llm=llm, functions=functions)
        
        self.assertIsInstance(dllm, DynamicLLM)
        self.assertListEqual(dllm.functions, functions)
        
    def test_dynamic_llm_calls_a_function_if_is_fcalling_returns_true_and_name_matches_and_appends_result (self):
        llm = FakeListLLM(responses=["[function(Hello World)->","<END>"])
        functions = [
            Function(
                name="function",
                description="description",
                call=lambda x: x
            )
        ]
        dllm = DynamicLLM(llm=llm, functions=functions)
        
        dstring = dllm(pdstr("<HEAD></HEAD><START>"))
        self.assertEqual(dstring.raw, "<HEAD></HEAD><START>[function(Hello World)->Hello World]<END>")
        
    def test_dynamic_llm_adds_function_names_and_descriptions_to_prefix_if_describe_functions_is_true (self):
        llm = FakeListLLM(responses=["[function(Hello World)->","<END>"])
        functions = [
            Function(
                name="function",
                description="description",
                call=lambda x: x
            )
        ]
        dllm = DynamicLLM(llm=llm, functions=functions, prefix="", describe_functions=True)
        prompt = dllm.build_prompt("")
        
        self.assertEqual(prompt, "function: description")
        
    def test_dynamic_llm_does_not_add_function_description_if_specified_at_init (self) :
        llm = FakeListLLM(responses=["[function(Hello World)->","<END>"])
        functions = [
            Function(
                name="function",
                description="description",
                call=lambda x: x
            )
        ]
        dllm = DynamicLLM(llm=llm, functions=functions, prefix="", describe_functions=False)
        prompt = dllm.build_prompt("")
        
        self.assertEqual(prompt, "")
        
    def test_dynamic_llm_accepts_sufix_when_init (self) :
        llm = FakeListLLM(responses=[""])
        dllm = DynamicLLM(llm=llm, sufix="sufix")
        
        self.assertIsInstance(dllm, DynamicLLM)
        
    def test_dynamic_llm_build_prompt_appends_sufix_just_before_prompt (self):
        llm = FakeListLLM(responses=[""])
        functions = [Function(name="function", description="description", call=lambda x: x)]
        dllm = DynamicLLM(llm=llm, sufix="sufix", functions=functions, prefix="prefix")
        
        prompt = dllm.build_prompt("prompt")
        self.assertEqual(prompt, "prefixfunction: descriptionsufixprompt")