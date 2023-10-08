import unittest
import synthetic

class FakeLLMTest(unittest.TestCase) :
    def test_fake_llm_returns_desired_string_each_time (self) :
        llm = synthetic.llms.FakeLLM(
            responses=["response 1", "response 2"]
        )
        
        self.assertIsInstance(llm, synthetic.llms.FakeLLM)
        self.assertEqual(llm(""), "response 1")
        self.assertEqual(llm(""), "response 2")
        self.assertEqual(llm(""), "response 1")
        
    def test_fake_llm_call_takes_stop_sequences (self) :
        llm = synthetic.llms.FakeLLM(
            responses=["contains, more", "this is (another) posible example", "this one raises"]
        )
        
        response = llm("", stop=[r","])
        self.assertEqual(response, "contains,")
        
        response = llm("", stop=[r"\((.*)\)"])
        self.assertEqual(response, "this is (another)")
        
        self.assertRaises(synthetic.RegexError, llm, "", stop = [")->"])
        