from typing import List, Callable

import re

def str_has_partial_head_body_structure (string: str) -> bool :
    extract_tags = re.compile(r"/<([A-Z/]*)>/gm")
    tags = ["HEAD", "/HEAD", "START", "END"]
    
    match = re.search(pattern=extract_tags, string=string)
    
    if match: print(match.groups())
    
    if (not match) and string != "" : return False
    
    print(match.groups())
    
    for idx, e in match.groups() :
        if e != tags[idx] :
            return False
        
    return True


PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure
]