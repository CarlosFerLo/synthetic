import re
from typing import List, Callable

def str_has_head_body_structure (string: str) -> bool :
    head_body_structure = re.compile(r"^<HEAD>(.*)</HEAD>(\s*)<START>(.*)<END>$")
    
    if re.match(string=string, pattern=head_body_structure) : return True
    else:  return False

def str_has_no_function_calls_in_the_head (string: str) -> bool :
    head_content_extractor = re.compile(r"<HEAD>(.*)</HEAD>")
    content = head_content_extractor.findall(string)[0]
    
    has_function_call = re.compile(r"\[(\S*)\((.*)\)->(.*)\]")
    return not has_function_call.search(content)

DSTR_VALIDATORS: List[Callable[[str], bool]] = [
    str_has_head_body_structure,
    str_has_no_function_calls_in_the_head
]
