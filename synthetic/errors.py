class Error (Exception) :
    """Base error class in synthetic"""
    
class RegexError (Error) :
    """ This error is raised if some regex expression fails to compile
    """
    
class PromptTemplateError (Error) :
    """ Base class for errors on Prompt Templates
    """