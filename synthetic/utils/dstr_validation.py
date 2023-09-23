import re
from typing import List, Callable

def str_has_head_body_structure (string: str) -> bool :
    head_body_structure = re.compile(r"^<HEAD>(.*)</HEAD>(\s*)<START>(.*)<END>$")
    
    if re.match(string=string, pattern=head_body_structure) : return True
    else:  return False

DSTR_VALIDATORS: List[Callable[[str], bool]] = [
    str_has_head_body_structure
]
