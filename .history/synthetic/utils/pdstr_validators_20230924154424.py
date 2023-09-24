from typing import List, Callable

import re

def str_has_partial_head_body_structure (string: str) -> bool :
    extract_tags = re.compile(r"<([^<>]*)>", flags=re.M)
    
    match = re.search(pattern=extract_tags, string=string)
        
    print(match)
    
    if not match: return False
    
    print(match)
        
    return True


PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure
]