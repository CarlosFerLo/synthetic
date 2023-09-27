import re

from synthetic.validators import ValidatorSet, Validator

def str_has_head_body_structure_test (string: str) -> bool :
    string = string.strip()
    head_body_structure = re.compile(r"^<HEAD>((.|\n)*)<\/HEAD>([\s\n]*)<START>((.|\n)*)<END>$", flags=re.M)
    
    if re.match(string=string, pattern=head_body_structure) : return True
    else:  return False
    
def str_has_no_function_calls_in_the_head_test (string: str) -> bool :
    head_content_extractor = re.compile(r"<HEAD>((.|\n)*)<\/HEAD>")
    content = head_content_extractor.match(string).group(1)
    
    has_function_call = re.compile(r"\[(\S*)\(((.|\n)*)\)->((.|\n)*)\]")
    return not has_function_call.search(content)

DSTR_DEFAULT_VALIDATOR_SET = ValidatorSet([
    Validator(test=str_has_head_body_structure_test),
    Validator(test=str_has_no_function_calls_in_the_head_test)
])