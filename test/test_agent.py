import unittest
import synthetic

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
