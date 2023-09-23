import re
from typing import List, Callable

def str_has_head_body_structure (string: str) -> bool :
    head_body_structure = re.compile(r"^<HEAD>(.*)</HEAD>(\w*)<START>(.*)<END>$")
    
    if re.match(string=string, pattern=head_body_structure) : return True
    else return False

VALIDATORS: List[Callable[[str], bool]] = [
    str_has_head_body_structure
]
