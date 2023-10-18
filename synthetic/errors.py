class Error (Exception) :
    """Base error class in synthetic"""
    
class RegexError (Error) :
    """ This error is raised if some regex expression fails to compile
    """
    
class PromptTemplateError (Error) :
    """ Base class for errors on Prompt Templates
    """
    
class InvalidSignatureError (Error) :
    """ This error raises if the validations checks for a signature fail
    """
    
class GenerationError (Error) :
    """ This error raises when the LLM generation causes an irregularity on the working of the Agent.
    """
    
class InvalidFunctionNameError (GenerationError) :
    """ This error raises if the LLM tries to call a function that is not in the functions list of the Agent.
    """