class Error (Exception) :
    """Base error class in synthetic"""
    
class RegexError (Error) :
    """ This error is raised if some regex expression fails to compile
    """
    
class PromptTemplateError (Error) :
    """ Base class for errors on Prompt Templates
    """
    
class ComponentConflictError (PromptTemplateError) :
    """ This error raises if try to add two components with the same name to a template
    """
    
class DynamicComponentInPromptTemplateError (PromptTemplateError) :
    """ This error raises if try to add a dynamic component to a PromptTemplate
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
    
class ComponentError (Error) :
    """ This is the base class for errors raised by the components module.
    """
    
class LoadComponentsError (ComponentError) :
    """ This is the base class for errors raised by the load_components function.
    """